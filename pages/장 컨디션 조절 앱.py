import streamlit as st
import pandas as pd
from datetime import date, datetime
from io import StringIO

st.set_page_config(
    page_title="GutCare | 장 컨디션 다이어리",
    page_icon="🌿",
    layout="wide",
)

# ---------- 디자인 ----------
st.markdown("""
<style>
.stApp {
    background-color: #F7F9F4;
}
.main-title {
    font-size: 2.2rem;
    font-weight: 800;
    color: #315B45;
}
.subtitle {
    color: #68796B;
    font-size: 1rem;
}
div[data-testid="stMetric"] {
    background: white;
    border: 1px solid #E1E9DE;
    padding: 16px;
    border-radius: 14px;
}
div.stButton > button {
    border-radius: 10px;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)


# ---------- 데이터 ----------
COLUMNS = [
    "날짜", "복통", "복부팽만", "가스", "배변상태",
    "스트레스", "수면시간", "물섭취(ml)", "식사메모",
    "식후불편함", "컨디션점수", "기록시간"
]

if "records" not in st.session_state:
    st.session_state.records = []

if "saved_message" not in st.session_state:
    st.session_state.saved_message = ""


def calculate_score(pain, bloating, gas, stool, stress, sleep):
    """0~100점의 참고용 컨디션 점수."""
    stool_penalty = {
        "편안함": 0,
        "조금 딱딱함": 8,
        "조금 묽음": 8,
        "변비 느낌": 18,
        "설사 느낌": 18,
        "아직 배변하지 않음": 5,
    }

    score = 100
    score -= pain * 7
    score -= bloating * 5
    score -= gas * 4
    score -= stool_penalty.get(stool, 0)
    score -= stress * 3

    if sleep < 5:
        score -= 12
    elif sleep < 7:
        score -= 5

    return max(0, min(100, int(score)))


def get_status(score):
    if score >= 80:
        return "좋음", "🌿"
    if score >= 60:
        return "보통", "🙂"
    if score >= 40:
        return "주의해서 관찰", "📝"
    return "불편함이 큰 날", "💚"


def make_csv(records):
    """한글이 깨지지 않도록 UTF-8 BOM을 추가한다."""
    df = pd.DataFrame(records, columns=COLUMNS)
    return df.to_csv(index=False).encode("utf-8-sig")


# ---------- 사이드바 ----------
with st.sidebar:
    st.markdown("## 🌿 GutCare")
    st.caption("나의 장 컨디션 다이어리")
    page = st.radio(
        "메뉴",
        [
            "🏠 오늘의 기록",
            "📊 기록 분석",
            "📚 장 건강 가이드",
        ],
    )
    st.divider()
    st.caption("매일의 작은 기록으로 나의 패턴을 살펴보세요.")


# ---------- 공통 제목 ----------
st.markdown(
    '<div class="main-title">🌿 GutCare</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="subtitle">오늘의 장 컨디션을 기록하고 생활 습관을 돌아봐요.</div>',
    unsafe_allow_html=True,
)
st.write("")


# ---------- 1. 오늘의 기록 ----------
if page == "🏠 오늘의 기록":
    st.subheader("오늘의 장 컨디션 체크")
    st.info(
        "증상과 생활 습관을 기록하는 자기 관찰용 앱이에요. "
        "점수는 의학적 진단이나 검사 결과가 아닙니다."
    )

    with st.form("daily_form"):
        record_date = st.date_input("기록 날짜", value=date.today())

        st.markdown("#### 1. 몸 상태")
        c1, c2, c3 = st.columns(3)

        with c1:
            pain = st.slider("복통 정도", 0, 5, 0)
        with c2:
            bloating = st.slider("복부 팽만감", 0, 5, 0)
        with c3:
            gas = st.slider("가스 불편함", 0, 5, 0)

        stool = st.selectbox(
            "오늘의 배변 상태",
            [
                "편안함",
                "조금 딱딱함",
                "조금 묽음",
                "변비 느낌",
                "설사 느낌",
                "아직 배변하지 않음",
            ],
        )

        st.markdown("#### 2. 생활 습관")
        c4, c5 = st.columns(2)

        with c4:
            stress = st.slider("스트레스 정도", 0, 5, 0)
            sleep = st.number_input(
                "수면 시간",
                min_value=0.0,
                max_value=24.0,
                value=8.0,
                step=0.5,
            )

        with c5:
            water = st.number_input(
                "오늘 마신 물 (ml)",
                min_value=0,
                max_value=10000,
                value=1000,
                step=100,
            )
            meal_note = st.text_input(
                "먹은 음식 메모",
                placeholder="예: 밥, 달걀, 우유, 매운 음식",
                max_chars=300,
            )

        after_meal = st.radio(
            "식사 후 불편함이 있었나요?",
            ["없음", "있음", "잘 모르겠음"],
            horizontal=True,
        )

        submitted = st.form_submit_button(
            "🌱 오늘의 기록 저장",
            use_container_width=True,
        )

    if submitted:
        score = calculate_score(
            pain, bloating, gas, stool, stress, sleep
        )

        new_record = {
            "날짜": record_date.isoformat(),
            "복통": pain,
            "복부팽만": bloating,
            "가스": gas,
            "배변상태": stool,
            "스트레스": stress,
            "수면시간": sleep,
            "물섭취(ml)": water,
            "식사메모": meal_note.strip(),
            "식후불편함": after_meal,
            "컨디
