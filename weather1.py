import streamlit as st
import requests
from streamlit_lottie import st_lottie

# 1. 페이지 기본 설정 (깔끔한 기본 테마 활용)
st.set_page_config(page_title="방배동 종합 날씨 정보", page_icon="🌤️", layout="centered")

# 2. 글로벌 기상 데이터 수집 함수 (실패 시 안전장치 포함)
def get_bangbae_weather_global():
    url = "https://wttr.in/Bangbae-dong?format=j1"
    default_return = (22, "Clear", "맑음 (기본 로드)", "보통", "15km", "05:32", "19:51")
    try:
        response = requests.get(url, timeout=4)
        if response.status_code == 200:
            data = response.json()
            current = data['current_condition'][0]
            astronomy = data['weather'][0]['astronomy'][0]
            
            temp = round(float(current['temp_C'])) 
            weather_desc_en = current['weatherDesc'][0]['value'].lower()
            
            visibility = current['visibility'] + "km"
            humidity = int(current['humidity'])
            
            if humidity > 85: dust = "좋음"
            elif 40 <= humidity <= 85: dust = "보통"
            else: dust = "나쁨 (건조)"
            
            sunrise = astronomy['sunrise']
            sunset = astronomy['sunset']
            
            weather_main = "Clear"
            weather_desc_kr = "맑음"
            
            if "cloud" in weather_desc_en or "overcast" in weather_desc_en:
                weather_main = "Clouds"
                weather_desc_kr = "구름 많음"
            elif "rain" in weather_desc_en or "shower" in weather_desc_en or "drizzle" in weather_desc_en:
                weather_main = "Rain"
                weather_desc_kr = "비옴"
            elif "snow" in weather_desc_en or "ice" in weather_desc_en:
                weather_main = "Snow"
                weather_desc_kr = "눈"
                
            return temp, weather_main, weather_desc_kr, dust, visibility, sunrise, sunset
        else:
            return default_return
    except:
        return default_return

# Lottie 로드 함수
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200: return None
    return r.json()

# 데이터 로드
temp, weather_main, weather_desc, dust, visibility, sunrise, sunset = get_bangbae_weather_global()

# 미세먼지 색상 설정
dust_color = "#2ed573" if "좋음" in dust or "보통" in dust else "#ff4757"

# Lottie 카드 매핑
lottie_urls = {
    "Clear": "https://assets3.lottiefiles.com/packages/lf20_xl8aHg.json",
    "Clouds": "https://assets9.lottiefiles.com/packages/lf20_w98qf0as.json",
    "Rain": "https://assets4.lottiefiles.com/packages/lf20_iam97t69.json",
    "Snow": "https://assets1.lottiefiles.com/packages/lf20_96bva6g1.json"
}
lottie_url = lottie_urls.get(weather_main, "https://assets5.lottiefiles.com/packages/lf20_xl8aHg.json")

# 3. 가독성을 극대화한 깔끔한 카드 CSS 주입
st.markdown(f"""
    <link href="https://fonts.googleapis.com/css2?family=Gowun+Dodum&display=swap" rel="stylesheet">
    <style>
        html, body, [data-testid="stAppViewContainer"] {{
            font-family: 'Gowun Dodum', sans-serif;
            background-color: #f8f9fa !important;
        }}
        .main-title {{ text-align: center; font-size: 2.3rem; font-weight: bold; color: #222222; margin-top: 20px; }}
        .sub-title {{ text-align: center; color: #666666; margin-bottom: 30px; }}
        
        /* 정보 가독성을 위한 기본 화이트 카드 디자인 */
        .weather-card {{
            background: #ffffff;
            border-radius: 16px;
            padding: 25px;
            box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.05);
            border: 1px solid #eaeaea;
            margin-bottom: 20px;
        }}
        
        /* 대기 지표 그리드 레이아웃 */
        .info-grid {{ display: flex; justify-content: space-between; gap: 15px; margin-top: 15px; }}
        .info-box {{
            flex: 1; background: #f1f3f5; border-radius: 12px; padding: 15px;
            text-align: center;
        }}
        .info-icon {{ font-size: 2rem; margin-bottom: 5px; }}
        .info-title {{ font-size: 0.85rem; color: #666666; margin-bottom: 4px; }}
        .info-value {{ font-size: 1.05rem; font-weight: bold; color: #222222; }}
        
        .bar-container {{ background: #dee2e6; border-radius: 10px; height: 6px; margin-top: 8px; overflow: hidden; }}
        .bar-fill {{ background: {dust_color}; height: 100%; border-radius: 100px; }}

        .highlight {{ color: #ff4757; font-weight: bold; }}
    </style>
""", unsafe_allow_html=True)

