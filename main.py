import streamlit as st
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# 학교 데이터
data = {
    "학교명": [
        "서울서초초등학교",
        "서운중학교",
        "서초고등학교",
        "동덕여자고등학교"  # 추가됨
    ],
    "주소": [
        "서울특별시 서초구 서초대로 50",
        "서울특별시 서초구 반포대로 10",
        "서울특별시 서초구 반포대로 85",
        "서울특별시 강남구 선릉로 119길 26"  # 동덕여고 주소
    ],
    "위도": [
        37.4877,
        37.4945,
        37.5002,
        37.5197  # 동덕여고 위도
    ],
    "경도": [
        127.0156,
        127.0124,
        127.0053,
        127.0430  # 동덕여고 경도
    ]
}

df = pd.DataFrame(data)

# Streamlit 앱
st.title("서초구 학교 지도 (동덕여고 포함)")
st.write("서울시 서초구 및 인근의 학교들을 지도에 표시합니다.")

# folium 지도 생성
m = folium.Map(location=[37.4900, 127.0200], zoom_start=13)

# 마커 추가
for idx, row in df.iterrows():
    color = "blue" if "동덕" not in row["학교명"] else "red"
    folium.Marker(
        location=[row["위도"], row["경도"]],
        popup=f"{row['학교명']}<br>{row['주소']}",
        tooltip=row["학교명"],
        icon=folium.Icon(color=color, icon="info-sign")
    ).add_to(m)

# Streamlit에 지도 표시
st_data = st_folium(m, width=700, height=500)

