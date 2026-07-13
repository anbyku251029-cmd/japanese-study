# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
import datetime
import json
import os
import google.generativeai as genai
from database import get_vocab_by_level, VOCABULARY_DECK

# 1. 페이지 기본 설정 및 스타일 초기화
st.set_page_config(
    page_title="니혼고 마스터 - Premium Japanese Study",
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

/* 글래스모피즘 학습 카드 */
.glass-card {
    background: rgba(255, 255, 255, 0.02);
    border-radius: 20px;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.05);
    padding: 35px;
    margin-bottom: 25px;
    transition: transform 0.3s ease, border-color 0.3s ease;
}
.glass-card:hover {
    transform: translateY(-4px);
    border-color: rgba(102, 252, 241, 0.3);
}

/* 텍스트 네온 이펙트 */
.neon-title {
    font-size: 3rem;
    font-weight: 800;
    background: linear-gradient(45deg, #66fcf1, #45f3ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 0 0 20px rgba(102, 252, 241, 0.2);
    margin-bottom: 20px;
}
.neon-subtitle {
    color: #66fcf1;
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: 15px;
}
.accent-purple {
    color: #bb86fc;
}

/* 플래시카드 단어 표기 스타일 */
.flashcard-word {
    font-size: 4rem;
    font-weight: 800;
    text-align: center;
    color: #ffffff;
    margin-bottom: 10px;
    letter-spacing: 2px;
}
.flashcard-reading {
    font-size: 2rem;
    text-align: center;
    color: #66fcf1;
    margin-bottom: 5px;
}
.flashcard-pronunciation {
    font-size: 1.6rem;
    text-align: center;
    color: #bb86fc;
    margin-bottom: 20px;
    font-style: italic;
}
.flashcard-meaning {
    font-size: 2.2rem;
    text-align: center;
    color: #e5e5e5;
    font-weight: 600;
    border-top: 1px solid rgba(255,255,255,0.1);
    padding-top: 15px;
    margin-top: 15px;
}

/* 대시보드 미레기 카드 */
.metric-box {
    background: rgba(102, 252, 241, 0.03);
    border-radius: 12px;
    border: 1px solid rgba(102, 252, 241, 0.1);
    padding: 20px;
    text-align: center;
}
.metric-val {
    font-size: 2.5rem;
    font-weight: 700;
    color: #66fcf1;
}
.metric-lbl {
    font-size: 1rem;
    color: #8f94fb;
}

/* 버튼 커스터마이징 */
div.stButton > button {
    background: linear-gradient(135deg, #1f2833, #0b0c10);
    color: #66fcf1 !important;
    border: 1px solid #66fcf1;
    padding: 12px 28px;
    border-radius: 10px;
    font-weight: 600;
    transition: all 0.3s ease;
}
div.stButton > button:hover {
    background: #66fcf1;
    color: #0b0c10 !important;
    box-shadow: 0 0 15px rgba(102, 252, 241, 0.4);
    transform: translateY(-2px);
}

/* 복습 성공/실패 버튼 커스텀 */
.btn-success button {
    border-color: #2ecc71 !important;
    color: #2ecc71 !important;
}
.btn-success button:hover {
    background: #2ecc71 !important;
    color: #ffffff !important;
}
.btn-fail button {
    border-color: #e74c3c !important;
    color: #e74c3c !important;
}
.btn-fail button:hover {
    background: #e74c3c !important;
    color: #ffffff !important;
}
</style>
""", unsafe_allow_html=True)

# 3. 세션 상태 (Session State) 초기화
if "srs" not in st.session_state:
    # 각 단어 ID를 키로 하여 SRS 정보 저장
    # level: 1~5 (암기 수준), next_review: 다음 복습 시점 (ISO 포맷), reps: 반복성공 횟수
    st.session_state.srs = {}
    for word in VOCABULARY_DECK:
        st.session_state.srs[str(word["id"])] = {
            "level": 0,           # 아직 미학습
            "next_review": None,
            "reps": 0
        }

if "daily_count" not in st.session_state:
    st.session_state.daily_count = 0

if "current_card_idx" not in st.session_state:
    st.session_state.current_card_idx = 0

if "show_answer" not in st.session_state:
    st.session_state.show_answer = False

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 4. 사이드바 제어 영역
with st.sidebar:
    st.markdown("<h2 class='neon-subtitle'>Study Options</h2>", unsafe_allow_html=True)
    
    # 메뉴 네비게이션
    menu = st.radio(
        "이동할 화면을 선택하세요",
        ["대시보드", "단어 카드 학습", "간격 반복 복습 (SRS)", "AI 회화 파트너"]
    )
    
    st.markdown("---")
    st.markdown("<h3 class='accent-purple'>한글 독음 설정</h3>", unsafe_allow_html=True)
    show_pronunciation = st.checkbox("한글 독음 상시 표시", value=True)
    
    st.markdown("---")
    st.markdown("<h3 class='accent-purple'>Gemini AI 설정</h3>", unsafe_allow_html=True)
    api_key_input = st.text_input("Gemini API Key", type="password", help="AI 회화 기능을 사용하려면 API 키를 입력하세요.")
    
    # 환경변수 혹은 입력값 중 유효한 키 선택
    api_key = api_key_input if api_key_input else os.getenv("GEMINI_API_KEY")
    if api_key:
        genai.configure(api_key=api_key)
        st.success("API Key가 연동되었습니다.")
    else:
        st.warning("API Key가 설정되지 않았습니다.")

# 5. 화면별 구현

# [화면 1: 대시보드]
if menu == "대시보드":
    st.markdown("<h1 class='neon-title'>학습 대시보드</h1>", unsafe_allow_html=True)
    
    # 통계 연산
    total_words = len(VOCABULARY_DECK)
    srs_values = st.session_state.srs.values()
    learned_words = sum(1 for item in srs_values if item["level"] > 0)
    mastered_words = sum(1 for item in srs_values if item["level"] >= 4)
    review_needed = 0
    now = datetime.datetime.now()
    for item in srs_values:
        if item["next_review"]:
            next_time = datetime.datetime.fromisoformat(item["next_review"])
            if next_time <= now:
                review_needed += 1

    # 상단 대시보드 메트릭
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-val">{total_words}</div>
            <div class="metric-lbl">전체 학습 단어 수</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-val">{learned_words}</div>
            <div class="metric-lbl">현재 학습 중인 단어</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-val">{mastered_words}</div>
            <div class="metric-lbl">완벽히 암기한 단어</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-val" style="color: #e74c3c;">{review_needed}</div>
            <div class="metric-lbl" style="color: #e74c3c;">복습 대기 단어</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # 학습 안내 카드
    st.markdown(f"""
    <div class="glass-card">
        <h3>환영합니다!</h3>
        <p>본 프로그램은 <b>JLPT N5부터 N1 등급</b>의 핵심 단어들을 효과적으로 암기할 수 있는 <b>간격 반복 학습(SRS)</b> 알고리즘을 제공합니다.</p>
        <p>단어 카드를 확인하고 암기 수준을 체크하면 다음 복습 일정이 자동으로 계산됩니다.</p>
    </div>
    """, unsafe_allow_html=True)

    # 데이터 백업 / 복구 기능 (세션 휘발 방지용 UX)
    st.markdown("### 데이터 백업 및 복구")
    col_backup, col_restore = st.columns(2)
    with col_backup:
        st.markdown("현재까지의 학습 통계 및 SRS 진행 내역을 JSON 파일로 백업합니다.")
        backup_data = {
            "srs": st.session_state.srs,
            "daily_count": st.session_state.daily_count
        }
        json_str = json.dumps(backup_data, indent=4)
        st.download_button(
            label="학습 데이터 백업 다운로드",
            data=json_str,
            file_name="japanese_study_backup.json",
            mime="application/json"
        )
    with col_restore:
        st.markdown("백업해 둔 JSON 파일을 업로드하여 학습 기록을 복구합니다.")
        uploaded_file = st.file_uploader("백업 파일 선택", type="json")
        if uploaded_file is not None:
            try:
                restore_data = json.load(uploaded_file)
                if "srs" in restore_data:
                    st.session_state.srs = restore_data["srs"]
                    st.session_state.daily_count = restore_data.get("daily_count", 0)
                    st.success("학습 데이터가 성공적으로 복구되었습니다!")
                    st.rerun()
            except Exception as e:
                st.error("올바르지 않은 파일 포맷입니다.")

# [화면 2: 단어 카드 학습]
elif menu == "단어 카드 학습":
    st.markdown("<h1 class='neon-title'>단어 카드 학습</h1>", unsafe_allow_html=True)
    
    # 필터 옵션
    level_filter = st.selectbox("학습할 JLPT 등급을 선택하세요", ["All", "N5", "N4", "N3", "N2", "N1"])
    deck = get_vocab_by_level(level_filter)
    
    if not deck:
        st.info("해당 등급의 단어가 존재하지 않습니다.")
    else:
        # 안전한 인덱스 제어
        if st.session_state.current_card_idx >= len(deck):
            st.session_state.current_card_idx = 0
            
        current_word = deck[st.session_state.current_card_idx]
        
        # 플래시카드 렌더링
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown(f"<div class='flashcard-word'>{current_word['word']}</div>", unsafe_allow_html=True)
        
        if show_pronunciation:
            st.markdown(f"<div class='flashcard-reading'>{current_word['reading']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='flashcard-pronunciation'>[{current_word['pronunciation']}]</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div style='height: 70px;'></div>", unsafe_allow_html=True)
            
        if st.session_state.show_answer:
            st.markdown(f"<div class='flashcard-meaning'>{current_word['meaning']}</div>", unsafe_allow_html=True)
            st.markdown("<br><hr>", unsafe_allow_html=True)
            st.markdown(f"**예문:** {current_word['example']}")
            st.markdown(f"**읽기:** {current_word['example_reading']}")
            st.markdown(f"**독음:** {current_word['example_pronunciation']}")
            st.markdown(f"**해석:** {current_word['example_meaning']}")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # 카드 제어 버튼
        col_show, col_next = st.columns(2)
        with col_show:
            if st.button("뜻 / 예문 보기", use_container_width=True):
                st.session_state.show_answer = not st.session_state.show_answer
                st.rerun()
                
        with col_next:
            if st.button("다음 단어", use_container_width=True):
                st.session_state.current_card_idx = (st.session_state.current_card_idx + 1) % len(deck)
                st.session_state.show_answer = False
                st.rerun()
                
        # 암기 피드백 버튼 (대답 시 SRS 스케줄링)
        st.markdown("### 암기 피드백")
        col_know, col_dont = st.columns(2)
        word_id_str = str(current_word["id"])
        
        with col_know:
            st.markdown("<div class='btn-success'>", unsafe_allow_html=True)
            if st.button("알고 있음 (복습 주기 연장)", key="know_btn", use_container_width=True):
                # SRS 알고리즘: 레벨 올리고 다음 복습 일정 설정 (레벨별로 1분, 5분, 30분, 1일, 7일 복습 대기)
                curr_srs = st.session_state.srs[word_id_str]
                next_lvl = min(curr_srs["level"] + 1, 5)
                intervals = [0, 1, 5, 30, 1440, 10080] # 분 단위 스케줄
                next_review_time = datetime.datetime.now() + datetime.timedelta(minutes=intervals[next_lvl])
                
                st.session_state.srs[word_id_str] = {
                    "level": next_lvl,
                    "next_review": next_review_time.isoformat(),
                    "reps": curr_srs["reps"] + 1
                }
                st.success("암기 상태가 업데이트되었습니다. 다음 복습 주기가 연장됩니다.")
                st.session_state.current_card_idx = (st.session_state.current_card_idx + 1) % len(deck)
                st.session_state.show_answer = False
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col_dont:
            st.markdown("<div class='btn-fail'>", unsafe_allow_html=True)
            if st.button("모르겠음 (즉시 복습)", key="dont_btn", use_container_width=True):
                # SRS 리셋
                st.session_state.srs[word_id_str] = {
                    "level": 1,
                    "next_review": (datetime.datetime.now() + datetime.timedelta(minutes=1)).isoformat(),
                    "reps": 0
                }
                st.warning("단어 카드가 복습 대기 상태로 재설정되었습니다.")
                st.session_state.current_card_idx = (st.session_state.current_card_idx + 1) % len(deck)
                st.session_state.show_answer = False
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

# [화면 3: 간격 반복 복습 (SRS)]
elif menu == "간격 반복 복습 (SRS)":
    st.markdown("<h1 class='neon-title'>간격 반복 복습</h1>", unsafe_allow_html=True)
    
    # 복습 대상 추출
    now = datetime.datetime.now()
    review_deck = []
    
    for word in VOCABULARY_DECK:
        word_id_str = str(word["id"])
        srs_info = st.session_state.srs[word_id_str]
        
        # 복습 일정이 설정되어 있고, 그 일정이 현재 시각 이전인 경우 복습 대상
        if srs_info["next_review"]:
            next_time = datetime.datetime.fromisoformat(srs_info["next_review"])
            if next_time <= now:
                review_deck.append(word)
                
    if not review_deck:
        st.success("현재 복습할 단어가 없습니다. 아주 훌륭합니다!")
    else:
        st.markdown(f"총 **{len(review_deck)}**개의 단어가 복습을 기다리고 있습니다.")
        
        # 첫 번째 복습 대상 단어 렌더링
        word_to_review = review_deck[0]
        word_id_str = str(word_to_review["id"])
        
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown(f"<div class='flashcard-word'>{word_to_review['word']}</div>", unsafe_allow_html=True)
        
        if show_pronunciation:
            st.markdown(f"<div class='flashcard-reading'>{word_to_review['reading']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='flashcard-pronunciation'>[{word_to_review['pronunciation']}]</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div style='height: 70px;'></div>", unsafe_allow_html=True)
            
        if st.session_state.show_answer:
            st.markdown(f"<div class='flashcard-meaning'>{word_to_review['meaning']}</div>", unsafe_allow_html=True)
            st.markdown("<br><hr>", unsafe_allow_html=True)
            st.markdown(f"**예문:** {word_to_review['example']}")
            st.markdown(f"**읽기:** {word_to_review['example_reading']}")
            st.markdown(f"**독음:** {word_to_review['example_pronunciation']}")
            st.markdown(f"**해석:** {word_to_review['example_meaning']}")
            
        st.markdown("</div>", unsafe_allow_html=True)
        
        col_show, col_feedback = st.columns([1, 2])
        with col_show:
            if st.button("정답 확인", key="review_show_btn", use_container_width=True):
                st.session_state.show_answer = not st.session_state.show_answer
                st.rerun()
                
        with col_feedback:
            col_know, col_dont = st.columns(2)
            with col_know:
                st.markdown("<div class='btn-success'>", unsafe_allow_html=True)
                if st.button("알고 있음", key="review_know_btn", use_container_width=True):
                    curr_srs = st.session_state.srs[word_id_str]
                    next_lvl = min(curr_srs["level"] + 1, 5)
                    intervals = [0, 1, 5, 30, 1440, 10080]
                    next_review_time = datetime.datetime.now() + datetime.timedelta(minutes=intervals[next_lvl])
                    
                    st.session_state.srs[word_id_str] = {
                        "level": next_lvl,
                        "next_review": next_review_time.isoformat(),
                        "reps": curr_srs["reps"] + 1
                    }
                    st.success("복습 성공 처리되었습니다.")
                    st.session_state.show_answer = False
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
                
            with col_dont:
                st.markdown("<div class='btn-fail'>", unsafe_allow_html=True)
                if st.button("모르겠음", key="review_dont_btn", use_container_width=True):
                    st.session_state.srs[word_id_str] = {
                        "level": 1,
                        "next_review": (datetime.datetime.now() + datetime.timedelta(minutes=1)).isoformat(),
                        "reps": 0
                    }
                    st.warning("단어가 복습 대기 상태로 유지됩니다.")
                    st.session_state.show_answer = False
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)

# [화면 4: AI 회화 파트너]
elif menu == "AI 회화 파트너":
    st.markdown("<h1 class='neon-title'>AI 일본어 회화 파트너</h1>", unsafe_allow_html=True)
    st.markdown("Gemini AI를 활용하여 실시간으로 일본어 대화를 나눌 수 있는 파트너 시스템입니다.")
    
    if not api_key:
        st.info("사이드바에 Gemini API Key를 입력하면 AI 회화 기능을 사용하실 수 있습니다.")
    else:
        # 채팅 출력 영역
        for chat in st.session_state.chat_history:
            role_css = "accent-purple" if chat["role"] == "user" else "neon-text-cyan"
            st.markdown(f"**[{chat['role'].upper()}]**")
            st.markdown(f"<div class='glass-card'>{chat['content']}</div>", unsafe_allow_html=True)
            
        # 메시지 입력
        user_msg = st.text_input("일본어로 대화를 시작해 보세요 (예: こんにちは！)", key="chat_input")
        
        if st.button("전송", key="send_chat_btn"):
            if user_msg:
                # 사용자 메시지 저장
                st.session_state.chat_history.append({"role": "user", "content": user_msg})
                
                # AI 응답 생성
                try:
                    # 회화 훈련용 시스템 지침 프롬프트 구성
                    system_prompt = (
                        "당신은 친절한 일본어 회화 강사입니다. 학습자의 일본어 수준에 맞게 쉽고 자연스러운 일본어 회화 파트너가 되어 주세요. "
                        "답변 규칙:\n"
                        "1. 반드시 자연스러운 일본어 문장으로 답변을 작성해 주세요.\n"
                        "2. 학습자가 발음을 확인하고 뜻을 파악할 수 있도록, 일본어 답변 바로 밑에 '한글 독음'과 '한국어 번역'을 반드시 줄바꿈하여 병기해 주세요.\n"
                        "예시:\n"
                        "こんにちは！今日のお天気はいかがですか？\n"
                        "(곤니치와! 쿄-노 오텐키와 이카가데스카?)\n"
                        "안녕하세요! 오늘 날씨는 어떠신가요?"
                    )
                    
                    model = genai.GenerativeModel('gemini-pro')
                    
                    # 최근 대화 문맥 구축
                    full_prompt = system_prompt + "\n\n대화 내역:\n"
                    for chat in st.session_state.chat_history[-5:]: # 최근 5개만 전달
                        full_prompt += f"{chat['role']}: {chat['content']}\n"
                    full_prompt += "model (일본어 교사):"
                    
                    with st.spinner("AI가 답변을 생각하고 있습니다..."):
                        response = model.generate_content(full_prompt)
                        ai_response = response.text
                        
                    st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
                    st.rerun()
                except Exception as e:
                    st.error(f"오류가 발생했습니다: {str(e)}")
