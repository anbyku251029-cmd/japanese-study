# -*- coding: utf-8 -*-

import streamlit as st
import random
import urllib.parse
# from database import get_phrases_by_category, get_all_categories, get_all_phrases_flat

# 1. 페이지 기본 설정 및 스타일 초기화
st.set_page_config(
    page_title="니혼고 마스터 - 상황별 기초 회화 150선",
    page_icon="🇯🇵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. 커스텀 CSS 주입 (다크 네온 & 글래스모피즘 디자인)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Noto+Sans+KR:wght@300;400;700&display=swap');

/* 메인 배경 및 레이아웃 */
.stApp {
    background-color: #0b0c10;
    color: #c5c6c7;
    font-family: 'Outfit', 'Noto Sans KR', sans-serif;
}

/* 사이드바 스타일 */
section[data-testid="stSidebar"] {
    background-color: #1f2833;
    border-right: 1px solid rgba(102, 252, 241, 0.1);
}

/* 리스트형 글래스모피즘 카드 */
.phrase-card {
    background: rgba(255, 255, 255, 0.02);
    border-radius: 12px;
    box-shadow: 0 4px 15px 0 rgba(0, 0, 0, 0.2);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    border: 1px solid rgba(255, 255, 255, 0.05);
    padding: 20px;
    margin-bottom: 15px;
    transition: border-color 0.2s ease;
}
.phrase-card:hover {
    border-color: rgba(102, 252, 241, 0.2);
    background: rgba(255, 255, 255, 0.03);
}

/* 네온 이펙트 텍스트 */
.neon-title {
    font-size: 2.5rem;
    font-weight: 800;
    background: linear-gradient(45deg, #66fcf1, #45f3ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 0 0 20px rgba(102, 252, 241, 0.2);
    margin-bottom: 25px;
}
.neon-subtitle {
    color: #66fcf1;
    font-size: 1.4rem;
    font-weight: 600;
    margin-bottom: 15px;
}

/* 문장 출력 컴포넌트 세부 스타일 */
.phrase-kr {
    font-size: 1.4rem;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 6px;
    line-height: 1.4;
}
.phrase-kanji {
    font-size: 1.25rem;
    font-weight: 400;
    color: #66fcf1;
    margin-bottom: 6px;
    letter-spacing: 0.5px;
}
.phrase-roma {
    font-size: 1.15rem;
    font-weight: 600;
    color: #bb86fc;
}

/* 복습 체크용 별표 버튼 스타일 */
div.stButton > button[key^="fav_"] {
    background: transparent !important;
    border: none !important;
    color: #ffcc00 !important;
    font-size: 1.5rem !important;
    padding: 0 !important;
    margin-top: 5px;
}

/* 초경량 TTS 재생 버튼 스타일 */
.tts-play-btn {
    background: transparent;
    border: 1px solid #66fcf1;
    color: #66fcf1;
    border-radius: 6px;
    padding: 6px 14px;
    font-size: 0.95rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
    display: inline-flex;
    align-items: center;
    gap: 5px;
}
.tts-play-btn:hover {
    background: #66fcf1;
    color: #0b0c10;
    box-shadow: 0 0 10px rgba(102, 252, 241, 0.3);
}

/* 메인으로 이동 버튼 전용 스타일 */
div.stButton > button[key="go_main"] {
    width: 100% !important;
    background: linear-gradient(45deg, #1f2833, #0b0c10) !important;
    border: 1px solid #66fcf1 !important;
    color: #66fcf1 !important;
    font-weight: 700 !important;
    border-radius: 8px !important;
    padding: 10px 15px !important;
    transition: all 0.3s ease !important;
}
div.stButton > button[key="go_main"]:hover {
    background: #66fcf1 !important;
    color: #0b0c10 !important;
    box-shadow: 0 0 15px rgba(102, 252, 241, 0.4) !important;
}
</style>
""", unsafe_allow_html=True)

# 3. 세션 상태 (Session State) 초기화
if "review_list" not in st.session_state:
    st.session_state.review_list = []
if "category_index" not in st.session_state:
    st.session_state.category_index = 0
if "show_reviews_val" not in st.session_state:
    st.session_state.show_reviews_val = False

categories = get_all_categories()

# 4. 사이드바 제어 영역
with st.sidebar:
    st.markdown("<h2 class='neon-subtitle'>Study Options</h2>", unsafe_allow_html=True)
    
    # 5대 상황 카테고리 표시 (세션에 보존된 category_index 반영)
    selected_category = st.radio(
        "상황별 문장",
        categories,
        index=st.session_state.category_index,
        key="category_radio"
    )
    # 라디오 선택 변경 시 세션 상태 동기화
    for i, cat in enumerate(categories):
        if cat == selected_category:
            st.session_state.category_index = i
            
    st.markdown("---")
    
    # 별도 '내가 체크한 복습 문장' 단독 선택 기능 탑재 (세션 상태 동기화)
    show_reviews = st.checkbox(
        "🔄 내가 체크한 복습 문장", 
        value=st.session_state.show_reviews_val,
        key="reviews_checkbox"
    )
    st.session_state.show_reviews_val = show_reviews

# 5. 카테고리 셔플 및 캐싱 로직
current_key = "reviews" if show_reviews else selected_category

if "last_category" not in st.session_state or st.session_state.last_category != current_key:
    st.session_state.last_category = current_key
    if current_key == "reviews":
        # 사용자가 복습 체크한 문장들만 데이터베이스에서 필터링하여 일괄 로딩
        phrases = [p for p in get_all_phrases_flat() if p["id"] in st.session_state.review_list]
    else:
        # 카테고리가 전환된 시점에만 1회 셔플하여 세션 상태에 고정 저장
        phrases = get_phrases_by_category(selected_category).copy()
        random.shuffle(phrases)
    st.session_state.shuffled_phrases = phrases

# 만약 복습 뷰 활성화 도중 데이터가 추가/삭제되어 동기화가 필요한 경우 처리
if current_key == "reviews":
    st.session_state.shuffled_phrases = [p for p in get_all_phrases_flat() if p["id"] in st.session_state.review_list]

# 6. 메인 화면 헤더 출력
st.markdown(f"<h1 class='neon-title'>일본어 상황별 문장 학습</h1>", unsafe_allow_html=True)
display_title = "🔄 내가 체크한 복습 문장" if show_reviews else selected_category
st.markdown(f"<h3>📍 {display_title}</h3>", unsafe_allow_html=True)

st.markdown("---")

# 7. 문장 일괄 렌더링
phrases_to_show = st.session_state.shuffled_phrases

if not phrases_to_show:
    if show_reviews:
        st.info("복습 체크한 문장이 없습니다. 리스트 문장 옆의 별표(★)를 눌러 복습에 추가해 보세요.")
    else:
        st.info("해당 카테고리에 문장이 존재하지 않습니다.")
else:
    for idx, phrase in enumerate(phrases_to_show, start=1):
        phrase_id = phrase["id"]
        is_fav = phrase_id in st.session_state.review_list
        
        # 글래스모피즘 리스트 카드 및 레이아웃 구성
        st.markdown(f"""
        <div class="phrase-card">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div style="flex: 1;">
                    <div class="phrase-kr">{idx}. {phrase['kr']}</div>
                    <div class="phrase-kanji">{phrase['kanji']}</div>
                    <div class="phrase-roma">{phrase['roma']}</div>
                </div>
                <div style="text-align: right; display: flex; flex-direction: column; align-items: flex-end; gap: 10px;">
                    <!-- Google Translate TTS API를 활용한 HTML5 오디오 재생 코드 오버레이 -->
                    <audio id="audio-{phrase_id}" src="https://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&tl=ja&q={urllib.parse.quote(phrase['kanji'])}"></audio>
                    <button class="tts-play-btn" onclick="document.getElementById('audio-{phrase_id}').play()">
                        🔊 소리 듣기
                    </button>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Streamlit 별표 복습 버튼 배치 (HTML 카드 레이아웃 하단에 자연스럽게 녹아들게 함)
        # st.button으로 체크 상태 토글 처리
        btn_label = "★ 복습 해제" if is_fav else "☆ 복습 추가"
        if st.button(btn_label, key=f"fav_{phrase_id}", help="복습 목록에 문장을 추가하거나 해제합니다."):
            if is_fav:
                st.session_state.review_list.remove(phrase_id)
            else:
                st.session_state.review_list.append(phrase_id)
            st.rerun()
