
import math
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ==========================================
# 기본 설정
# ==========================================
st.set_page_config(
    page_title="오성고 안심화장실",
    page_icon="🚻",
    layout="wide",
)

st.title("🏫 오성고 안심화장실")
st.caption("천안오성고등학교 배치도 참고 · IBS 학생을 위한 화장실 찾기")

st.info(
    "학교 배치도 사진을 바탕으로 만든 시범 지도입니다. "
    "위치와 거리는 개략적이며 실제 측량 결과가 아닙니다."
)

# ==========================================
# 학교 공간 데이터
# 좌표: x=가로, y=세로, z=층
# 사진의 구조를 단순화한 참고용 좌표
# ==========================================
FLOORS = [1, 2, 3, 4, 5]

# 층별 화장실 위치
TOILETS = {
    1: [
        {"name": "1층 서쪽 화장실", "x": 18, "y": 55},
        {"name": "1층 중앙 화장실", "x": 43, "y": 55},
        {"name": "1층 동쪽 화장실", "x": 79, "y": 55},
        {"name": "1층 강당 옆 화장실", "x": 88, "y": 28},
    ],
    2: [
        {"name": "2층 서쪽 화장실", "x": 20, "y": 70},
        {"name": "2층 중앙 화장실", "x": 53, "y": 70},
        {"name": "2층 동쪽 화장실", "x": 85, "y": 70},
        {"name": "2층 서쪽 아래 화장실", "x": 27, "y": 43},
        {"name": "2층 중앙 아래 화장실", "x": 57, "y": 43},
        {"name": "2층 동쪽 아래 화장실", "x": 86, "y": 43},
    ],
    3: [
        {"name": "3층 서쪽 화장실", "x": 20, "y": 70},
        {"name": "3층 중앙 화장실", "x": 53, "y": 70},
        {"name": "3층 동쪽 화장실", "x": 85, "y": 70},
        {"name": "3층 서쪽 아래 화장실", "x": 27, "y": 43},
        {"name": "3층 중앙 아래 화장실", "x": 57, "y": 43},
        {"name": "3층 동쪽 아래 화장실", "x": 86, "y": 43},
    ],
    4: [
        {"name": "4층 서쪽 화장실", "x": 20, "y": 70},
        {"name": "4층 중앙 화장실", "x": 53, "y": 70},
        {"name": "4층 동쪽 화장실", "x": 85, "y": 70},
        {"name": "4층 서쪽 아래 화장실", "x": 27, "y": 43},
        {"name": "4층 중앙 아래 화장실", "x": 57, "y": 43},
        {"name": "4층 동쪽 아래 화장실", "x": 86, "y": 43},
    ],
    5: [
        {"name": "5층 서쪽 화장실", "x": 24, "y": 76},
        {"name": "5층 중앙 화장실", "x": 55, "y": 76},
        {"name": "5층 동쪽 화장실", "x": 86, "y": 76},
        {"name": "5층 서쪽 아래 화장실", "x": 30, "y": 48},
        {"name": "5층 중앙 아래 화장실", "x": 59, "y": 48},
        {"name": "5층 동쪽 아래 화장실", "x": 88, "y": 48},
    ],
}

