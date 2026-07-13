# -*- coding: utf-8 -*-

# JLPT 등급별 샘플 어휘 데이터베이스
# 각 단어는 일본어 표기, 요미가나, 한글 독음, 뜻, JLPT 등급, 예문, 예문 요미가나, 예문 독음, 예문 뜻을 포함합니다.

VOCABULARY_DECK = [
    # JLPT N5
    {
        "id": 1,
        "word": "日本語",
        "reading": "にほんご",
        "pronunciation": "니혼고",
        "meaning": "일본어",
        "level": "N5",
        "example": "日本語を勉強します。",
        "example_reading": "にほんごをべんきょうします。",
        "example_pronunciation": "니혼고오 벤쿄-시마스.",
        "example_meaning": "일본어를 공부합니다."
    },
    {
        "id": 2,
        "word": "友達",
        "reading": "ともだち",
        "pronunciation": "토모다치",
        "meaning": "친구",
        "level": "N5",
        "example": "友達と遊びます。",
        "example_reading": "ともだちとあそびます。",
        "example_pronunciation": "토모다치토 아소비마스.",
        "example_meaning": "친구와 놉니다."
    },
    {
        "id": 3,
        "word": "美味しい",
        "reading": "おいしい",
        "pronunciation": "오이시-",
        "meaning": "맛있다",
        "level": "N5",
        "example": "この寿司は美味しいです。",
        "example_reading": "このすしはおいしいです。",
        "example_pronunciation": "코노 스시와 오이시-데스.",
        "example_meaning": "이 초밥은 맛있습니다."
    },
    {
        "id": 4,
        "word": "先生",
        "reading": "せんせい",
        "pronunciation": "센세-",
        "meaning": "선생님",
        "level": "N5",
        "example": "山田先生は親切です。",
        "example_reading": "やまだせんせいはしんせつです。",
        "example_pronunciation": "야마다 센세-와 신세츠데스.",
        "example_meaning": "야마다 선생님은 친절합니다."
    },
    {
        "id": 5,
        "word": "本",
        "reading": "ほん",
        "pronunciation": "혼",
        "meaning": "책",
        "level": "N5",
        "example": "毎日本を読みます。",
        "example_reading": "まいにちほんをよみます。",
        "example_pronunciation": "마이니치 혼오 요미마스.",
        "example_meaning": "매일 책을 읽습니다."
    },

    # JLPT N4
    {
        "id": 6,
        "word": "家族",
        "reading": "かぞく",
        "pronunciation": "카조쿠",
        "meaning": "가족",
        "level": "N4",
        "example": "家族と一緒に住んでいます。",
        "example_reading": "かぞくといっしょにすんでいます。",
        "example_pronunciation": "카조쿠토 잇쇼니 순데이마스.",
        "example_meaning": "가족과 함께 살고 있습니다."
    },
    {
        "id": 7,
        "word": "試験",
        "reading": "しけん",
        "pronunciation": "시켄",
        "meaning": "시험",
        "level": "N4",
        "example": "明日は日本語の試験があります。",
        "example_reading": "あしたはにほんごのしけんがあります。",
        "example_pronunciation": "아시타와 니혼고노 시켄가 아리마스.",
        "example_meaning": "내일은 일본어 시험이 있습니다."
    },
    {
        "id": 8,
        "word": "運転",
        "reading": "うんてん",
        "pronunciation": "운텐",
        "meaning": "운전",
        "level": "N4",
        "example": "車の運転ができますか。",
        "example_reading": "くるまのうんてんができますか。",
        "example_pronunciation": "쿠루마노 운텐가 데키마스카.",
        "example_meaning": "자동차 운전을 할 수 있습니까?"
    },
    {
        "id": 9,
        "word": "台所",
        "reading": "だいどころ",
        "pronunciation": "다이도코로",
        "meaning": "부엌",
        "level": "N4",
        "example": "母は台所で料理をしています。",
        "example_reading": "はははだいどころでりょうりをしています。",
        "example_pronunciation": "하하와 다이도코로데 료-리오 시테이마스.",
        "example_meaning": "어머니는 부엌에서 요리를 하고 있습니다."
    },

    # JLPT N3
    {
        "id": 10,
        "word": "準備",
        "reading": "じゅんび",
        "pronunciation": "쥰비",
        "meaning": "준비",
        "level": "N3",
        "example": "旅行の準備は終わりましたか。",
        "example_reading": "りょこうのじゅんびはおわりましたか。",
        "example_pronunciation": "료코-노 쥰비와 오와리마시타카.",
        "example_meaning": "여행 준비는 끝났습니까?"
    },
    {
        "id": 11,
        "word": "興味",
        "reading": "きょうみ",
        "pronunciation": "쿄-미",
        "meaning": "흥미, 관심",
        "level": "N3",
        "example": "日本の文化に興味があります。",
        "example_reading": "にほんのぶんかにきょうみがあります。",
        "example_pronunciation": "니혼노 분카니 쿄-미가 아리마스.",
        "example_meaning": "일본 문화에 흥미가 있습니다."
    },
    {
        "id": 12,
        "word": "解決",
        "reading": "かいけつ",
        "pronunciation": "카이케츠",
        "meaning": "해결",
        "level": "N3",
        "example": "この問題はすぐに解決できます。",
        "example_reading": "このもんだいはすぐにかいけつできます。",
        "example_pronunciation": "코노 몬다이와 스구니 카이케츠 데키마스.",
        "example_meaning": "이 문제는 곧 해결할 수 있습니다."
    },

    # JLPT N2
    {
        "id": 13,
        "word": "影響",
        "reading": "えいきょう",
        "pronunciation": "에이쿄-",
        "meaning": "영향",
        "level": "N2",
        "example": "環境は子供の発達に影響を与えます。",
        "example_reading": "かんきょうはこどものはったつにえいきょうをあたえます。",
        "example_pronunciation": "캉쿄-와 코도모노 핫타츠니 에이쿄-오 아타에마스.",
        "example_meaning": "환경은 아이의 발달에 영향을 줍니다."
    },
    {
        "id": 14,
        "word": "緊張",
        "reading": "きんちょう",
        "pronunciation": "킨쵸-",
        "meaning": "긴장",
        "level": "N2",
        "example": "面接の前にとても緊張しました。",
        "example_reading": "めんせつのまえにとてもきんちょうしました。",
        "example_pronunciation": "멘세츠노 마에니 토테모 킨쵸-시마시타.",
        "example_meaning": "면접 전에 매우 긴장했습니다."
    },
    {
        "id": 15,
        "word": "豊富",
        "reading": "ほうふ",
        "pronunciation": "호-후",
        "meaning": "풍부함",
        "level": "N2",
        "example": "彼は経験が豊富なエンジニアです。",
        "example_reading": "かれはけいけんがほうふなえんじにあです。",
        "example_pronunciation": "카레와 케이켄가 호-후나 엔지니아데스.",
        "example_meaning": "그는 경험이 풍부한 엔지니어입니다."
    },

    # JLPT N1
    {
        "id": 16,
        "word": "矛盾",
        "reading": "むじゅん",
        "pronunciation": "무쥰",
        "meaning": "모순",
        "level": "N1",
        "example": "彼の発言には矛盾が多いです。",
        "example_reading": "かれのはつげんにはむじゅんがおおいです。",
        "example_pronunciation": "카레노 하츠겐니와 무쥰가 오오이데스.",
        "example_meaning": "그의 발언에는 모순이 많습니다."
    },
    {
        "id": 17,
        "word": "詳細",
        "reading": "しょうさい",
        "pronunciation": "쇼-사이",
        "meaning": "상세함, 자세함",
        "level": "N1",
        "example": "詳細はウェブサイトをご参照ください。",
        "example_reading": "しょうさいはウェブサイトをごさんしょうください。",
        "example_pronunciation": "쇼-사이와 웨부사이토오 고산쇼-쿠다사이.",
        "example_meaning": "자세한 내용은 웹사이트를 참조해 주십시오."
    },
    {
        "id": 18,
        "word": "迅速",
        "reading": "じんそく",
        "pronunciation": "진소쿠",
        "meaning": "신속함",
        "level": "N1",
        "example": "トラブルに対して迅速に対応しました。",
        "example_reading": "とらぶるにたいしてじんそくにたいおうしました。",
        "example_pronunciation": "토라부루니 타이시테 진소쿠니 타이오-시마시타.",
        "example_meaning": "문제에 대해 신속하게 대응했습니다."
    }
]

# 단어 덱 데이터를 가져오는 함수
def get_vocab_by_level(level="All"):
    if level == "All":
        return VOCABULARY_DECK
    return [word for word in VOCABULARY_DECK if word["level"] == level]
