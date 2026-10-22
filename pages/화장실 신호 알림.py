import streamlit as st
import json
from pathlib import Path
from datetime import datetime

st.set_page_config(page_title="화장실 신호 알림", page_icon="🚻")

FILE = Path("requests.json")


def load_data():
    try:
        return json.loads(FILE.read_text(encoding="utf-8"))
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
        st.error("저장에 실패했습니다.")
        return False


st.title("🚻 화장실 신호 알림")
page = st.radio("화면 선택", ["학생", "선생님"], horizontal=True)
data = load_data()

if page == "학생":
    name = st.text_input("이름")

    if st.button("🚻 화장실 가고 싶어요!", type="primary"):
        name = name.strip()

        if not name:
            st.warning("이름을 입력해 주세요.")
        elif any(
            item.get("name") == name
            and item.get("status") != "완료"
            for item in data
        ):
            st.info("이미 처리 중인 요청이 있습니다.")
        else:
            data.append({
                "id": datetime.now().isoformat(),
                "name": name,
                "time": datetime.now().strftime("%H:%M:%S"),
                "status": "대기 중",
            })

            if save_data(data):
                st.success("선생님께 신호를 보냈어요!")
                st.rerun()

    st.subheader("📋 요청 상태 확인")
    check_name = st.text_input("확인할 이름")

    if check_name.strip():
        matches = [
            item for item in data
            if item.get("name") == check_name.strip()
            and item.get("status") != "완료"
        ]

        if not matches:
            st.info("처리 중인 요청이 없습니다.")

        for item in matches:
            st.write(
                "{} · {}".format(
                    item.get("name", ""),
                    item.get("status", ""),
                )
            )

else:
    try:
        correct_pin = str(st.secrets["TEACHER_PIN"])
    except Exception:
        correct_pin = "1234"

    if not st.session_state.get("logged_in", False):
        pin = st.text_input("선생님 PIN", type="password")

        if st.button("로그인"):
            if pin == correct_pin:
                st.session_state["logged_in"] = True
                st.rerun()
            else:
                st.error("PIN이 올바르지 않습니다.")

        st.stop()

    if st.button("로그아웃"):
        st.session_state["logged_in"] = False
        st.rerun()

    st.subheader("📬 학생 요청 목록")
    st.write(
        "대기 중: {}".format(
            sum(item.get("status") == "대기 중" for item in data)
        )
    )

    for item in data:
        with st.container(border=True):
            st.write("🚻 {}".format(item.get("name", "")))
            st.write("요청 시각: {}".format(item.get("time", "")))
            st.write("상태: {}".format(item.get("status", "")))

            item_id = item.get("id", "")

            if item.get("status") == "대기 중":
                if st.button("승인", key="approve_" + item_id):
                    for row in data:
                        if row.get("id") == item_id:
                            row["status"] = "승인됨"

                    if save_data(data):
                        st.rerun()

            if item.get("status") != "완료":
                if st.button("완료 처리", key="done_" + item_id):
                    for row in data:
                        if row.get("id") == item_id:
                            row["status"] = "완료"

                    if save_data(data):
                        st.rerun()

    if st.button("새로고침"):
        st.rerun()
