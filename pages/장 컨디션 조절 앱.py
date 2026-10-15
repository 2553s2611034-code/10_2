import streamlit as st
import pandas as pd
from datetime import date, datetime

st.set_page_config(
    page_title="GutCare",
    page_icon="🌿",
    layout="wide",
)

COLUMNS = [
    "날짜",
    "복통",
    "복부팽만",
    "가스",
    "배변상태",
    "스트레스",
    "수면시간",
    "물섭취",
    "음식메모",
    "식후불편함",
    "점수",
]


def calculate_score(pain, bloating, gas, stool, stress, sleep):
    score = 100
    score -= pain * 7
    score -= bloating * 5
    score -= gas * 4
    score -= stress * 3

    penalties = {
        "편안함": 0,
        "조금 딱딱함": 8,
        "조금 묽음": 8,
        "변비 느낌": 18,
        "설사 느낌": 18,
        "아직 배변하지 않음": 5,
    }

    score -= penalties.get(stool, 0)

    if sleep < 5:
        score -= 12
    elif sleep < 7:
        score -= 5

    return max(0, min(100, int(score)))


def get_status(score):
    if score >= 80:
        return "좋음"
    if score >= 60:
        return "보통"
    if score >= 40:
        return "불편함 관찰"
    return "불편함이 큰 날"


def export_csv(records):
    df = pd.DataFrame(records, columns=COLUMNS)
    return df.to_csv(index=False).encode("utf-8-sig")


if "records" not in st.session_state:
    st.session_state.records = []

st.title("🌿 GutCare")
st.write("나의 장 컨디션을 기록하고 생활 습관을 살펴보세요.")

page = st.sidebar.radio(
    "메뉴",
    ["오늘의 기록", "기록 분석", "장 건강 가이드"],
)

st.sidebar.caption("GutCare 장 컨디션 다이어리")

if page == "오늘의 기록":
    st.header("오늘의 장 컨디션")

    st.info(
        "이 앱은 개인 기록을 위한 도구입니다. "
        "점수는 의학적 진단 결과가 아닙니다."
    )

    with st.form("record_form"):
        selected_date = st.date_input("날짜", value=date.today())

        st.subheader("몸 상태")

        col1, col2, col3 = st.columns(3)

        with col1:
            pain = st.slider("복통", 0, 5, 0)

        with col2:
            bloating = st.slider("복부 팽만감", 0, 5, 0)

        with col3:
            gas = st.slider("가스 불편함", 0, 5, 0)

        stool = st.selectbox(
            "배변 상태",
            [
                "편안함",
                "조금 딱딱함",
                "조금 묽음",
                "변비 느낌",
                "설사 느낌",
                "아직 배변하지 않음",
            ],
        )

        st.subheader("생활 습관")

        stress = st.slider("스트레스", 0, 5, 0)

        sleep = st.number_input(
            "수면 시간",
            min_value=0.0,
            max_value=24.0,
            value=8.0,
            step=0.5,
        )

        water = st.number_input(
            "물 섭취량 (ml)",
            min_value=0,
            max_value=10000,
            value=1000,
            step=100,
        )

        meal = st.text_input(
            "먹은 음식",
            max_chars=200,
            placeholder="예: 밥, 달걀, 우유",
        )

        after_meal = st.selectbox(
            "식후 불편함",
            ["없음", "있음", "잘 모르겠음"],
        )

        submitted = st.form_submit_button("기록 저장")

    if submitted:
        score = calculate_score(
            pain,
            bloating,
            gas,
            stool,
            stress,
            sleep,
        )

        record = {
            "날짜": selected_date.isoformat(),
            "복통": pain,
            "복부팽만": bloating,
            "가스": gas,
            "배변상태": stool,
            "스트레스": stress,
            "수면시간": sleep,
            "물섭취": water,
            "음식메모": meal.strip(),
            "식후불편함": after_meal,
            "점수": score,
        }

        records = [
            item
            for item in st.session_state.records
            if item["날짜"] != selected_date.isoformat()
        ]

        records.append(record)
        records.sort(key=lambda item: item["날짜"])
        st.session_state.records = records

        st.success("기록을 저장했습니다!")

    records = st.session_state.records

    today_record = next(
        (
            item
            for item in records
            if item["날짜"] == date.today().isoformat()
        ),
        None,
    )

    if today_record is not None:
        st.subheader("오늘의 결과")

        col1, col2, col3 = st.columns(3)

        col1.metric("컨디션 점수", str(today_record["점수"]) + "/100")
        col2.metric("상태", get_status(today_record["점수"]))
        col3.metric("수면 시간", str(today_record["수면시간"]) + "시간")

        st.progress(today_record["점수"] / 100)

        tips = []

        if today_record["물섭취"] < 1000:
            tips.append("물을 조금씩 나누어 마셔 보세요.")

        if today_record["수면시간"] < 7:
            tips.append("규칙적인 수면 시간을 확보해 보세요.")

        if today_record["스트레스"] >= 4:
            tips.append("잠시 쉬면서 긴장을 풀어 보세요.")

        if max(
            today_record["복통"],
            today_record["복부팽만"],
            today_record["가스"],
        ) >= 3:
            tips.append("증상의 발생 시간과 지속 시간을 기록해 보세요.")

        st.subheader("생활 습관 제안")

        if tips:
            for tip in tips:
                st.write("- " + tip)
        else:
            st.write("규칙적인 식사와 수면을 유지해 보세요.")

    st.divider()
    st.subheader("기록 관리")

    if records:
        st.dataframe(
            pd.DataFrame(records, columns=COLUMNS),
            use_container_width=True,
            hide_index=True,
        )

        st.download_button(
            label="CSV 다운로드",
            data=export_csv(records),
            file_name="gutcare_records.csv",
            mime="text/csv",
        )

        delete_date = st.selectbox(
            "삭제할 기록 날짜",
            options=[item["날짜"] for item in records],
        )

        if st.button("선택한 기록 삭제"):
            st.session_state.records = [
                item
                for item in st.session_state.records
                if item["날짜"] != delete_date
            ]
            st.rerun()

    else:
        st.write("아직 저장된 기록이 없습니다.")

