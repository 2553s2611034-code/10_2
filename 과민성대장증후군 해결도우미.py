import streamlit as st import pandas as pd from datetime import date

st.setpageconfig( pagetitle="과민성대장증후군 해결도우미", pageicon="🌿", layout="centered", )

st.title("🌿 과민성대장증후군 해결도우미") st.caption("내 몸의 패턴을 기록하고, 나에게 맞는 관리법을 찾아보세요.")

st.info( "이 앱은 증상 관리와 생활 습관 개선을 돕는 도구입니다. " "의학적 진단이나 치료를 대신하지 않습니다." )

if "records" not in st.sessionstate: st.sessionstate.records = []

tab1, tab2, tab3 = st.tabs( ["📝 증상 기록", "📊 내 패턴", "🌱 관리 가이드"] )

with tab1: st.subheader("오늘의 몸 상태")

with st.form("symptomform"): recorddate = st.date_input("기록 날짜", value=date.today())

col1, col2 = st.columns(2)

with col1: pain = st.slider("복통", 0, 10, 0) bloating = st.slider("복부 팽만", 0, 10, 0)

with col2: diarrhea = st.slider("설사 증상", 0, 10, 0) constipation = st.slider("변비 증상", 0, 10, 0)

stress = st.slider("스트레스", 0, 10, 3) sleep = st.slider("수면 시간", 0.0, 12.0, 7.0, 0.5)

bowel = st.selectbox( "오늘의 배변 상태", [ "정상", "묽은 변", "물설사", "딱딱한 변", "배변이 어려움", "배변하지 않음", ], )

foods = st.text_input( "오늘 먹은 음식", placeholder="예: 커피, 우유, 라면, 사과", )

notes = st.text_area( "추가 메모", placeholder="식사 후 증상, 운동 등", )

submitted = st.formsubmitbutton( "오늘 기록 저장하기", usecontainerwidth=True, )

if submitted: st.sessionstate.records.append( { "날짜": str(recorddate), "복통": pain, "복부 팽만": bloating, "설사": diarrhea, "변비": constipation, "스트레스": stress, "수면 시간": sleep, "배변 상태": bowel, "먹은 음식": foods.strip(), "메모": notes.strip(), } ) st.success("오늘의 기록을 저장했어요!")

st.caption( "기록은 현재 세션에 보관됩니다. " "세션이 끝나면 사라질 수 있으니 CSV로 다운로드하세요." )

with tab2: st.subheader("나의 증상 패턴")

if not st.sessionstate.records: st.info("먼저 증상 기록 탭에서 기록을 남겨보세요.") else: df = pd.DataFrame(st.sessionstate.records)

st.metric("누적 기록", f"{len(df)}일")

symptomcols = ["복통", "복부 팽만", "설사", "변비"] averages = df[symptomcols].mean().round(1)

st.markdown("### 증상 평균 점수") st.bar_chart(averages)

st.markdown("### 날짜별 기록") st.dataframe( df.sortvalues("날짜", ascending=False), usecontainerwidth=True, hideindex=True, )

st.markdown("### 관찰해 볼 점")

dailysymptoms = df[symptomcols].mean(axis=1) stresscorr = df["스트레스"].corr(dailysymptoms)

if len(df) >= 3 and pd.notna(stresscorr): if stresscorr >= 0.4: st.write( "스트레스가 높을 때 증상 점수도 높아지는 " "경향이 관찰됩니다. 더 많은 기록으로 확인해 보세요." ) elif stress_corr <= -0.4: st.write( "스트레스와 증상 점수가 반대 방향으로 움직이는 " "경향이 있습니다. 기록을 더 쌓아 관찰해 보세요." ) else: st.write( "현재 기록에서는 스트레스와 증상 사이에 " "뚜렷한 선형 관계가 보이지 않습니다." ) else: st.write("며칠 더 기록하면 패턴을 살펴보는 데 도움이 됩니다.")

food_df = df[df["먹은 음식"].fillna("").str.strip() != ""]

if not food_df.empty: st.write( "음식 섭취와 증상이 나타난 날짜를 비교해 보세요. " "이 기록만으로 특정 음식이 원인이라고 판단할 수는 없습니다." )

csv = df.to_csv(index=False).encode("utf-8-sig")

st.downloadbutton( "📥 기록 CSV 다운로드", data=csv, filename="ibssymptomlog.csv", mime="text/csv", usecontainerwidth=True, )

with tab3: st.subheader("오늘부터 실천하는 관리 가이드")

st.markdown("### 🍚 식사 관리") st.write( "- 규칙적으로 식사하고 천천히 먹어 보세요.\n" "- 커피, 술, 탄산음료 등이 증상에 영향을 주는지 기록하세요.\n" "- 여러 음식을 한꺼번에 제한하지 말고 하나씩 관찰하세요." )

st.markdown("### 💧 생활 습관") st.write( "- 수분을 충분히 섭취하세요.\n" "- 가벼운 걷기와 규칙적인 수면을 시도하세요.\n" "- 복식호흡이나 짧은 이완 시간을 가져 보세요." )

st.markdown("### 🥗 저포드맵 식단") st.write( "일부 IBS 환자는 저포드맵 식단에서 도움을 얻을 수 있습니다. " "다만 모든 사람에게 필요한 것은 아닙니다. " "장기간 식품을 제한하기 전에는 의료진이나 영양사와 상담하세요." )

st.warning( "혈변, 검은 변, 원인 모를 체중 감소, 발열 또는 지속적인 " "심한 복통이 있으면 의료진의 진료를 받으세요. " "갑작스럽고 극심한 복통이나 심한 출혈은 응급 진료가 필요합니다." )

st.divider() st.caption("IBS Helper | 나의 기록이 더 나은 관리의 시작입니다.")
