import streamlit as st
import requests
from streamlit_lottie import st_lottie

# 1. 페이지 기본 설정
st.set_page_config(page_title="방배동 종합 날씨 정보", page_icon="🌤️", layout="centered")

# 2. 글로벌 기상 데이터 수집 함수
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

# 3. 날씨별 배경(하늘, 땅, 태양/구름 오브젝트) 테마 구성
weather_themes = {
    "Clear": {
        "sky": "linear-gradient(to bottom, #74b9ff, #a29bfe)", 
        "ground": "#55efc4",
        "objects": '<div class="sun"></div><div class="cloud-ani c1"></div><div class="cloud-ani c2"></div>',
        "lottie": "https://assets3.lottiefiles.com/packages/lf20_xl8aHg.json"
    },
    "Clouds": {
        "sky": "linear-gradient(to bottom, #747d8c, #a4b0be)", 
        "ground": "#2ed573",
        "objects": '<div class="cloud-ani c1" style="opacity: 0.9;"></div><div class="cloud-ani c2" style="transform: scale(1.4); top: 22%; animation-duration: 25s;"></div>',
        "lottie": "https://assets9.lottiefiles.com/packages/lf20_w98qf0as.json"
    },
    "Rain": {
        "sky": "linear-gradient(to bottom, #2f3640, #718093)", 
        "ground": "#05c46b",
        "objects": '<div class="cloud-ani c1" style="background: #718093;"></div><div class="rain-drop r1"></div><div class="rain-drop r2"></div><div class="rain-drop r3"></div>',
        "lottie": "https://assets4.lottiefiles.com/packages/lf20_iam97t69.json"
    },
    "Snow": {
        "sky": "linear-gradient(to bottom, #dfe4ea, #f1f2f6)", 
        "ground": "#ffffff",
        "objects": '<div class="snowflake s1"></div><div class="snowflake s2"></div><div class="snowflake s3"></div>',
        "lottie": "https://assets1.lottiefiles.com/packages/lf20_96bva6g1.json"
    }
}

theme = weather_themes.get(weather_main, weather_themes["Clear"])