elif page == "기록 분석":
    st.header("📊 기록 분석")

    records = st.session_state.records

    if not records:
        st.info("먼저 오늘의 기록 메뉴에서 기록을 저장하세요.")

    else:
        df = pd.DataFrame(records, columns=COLUMNS)
        df["날짜"] = pd.to_datetime(df["날짜"])
        df = df.sort_values("날짜")

        col1, col2, col3 = st.columns(3)

        col1.metric("기록 일수", str(len(df)) + "일")
        col2.metric("평균 점수", str(round(df["점수"].mean())) + "/100")
        col3.metric("최근 점수", str(int(df.iloc[-1]["점수"])) + "/100")

        st.subheader("날짜별 컨디션 점수")

        chart = df.set_index("날짜")[["점수"]]
        st.line_chart(chart)

        st.subheader("증상 변화")

        symptoms = df.set_index("날짜")[
            ["복통", "복부팽만", "가스", "스트레스"]
        ]

        st.line_chart(symptoms)

        st.subheader("생활 습관")

        habits = df.set_index("날짜")[["수면시간", "물섭취"]]
        st.dataframe(habits, use_container_width=True)

        st.caption(
            "기록에서 함께 나타난 음식과 증상만으로 "
            "원인 관계를 확정할 수는 없습니다."
        )

elif page == "장 건강 가이드":
    st.header("📚 장 건강 가이드")

    with st.expander("규칙적인 식사"):
        st.write(
            "식사 시간과 음식 종류를 기록하며 "
            "자신에게 맞는 식사 패턴을 관찰해 보세요."
        )

    with st.expander("수분 섭취"):
        st.write(
            "물을 나누어 마시고 하루 섭취량을 기록해 보세요. "
            "필요한 수분량은 개인마다 다릅니다."
        )

    with st.expander("수면과 스트레스"):
        st.write(
            "수면 시간과 스트레스 정도를 기록하면 "
            "컨디션 변화를 돌아보는 데 도움이 됩니다."
        )

    with st.expander("증상 기록"):
        st.write(
            "증상 발생 시간, 지속 시간, 먹은 음식, "
            "배변 상태를 기록해 보세요."
        )

    st.warning(
        "심한 복통, 혈변이나 검은 변, 지속적인 구토 또는 "
        "탈수 증상이 있다면 의료진의 평가를 받으세요."
    )

st.divider()

st.caption(
    "GutCare | 건강 기록용 앱입니다. "
    "기록은 현재 앱 세션에 저장되므로 CSV 파일로 보관하세요."
)
