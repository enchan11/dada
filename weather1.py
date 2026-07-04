import streamlit as st
import requests
from streamlit_lottie import st_lottie

# 1. 페이지 기본 설정
st.set_page_config(page_title="방배동 날씨 동화 세계 🌤️", page_icon="✨", layout="centered")

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

# 3. 날씨 테마별 스타일 및 애니메이션 설정
weather_themes = {
    "Clear": {
        "sky": "linear-gradient(to bottom, #74b9ff, #a29bfe)", "ground": "#55efc4",
        "objects": '<div class="sun"></div><div class="cloud-ani c1"></div><div class="cloud-ani c2"></div>',
        "lottie": "https://assets3.lottiefiles.com/packages/lf20_xl8aHg.json"
    },
    "Clouds": {
        "sky": "linear-gradient(to bottom, #747d8c, #a4b0be)", "ground": "#2ed573",
        "objects": '<div class="cloud-ani c1" style="opacity: 0.9;"></div><div class="cloud-ani c2" style="transform: scale(1.4); top: 20%; animation-duration: 25s;"></div>',
        "lottie": "https://assets9.lottiefiles.com/packages/lf20_w98qf0as.json"
    },
    "Rain": {
        "sky": "linear-gradient(to bottom, #2f3640, #718093)", "ground": "#05c46b",
        "objects": '<div class="cloud-ani c1" style="background: #718093;"></div><div class="rain-drop r1"></div><div class="rain-drop r2"></div><div class="rain-drop r3"></div>',
        "lottie": "https://assets4.lottiefiles.com/packages/lf20_iam97t69.json"
    },
    "Snow": {
        "sky": "linear-gradient(to bottom, #dfe4ea, #f1f2f6)", "ground": "#ffffff",
        "objects": '<div class="snowflake s1"></div><div class="snowflake s2"></div><div class="snowflake s3"></div>',
        "lottie": "https://assets1.lottiefiles.com/packages/lf20_96bva6g1.json"
    },
    "Default": {
        "sky": "linear-gradient(to bottom, #74b9ff, #a29bfe)", "ground": "#55efc4",
        "objects": '<div class="sun"></div>', "lottie": "https://assets5.lottiefiles.com/packages/lf20_xl8aHg.json"
    }
}

theme = weather_themes.get(weather_main, weather_themes["Default"])
dust_color = "#2ed573" if "좋음" in dust or "보통" in dust else "#ff4757"