# 학생이 현재 위치를 직접 선택할 수 있는 주요 장소
LOCATIONS = {
    1: {
        "교무센터1": (27, 17),
        "교장실": (43, 17),
        "행정실": (53, 17),
        "보건실": (49, 45),
        "학생부 교무실": (15, 45),
        "소강당": (87, 20),
        "식생활교육관": (91, 7),
        "PBL2": (76, 36),
        "PBL3": (76, 47),
        "운영사무실": (48, 45),
        "1층 복도 중앙": (50, 55),
        "주 출입구": (60, 10),
    },
    2: {
        "1-1 교실": (20, 84),
        "1-2 교실": (20, 78),
        "1-3 교실": (20, 72),
        "1-4 교실": (20, 66),
        "1-5 교실": (20, 60),
        "1학년 교무실": (30, 17),
        "정보자료실(도서실)": (60, 17),
        "건강체육부": (76, 17),
        "AI실습실": (84, 37),
        "2층 복도 중앙": (50, 53),
        "계단 앞": (27, 44),
    },
    3: {
        "2-1 교실": (20, 84),
        "2-2 교실": (20, 78),
        "2-3 교실": (20, 72),
        "2-4 교실": (20, 66),
        "2-5 교실": (20, 60),
        "2학년 교무실": (62, 17),
        "만만화실": (30, 17),
        "PBL5": (65, 17),
        "AI실습실": (85, 36),
        "3층 복도 중앙": (50, 53),
        "계단 앞": (27, 44),
    },
    4: {
        "3-1 교실": (20, 84),
        "3-2 교실": (20, 78),
        "3-3 교실": (20, 72),
        "3-4 교실": (20, 66),
        "3-5 교실": (20, 60),
        "3-6 교실": (53, 84),
        "3-7 교실": (53, 78),
        "3-8 교실": (53, 72),
        "3-9 교실": (53, 66),
        "3-10 교실": (78, 60),
        "3-11 교실": (78, 66),
        "3-12 교실": (78, 72),
        "3-13 교실": (78, 78),
        "4층 복도 중앙": (50, 53),
        "계단 앞": (27, 44),
    },
    5: {
        "미술실": (18, 88),
        "융합정보실": (18, 76),
        "시청각실": (15, 40),
        "교무센터2": (35, 30),
        "생명과학실": (53, 76),
        "지구과학실": (77, 88),
        "물리실": (77, 70),
        "음악실1": (88, 44),
        "음악실2": (88, 30),
        "5층 복도 중앙": (52, 52),
        "계단 앞": (27, 44),
    },
}


def distance_2d(a, b):
    """평면 좌표상 직선거리. 실제 미터 단위는 아님."""
    return math.sqrt(
        (a["x"] - b[0]) ** 2 + (a["y"] - b[1]) ** 2
    )


def make_3d_school(current_floor, current_xy):
    """층을 쌓아 학교 건물처럼 보이는 3D 시각화."""
    fig = go.Figure()

    # 층별 바닥판과 외곽선
    for floor in FLOORS:
        z = floor * 5

        # 학교 층별 판
        fig.add_trace(
            go.Mesh3d(
                x=[0, 100, 100, 0],
                y=[0, 0, 100, 100],
                z=[z, z, z, z],
                i=[0, 0],
                j=[1, 2],
                k=[2, 3],
                color="#d9e6ee",
                opacity=0.22,
                name=f"{floor}층",
                hovertemplate=f"{floor}층<extra></extra>",
                showscale=False,
            )
        )

        # 층 외곽선
        fig.add_trace(
            go.Scatter3d(
                x=[0, 100, 100, 0, 0],
                y=[0, 0, 100, 100, 0],
                z=[z, z, z, z, z],
                mode="lines",
                line=dict(color="#64748b", width=3),
                showlegend=False,
                hoverinfo="skip",
            )
        )

        # 층 이름
        fig.add_trace(
            go.Scatter3d(
                x=[-8],
                y=[50],
                z=[z],
                mode="text",
                text=[f"{floor}층"],
                textfont=dict(size=13, color="#1f2937"),
                showlegend=False,
                hoverinfo="skip",
            )
        )

        # 층별 화장실 위치
        toilets = TOILETS[floor]
        fig.add_trace(
            go.Scatter3d(
                x=[t["x"] for t in toilets],
                y=[t["y"] for t in toilets],
                z=[z + 0.7] * len(toilets),
                mode="markers",
                marker=dict(
                    size=7,
                    color="#159b82",
                    symbol="diamond",
                    line=dict(color="white", width=1),
                ),
                name=f"{floor}층 화장실",
                text=[t["name"] for t in toilets],
                hovertemplate="%{text}<extra></extra>",
            )
        )

    # 현재 위치 표시
    if current_xy:
        fig.add_trace(
            go.Scatter3d(
                x=[current_xy[0]],
                y=[current_xy[1]],
                z=[current_floor * 5 + 1.5],
                mode="markers+text",
                marker=dict(
                    size=10,
                    color="#ef4444",
                    symbol="circle",
                    line=dict(color="white", width=2),
                ),
                text=["현재 위치"],
                textposition="top center",
                name="현재 위치",
                hovertemplate="현재 위치<extra></extra>",
            )
        )

    fig.update_layout(
        height=620,
        margin=dict(l=0, r=0, t=25, b=0),
        scene=dict(
            xaxis=dict(title="학교 가로 방향", range=[-12, 105]),
            yaxis=dict(title="학교 세로 방향", range=[0, 105]),
            zaxis=dict(
                title="층",
                tickvals=[f * 5 for f in FLOORS],
                ticktext=[f"{f}층" for f in FLOORS],
                range=[0, 31],
            ),
            aspectmode="manual",
            aspectratio=dict(x=1.2, y=1.0, z=0.65),
            camera=dict(eye=dict(x=1.6, y=1.6, z=1.2)),
        ),
        legend=dict(orientation="h", y=-0.08),
    )
    return fig


