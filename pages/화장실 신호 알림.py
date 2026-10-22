import streamlit as st
import json
from pathlib import Path
from datetime import datetime

st.set_page_config(page_title="화장실 신호 알림", page_icon="🚻", layout="centered")

FILE = Path("requests.json")


def load_data():
    try:
        data = json.loads(FILE.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except (OSError, ValueError):
        return []


def save_data(data):
    try:
        FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        return True
    except OSError:
        st.error("저장에 실패했습니다.")
        return False


st.markdown("""
<style>
.stApp {background: linear-gradient(180deg, #eaf5ff, #ffffff);}
.block-container {max-width: 800px; padding-top: 2rem;}
h1, h2, h3 {color: #24527a;}
div.stButton > button {
    border-radius: 12px;
    min-height: 44px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

st.title("🚻 화장실 신호 알림")
st.caption("필요할 때 조용히 신호를 보내세요.")

page = st.radio("화면 선택", ["🙋 학생", "👩‍🏫 선생님"], horizontal=True)
data = load_data()

if page == "🙋 학생":
    st.subheader("💙 화장실 요청")

    with st.form("student_form"):
        name = st.text_input("이름", max_chars=20)
        urgent = st.checkbox("⏰ 조금 급해요")
        submitted = st.form_submit_button("🚻 선생님께 신호 보내기", type="primary")

    if submitted:
        name = name.strip()

        if not name:
            st.warning("이름을 입력해 주세요.")
        elif any(
            x.get("name") == name and x.get("status") != "완료"
            for x in data
        ):
            st.info("이미 처리 중인 요청이 있습니다.")
        else:
            data.append({
                "id": datetime.now().isoformat(),
                "name": name,
                "time": datetime.now().strftime("%H:%M:%S"),
                "status": "대기 중",
                "urgent": urgent,
            })
            if save_data(data):
                st.success("신호를 보냈어요! 선생님의 확인을 기다려 주세요.")
                st.rerun()

    st.divider()
    st.subheader("📋 내 요청 확인")

    check_name = st.text_input("이름을 입력해 상태 확인", key="check_name")

    if check_name.strip():
        mine = [
            x for x in data
            if x.get("name") == check_name.strip()
            and x.get("status") != "완료"
        ]

        if not mine:
            st.info("현재 처리 중인 요청이 없습니다.")

        for item in mine:
            with st.container(border=True):
                st.write("상태: " + item.get("status", "대기 중"))
                st.write("요청 시간: " + item.get("time", ""))

                if item.get("urgent"):
                    st.warning("⏰ 급한 요청")

                if st.button("요청 취소", key="cancel_" + item["id"]):
                    updated = [
                        x for x in load_data()
                        if x.get("id") != item["id"]
                    ]
                    if save_data(updated):
                        st.success("요청을 취소했습니다.")
                        st.rerun()

    if st.button("🔄 새로고침", use_container_width=True):
        st.rerun()

else:
    st.subheader("🔐 선생님 전용 화면")

    try:
        correct_pin = str(st.secrets["TEACHER_PIN"])
    except Exception:
        correct_pin = "1234"

    if not st.session_state.get("teacher_login", False):
        pin = st.text_input("선생님 PIN", type="password")

        if st.button("로그인", type="primary"):
            if pin == correct_pin:
                st.session_state["teacher_login"] = True
                st.rerun()
            else:
                st.error("PIN이 올바르지 않습니다.")

        st.caption("배포 전 Secrets에서 PIN을 변경하세요.")
        st.stop()

    if st.button("로그아웃"):
        st.session_state["teacher_login"] = False
        st.rerun()

    data = load_data()
    waiting = [x for x in data if x.get("status") == "대기 중"]
    approved = [x for x in data if x.get("status") == "승인됨"]
    completed = [x for x in data if x.get("status") == "완료"]

    c1, c2, c3 = st.columns(3)
    c1.metric("⏳ 대기", len(waiting))
    c2.metric("✅ 승인", len(approved))
    c3.metric("🏁 완료", len(completed))

    st.divider()
    view = st.selectbox("요청 필터", ["전체", "대기 중", "승인됨", "완료"])

    for item in reversed(data):
        if view != "전체" and item.get("status") != view:
            continue

        with st.container(border=True):
            if item.get("urgent"):
                st.warning("⏰ 급한 요청")

            st.markdown("### 🚻 " + item.get("name", "이름 없음"))
            st.write("요청 시간: " + item.get("time", ""))
            st.write("현재 상태: " + item.get("status", ""))

            item_id = item.get("id", "")

            if item.get("status") == "대기 중":
                if st.button("✅ 승인", key="approve_" + item_id):
                    updated = load_data()
                    for row in updated:
                        if row.get("id") == item_id:
                            row["status"] = "승인됨"
                    if save_data(updated):
                        st.rerun()

            if item.get("status") != "완료":
                if st.button("🏁 완료 처리", key="done_" + item_id):
                    updated = load_data()
                    for row in updated:
                        if row.get("id") == item_id:
                            row["status"] = "완료"
                    if save_data(updated):
                        st.rerun()

    st.divider()
    st.subheader("🗂️ 기록 관리")

    if st.button("완료된 요청 모두 삭제"):
        updated = [
            x for x in load_data()
            if x.get("status") != "완료"
        ]
        if save_data(updated):
            st.success("완료 기록을 삭제했습니다.")
            st.rerun()

    if st.button("🔄 최신 요청 불러오기"):
        st.rerun()

st.divider()
st.caption("화장실 신호 알림 · 교실에서 서로 배려해요 💙")
