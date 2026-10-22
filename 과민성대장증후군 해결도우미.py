import streamlit as st
from datetime import datetime, date, time, timedelta

st.set_page_config(
    page_title="안심장 | 과민성 대장증후군 도우미",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Theme ----------
st.markdown("""
<style>
    :root {
        --ink: #344054;
        --muted: #737b8c;
        --sage: #7d9f91;
        --deep-sage: #466f60;
        --lavender: #b7a6d9;
        --peach: #f2bda7;
        --butter: #f4dfa0;
        --paper: #fffdf9;
    }
    .stApp {
        background:
          radial-gradient(ellipse at 8% 0%, rgba(242,189,167,.22), transparent 32%),
          radial-gradient(ellipse at 92% 5%, rgba(183,166,217,.22), transparent 30%),
          linear-gradient(180deg, #fbf8f4 0%, #f7f8f5 48%, #fffdf9 100%);
        color: var(--ink);
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #eee8f7 0%, #f5e9e3 54%, #e8f1eb 100%);
        border-right: 1px solid rgba(110, 105, 135, .12);
    }
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2 {
        color: #4d456c;
        letter-spacing: -.03em;
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] label {
        border-radius: 12px;
    }
    .hero {
        position: relative;
        overflow: hidden;
        padding: 1.8rem 1.9rem;
        border-radius: 24px;
        background: linear-gradient(118deg, #e3eee6 0%, #f8e8df 48%, #eee7f8 100%);
        border: 1px solid rgba(125, 159, 145, .25);
        box-shadow: 0 10px 30px rgba(83, 88, 100, .06);
        margin-bottom: 1.15rem;
    }
    .hero:after {
        content: "✿";
        position: absolute;
        right: 1.5rem;
        top: -.9rem;
        font-size: 6.5rem;
        color: rgba(255,255,255,.55);
        transform: rotate(14deg);
        pointer-events: none;
    }
    .hero h1 {
        margin: 0;
        color: #3d5f52;
        font-size: 2.35rem;
        letter-spacing: -.045em;
    }
    .hero p {
        color: #626b76;
        margin: .55rem 0 0 0;
        font-size: 1.03rem;
        line-height: 1.7;
    }
    .mini-card {
        background: rgba(255,255,255,.88);
        border: 1px solid #ebe5e3;
        border-radius: 19px;
        padding: 1.05rem 1.1rem;
        min-height: 150px;
        box-shadow: 0 7px 22px rgba(70, 73, 84, .045);
        transition: transform .18s ease, box-shadow .18s ease;
    }
    .mini-card h3 {
        color: #4b5f58;
        margin-top: .35rem;
        letter-spacing: -.02em;
    }
    .mini-card p {
        color: #727b86;
        line-height: 1.6;
    }
    .muted { color: var(--muted); font-size: .9rem; }
    .notice {
        border-left: 4px solid #dca68f;
        background: linear-gradient(100deg, #fff0e8, #f8f0fb);
        padding: .9rem 1rem;
        border-radius: 10px;
        color: #675b68;
    }
    .small-label { color: #647f73; font-weight: 600; }
    h1, h2, h3 { letter-spacing: -.025em; }
    [data-testid="stMetric"] {
        background: rgba(255,255,255,.75);
        border: 1px solid #ece7e5;
        border-radius: 16px;
        padding: 12px 15px;
    }
    [data-testid="stExpander"] {
        border: 1px solid #e9e3e8;
        border-radius: 14px;
        background: rgba(255,255,255,.7);
    }
    div.stButton > button, div.stFormSubmitButton > button {
        border-radius: 13px;
        border: 1px solid #c9d9cf;
        background: linear-gradient(110deg, #e5f0e8, #f5e9e4);
        color: #3d5f52;
        font-weight: 650;
        transition: all .18s ease;
    }
    div.stButton > button:hover, div.stFormSubmitButton > button:hover {
        border-color: #b7a6d9;
        color: #4d456c;
        box-shadow: 0 5px 14px rgba(105, 91, 130, .12);
        transform: translateY(-1px);
    }
    div[data-baseweb="select"] > div, div[data-baseweb="input"] > div,
    div[data-baseweb="textarea"] > div {
        border-radius: 12px;
        border-color: #e2dce7;
        background-color: rgba(255,255,255,.85);
    }
    div[data-testid="stAlert"] {
        border-radius: 13px;
    }
    hr { border-color: rgba(151, 143, 164, .2); }
</style>
""", unsafe_allow_html=True)

if "logs" not in st.session_state:
    st.session_state.logs = []
if "signal_time" not in st.session_state:
    st.session_state.signal_time = None
if "signal_note" not in st.session_state:
    st.session_state.signal_note = ""

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("## 🌿 안심장")
    st.caption("과민성 대장증후군 일상 도우미")
    page = st.radio(
        "메뉴",
        ["🏠 홈", "🚻 안심 화장실 지도", "🔔 화장실 신호 알림", "🌱 장 컨디션 조절"],
        label_visibility="collapsed",
    )
    st.divider()
    st.caption("작은 기록이 나에게 맞는 생활 패턴을 찾는 데 도움이 될 수 있어요.")
    st.caption("※ 의료 진단이나 치료를 대신하지 않습니다.")

# ---------- Home ----------
if page == "🏠 홈":
    st.markdown("""
    <div class="hero">
      <h1>오늘도, 조금 더 안심 🌿</h1>
      <p>화장실 위치부터 몸의 신호, 생활 습관까지.<br>불안한 순간을 줄이기 위한 나만의 IBS 도우미예요.</p>
    </div>
    """, unsafe_allow_html=True)
    st.subheader("필요한 기능을 골라 시작해 보세요")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="mini-card"><div style="font-size:2rem">🚻</div><h3>안심 화장실 지도</h3><p>건물과 층을 골라 화장실 위치 및 안내를 확인해요.</p></div>', unsafe_allow_html=True)
        if st.button("화장실 찾기 →", use_container_width=True):
            st.session_state.home_jump = "🚻 안심 화장실 지도"
            st.rerun()
    with c2:
        st.markdown('<div class="mini-card"><div style="font-size:2rem">🔔</div><h3>화장실 신호 알림</h3><p>배변 신호를 기록하고 이용 알림 시간을 설정해요.</p></div>', unsafe_allow_html=True)
        if st.button("신호 기록하기 →", use_container_width=True):
            st.session_state.home_jump = "🔔 화장실 신호 알림"
            st.rerun()
    with c3:
        st.markdown('<div class="mini-card"><div style="font-size:2rem">🌱</div><h3>장 컨디션 조절</h3><p>식사, 수면, 스트레스와 불편감을 기록해요.</p></div>', unsafe_allow_html=True)
        if st.button("컨디션 기록하기 →", use_container_width=True):
            st.session_state.home_jump = "🌱 장 컨디션 조절"
            st.rerun()

    # Handle home navigation by switching next rerun's radio default is not reliable,
    # so show direct navigation hint instead of mutating a widget's state.
    if "home_jump" in st.session_state:
        target = st.session_state.pop("home_jump")
        st.info(f"왼쪽 메뉴에서 **{target}** 을 선택하면 해당 기능을 이용할 수 있어요.")

    st.divider()
    st.subheader("오늘의 안심 루틴")
    routine = st.columns(3)
    with routine[0]:
        st.markdown("**💧 수분 챙기기**")
        st.caption("물을 조금씩 나누어 마셔요.")
    with routine[1]:
        st.markdown("**🍽️ 천천히 먹기**")
        st.caption("급하게 먹지 않고 몸의 반응을 살펴요.")
    with routine[2]:
        st.markdown("**📝 내 패턴 기록하기**")
        st.caption("증상과 생활 습관을 함께 적어봐요.")
    st.markdown('<div class="notice">복통이나 배변 습관의 변화가 지속되거나 심해지면 보호자와 의료진에게 상담해 주세요.</div>', unsafe_allow_html=True)

# ---------- Restroom map ----------
elif page == "🚻 안심 화장실 지도":
    st.title("🚻 안심 화장실 지도")
    st.write("건물과 층을 선택해 화장실 위치를 확인해요. 아래 위치는 **예시 데이터**이므로 실제 학교·건물 정보로 바꿔 사용하세요.")
    st.info("이 버전은 실제 GPS나 실시간 실내 측위를 사용하지 않습니다. 위치와 경로는 등록된 예시 정보를 바탕으로 안내합니다.")

    building_data = {
        "학교 건물 (예시)": {
            "1층": [
                {"name": "중앙 복도 화장실", "where": "중앙 계단 옆", "access": "복도에서 접근", "crowd": "수업 시간대에 이용자가 있을 수 있어요."},
                {"name": "별관 화장실", "where": "별관 연결 통로 근처", "access": "별관 방향 복도", "crowd": "이동 거리를 확인하고 선택하세요."},
            ],
            "2층": [
                {"name": "동쪽 복도 화장실", "where": "동쪽 계단 근처", "access": "동쪽 복도 끝", "crowd": "교실 위치에 따라 가까울 수 있어요."},
                {"name": "중앙 복도 화장실", "where": "중앙 계단 옆", "access": "중앙 복도", "crowd": "가까운 계단을 이용하세요."},
            ],
            "3층": [
                {"name": "서쪽 복도 화장실", "where": "서쪽 계단 근처", "access": "서쪽 복도 끝", "crowd": "가장 가까운 연결 통로를 확인하세요."},
                {"name": "중앙 복도 화장실", "where": "중앙 계단 옆", "access": "중앙 복도", "crowd": "교실 위치에 따라 가까울 수 있어요."},
            ],
        },
        "도서관 (예시)": {
            "1층": [
                {"name": "로비 화장실", "where": "안내 데스크 근처", "access": "로비 복도", "crowd": "안내 데스크에 위치를 확인할 수 있어요."},
            ],
            "2층": [
                {"name": "열람실 옆 화장실", "where": "열람실 출입구 옆", "access": "열람실 복도", "crowd": "조용히 이동해 주세요."},
            ],
        },
        "상가 건물 (예시)": {
            "1층": [
                {"name": "로비 화장실", "where": "엘리베이터 홀 근처", "access": "공용 로비", "crowd": "매장 전용 시설인지 확인하세요."},
            ],
            "2층": [
                {"name": "공용 화장실", "where": "에스컬레이터 옆 복도", "access": "공용 복도", "crowd": "영업시간 및 이용 조건을 확인하세요."},
            ],
        },
    }

    left, right = st.columns([1, 1.25], gap="large")
    with left:
        building = st.selectbox("🏢 건물 선택", list(building_data.keys()))
        floor = st.selectbox("층 선택", list(building_data[building].keys()))
        toilets = building_data[building][floor]
        toilet_names = [t["name"] for t in toilets]
        selected_name = st.selectbox("목적지 화장실", toilet_names)
        selected = next((t for t in toilets if t["name"] == selected_name), toilets[0])
        st.markdown("#### 📍 위치 정보")
        st.write(f"**위치:** {selected['where']}")
        st.write(f"**접근:** {selected['access']}")
        st.caption(selected["crowd"])
        st.markdown("#### 🧭 이동 안내")
        start = st.selectbox("현재 위치", ["현재 층 중앙 복도", "동쪽 계단", "서쪽 계단", "중앙 계단", "엘리베이터 홀", "안내 데스크"])
        if start in selected["where"]:
            route = f"{start}에서 주변 표지판을 확인하세요."
        else:
            route = f"{start}에서 {selected['where']} 방향으로 이동한 뒤, 화장실 표지판을 확인하세요."
        st.success(f"추천 경로: {route}")
    with right:
        st.markdown("#### 🗺️ 층별 개념도")
        # schematic diagram, intentionally not presented as a real architectural plan
        st.caption("개념도 · 실제 평면도 아님")
        st.markdown("""
        <div style="border:2px solid #b9cdbd;border-radius:18px;padding:16px;background:#fff">
          <div style="text-align:center;background:#edf5ef;padding:10px;border-radius:10px;font-weight:700;color:#315b42">복도 / 교실 방향</div>
          <div style="display:flex;gap:10px;margin:14px 0;align-items:stretch">
            <div style="flex:1;border:1px solid #d9e5dc;border-radius:10px;padding:18px 8px;text-align:center;background:#f8fbf8">교실<br><span style="font-size:.8rem;color:#6a8171">공간 A</span></div>
            <div style="flex:1;border:2px solid #86b894;border-radius:10px;padding:18px 8px;text-align:center;background:#e8f5eb;color:#285640;font-weight:700">🚻<br>화장실</div>
            <div style="flex:1;border:1px solid #d9e5dc;border-radius:10px;padding:18px 8px;text-align:center;background:#f8fbf8">계단 / 통로</div>
          </div>
          <div style="text-align:center;background:#f5f7f5;padding:10px;border-radius:10px;color:#607568">이동 통로</div>
        </div>
        """, unsafe_allow_html=True)
        st.caption("실제 시설에 맞게 화장실 이름·위치·층 정보를 수정해야 정확한 안내가 가능합니다.")
    with st.expander("건물별 정보를 수정하려면"):
        st.write("app.py에서 `building_data` 딕셔너리의 건물명, 층, 화장실 이름과 위치 설명을 실제 정보로 바꾸세요. 이 앱은 실제 건축 도면이나 화장실 운영 여부를 자동으로 가져오지 않습니다.")

# ---------- Signal reminder ----------
elif page == "🔔 화장실 신호 알림":
    st.title("🔔 화장실 신호 알림")
    st.write("몸의 신호를 무시하지 않도록 기록하고, 필요할 때 확인할 알림을 설정해요.")
    st.markdown('<div class="notice">이 앱의 알림은 페이지 안에서 확인하는 알림입니다. 브라우저가 닫혀 있거나 앱을 사용하지 않을 때 자동으로 울리는 푸시 알림은 지원하지 않아요.</div>', unsafe_allow_html=True)
    with st.form("signal_form"):
        signal = st.slider("지금 화장실 신호가 얼마나 급한가요?", 0, 10, 5, help="0은 전혀 급하지 않음, 10은 매우 급함")
        symptom = st.selectbox("함께 느끼는 상태", ["특별한 증상 없음", "복부 불편감", "복부 팽만감", "묽은 변 느낌", "변비 느낌", "기타"])
        reminder_date = st.date_input("알림 날짜", value=date.today(), min_value=date.today())
        reminder_clock = st.time_input("알림 시간", value=(datetime.now() + timedelta(minutes=15)).time().replace(second=0, microsecond=0))
        note = st.text_input("메모 (선택)", placeholder="예: 수업 시작 전 화장실 위치 확인")
        submitted = st.form_submit_button("신호 기록 및 알림 설정", use_container_width=True)
    if submitted:
        dt = datetime.combine(reminder_date, reminder_clock)
        st.session_state.signal_time = dt
        st.session_state.signal_note = note.strip()
        st.session_state.logs.append({
            "일시": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "종류": "신호",
            "강도": signal,
            "내용": f"{symptom}" + (f" · {note.strip()}" if note.strip() else ""),
        })
        st.success("기록했어요. 아래에서 알림 시간을 확인할 수 있어요.")
        st.rerun()

    if st.session_state.signal_time:
        target = st.session_state.signal_time
        st.subheader("⏰ 설정된 알림")
        if target <= datetime.now():
            st.warning(f"알림 시간이에요! ({target.strftime('%Y-%m-%d %H:%M')}) 몸의 상태를 확인하고 필요하면 화장실을 이용하세요.")
        else:
            st.info(f"확인 예정: **{target.strftime('%Y-%m-%d %H:%M')}**")
        if st.session_state.signal_note:
            st.caption(f"메모: {st.session_state.signal_note}")
        if st.button("알림 해제"):
            st.session_state.signal_time = None
            st.session_state.signal_note = ""
            st.rerun()
    else:
        st.caption("아직 설정된 알림이 없어요.")

    st.divider()
    st.subheader("기억해 둘 점")
    st.write("- 신호가 강하거나 불편감이 심하면 알림 시간까지 기다리지 말고 화장실을 이용하세요.")
    st.write("- 증상이 갑자기 심해지거나 혈변, 발열, 원인 모를 체중 감소 등 걱정되는 증상이 있다면 의료진과 상담하세요.")

# ---------- Gut condition ----------
elif page == "🌱 장 컨디션 조절":
    st.title("🌱 장 컨디션 조절")
    st.write("하루의 증상과 생활 습관을 기록해 나에게 맞는 패턴을 찾아보세요.")
    with st.form("condition_form"):
        entry_date = st.date_input("기록 날짜", value=date.today(), key="condition_date")
        discomfort = st.slider("복부 불편감", 0, 10, 3, help="0은 불편감 없음, 10은 매우 심함")
        bowel = st.select_slider("오늘의 배변 상태", options=["딱딱함", "조금 딱딱함", "보통", "조금 묽음", "묽음"], value="보통")
        meals = st.selectbox("식사 패턴", ["평소와 비슷함", "급하게 먹음", "평소보다 많이 먹음", "끼니를 거름", "특정 음식 후 불편함"])
        sleep_hours = st.slider("지난밤 수면 시간", 0.0, 12.0, 7.0, step=0.5)
        stress = st.slider("오늘 스트레스 정도", 0, 10, 3)
        water = st.selectbox("수분 섭취", ["부족했음", "보통", "충분했음"])
        memo = st.text_area("추가 메모 (선택)", placeholder="불편감이 생긴 시간, 먹은 음식 등")
        save = st.form_submit_button("오늘 기록 저장", use_container_width=True)
    if save:
        st.session_state.logs.append({
            "일시": entry_date.strftime("%Y-%m-%d"),
            "종류": "컨디션",
            "강도": discomfort,
            "내용": f"배변: {bowel} · 식사: {meals} · 수면: {sleep_hours:g}시간 · 스트레스: {stress}/10 · 수분: {water}" + (f" · 메모: {memo.strip()}" if memo.strip() else ""),
        })
        st.success("오늘의 컨디션을 기록했어요.")
        st.rerun()

    st.divider()
    st.subheader("오늘의 셀프 케어 체크리스트")
    checks = [
        "물을 한 번에 많이 마시기보다 나누어 마시기",
        "식사를 규칙적으로 하고 천천히 먹기",
        "가벼운 걷기나 편안한 호흡으로 긴장 풀기",
        "증상과 식사·수면·스트레스의 관계 기록하기",
    ]
    for item in checks:
        st.checkbox(item, key=f"care_{item}")

    st.info("특정 음식을 무조건 끊기보다 증상과 식사 기록을 통해 관련성을 살펴보세요. 제한 식단이나 보충제를 시작하기 전에는 의료진 또는 영양 전문가와 상담하는 것이 좋아요.")

    st.divider()
    st.subheader("🗂️ 최근 기록")
    if st.session_state.logs:
        for item in reversed(st.session_state.logs[-10:]):
            with st.expander(f"{item['일시']} · {item['종류']} · 강도 {item['강도']}/10"):
                st.write(item["내용"])
        if st.button("기록 전체 삭제", type="secondary"):
            st.session_state.logs = []
            st.rerun()
    else:
        st.caption("아직 기록이 없어요. 위에서 첫 기록을 남겨보세요.")

st.divider()
st.caption("안심장은 생활 기록과 편의 안내를 위한 도구이며, 진단·치료를 제공하지 않습니다. 증상이 지속되거나 심하면 의료진과 상담하세요.")
