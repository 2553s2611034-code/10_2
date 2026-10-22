import streamlit as st
import json
from pathlib import Path
from datetime import datetime

st.set_page_config(page_title="화장실 신호 알림", page_icon="🚻")
FILE = Path("requests.json")

def load():
    try:
        return json.loads(FILE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return []

def save(data):
    try:
        FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        return True
    except OSError:
        st.error("저장에 실패했습니다.")
        return False

st.title("🚻 화장실 신호 알림")
page = st.radio("화면", ["학생", "선생님"], horizontal=True)
data = load()

if page == "학생":
    name = st.text_input("이름")
    if st.button("🚻 화장실 가고 싶어요!", type="primary"):
        name = name.strip()
        if not name:
            st.warning("이름을 입력하세요.")
        elif any(x["name"] ==
