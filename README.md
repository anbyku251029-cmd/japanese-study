# 일본어 학습 프로그램 (Japanese Learning Program)

Streamlit을 기반으로 구축된 종합 일본어 학습 프로그램입니다.

## 주요 기능
1. **단어 카드 학습**: JLPT N5~N1 등급별 단어의 표기, 한글 독음, 뜻을 활용한 플래시카드 학습을 제공합니다.
2. **간격 반복 복습 (SRS)**: 사용자의 암기 상태에 맞추어 다음 복습 주기를 자동으로 계산하여 스케줄링합니다.
3. **AI 일본어 회화 파트너**: Gemini API를 활용하여 일본어 롤플레이 및 프리토킹 연습이 가능하며, 대화 내용에 한글 독음과 한국어 번역이 병기됩니다.
4. **학습 대시보드**: 학습한 단어 수와 암기 진척도를 시각적으로 보여줍니다.

## 실행 방법

### 1. 패키지 설치
```bash
pip install -r requirements.txt
```

### 2. 환경 변수 설정
AI 회화 기능을 이용하기 위해서는 Gemini API Key가 필요합니다.
프로젝트 루트 폴더에 `.env` 파일을 생성하거나 Streamlit 비밀 설정(secrets.toml)에 입력해 주세요.
```env
GEMINI_API_KEY=your_gemini_api_key_here
```
또는 앱 실행 후 웹 UI 상의 사이드바에서 직접 API Key를 입력할 수 있습니다.

### 3. 로컬 앱 실행
```bash
streamlit run app.py
```