# 4. 강제 레이어 최상단 노출 및 고해상도 CSS 스타일 주입
st.markdown(f"""
    <link href="https://fonts.googleapis.com/css2?family=Gowun+Dodum&display=swap" rel="stylesheet">
    <style>
        /* 기본 배경 하늘 설정 */
        html, body, [data-testid="stAppViewContainer"] {{
            font-family: 'Gowun Dodum', sans-serif;
            background: {theme["sky"]} !important;
            overflow-x: hidden; position: relative;
        }}
        
        /* 메인 콘텐츠 영역을 배경(언덕)보다 무조건 위로 배치 (z-index 강제 부여) */
        [data-testid="stVerticalBlock"] {{
            position: relative;
            z-index: 9999 !important;
        }}
        
        /* 하단 3D 언덕 배경 지형 (우선순위를 -1로 낮춰 절대 글자를 못 가리게 설정) */
        [data-testid="stAppViewContainer"]::after {{
            content: ""; position: fixed; bottom: -150px; left: -10%; width: 120%; height: 320px;
            background: {theme["ground"]}; border-radius: 50% 50% 0 0; z-index: -1 !important;
            box-shadow: inset 0 20px 30px rgba(0,0,0,0.05); transition: all 0.8s ease;
        }}

        /* 태양 맥박 애니메이션 (z-index 최소화) */
        .sun {{
            position: fixed; top: 8%; right: 12%; width: 90px; height: 90px;
            background: radial-gradient(circle, #fffa65, #ffaf40); border-radius: 50%; z-index: -1;
            box-shadow: 0 0 40px #ffaf40; animation: pulse 4s infinite alternate;
        }}
        @keyframes pulse {{ 0% {{ transform: scale(1); }} 100% {{ transform: scale(1.08); }} }}

        /* 구름 흐르기 애니메이션 */
        .cloud-ani {{ position: fixed; background: rgba(255,255,255,0.85); border-radius: 100px; width: 160px; height: 50px; z-index: -1; }}
        .cloud-ani::before, .cloud-ani::after {{ content: ""; position: absolute; background: rgba(255,255,255,0.85); border-radius: 50%; }}
        .cloud-ani::before {{ width: 70px; height: 70px; top: -35px; left: 25px; }}
        .cloud-ani::after {{ width: 90px; height: 90px; top: -45px; right: 15px; }}
        .c1 {{ top: 12%; left: -200px; animation: floatCloud 22s infinite linear; }}
        .c2 {{ top: 26%; left: -200px; animation: floatCloud 32s infinite linear; animation-delay: 4s; }}
        @keyframes floatCloud {{ 0% {{ left: -200px; }} 100% {{ left: 105%; }} }}

        /* 비/눈 내리는 효과 */
        .rain-drop {{ position: fixed; background: #e1f5fe; width: 3px; height: 22px; border-radius: 50%; animation: fall 1.3s infinite linear; z-index: -1; }}
        .r1 {{ left: 15%; top: -50px; }} .r2 {{ left: 45%; top: -50px; animation-delay: 0.4s; }} .r3 {{ left: 75%; top: -50px; animation-delay: 0.8s; }}
        @keyframes fall {{ 0% {{ top: -50px; }} 100% {{ top: 85vh; }} }}

        .snowflake {{ position: fixed; background: white; width: 10px; height: 10px; border-radius: 50%; animation: snowFall 3.8s infinite linear; z-index: -1; }}
        .s1 {{ left: 20%; top: -20px; }} .s2 {{ left: 55%; top: -20px; animation-delay: 1.2s; }} .s3 {{ left: 80%; top: -20px; animation-delay: 2.2s; }}
        @keyframes snowFall {{ 0% {{ top: -20px; transform: translateX(0); }} 50% {{ transform: translateX(15px); }} 100% {{ top: 85vh; transform: translateX(-15px); }} }}

        /* 반투명 글래스모피즘 카드 레이아웃 (글자 선명도 극대화) */
        .main-title {{ text-align: center; font-size: 2.5rem; font-weight: bold; color: #1e272e !important; }}
        .sub-title {{ text-align: center; color: #2f3542 !important; margin-bottom: 20px; }}
        
        .clay-card {{
            background: rgba(255, 255, 255, 0.85) !important; /* 투명도를 낮춰 가독성 업 */
            backdrop-filter: blur(15px);
            border-radius: 28px; padding: 25px; border: 1px solid rgba(255, 255, 255, 0.5);
            box-shadow: inset 0px 4px 10px rgba(255, 255, 255, 0.6), 0px 20px 40px rgba(0, 0, 0, 0.08);
            margin-bottom: 20px;
        }}
        
        /* 인포그래픽 정렬 */
        .info-grid {{ display: flex; justify-content: space-between; gap: 15px; margin-top: 15px; }}
        .info-box {{
            flex: 1; background: rgba(255, 255, 255, 0.6); border-radius: 20px; padding: 15px;
            text-align: center; box-shadow: 0 8px 16px rgba(0,0,0,0.03);
        }}
        .info-icon {{ font-size: 2.2rem; margin-bottom: 8px; }}
        .info-title {{ font-size: 0.9rem; color: #57606f; margin-bottom: 4px; }}
        .info-value {{ font-size: 1.1rem; font-weight: bold; color: #2f3542; }}
        
        .bar-container {{ background: #dfe4ea; border-radius: 10px; height: 8px; margin-top: 8px; overflow: hidden; }}
        .bar-fill {{ background: {dust_color}; height: 100%; width: 70%; border-radius: 100px; }}

        .highlight {{ color: #ff4757; font-weight: bold; }}
        [data-testid="stHeader"] {{ background: transparent !important; }}
    </style>
""", unsafe_allow_html=True)