# 4. 레이어 분리형 고해상도 CSS 주입
st.markdown(f"""
    <link href="https://fonts.googleapis.com/css2?family=Gowun+Dodum&display=swap" rel="stylesheet">
    <style>
        /* [핵심] 최하단 기본 브라우저 영역에만 배경 하늘색 부여 */
        html, body, [data-testid="stAppViewContainer"] {{
            font-family: 'Gowun Dodum', sans-serif;
            background: {theme["sky"]} !important;
            overflow-x: hidden;
            position: relative;
        }}
        
        /* [핵심] 3D 땅(언덕)을 최하단 z-index로 깔아 글자 영역 침범 차단 */
        [data-testid="stAppViewContainer"]::after {{
            content: ""; position: fixed; bottom: -150px; left: -10%; width: 120%; height: 320px;
            background: {theme["ground"]}; border-radius: 50% 50% 0 0; 
            z-index: -2 !important; /* 글자 뒤로 완전히 밀어내기 */
            box-shadow: inset 0 20px 30px rgba(0,0,0,0.05);
        }}

        /* 날씨 테마별 그래픽 오브젝트 스타일 */
        .sun {{
            position: fixed; top: 10%; right: 10%; width: 85px; height: 85px;
            background: radial-gradient(circle, #fffa65, #ffaf40); border-radius: 50%; z-index: -1;
            box-shadow: 0 0 40px #ffaf40; animation: pulse 4s infinite alternate;
        }}
        @keyframes pulse {{ 0% {{ transform: scale(1); }} 100% {{ transform: scale(1.06); }} }}

        .cloud-ani {{ position: fixed; background: rgba(255,255,255,0.8); border-radius: 100px; width: 150px; height: 45px; z-index: -1; }}
        .cloud-ani::before, .cloud-ani::after {{ content: ""; position: absolute; background: rgba(255,255,255,0.8); border-radius: 50%; }}
        .cloud-ani::before {{ width: 65px; height: 65px; top: -30px; left: 20px; }}
        .cloud-ani::after {{ width: 85px; height: 85px; top: -40px; right: 15px; }}
        .c1 {{ top: 15%; left: -200px; animation: floatCloud 24s infinite linear; }}
        .c2 {{ top: 28%; left: -200px; animation: floatCloud 34s infinite linear; animation-delay: 5s; }}
        @keyframes floatCloud {{ 0% {{ left: -200px; }} 100% {{ left: 105%; }} }}

        .rain-drop {{ position: fixed; background: #e1f5fe; width: 3px; height: 20px; border-radius: 50%; animation: fall 1.3s infinite linear; z-index: -1; }}
        .r1 {{ left: 15%; top: -50px; }} .r2 {{ left: 50%; top: -50px; animation-delay: 0.4s; }} .r3 {{ left: 85%; top: -50px; animation-delay: 0.8s; }}
        @keyframes fall {{ 0% {{ top: -50px; }} 100% {{ top: 85vh; }} }}

        .snowflake {{ position: fixed; background: white; width: 8px; height: 8px; border-radius: 50%; animation: snowFall 4s infinite linear; z-index: -1; }}
        .s1 {{ left: 20%; top: -20px; }} .s2 {{ left: 60%; top: -20px; animation-delay: 1.5s; }} .s3 {{ left: 85%; top: -20px; animation-delay: 2.5s; }}
        @keyframes snowFall {{ 0% {{ top: -20px; transform: translateX(0); }} 50% {{ transform: translateX(15px); }} 100% {{ top: 85vh; transform: translateX(-15px); }} }}

        /* 메인 텍스트 및 정보 카드 스타일 */
        .main-title {{ text-align: center; font-size: 2.3rem; font-weight: bold; color: #1e272e; position: relative; }}
        .sub-title {{ text-align: center; color: #2f3542; margin-bottom: 25px; position: relative; }}
        
        .weather-card {{
            background: rgba(255, 255, 255, 0.85); /* 글씨가 잘 보이도록 반투명도 보강 */
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 22px;
            box-shadow: 0px 8px 24px rgba(0, 0, 0, 0.06);
            border: 1px solid rgba(255, 255, 255, 0.5);
            margin-bottom: 20px;
            position: relative;
        }}
        
        .info-grid {{ display: flex; justify-content: space-between; gap: 12px; margin-top: 15px; }}
        .info-box {{
            flex: 1; background: rgba(255, 255, 255, 0.6); border-radius: 14px; padding: 12px;
            text-align: center; box-shadow: 0 4px 10px rgba(0,0,0,0.02);
        }}
        .info-icon {{ font-size: 1.8rem; margin-bottom: 4px; }}
        .info-title {{ font-size: 0.8rem; color: #57606f; margin-bottom: 3px; }}
        .info-value {{ font-size: 1rem; font-weight: bold; color: #2f3542; }}
        
        .bar-container {{ background: #dee2e6; border-radius: 10px; height: 6px; margin-top: 8px; overflow: hidden; }}
        .bar-fill {{ background: {dust_color}; height: 100%; border-radius: 100px; }}

        .highlight {{ color: #ff4757; font-weight: bold; }}
        [data-testid="stHeader"] {{ background: transparent !important; }}
    </style>
""", unsafe_allow_html=True)

# 실시간 기후 요소 오브젝트(태양, 구름, 비, 눈) 배경층에 주입
st.markdown(theme["objects"], unsafe_allow_html=True)

# 5. 상단 타이틀 구성
st.markdown("<h1 class='main-title'>📍 방배동 실시간 종합 날씨</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>대기질 환경 지표 및 스마트 코디 가이드</p>", unsafe_allow_html=True)

# 중앙 날씨 캐릭터 Lottie 애니메이션 출력
lottie_motion = load_lottieurl(theme["lottie"])
if lottie_motion:
    st_lottie(lottie_motion, height=160, key="center_lottie")

# 6. 현재 기온 메인 카드 출력
st.markdown(f"""
    <div class='weather-card' style='text-align: center;'>
        <h2 style='margin: 0; color: #2f3542;'>🌡️ 현재 기온: {temp}°C ({weather_desc})</h2>
    </div>
""", unsafe_allow_html=True)

# 7. 대기질 및 일출·일몰 인포그래픽 카드 출력
st.markdown(f"""
    <div class='weather-card'>
        <h3 style='margin-top:0; color:#2f3542; font-size:1.2rem; text-align:center;'>📊 실시간 기상 인덱스</h3>
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

# 8. 기온별 맞춤형 코디 제안 카드 출력
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
    <div class='weather-card' style='font-size: 1.1rem; line-height: 1.8; color: #2f3542;'>
        {card_content}
    </div>
""", unsafe_allow_html=True)
