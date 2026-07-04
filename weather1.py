import streamlit as st
import requests
from bs4 import BeautifulSoup
from streamlit_lottie import st_lottie

# 1. 페이지 기본 설정
st.set_page_config(page_title="방배동 날씨 & 코디 🌤️", page_icon="✨", layout="centered")

# 2. 크롤링으로 네이버에서 방배동 날씨 가져오기 함수
def get_bangbae_weather_crawling():
    url = "https://search.naver.com/search.naver?query=방배동+날씨"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        
        # 네이버 날씨 구조 분석 후 태그 추출
        temperature_tag = soup.select_one(".temperature_text strong")
        weather_status_tag = soup.select_one(".weather_before_text + .weather_main") or soup.select_one(".before_weather") or soup.select_one(".txt_transition")
        
        if temperature_tag:
            temp_text = temperature_tag.text.replace("현재 온도", "").replace("°", "").strip()
            temp = round(float(temp_text))
            
            weather_desc = weather_status_tag.text.strip() if weather_status_tag else "맑음"
            
            # 애니메이션 및 배경 전환용 영어 매핑
            weather_main = "Clear"
            if "흐림" in weather_desc or "구름" in weather_desc:
                weather_main = "Clouds"
            elif "비" in weather_desc or "소나기" in weather_desc:
                weather_main = "Rain"
            elif "눈" in weather_desc:
                weather_main = "Snow"
                
            return temp, weather_main, weather_desc
        else:
            return None, None, "날씨 데이터를 찾을 수 없습니다."
    except Exception as e:
        return None, None, f"에러 발생: {str(e)}"

# Lottie 애니메이션 로드 함수
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200: return None
    return r.json()

# 실시간 날씨 데이터 가동
temp, weather_main, weather_desc = get_bangbae_weather_crawling()

# 3. 날씨별 배경 그라데이션 및 3D Lottie 애니메이션 매핑 설정
weather_styles = {
    "Clear": {
        "bg": "linear-gradient(135deg, #FFDEE9 0%, #B5FFFC 100%)", # 화사한 3D 햇살 톤
        "lottie": "https://assets3.lottiefiles.com/packages/lf20_xl8aHg.json",
        "card_bg": "rgba(255, 255, 255, 0.75)"
    },
    "Clouds": {
        "bg": "linear-gradient(135deg, #bdc3c7 0%, #2c3e50 100%)", # 구름 낀 차분한 톤
        "lottie": "https://assets9.lottiefiles.com/packages/lf20_w98qf0as.json",
        "card_bg": "rgba(255, 255, 255, 0.65)"
    },
    "Rain": {
        "bg": "linear-gradient(135deg, #61a5c2 0%, #2a6f97 100%)", # 촉촉한 빗방울 블루 톤
        "lottie": "https://assets4.lottiefiles.com/packages/lf20_iam97t69.json",
        "card_bg": "rgba(255, 255, 255, 0.7)"
    },
    "Snow": {
        "bg": "linear-gradient(135deg, #E0EAFC 0%, #CFDEF3 100%)", # 포근한 눈송이 화이트 톤
        "lottie": "https://assets1.lottiefiles.com/packages/lf20_96bva6g1.json",
        "card_bg": "rgba(255, 255, 255, 0.8)"
    },
    "Default": {
        "bg": "linear-gradient(135deg, #f5f7fa 0%, #e4e8f0 100%)",
        "lottie": "https://assets5.lottiefiles.com/packages/lf20_xl8aHg.json",
        "card_bg": "rgba(255, 255, 255, 0.75)"
    }
}

current_style = weather_styles.get(weather_main, weather_styles["Default"])

# 4. 동적 CSS 주입 (클레이모피즘 및 글래스모피즘 3D 스타일)
st.markdown(f"""
    <link href="https://fonts.googleapis.com/css2?family=Gowun+Dodum&display=swap" rel="stylesheet">
    <style>
        html, body, [data-testid="stAppViewContainer"] {{
            font-family: 'Gowun Dodum', sans-serif;
            background: {current_style["bg"]} !important;
            transition: background 0.8s ease-in-out;
        }}
        .main-title {{ text-align: center; font-size: 2.6rem; font-weight: bold; color: #1e272e; margin-bottom: 5px; }}
        .sub-title {{ text-align: center; color: #485460; margin-bottom: 25px; }}
        
        /* 동글동글하고 쫀득한 3D 투명 카드 디자인 */
        .clay-card {{
            background: {current_style["card_bg"]};
            backdrop-filter: blur(10px);
            border-radius: 30px;
            padding: 30px;
            box-shadow: inset 0px 4px 10px rgba(255, 255, 255, 0.8), 0px 20px 40px rgba(0, 0, 0, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.4);
            margin-bottom: 25px;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }}
        .clay-card:hover {{
            transform: scale(1.02) translateY(-5px);
            box-shadow: inset 0px 4px 10px rgba(255, 255, 255, 0.9), 0px 25px 50px rgba(0, 0, 0, 0.12);
        }}
        .recommend-text {{ font-size: 1.25rem; line-height: 1.8; color: #2c3e50; }}
        .highlight {{ color: #ff3f34; font-weight: bold; }}
    </style>
""", unsafe_allow_html=True)

