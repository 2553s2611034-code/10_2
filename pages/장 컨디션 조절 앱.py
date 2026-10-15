import streamlit as st
import pandas as pd
from datetime import date
from pathlib import Path

st.set_page_config(page_title="장 컨디션 노트", page_icon="🌿", layout="centered")

DATA_FILE = Path("gut_log.csv")
COLUMNS = [
    "날짜", "배변 횟수", "변 상태", "복부 불편감(0-10)",
    "복부 팽만감(0-10)", "스트레스(0-10)", "물 섭취량(컵)",
    "먹은 음식", "메모"
]

def load_data():
    if DATA_FILE.exists():
        df = pd.read_csv(DATA_FILE)
        for col in COLUMNS:
            if col not in df.columns:
                df[col] = ""
        return df[COLUMNS]
    return pd.DataFrame(columns=COLUMNS)

st.title("🌿 장 컨디션 노트")
st.caption("매일의 생활 습관과 장 컨디션을 기록해 보세요. 이 앱은 의료 진단 도구가 아닙니다.")

with st.form("daily_log", clear_on_submit=True):
    st.subheader("오늘의 기록")
    log_date = st.date_input("날짜", value=date.today())
    bowel_count = st.number_input("배변 횟수", min_value=0, max_value=20, value=1, step=1)
    stool = st.selectbox(
        "변 상태",
        ["선택 안 함", "딱딱함", "조금 딱딱함", "보통", "무름", "물설사"]
    )
    pain = st.slider("복부 불편감 (0=없음, 10=매우 심함)", 0, 10, 0)
    bloating = st.slider("복부 팽만감 (0=없음, 10=매우 심함)", 0, 10, 0)
    stress = st.slider("스트레스 (0=낮음, 10=매우 높음)", 0, 10, 3)
    water = st.number_input("물 섭취량 (컵)", min_value=0, max_value=30, value=6, step=1)
    food = st.text_input("오늘 먹은 음식", placeholder="예: 밥, 달걀, 사과")
    memo = st.text_area("추가 메모", placeholder="식사 후 불편감, 수면, 운동 등")
    submitted = st.form_submit_button("기록 저장", type="primary")

if submitted:
    new_row = pd.DataFrame([{
        "날짜": log_date.isoformat(),
        "배변 횟수": int(bowel_count),
        "변 상태": stool,
        "복부 불편감(0-10)": pain,
        "복부 팽만감(0-10)": bloating,
        "스트레스(0-10)": stress,
        "물 섭취량(컵)": int(water),
        "먹은 음식": food,
        "메모": memo
    }], columns=COLUMNS)

    df = load_data()
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(DATA_FILE, index=False, encoding="utf-8-sig")
    st.success("오늘의 기록을 저장했어요!")
    st.rerun()

st.divider()
st.subheader("📊 기록 살펴보기")
df = load_data()

if df.empty:
    st.info("아직 기록이 없어요. 위에서 첫 기록을 추가해 보세요.")
else:
    df["날짜"] = pd.to_datetime(df["날짜"], errors="coerce")
    df = df.dropna(subset=["날짜"]).sort_values("날짜")
    latest = df.iloc[-1]

    c1, c2, c3 = st.columns(3)
    c1.metric("최근 배변 횟수", f"{latest['배변 횟수']}회")
    c2.metric("복부 불편감", f"{latest['복부 불편감(0-10)']}/10")
    c3.metric("팽만감", f"{latest['복부 팽만감(0-10)']}/10")

    chart_cols = ["복부 불편감(0-10)", "복부 팽만감(0-10)", "스트레스(0-10)"]
    chart_df = df.set_index("날짜")[chart_cols].apply(pd.to_numeric, errors="coerce")
    st.line_chart(chart_df)
    st.dataframe(df.sort_values("날짜", ascending=False), use_container_width=True, hide_index=True)

    csv = df.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        "📥 기록 CSV 다운로드",
        data=csv,
        file_name="gut_log.csv",
        mime="text/csv"
    )

st.divider()
st.subheader("⚠️ 건강 안내")
st.write(
    "이 기록은 본인의 패턴을 살펴보기 위한 참고 자료예요. "
    "증상이 지속되거나 일상생활에 지장을 주면 보호자와 상의하고 의료진에게 상담하세요. "
    "혈변, 심한 복통, 탈수 징후 등 걱정되는 증상이 있으면 신속하게 의료 도움을 받으세요."
)
st.caption("개인 건강 기록이므로 공개 저장소에 실제 기록 파일을 올리지 마세요.")