# 실시간 기후 요소 오브젝트 주입 (글자 뒤쪽 레이어 배치)
st.markdown(theme["objects"], unsafe_allow_html=True)

# 5. 메인 정보 컴포넌트 출력
st.markdown("<h1 class='main-title'>📍 방배동 종합 자연 동화</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>실시간 대기질 및 일출·일몰 인포그래픽 대시보드</p>", unsafe_allow_html=True)

# Lottie 모션 출력
lottie_motion = load_lottieurl(theme["lottie"])
if lottie_motion:
    st_lottie(lottie_motion, height=180, key="center_lottie")

# 6. 대시보드 및 코디 정보창 출력
st.markdown(f"""
    <div class='clay-card' style='text-align: center;'>
        <h2 style='margin: 0; color: #2f3542;'>🌡️ 현재 방배동: {temp}°C ({weather_desc})</h2>
    </div>
""", unsafe_allow_html=True)

st.markdown(f"""
    <div class='clay-card'>
        <h3 style='margin-top:0; color:#2f3542; font-size:1.3rem; text-align:center;'>📊 실시간 방배동 대기 환경 지표</h3>
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

# 기온별 스마트 코디 가이드 패널
card_content = ""
if temp >= 28:
    card_content = "☀️ <b>한여름 폭염 날씨예요!</b><br>👉 코디 가이드: <span class='highlight'>민소매, 반팔티, 린넨 쇼츠, 선글라스</span>"
elif 23 <= temp < 28:
    card_content = "🌤️ <b>산뜻하고 가벼운 여름 기온이에요.</b><br>👉 코디 가이드: <span class='highlight'>반팔 셔츠, 슬림 면바지, 오픈형 샌들</span>"
elif 20 <= temp < 23:
    card_content = "🍃 <b>선선하고 부드러운 봄/가을 온도대입니다.</b><br>👉 코디 가이드: <span class='highlight'>옥스퍼드 셔츠, 니트조끼, 데님 팬츠</span>"
elif 17 <= temp < 20:
    card_content = "🧥 <b>일교차가 가파릅니다. 아우터 필수 구비!</b><br>👉 코디 가이드: <span class='highlight'>맨투맨, 후디, 가디건 레이어링</span>"
elif 12 <= temp < 17:
    card_content = "🍂 <b>찬 기운이 옷깃을 가르는 쌀쌀한 환절기입니다.</b><br>👉 코디 가이드: <span class='highlight'>울 재킷, 트렌치 코트, 도톰한 니트</span>"
elif 9 <= temp < 12:
    card_content = "💨 <b>외풍이 강하니 레이어드룩이 제격입니다.</b><br>👉 코디 가이드: <span class='highlight'>야상 점퍼, 도톰한 헤비 니트, 기모바지</span>"
elif 5 <= temp < 9:
    card_content = "🥶 <b>서리가 내리는 초겨울 추위 시즌이에요!</b><br>👉 코디 가이드: <span class='highlight'>롱코트, 무스탕 재킷, 다운 패딩, 발열내의</span>"
else:
    card_content = "❄️ <b>동파 사고를 조심해야 하는 겨울 한파 침공 기온입니다!</b><br>👉 코디 가이드: <span class='highlight'>롱패딩, 방한 목도리, 장갑 필수</span>"

st.markdown(f"""
    <div class='clay-card' style='font-size: 1.2rem; line-height: 1.8; color: #2f3542;'>
        {card_content}
    </div>
""", unsafe_allow_html=True)