def make_floor_map(floor, current_xy, recommended=None):
    """선택 층의 개략적인 2D 위치 지도."""
    fig = go.Figure()

    # 학교 외곽
    fig.add_shape(
        type="rect",
        x0=0, y0=0, x1=100, y1=100,
        line=dict(color="#64748b", width=3),
        fillcolor="#f1f5f9",
    )

    # 공간을 단순화한 건물 구역
    rooms = [
        (5, 58, 25, 36, "서쪽 교실 구역"),
        (36, 58, 25, 36, "중앙 교실 구역"),
        (68, 58, 27, 36, "동쪽 교실 구역"),
        (5, 10, 25, 35, "서쪽 시설"),
        (36, 10, 25, 35, "중앙 시설"),
        (68, 10, 27, 35, "동쪽 시설"),
    ]

    for x0, y0, x1, y1, label in rooms:
        fig.add_shape(
            type="rect",
            x0=x0, y0=y0, x1=x0 + x1, y1=y0 + y1,
            line=dict(color="#a8b4c0", width=1),
            fillcolor="white",
        )

        fig.add_annotation(
            x=x0 + x1 / 2,
            y=y0 + y1 / 2,
            text=label,
            showarrow=False,
            font=dict(size=10, color="#64748b"),
        )

    # 화장실 표시
    toilets = TOILETS[floor]
    fig.add_trace(
        go.Scatter(
            x=[t["x"] for t in toilets],
            y=[t["y"] for t in toilets],
            mode="markers+text",
            marker=dict(
                size=16,
                color="#159b82",
                symbol="square",
                line=dict(color="white", width=1),
            ),
            text=["🚻" for _ in toilets],
            textposition="middle center",
            customdata=[t["name"] for t in toilets],
            name="화장실",
            hovertemplate="%{customdata}<extra></extra>",
        )
    )

    # 선택한 현재 위치와 추천 화장실 사이 참고선
    if current_xy and recommended:
        target = recommended[0]

        fig.add_trace(
            go.Scatter(
                x=[current_xy[0], target["x"]],
                y=[current_xy[1], target["y"]],
                mode="lines",
                line=dict(color="#ef4444", width=4, dash="dash"),
                name="참고 경로",
                hoverinfo="skip",
            )
        )

        fig.add_trace(
            go.Scatter(
                x=[current_xy[0]],
                y=[current_xy[1]],
                mode="markers+text",
                marker=dict(size=18, color="#ef4444"),
                text=["현재 위치"],
                textposition="top center",
                name="현재 위치",
            )
        )

    fig.update_layout(
        title=f"{floor}층 개략 지도",
        height=490,
        margin=dict(l=10, r=10, t=50, b=10),
        xaxis=dict(range=[-3, 103], visible=False),
        yaxis=dict(range=[-3, 103], visible=False, scaleanchor="x"),
        legend=dict(orientation="h", y=-0.12),
    )

    return fig


# ==========================================
# 메인 화면
# ==========================================
tab_map, tab_detail, tab_info = st.tabs(
    ["🏫 3D 학교 지도", "🚻 층별 화장실", "ℹ️ 이용 안내"]
)

