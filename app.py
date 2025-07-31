import streamlit as st
import requests
from datetime import datetime, timedelta

# API 키
API_KEY_KMA = st.secrets.get("kma_service_key")
API_KEY_OWM = st.secrets.get("openweathermap_api_key")

if not API_KEY_KMA:
    st.error("⚠️ 기상청 단기예보 API 키가 없습니다.")
    st.stop()

# 주요 도시와 기상청 격자 좌표 (nx, ny)
cities = {
    "Seoul": (60, 127),
    "Busan": (98, 76),
    "Incheon": (55, 124),
    "New York": (72, 141),  # 예시 좌표, 실제 사용 불가
    "London": (50, 120),    # 예시 좌표, 실제 사용 불가
}

def get_kma_weather(nx, ny):
    now = datetime.utcnow() + timedelta(hours=9)
    base_date = now.strftime("%Y%m%d")
    base_time = f"{(now.hour // 3) * 3:02}00"

    url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"
    params = {
        "serviceKey": API_KEY_KMA,
        "base_date": base_date,
        "base_time": base_time,
        "nx": nx,
        "ny": ny,
        "numOfRows": 1000,
        "pageNo": 1,
        "dataType": "JSON"
    }

    res = requests.get(url, params=params)
    if res.status_code != 200:
        return {"error": "API 호출 실패"}

    items = res.json().get("response", {}).get("body", {}).get("items", {}).get("item", [])
    forecast = {item['category']: item['fcstValue'] for item in items if item['fcstDate'] == base_date}

    return {
        "Temperature": forecast.get("TMP", "N/A") + "°C",
        "Weather": forecast.get("WFK", "맑음")
    }

def main():
    st.title("🌍 세계 도시 날씨 정보 (기상청 API)")

    city = st.selectbox("도시를 선택하세요", list(cities.keys()))

    if st.button("날씨 보기"):
        nx, ny = cities[city]
        weather = get_kma_weather(nx, ny)
        if "error" in weather:
            st.error(weather["error"])
        else:
            st.markdown(f"### 📍 {city}")
            st.write(f"🌡️ 기온: {weather['Temperature']}")
            st.write(f"🌤️ 날씨: {weather['Weather']}")

if __name__ == "__main__":
    main()