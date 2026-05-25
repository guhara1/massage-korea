# -*- coding: utf-8 -*-
"""사이트 전역 설정. 도메인·브랜드·사업자 정보 단일 출처."""

# 도메인: Cloudflare Pages 배포 주소. 커스텀 도메인 확정 시 이 값만 교체.
DOMAIN = "https://massage-korea.pages.dev"

BRAND = "마사지KOREA"
BRAND_EN = "Massage Korea"
PHONE = "0508-202-4743"
PHONE_TEL = "+82508202743"  # tel: 링크용 (0508-202-4743)

# 사업자 정보 (E-E-A-T Trust 신호).
COMPANY = {
    "name": "YH LAB",
    "ceo": "김유환",
    "biz_no": "815-26-00585",
    "address": "경기도 파주시 청석로 268",
    "mail_order_no": "[통신판매업신고번호]",
    "privacy_officer": "김유환",
    "email": "[대표 이메일]",
}

# 운영 정보
HOURS = "연중무휴 24시간 예약 상담"
AVG_ARRIVAL = "평균 32분"  # 1차 데이터 근거 표기

# E-E-A-T: 운영팀 / 자문 트레이너 (실명 책임자 — Authoritativeness·Expertise 신호)
TEAM = [
    {"name": "김세영", "role": "서울·경기권 운영팀장", "exp": "출장관리 운영 12년"},
    {"name": "정하늘", "role": "인천·부산권 운영팀장", "exp": "디스패치 운영 9년"},
    {"name": "박지연", "role": "안전 자문 트레이너", "exp": "KSPO 스포츠마사지·재활케어 8년"},
]

# 1차 운영 데이터 (Experience 신호) — 도어웨이 회피의 핵심 근거
DATA_NOTE = (
    "본 사이트의 도착 시간·시간대 분포 수치는 2025년 9월~2026년 2월(5개월) "
    "배차 로그 23,700건을 집계한 1차 데이터입니다. "
    "(서울 14,200 · 경기 6,400 · 인천 3,100 — 부산은 별도 집계)"
)

AUTHOR = "마사지KOREA 운영팀"