with tab_map:
    st.subheader("📍 현재 위치를 선택해 줘")

    left, right = st.columns([1, 1])

    with left:
        current_floor = st.selectbox(
            "현재 있는 층",
            FLOORS,
            format_func=lambda f: f"{f}층",
            key="current_floor",
        )

        place_names = list(LOCATIONS[current_floor].keys())

        current_place = st.selectbox(
            "현재 있는 교실 또는 시설",
            place_names,
            key=f"place_{current_floor}",
        )

        current_xy = LOCATIONS[current_floor][current_place]

        st.success(
            f"현재 위치: {current_floor}층 · {current_place}"
        )

        st.caption(
            "장소를 선택하면 해당 위치를 기준으로 "
            "같은 층의 가까운 화장실을 추천해."
        )

    with right:
        st.metric("현재 층", f"{current_floor}층")
        st.metric("등록된 해당 층 화장실", f"{len(TOILETS[current_floor])}곳")
        st.metric("현재 위치", current_place)

    # 같은 층 화장실 거리순 계산
    candidates = []

    for toilet in TOILETS[current_floor]:
        dist = distance_2d(toilet, current_xy)
        candidates.append({**toilet, "거리점수": dist})

    candidates.sort(key=lambda t: t["거리점수"])
    recommended = candidates[:3]

    st.markdown("### 🟢 가까운 화장실 추천")

    for i, toilet in enumerate(recommended, start=1):
        with st.container(border=True):
            c1, c2 = st.columns([3, 1])

            with c1:
                st.markdown(f"**{i}. 🚻 {toilet['name']}**")
                st.caption(
                    f"현재 위치에서 지도상 거리 점수: "
                    f"{toilet['거리점수']:.1f}"
                )

            with c2:
                st.write("같은 층")

    st.caption(
        "거리 점수는 개략적인 평면 좌표 간 거리이며 미터 단위가 아니야. "
        "실제 보행 거리나 가장 빠른 경로와 다를 수 있어."
    )

    st.markdown("### 🏢 입체적인 학교 전체 지도")

    fig_3d = make_3d_school(current_floor, current_xy)
    st.plotly_chart(fig_3d, use_container_width=True)

    st.markdown("### 🗺️ 현재 층 상세 지도")

    fig_2d = make_floor_map(
        current_floor,
        current_xy,
        recommended,
    )
    st.plotly_chart(fig_2d, use_container_width=True)


with tab_detail:
    st.subheader("층별 화장실 위치 확인")

    detail_floor = st.selectbox(
        "확인할 층",
        FLOORS,
        format_func=lambda f: f"{f}층",
        key="detail_floor",
    )

    floor_toilets = TOILETS[detail_floor]

    st.write(f"**{detail_floor}층 화장실: {len(floor_toilets)}곳**")

    detail_df = pd.DataFrame([
        {
            "화장실": t["name"],
            "가로 좌표(참고)": t["x"],
            "세로 좌표(참고)": t["y"],
        }
        for t in floor_toilets
    ])

    st.dataframe(
        detail_df,
        use_container_width=True,
        hide_index=True,
    )

    st.plotly_chart(
        make_floor_map(detail_floor, None),
        use_container_width=True,
    )

    st.warning(
        "이 화면은 사진을 바탕으로 공간을 단순화한 참고 지도야. "
        "실제 화장실 출입구와 통로 위치는 학교에서 확인해야 해."
    )


with tab_info:
    st.subheader("안심화장실 이용 방법")

    st.markdown(
        """
        1. **3D 학교 지도** 탭으로 이동해.
        2. 현재 있는 층을 선택해.
        3. 현재 있는 교실이나 시설을 선택해.
        4. 가까운 화장실 추천 목록을 확인해.
        5. 3D 지도와 층별 상세 지도로 위치를 확인해.

        ### 지도 정보 안내
        - 화장실 위치는 사용자가 제공한 학교 배치도를 참고한 개략적 위치야.
        - 좌표상 거리는 실제 미터나 보행 시간과 같지 않아.
        - 벽, 출입문, 계단, 이동 동선을 반영한 실내 길 찾기는 아직 구현되지 않았어.
        - 실제 이용 전에 화장실 위치와 접근 가능 여부를 확인해 줘.

        ### 개인정보 보호
        - 현재 위치는 사용자가 직접 선택해.
        - GPS나 건강정보를 자동으로 수집하지 않아.
        """
    )

st.divider()
st.caption(
    "오성고 안심화장실 | 학교 배치도 기반 시범 서비스"
)