# 5. 메인 화면 및 3D 애니메이션 이펙트 출력
st.markdown("<h1 class='main-title'>📍 방배동 실시간 날씨 & 코디</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>네이버 날씨를 기반으로 배경과 애니메이션이 변하는 추천 시스템</p>", unsafe_allow_html=True)

lottie_motion = load_lottieurl(current_style["lottie"])
if lottie_motion:
    st_lottie(lottie_motion, height=220, key="dynamic_weather_motion")

# 6. 실시간 날씨 디스플레이 및 코디 가이드
if temp is not None:
    st.markdown(f"""
        <div class='clay-card' style='text-align: center; background: rgba(255,255,255,0.4);'>
            <h2 style='margin: 0; color: #1e272e;'>🌡️ 현재 방배동: {temp}°C ({weather_desc})</h2>
        </div>
    """, unsafe_allow_html=True)

    card_content = ""
    if temp >= 28:
        card_content = "☀️ <b>한여름 폭염 날씨예요!</b><br>👉 추천 코디: <span class='highlight'>민소매, 반팔티, 반바지, 린넨 원피스</span>"
    elif 23 <= temp < 28:
        card_content = "🌤️ <b>가벼운 초여름 날씨예요!</b><br>👉 추천 코디: <span class='highlight'>반팔 셔츠, 얇은 면바지, 반바지</span>"
    elif 20 <= temp < 23:
        card_content = "🍃 <b>선선해서 걷기 좋은 봄/가을 날씨예요!</b><br>👉 추천 코디: <span class='highlight'>가벼운 셔츠, 얇은 긴팔티, 슬랙스, 청바지</span>"
    elif 17 <= temp < 20:
        card_content = "🧥 <b>일교차가 커요! 얇은 외투를 꼭 챙기세요.</b><br>👉 추천 코디: <span class='highlight'>맨투맨, 후드티, 가디건, 바람막이, 청바지</span>"
    elif 12 <= temp < 17:
        card_content = "🍂 <b>쌀쌀한 본격적인 환절기 날씨예요.</b><br>👉 추천 코디: <span class='highlight'>자켓, 트렌치코트, 도톰한 가디건, 면바지</span>"
    elif 9 <= temp < 12:
        card_content = "💨 <b>찬 바람이 불어 옷을 여러 겹 레이어드하기 좋은 날씨예요.</b><br>👉 추천 코디: <span class='highlight'>야상 점퍼, 도톰한 니트, 기모바지</span>"
    elif 5 <= temp < 9:
        card_content = "🥶 <b>입김이 서서히 나오는 초겨울 날씨예요!</b><br>👉 추천 코디: <span class='highlight'>울 코트, 가죽 자켓, 가벼운 다운 패딩, 히트텍</span>"
    else:
        card_content = "❄️ <b>손발이 꽁꽁 얼어붙는 생존 위주의 겨울 한파 날씨예요!</b><br>👉 추천 코디: <span class='highlight'>롱패딩, 두꺼운 패딩, 목도리, 장갑 필수</span>"

    st.markdown(f"""
        <div class='clay-card recommend-text'>
            {card_content}
        </div>
    """, unsafe_allow_html=True)
    
    # 눈/비 추가 다이내믹 안전 가이드 안내
    if "비" in weather_desc:
        st.markdown("<div class='clay-card' style='background: #e1f5fe; color: #0288d1;'>☔ 비 소식이 있으니 외출 시 <b>우산</b>을 꼭 챙기세요!</div>", unsafe_allow_html=True)
    elif "눈" in weather_desc:
        st.markdown("<div class='clay-card' style='background: #f3e5f5; color: #7b1fa2;'>☃️ 눈이 내리고 있으니 <b>빙판길 미끄럼 조심</b>하세요!</div>", unsafe_allow_html=True)
else:
    st.error(f"날씨 정보를 불러오지 못했습니다. 원인: {weather_desc}")