# 4. 상단 타이틀 구성
st.markdown("<h1 class='main-title'>📍 방배동 실시간 종합 날씨</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>대기질 환경 지표 및 스마트 코디 가이드</p>", unsafe_allow_html=True)

# 중앙 날씨 캐릭터 아이콘 출력
lottie_motion = load_lottieurl(lottie_url)
if lottie_motion:
    st_lottie(lottie_motion, height=180, key="center_lottie")

# 5. 현재 기온 및 대기질 메인 대시보드 카드 출력
st.markdown(f"""
    <div class='weather-card' style='text-align: center;'>
        <h2 style='margin: 0; color: #222222;'>🌡️ 현재 기온: {temp}°C ({weather_desc})</h2>
    </div>
""", unsafe_allow_html=True)

st.markdown(f"""
    <div class='weather-card'>
        <h3 style='margin-top:0; color:#222222; font-size:1.25rem; text-align:center;'>📊 실시간 기상 인덱스</h3>
        <div class='info-grid'>
            <div class='info-box'>
                <div class='info-icon'>🌅</div>
                <div class='info-title'>일출 시간</div>
                <div class='info-value'>{sunrise}</div>
            </div>
            <div class='info-box'>
                <div class='info-icon'>🌇</div>
                <div class='info-title'>일몰 시간</div>
                <div class='info-value'>{sunset}</div>
            </div>
            <div class='info-box'>
                <div class='info-icon'>😷</div>
                <div class='info-title'>대기 현황</div>
                <div class='info-value' style='color:{dust_color};'>{dust}</div>
                <div class='bar-container'><div class='bar-fill' style='width: {"35%" if "좋음" in dust or "보통" in dust else "80%"};'></div></div>
            </div>
            <div class='info-box'>
                <div class='info-icon'>👁️</div>
                <div class='info-title'>가시거리</div>
                <div class='info-value'>{visibility}</div>
                <div class='bar-container'><div class='bar-fill' style='background:#70a1ff; width: 85%;'></div></div>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# 6. 기온별 맞춤형 코디 제안 카드 출력
card_content = ""
if temp >= 28:
    card_content = "☀️ <b>한여름 폭염 날씨예요!</b><br>👉 추천 코디: <span class='highlight'>민소매, 반팔티, 린넨 쇼츠, 선글라스</span>"
elif 23 <= temp < 28:
    card_content = "🌤️ <b>산뜻하고 가벼운 여름 기온이에요.</b><br>👉 추천 코디: <span class='highlight'>반팔 셔츠, 슬림 면바지, 오픈형 샌들</span>"
elif 20 <= temp < 23:
    card_content = "🍃 <b>선선하고 부드러운 봄/가을 온도대입니다.</b><br>👉 추천 코디: <span class='highlight'>옥스퍼드 셔츠, 니트조끼, 데님 팬츠</span>"
elif 17 <= temp < 20:
    card_content = "🧥 <b>일교차가 가파릅니다. 아우터 필수 구비!</b><br>👉 추천 코디: <span class='highlight'>맨투맨, 후디, 가디건 레이어링</span>"
elif 12 <= temp < 17:
    card_content = "🍂 <b>찬 기운이 옷깃을 가르는 쌀쌀한 환절기입니다.</b><br>👉 추천 코디: <span class='highlight'>울 재킷, 트렌치 코트, 도톰한 니트</span>"
elif 9 <= temp < 12:
    card_content = "💨 <b>외풍이 강하니 레이어드룩이 제격입니다.</b><br>👉 추천 코디: <span class='highlight'>야상 점퍼, 도톰한 헤비 니트, 기모바지</span>"
elif 5 <= temp < 9:
    card_content = "🥶 <b>서리가 내리는 초겨울 추위 시즌이에요!</b><br>👉 추천 코디: <span class='highlight'>롱코트, 무스탕 재킷, 다운 패딩, 발열내의</span>"
else:
    card_content = "❄️ <b>동파 사고를 조심해야 하는 겨울 한파 침공 기온입니다!</b><br>👉 추천 코디: <span class='highlight'>롱패딩, 방한 목도리, 장갑 필수</span>"

st.markdown(f"""
    <div class='weather-card' style='font-size: 1.15rem; line-height: 1.8; color: #222222;'>
        {card_content}
    </div>
""", unsafe_allow_html=True)
