# -*- coding: utf-8 -*-
"""행정구별 고유 지역 데이터. 도어웨이 회피의 핵심.

각 항목: 대표 생활권(동/지역) 3~4곳 + 랜드마크 한 줄 + 권역 유형.
유형은 시간대 분포·추천 코스·후기 톤을 분기시킨다.

유형 키:
  biznight  업무+심야 (오피스·번화가 혼재)
  night     관광·번화가 (심야 비중 큼)
  office    업무지구 (퇴근 후 집중)
  resi      주거 위주 (저녁~밤 가족·직장인)
  univ      대학·청년 상권
  suburb    외곽·광역 (이동 시간 김)
"""

# key = "metro/slug"
PROFILES = {
    # ── 서울 25 ──
    "seoul/gangnam": {"areas": ["역삼동", "삼성동", "논현동", "청담동"], "landmark": "강남역·테헤란로 업무축", "type": "biznight"},
    "seoul/gangdong": {"areas": ["천호동", "길동", "둔촌동", "암사동"], "landmark": "천호역 생활권", "type": "resi"},
    "seoul/gangbuk": {"areas": ["미아동", "수유동", "번동"], "landmark": "수유역·북서울 생활권", "type": "resi"},
    "seoul/gangseo": {"areas": ["화곡동", "마곡동", "등촌동", "가양동"], "landmark": "마곡 업무지구·발산역", "type": "biznight"},
    "seoul/gwanak": {"areas": ["신림동", "봉천동", "서원동"], "landmark": "서울대입구·신림 청년 상권", "type": "univ"},
    "seoul/gwangjin": {"areas": ["구의동", "자양동", "화양동", "능동"], "landmark": "건대입구·성수 인접", "type": "univ"},
    "seoul/guro": {"areas": ["구로동", "신도림동", "개봉동"], "landmark": "구로디지털·신도림 환승", "type": "biznight"},
    "seoul/geumcheon": {"areas": ["가산동", "독산동", "시흥동"], "landmark": "가산디지털단지", "type": "office"},
    "seoul/nowon": {"areas": ["상계동", "중계동", "공릉동", "월계동"], "landmark": "노원역·중계 학원가", "type": "resi"},
    "seoul/dobong": {"areas": ["창동", "쌍문동", "방학동", "도봉동"], "landmark": "창동·쌍문 생활권", "type": "resi"},
    "seoul/dongdaemun": {"areas": ["전농동", "장안동", "답십리동", "회기동"], "landmark": "청량리·회기 대학가", "type": "univ"},
    "seoul/dongjak": {"areas": ["사당동", "상도동", "노량진동", "흑석동"], "landmark": "노량진·사당 환승", "type": "resi"},
    "seoul/mapo": {"areas": ["서교동", "합정동", "공덕동", "상암동"], "landmark": "홍대·합정 번화가, 상암 DMC", "type": "night"},
    "seoul/seodaemun": {"areas": ["신촌동", "연희동", "홍은동", "북아현동"], "landmark": "신촌 대학가", "type": "univ"},
    "seoul/seocho": {"areas": ["서초동", "반포동", "방배동", "양재동"], "landmark": "강남대로·양재 업무축", "type": "biznight"},
    "seoul/seongdong": {"areas": ["성수동", "왕십리도선동", "행당동"], "landmark": "성수 카페거리·왕십리 환승", "type": "biznight"},
    "seoul/seongbuk": {"areas": ["길음동", "정릉동", "안암동", "동선동"], "landmark": "성신여대·고려대 인접", "type": "univ"},
    "seoul/songpa": {"areas": ["잠실동", "방이동", "문정동", "가락동"], "landmark": "잠실·문정 업무지구", "type": "biznight"},
    "seoul/yangcheon": {"areas": ["목동", "신정동", "신월동"], "landmark": "목동 학원가", "type": "resi"},
    "seoul/yeongdeungpo": {"areas": ["여의도동", "당산동", "영등포동", "문래동"], "landmark": "여의도 금융가", "type": "office"},
    "seoul/yongsan": {"areas": ["이태원동", "한남동", "용산동", "효창동"], "landmark": "이태원·한남 번화가", "type": "night"},
    "seoul/eunpyeong": {"areas": ["불광동", "응암동", "역촌동", "녹번동"], "landmark": "연신내·불광 생활권", "type": "resi"},
    "seoul/jongno": {"areas": ["종로1가", "혜화동", "사직동", "평창동"], "landmark": "광화문·대학로", "type": "office"},
    "seoul/junggu": {"areas": ["을지로동", "명동", "신당동", "황학동"], "landmark": "명동·을지로 도심", "type": "biznight"},
    "seoul/jungnang": {"areas": ["면목동", "상봉동", "묵동", "중화동"], "landmark": "상봉·면목 생활권", "type": "resi"},
    # ── 경기 31 ──
    "gyeonggi/suwon": {"areas": ["인계동", "영통동", "권선동", "정자동"], "landmark": "인계동 번화가·광교", "type": "biznight"},
    "gyeonggi/seongnam": {"areas": ["분당 정자동", "판교동", "야탑동", "수내동"], "landmark": "판교 테크노밸리·분당", "type": "biznight"},
    "gyeonggi/goyang": {"areas": ["일산 장항동", "백석동", "화정동", "행신동"], "landmark": "일산 라페스타·킨텍스", "type": "resi"},
    "gyeonggi/yongin": {"areas": ["수지구 죽전동", "기흥구 보정동", "처인구 김량장동"], "landmark": "수지·기흥 생활권", "type": "resi"},
    "gyeonggi/bucheon": {"areas": ["중동", "상동", "송내동", "역곡동"], "landmark": "중동·상동 번화가", "type": "biznight"},
    "gyeonggi/ansan": {"areas": ["고잔동", "중앙동", "사동", "본오동"], "landmark": "중앙역·고잔 생활권", "type": "resi"},
    "gyeonggi/anyang": {"areas": ["평촌동", "범계동", "안양동", "비산동"], "landmark": "평촌·범계 번화가", "type": "biznight"},
    "gyeonggi/namyangju": {"areas": ["다산동", "별내동", "와부읍", "화도읍"], "landmark": "다산·별내 신도시", "type": "resi"},
    "gyeonggi/hwaseong": {"areas": ["동탄동", "병점동", "봉담읍", "향남읍"], "landmark": "동탄 신도시", "type": "resi"},
    "gyeonggi/pyeongtaek": {"areas": ["비전동", "송탄동", "안중읍", "고덕동"], "landmark": "고덕 국제신도시·송탄", "type": "suburb"},
    "gyeonggi/uijeongbu": {"areas": ["의정부동", "신곡동", "민락동", "호원동"], "landmark": "의정부역 번화가", "type": "resi"},
    "gyeonggi/siheung": {"areas": ["정왕동", "배곧동", "대야동", "은행동"], "landmark": "배곧 신도시·정왕", "type": "resi"},
    "gyeonggi/paju": {"areas": ["운정동", "금촌동", "교하동", "문산읍"], "landmark": "운정 신도시", "type": "suburb"},
    "gyeonggi/gimpo": {"areas": ["장기동", "구래동", "사우동", "고촌읍"], "landmark": "한강신도시 장기·구래", "type": "resi"},
    "gyeonggi/gwangmyeong": {"areas": ["철산동", "하안동", "소하동", "광명동"], "landmark": "철산·하안 생활권", "type": "resi"},
    "gyeonggi/gwangju": {"areas": ["경안동", "오포읍", "곤지암읍", "태전동"], "landmark": "경안·태전 생활권", "type": "suburb"},
    "gyeonggi/gunpo": {"areas": ["산본동", "당동", "금정동"], "landmark": "산본 번화가", "type": "resi"},
    "gyeonggi/osan": {"areas": ["오산동", "원동", "세교동", "갈곶동"], "landmark": "오산역 생활권", "type": "suburb"},
    "gyeonggi/icheon": {"areas": ["증포동", "창전동", "부발읍", "마장면"], "landmark": "이천 시내·부발", "type": "suburb"},
    "gyeonggi/anseong": {"areas": ["공도읍", "봉산동", "아양동", "죽산면"], "landmark": "공도·안성 시내", "type": "suburb"},
    "gyeonggi/uiwang": {"areas": ["내손동", "오전동", "고천동", "포일동"], "landmark": "인덕원 인접·내손", "type": "resi"},
    "gyeonggi/hanam": {"areas": ["미사동", "망월동", "신장동", "덕풍동"], "landmark": "미사강변도시·스타필드", "type": "resi"},
    "gyeonggi/yeoju": {"areas": ["여흥동", "가남읍", "점동면"], "landmark": "여주 시내", "type": "suburb"},
    "gyeonggi/yangpyeong": {"areas": ["양평읍", "용문면", "강상면"], "landmark": "양평 읍내", "type": "suburb"},
    "gyeonggi/dongducheon": {"areas": ["생연동", "지행동", "보산동"], "landmark": "지행·생연 생활권", "type": "suburb"},
    "gyeonggi/gwacheon": {"areas": ["별양동", "중앙동", "갈현동"], "landmark": "과천 정부청사", "type": "office"},
    "gyeonggi/guri": {"areas": ["수택동", "교문동", "인창동", "토평동"], "landmark": "구리역·돌다리 생활권", "type": "resi"},
    "gyeonggi/pocheon": {"areas": ["소흘읍", "송우리", "포천동"], "landmark": "송우리·소흘", "type": "suburb"},
    "gyeonggi/yangju": {"areas": ["옥정동", "회천동", "덕정동"], "landmark": "옥정 신도시", "type": "suburb"},
    "gyeonggi/gapyeong": {"areas": ["가평읍", "청평면", "설악면"], "landmark": "가평·청평 관광권", "type": "suburb"},
    "gyeonggi/yeoncheon": {"areas": ["전곡읍", "연천읍", "청산면"], "landmark": "전곡·연천 읍내", "type": "suburb"},
    # ── 인천 10 ──
    "incheon/junggu": {"areas": ["운서동", "영종동", "신포동", "연안동"], "landmark": "인천공항·영종도", "type": "suburb"},
    "incheon/donggu": {"areas": ["송림동", "송현동", "화수동"], "landmark": "동인천 생활권", "type": "resi"},
    "incheon/michuhol": {"areas": ["주안동", "용현동", "학익동", "관교동"], "landmark": "주안역 번화가", "type": "resi"},
    "incheon/yeonsu": {"areas": ["송도동", "연수동", "동춘동", "옥련동"], "landmark": "송도 국제도시", "type": "biznight"},
    "incheon/namdong": {"areas": ["구월동", "논현동", "간석동", "만수동"], "landmark": "구월동 번화가·인천시청", "type": "biznight"},
    "incheon/bupyeong": {"areas": ["부평동", "부개동", "삼산동", "산곡동"], "landmark": "부평역 번화가", "type": "night"},
    "incheon/gyeyang": {"areas": ["작전동", "계산동", "효성동"], "landmark": "계양·작전 생활권", "type": "resi"},
    "incheon/seogu": {"areas": ["청라동", "검단동", "가정동", "석남동"], "landmark": "청라 국제도시·검단", "type": "resi"},
    "incheon/ganghwa": {"areas": ["강화읍", "길상면", "선원면"], "landmark": "강화 읍내·관광권", "type": "suburb"},
    "incheon/ongjin": {"areas": ["영흥면", "백령면", "덕적면"], "landmark": "도서 권역(영흥·백령)", "type": "suburb"},
    # ── 부산 16 ──
    "busan/junggu": {"areas": ["남포동", "광복동", "중앙동"], "landmark": "남포동·광복로 번화가", "type": "night"},
    "busan/seogu": {"areas": ["서대신동", "동대신동", "암남동"], "landmark": "대신동 생활권", "type": "resi"},
    "busan/donggu": {"areas": ["초량동", "수정동", "범일동"], "landmark": "부산역·초량", "type": "office"},
    "busan/yeongdo": {"areas": ["동삼동", "영선동", "청학동"], "landmark": "영도·흰여울 관광권", "type": "resi"},
    "busan/busanjin": {"areas": ["부전동", "전포동", "양정동", "범천동"], "landmark": "서면 번화가", "type": "night"},
    "busan/dongnae": {"areas": ["명륜동", "온천동", "사직동"], "landmark": "동래·사직 생활권", "type": "resi"},
    "busan/namgu": {"areas": ["대연동", "용호동", "문현동"], "landmark": "경성대·부경대 상권", "type": "univ"},
    "busan/bukgu": {"areas": ["화명동", "구포동", "덕천동"], "landmark": "화명·덕천 생활권", "type": "resi"},
    "busan/haeundae": {"areas": ["우동", "중동", "좌동", "재송동"], "landmark": "해운대 해수욕장·마린시티", "type": "night"},
    "busan/saha": {"areas": ["하단동", "괴정동", "다대동"], "landmark": "하단·다대 생활권", "type": "resi"},
    "busan/geumjeong": {"areas": ["장전동", "구서동", "부곡동"], "landmark": "부산대 상권", "type": "univ"},
    "busan/gangseo": {"areas": ["명지동", "녹산동", "대저동"], "landmark": "명지 국제신도시", "type": "suburb"},
    "busan/yeonje": {"areas": ["연산동", "거제동"], "landmark": "연산 로터리·시청", "type": "biznight"},
    "busan/suyeong": {"areas": ["광안동", "민락동", "남천동"], "landmark": "광안리 해수욕장", "type": "night"},
    "busan/sasang": {"areas": ["괘법동", "주례동", "감전동"], "landmark": "사상 번화가·서부터미널", "type": "biznight"},
    "busan/gijang": {"areas": ["기장읍", "정관읍", "일광읍"], "landmark": "정관 신도시·기장", "type": "suburb"},
}

