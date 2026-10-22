import streamlit as st
import json
from pathlib import Path
from datetime import datetime

st.set_page_config(page_title="화장실 신호 알림", page_icon="🚻")

FILE = Path("requests.json")


def load_data():
    try:
        data = json.loads(FILE.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except (OSError, ValueError):
        return []


def save_data(data):
    try:
        FILE.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return True
    except OSError:
        st.error("저장 오류가 발생했습니다.")
        return False


st.title("🚻 화장실 신호 알림")
st.caption("화장실에 가고 싶을 때 선생님께 알려요.")

page = st.radio("화면", ["학생", "선생님"], horizontal=True)
data = load_data()

if page == "학생":
    name = st.text_input("학생 이름")

    if st.button("🚻 화장실 가고 싶어요!", type="primary"):
        name = name.strip()

        if not name:
            st.warning("이름을 입력하세요.")
        elif any(
            x.get("name") == name and x.get("status") != "완료"
            for x in data
        ):
            st.info("이미 요청이 등록되어 있습니다.")
        else:
            data.append({
                "id": datetime.now().isoformat(),
                "name": name,
                "time": datetime.now().strftime("%H:%M:%S"),
                "status": "대기 중",
            })

            if save_data(data):
                st.success("신호를 보냈습니다!")
                st.rerun()

    st.subheader("요청 상태 확인")
    check = st.text_input("이름 입력", key="check_name")

    if check.strip():
        found = [
            x for x in data
            if x.get("name") == check.strip()
            and x.get("status") != "완료"
        ]

        if not found:
            st.info("진행 중인 요청이 없습니다.")

        for x in found:
            st.write(x["name"] + " : " + x["status"])

else:
    try:
        correct_pin = str(st.secrets["TEACHER_PIN"])
    except Exception:
        correct_pin = "1234"

    if not st.session_state.get("teacher_login", False):
        pin = st.text_input("선생님 PIN", type="password")

        if st.button("로그인"):
            if pin == correct_pin:
                st.session_state["teacher_login"] = True
                st.rerun()
            else:
                st.error("PIN이 틀렸습니다.")

        st.stop()

    if st.button("로그아웃"):
        st.session_state["teacher_login"] = False
        st.rerun()

    st.subheader("📬 학생 요청 관리")

    waiting = sum(x.get("status") == "대기 중" for x in data)
    st.metric("대기 중인 요청", waiting)

    for x in data:
        with st.container(border=True):
            st.write("학생: " + str(x.get("name", "")))
            st.write("요청 시간: " + str(x.get("time", "")))
            st.write("상태: " + str(x.get("status", "")))

            item_id = str(x.get("id", ""))

            if x.get("status") == "대기 중":
                if st.button("승인", key="approve_" + item_id):
                    for row in data:
                        if row.get("id") == item_id:
                            row["status"] = "승인됨"

                    if save_data(data):
                        st.rerun()

            if x.get("status") != "완료":
                if st.button("완료 처리", key="done_" + item_id):
                    for row in data:
                        if row.get("id") == item_id:
                            row["status"] = "완료"

                    if save_data(data):
                        st.rerun()

    if st.button("새로고침"):
        st.rerun()
