import streamlit as st
import requests

# 주요 도시 목록
cities = {
    "New York": "5128581",
    "London": "2643743",
    "Paris": "2988507",
    "Seoul": "1835848",
    "Tokyo": "1850147",
    "Beijing": "1816670",
    "Sydney": "2147714"
}

API_KEY = st.secrets["openweathermap_api_key"]

def get_weather(city_id):
    url = f"http://api.openweathermap.org/data/2.5/weather?id={city_id}&appid={API_KEY}&units=metric"
    res = requests.get(url)
    data = res.json()
    return {
        "Temperature": f"{data['main']['temp']}°C",
        "Weather": data['weather'][0]['description'].title()
    }

def get_air_quality(city_id):
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?appid={API_KEY}&id={city_id}"
    res = requests.get(url)
    data = res.json()
    pm2_5 = data['list'][0]['components']['pm2_5']
    return f"{pm2_5} μg/m³"

def main():
    st.title("🌍 세계 도시 날씨 & 미세먼지 정보")

    city = st.selectbox("도시를 선택하세요", list(cities.keys()))

    if st.button("정보 보기"):
        city_id = cities[city]
        with st.spinner("데이터 가져오는 중..."):
            weather = get_weather(city_id)
            air_quality = get_air_quality(city_id)

        st.markdown(f"### 📍 {city}")
        st.write(f"🌤️ 날씨: {weather['Weather']}")
        st.write(f"🌡️ 기온: {weather['Temperature']}")
        st.write(f"🌫️ PM2.5(미세먼지): {air_quality}")

if __name__ == "__main__":
    main()