# 권역 유형별 콘텐츠 분기
TYPE_INFO = {
    "biznight": {
        "label": "업무·번화가 혼재",
        "peak": "퇴근 직후(19~22시)와 심야(24~02시) 양쪽에 콜이 몰립니다",
        "course": "업무 피로 누적이 많아 스웨디시·아로마 선호가 높고, 늦은 시간에는 강한 압의 스포츠 요청이 늘어납니다",
    },
    "night": {
        "label": "관광·번화가",
        "peak": "심야(23~03시) 콜 비중이 다른 권역보다 뚜렷하게 높습니다",
        "course": "여행·약속 후 늦은 이완 수요가 많아 아로마·로미로미 선호가 두드러집니다",
    },
    "office": {
        "label": "업무지구",
        "peak": "평일 퇴근 직후(18~21시)에 콜이 집중됩니다",
        "course": "장시간 좌식 업무로 어깨·목 부담이 커 스웨디시와 스포츠 조합 요청이 많습니다",
    },
    "resi": {
        "label": "주거 생활권",
        "peak": "저녁(20~23시) 시간대가 가장 안정적으로 분포합니다",
        "course": "가정·직장인 휴식 목적이 많아 부담이 적은 스웨디시·아로마 비중이 높습니다",
    },
    "univ": {
        "label": "대학·청년 상권",
        "peak": "야간(21~01시)에 비교적 고르게 분포합니다",
        "course": "젊은 층 비중이 높아 타이 스트레칭과 스포츠 요청이 상대적으로 많습니다",
    },
    "suburb": {
        "label": "외곽·광역 권역",
        "peak": "이동 거리가 있어 예약 후 도착까지 여유 시간을 두는 편입니다",
        "course": "충분한 휴식을 원하는 90·120분 코스 비중이 다른 권역보다 높습니다",
    },
}

