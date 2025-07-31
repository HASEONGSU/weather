import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="세계 주요 도시 날씨", layout="centered")

st.title("🌏 세계 주요 도시 날씨 정보")
st.markdown("※ 데이터 출처: [기상청 세계날씨](https://www.weather.go.kr/w/theme/world-weather.do)")

# 도시 목록 (기상청 웹사이트 기준 일부 예시)
city_dict = {
    "서울 (Seoul)": "182",
    "도쿄 (Tokyo)": "237",
    "뉴욕 (New York)": "133",
    "런던 (London)": "96",
    "베이징 (Beijing)": "25",
    "하노이 (Hanoi)": "61",
    "시드니 (Sydney)": "173",
    "파리 (Paris)": "157",
    "싱가포르 (Singapore)": "166"
}

city_name = st.selectbox("도시를 선택하세요", list(city_dict.keys()))

if city_name:
    city_code = city_dict[city_name]
    url = f"https://www.weather.go.kr/w/theme/world-weather.do?worldWeatherType=WORLDW&worldWeatherCode={city_code}"

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        temp = soup.select_one(".weather_table td.temp")
        desc = soup.select_one(".weather_table td.weather")

        if temp and desc:
            st.subheader(f"📍 {city_name}")
            st.metric("기온", temp.text.strip())
            st.markdown(f"**날씨 상태**: {desc.text.strip()}")
        else:
            st.error("❌ 날씨 정보를 찾을 수 없습니다.")
    except Exception as e:
        st.error(f"오류 발생: {e}")