# 후기 템플릿 풀 (행정구·동·코스로 채워 고유화)
REVIEW_POOL = [
    ("{district} {area} 쪽으로 불렀는데 안내받은 시간 안에 도착했어요. {course} 받고 그날 푹 잤습니다.", 5),
    ("{district} {area}에서 처음 이용했는데 강도를 미리 물어봐 주셔서 편했어요. {course} 만족합니다.", 5),
    ("{district} {area} 자취방인데 늦은 시간에도 예약이 됐어요. 금액도 안내 그대로였습니다.", 5),
    ("업무로 {district} {area} 머무는 중에 {course} 받았는데 어깨가 한결 가벼워졌어요.", 4),
    ("{district} {area} 근처라 빨리 와주실까 걱정했는데 생각보다 금방 도착했습니다.", 5),
    ("{district} {area}에서 {course} 받아봤어요. 응대가 정중하고 위생도 신경 쓰는 게 느껴졌습니다.", 5),
    ("{district} {area}에서 가족이 같이 받았는데 둘 다 만족했어요. 다음에 또 부를게요.", 5),
    ("{district} {area} 야근 끝나고 {course} 예약했어요. 추가 비용 없이 안내 금액 그대로라 좋았습니다.", 5),
    ("{district} {area} 쪽 도로가 복잡한데도 예상 시간 안에 오셨어요. 강도 조절이 좋았습니다.", 4),
    ("처음이라 긴장했는데 {district} {area}까지 와주셔서 {course} 잘 받았습니다. 친절했어요.", 5),
    ("{district} {area} 거주 중인데 재방문이에요. 매번 안내 시간 잘 지켜주셔서 신뢰가 갑니다.", 5),
    ("{district} {area}에서 심야에 {course} 받았는데 다음 날 컨디션이 확실히 달랐어요.", 5),
]
