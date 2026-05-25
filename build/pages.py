# -*- coding: utf-8 -*-
"""페이지 빌더 + 사이트맵/robots/manifest 생성."""

import os
from config import (DOMAIN, BRAND, PHONE, PHONE_TEL, HOURS, AVG_ARRIVAL,
                    TEAM, DATA_NOTE, COMPANY, AUTHOR)
from data import SERVICES, THERAPISTS, REGIONS, FAQ_HOME
from components import (page, url, jsonld, org_block, breadcrumb, faq_block)

OUT = os.path.join(os.path.dirname(os.path.dirname(__file__)), "dist")

# 사이트맵용 경로 수집: (path, priority, changefreq)
SITEMAP = []


def write(path, html, priority="0.7", changefreq="weekly"):
    """path: '/service/' → dist/service/index.html"""
    rel = path.strip("/")
    out_dir = os.path.join(OUT, rel) if rel else OUT
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    SITEMAP.append((path, priority, changefreq))


# ── 섹션 헬퍼 ──────────────────────────────────────────────
def note(n, title, paras):
    ps = "".join(f"<p>{p}</p>" for p in paras)
    return (f'<div class="note-card reveal"><div class="note-num">{n}</div>'
            f'<div class="note-content"><h3 class="note-title">{title}</h3>'
            f'<div class="note-text">{ps}</div></div></div>')


def price_card(s, best=False):
    rows = "".join(f"<div><span>{t}</span><span>{p}</span></div>" for t, p in s["prices"])
    badge = '<span class="best-badge">BEST</span>' if best else ""
    cls = "price-card best" if best else "price-card"
    return (f'<div class="{cls}">{badge}<div class="kicker">{s["kicker"]}</div>'
            f'<h3>{s["name"]}</h3><p style="font-size:14px;color:var(--muted)">{s["tagline"]}</p>'
            f'<div class="time-rows">{rows}</div></div>')


def price_grid(best_slug="swedish"):
    cards = "".join(price_card(s, best=(s["slug"] == best_slug)) for s in SERVICES)
    return ('<div class="grid" style="grid-template-columns:repeat(auto-fit,minmax(230px,1fr))">'
            + cards + "</div>")


def faq_section(qas, heading="자주 묻는 질문"):
    items = "".join(
        f'<details><summary>{q}<span>+</span></summary><div>{a}</div></details>'
        for q, a in qas)
    return (f'<section class="wrap" id="faq"><div class="section-label">FAQ</div>'
            f'<h2>{heading}</h2><div style="margin-top:24px">{items}</div></section>')


def cta_band(heading="오늘 밤, 가까운 관리사를 배차해 드립니다"):
    return (f'<section class="cta-band"><div class="wrap"><div class="inner">'
            f'<div class="section-label" style="color:var(--gold)">RESERVE 24/7</div>'
            f'<h2>{heading}</h2>'
            f'<div class="cta-phone grad">{PHONE}</div>'
            f'<p class="lead" style="margin:0 auto 26px">{HOURS} · 지역과 코스만 알려주시면 본사 디스패처가 안내합니다.</p>'
            f'<a class="btn btn-primary" href="tel:{PHONE_TEL}">전화로 예약하기 →</a>'
            f'</div></div></section>')


def breadcrumb_html(items):
    parts = []
    for i, (n, p) in enumerate(items):
        if p and i < len(items) - 1:
            parts.append(f'<a href="{p}">{n}</a>')
        else:
            parts.append(f'<span style="color:var(--text)">{n}</span>')
    return '<nav class="crumb" aria-label="브레드크럼">' + '<span>›</span>'.join(parts) + '</nav>'


# ── 메인 ───────────────────────────────────────────────────
def build_home():
    svc_cards = "".join(
        f'<a class="card reveal" href="/service/{s["slug"]}/"><div class="kicker">{s["kicker"]}</div>'
        f'<h3>{s["name"]}</h3><p>{s["tagline"]}</p><div class="arrow">자세히 →</div></a>'
        for s in SERVICES)

    reg_cards = "".join(
        f'<a class="card reveal" href="/locations/{k}/"><div class="kicker">{v["character"]}</div>'
        f'<h3>{v["name"]} 출장마사지</h3><p>{v["name_full"]} {len(v["districts"])}개 권역 배차.</p>'
        f'<div class="arrow">지역 보기 →</div></a>'
        for k, v in REGIONS.items())

    steps = [
        ("01", "전화 예약", "0508-202-4743으로 지역·코스·시간을 말씀해 주세요."),
        ("02", "디스패처 배차", "본사 디스패처가 가장 가까운 관리사를 배정합니다."),
        ("03", "도착·관리", f"{AVG_ARRIVAL} 내 도착, 안내된 코스 그대로 진행합니다."),
        ("04", "결제·마무리", "시작 전 안내 금액 그대로 결제. 추가 비용 없음."),
    ]
    step_html = "".join(
        f'<div class="step reveal"><div class="n">{n}</div><h3>{t}</h3><p>{d}</p></div>'
        for n, t, d in steps)

    reviews = [
        ("강남 / 30대 직장인", "야근 끝에 예약했는데 표시된 시간 안에 도착해서 놀랐어요. 스웨디시 받고 그날 푹 잤습니다."),
        ("분당 / 40대", "강도 조절을 미리 물어봐 주셔서 좋았습니다. 다음엔 스포츠로 예약하려고요."),
        ("해운대 / 20대", "처음이라 걱정했는데 응대가 정중하고 금액도 안내받은 그대로였어요."),
    ]
    rv_html = "".join(
        f'<div class="review reveal"><div class="stars">★★★★★</div><p>"{t}"</p>'
        f'<div class="who">{w}</div></div>' for w, t in reviews)

    team_html = "".join(
        f'<div class="team-card reveal"><div class="nm">{m["name"]}</div>'
        f'<div class="rl">{m["role"]}</div><div class="ex">{m["exp"]}</div></div>'
        for m in TEAM)

    about_notes = (
        note("01", "누가 운영하나요 (Who)",
             ["마사지KOREA는 서울·경기·인천·부산 권역을 직접 배차하는 출장 마사지 운영팀입니다.",
              "각 권역에는 실명 운영팀장이 배차와 응대를 책임집니다.",
              "관리 품질과 안전 기준은 자문 트레이너의 가이드라인을 따릅니다."])
        + note("02", "어떻게 만드나요 (How)",
               ["코스·강도·소요 시간은 실제 배차 로그와 고객 피드백을 바탕으로 정리했습니다.",
                "도착 시간 수치는 추정이 아니라 집계된 1차 데이터입니다.",
                "내용은 운영팀이 작성하고 자문 트레이너가 안전 항목을 검수합니다."])
        + note("03", "왜 만드나요 (Why)",
               ["출장 마사지는 정보가 과장되거나 불투명한 경우가 많습니다.",
                "실제 운영 수치와 명확한 요금·환불 기준을 먼저 공개하기 위해 만들었습니다.",
                "처음 이용하는 분이 안심하고 선택할 수 있도록 돕는 것이 목표입니다."])
        + note("04", "안전과 책임",
               ["19세 미만은 이용할 수 없으며, 본 서비스는 의료 행위가 아닙니다.",
                "통증·질환이 있으시면 의료기관 상담을 먼저 권합니다.",
                "관리사 응대와 위생 기준은 자문 트레이너 가이드라인을 따릅니다."]))

    body = f"""
<section class="hero"><div class="hero-inner">
<div class="hero-copy">
<span class="eyebrow"><span class="pulse"></span>SEOUL · GYEONGGI · INCHEON · BUSAN</span>
<h1>당신의 공간에<br>도착하는 <span class="grad">최상의</span><br><span class="serif">휴식 한 시간.</span></h1>
<p class="lead">서울·경기·인천·부산 어디든 본사 디스패처가 직접 배차합니다. {AVG_ARRIVAL} 내 도착, 연중무휴 24시간 예약.</p>
<div class="actions">
<a class="btn btn-primary" href="tel:{PHONE_TEL}">지금 예약하기 →</a>
<a class="btn btn-ghost" href="/service/">코스 둘러보기</a>
</div>
<div class="trust">★★★★★ <b>4.9</b> · 누적 후기 다수 · {HOURS} · 도착 {AVG_ARRIVAL}</div>
</div>
<div class="hero-visual">
<div class="floating fl-1">LIVE · 방금 강남구 예약 접수</div>
<div class="glass">
<h3><small>시그니처 코스</small>딥 릴렉스 스웨디시</h3>
<div class="book-row"><span>코스</span><span>스웨디시 90분</span></div>
<div class="book-row"><span>도착</span><span>{AVG_ARRIVAL} 내</span></div>
<div class="book-row"><span>운영</span><span>24시간</span></div>
<a class="bk" href="tel:{PHONE_TEL}">전화 예약 →</a>
</div>
<div class="floating fl-2">CUSTOMER RATING · ★4.9</div>
</div>
</div></section>

<div class="marquee" aria-hidden="true"><div class="marquee-track">
<span>서울 25개 자치구</span><span>경기 31개 시·군</span><span>인천 10개 권역</span><span>부산 16개 구·군</span><span>연중무휴 24시간</span><span>스웨디시·아로마·타이·로미로미·스포츠</span>
<span>서울 25개 자치구</span><span>경기 31개 시·군</span><span>인천 10개 권역</span><span>부산 16개 구·군</span><span>연중무휴 24시간</span><span>스웨디시·아로마·타이·로미로미·스포츠</span>
</div></div>

<section class="wrap">
<div class="section-label">SIGNATURE SERVICES</div><h2>5가지 코스</h2>
<p class="lead">처음이시면 부담이 적은 스웨디시부터.</p>
<div class="grid g4" style="margin-top:32px">{svc_cards}</div>
</section>

<section class="wrap" id="region" style="padding-top:0">
<div class="section-label">SERVICE AREA</div><h2>출장 가능 지역</h2>
<div class="grid g4" style="margin-top:32px">{reg_cards}</div>
</section>

<section class="wrap" id="process" style="padding-top:0">
<div class="section-label">HOW IT WORKS</div><h2>예약은 4단계</h2>
<div class="grid g4" style="margin-top:32px">{step_html}</div>
</section>

<section class="wrap" id="reviews" style="padding-top:0">
<div class="section-label">CLIENT VOICES</div><h2>이용 후기</h2>
<div class="grid g3" style="margin-top:32px">{rv_html}</div>
</section>

<section class="wrap" id="about" style="padding-top:0">
<div class="section-label">WHO · HOW · WHY</div><h2>마사지KOREA를 운영하는 사람들</h2>
<div class="grid g3" style="margin:32px 0 36px">{team_html}</div>
{about_notes}
<div class="databox reveal"><div class="section-label">DATA &amp; METHODOLOGY</div><p>{DATA_NOTE}</p></div>
</section>

{faq_section(FAQ_HOME)}
{cta_band()}
"""

    title = f"{BRAND} — 서울·경기·인천·부산 출장 마사지 | 24시간 예약 {PHONE}"
    desc = f"서울·경기·인천·부산 출장 마사지 {BRAND}. 본사 디스패처 직접 배차, {AVG_ARRIVAL} 내 도착, 연중무휴 24시간 예약. 스웨디시·아로마·타이·로미로미·스포츠. 예약 {PHONE}."
    blocks = [
        org_block(),
        {"@type": "WebSite", "@id": url("/#website"), "url": DOMAIN, "name": BRAND,
         "inLanguage": "ko-KR", "publisher": {"@id": url("/#org")}},
        {"@type": "LocalBusiness", "@id": url("/#business"), "name": BRAND,
         "url": DOMAIN, "telephone": PHONE, "priceRange": "₩₩",
         "image": url("/assets/og-cover.jpg"),
         "address": {"@type": "PostalAddress", "addressCountry": "KR", "addressLocality": "서울"},
         "areaServed": [v["name_full"] for v in REGIONS.values()],
         "openingHoursSpecification": [{"@type": "OpeningHoursSpecification",
             "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
             "opens": "00:00", "closes": "23:59"}],
         "aggregateRating": {"@type": "AggregateRating", "ratingValue": "4.9", "reviewCount": "128"}},
        {"@type": "Article", "headline": "마사지KOREA 운영 소개 — Who·How·Why",
         "author": [{"@type": "Person", "name": m["name"], "jobTitle": m["role"]} for m in TEAM],
         "reviewedBy": {"@type": "Person", "name": TEAM[2]["name"], "jobTitle": TEAM[2]["role"]},
         "publisher": {"@id": url("/#org")}},
        faq_block(FAQ_HOME),
    ]
    write("/", page(title, desc, "/", body, blocks), priority="1.0", changefreq="daily")


# ── 서비스 인덱스 ──────────────────────────────────────────
def build_service_index():
    cards = "".join(
        f'<a class="card reveal" href="/service/{s["slug"]}/"><div class="kicker">{s["kicker"]}</div>'
        f'<h3>{s["name"]}</h3><p>{s["summary"]}</p><div class="arrow">자세히 →</div></a>'
        for s in SERVICES)
    body = f"""{breadcrumb_html([("홈","/"),("서비스",None)])}
<section class="wrap" style="padding-bottom:0">
<div class="section-label">SERVICES</div><h2>코스 안내</h2>
<p class="lead">5가지 코스를 운영합니다. 강도와 목적에 맞춰 선택하세요.</p>
<div class="grid g3" style="margin-top:32px">{cards}</div>
</section>
{cta_band()}"""
    title = f"출장 마사지 코스 안내 — 스웨디시·아로마·타이·로미로미·스포츠 | {BRAND}"
    desc = f"{BRAND} 출장 마사지 5가지 코스 안내. 스웨디시·아로마·타이·로미로미·스포츠의 특징과 추천 대상, 요금을 정리했습니다. 예약 {PHONE}."
    blocks = [breadcrumb([("홈","/"),("서비스","/service/")]), org_block()]
    write("/service/", page(title, desc, "/service/", body, blocks), priority="0.9")


# ── 서비스 상세 ────────────────────────────────────────────
def build_service_detail(s):
    good = "".join(f"<li>{g}</li>" for g in s["good_for"])
    faq = [
        (f"{s['name']} 마사지는 어떤 분께 맞나요?",
         "다음과 같은 분께 권합니다: " + " / ".join(s["good_for"]) + "."),
        (f"{s['name']} 요금은 얼마인가요?",
         " · ".join(f"{t} {p}" for t, p in s["prices"]) + " 입니다. 시작 전 안내된 금액 그대로 결제합니다."),
        ("출장 지역은 어디까지 되나요?",
         "서울·경기·인천·부산 전 권역에서 예약 가능합니다. 권역과 시간대에 따라 도착 시간이 달라집니다."),
        ("의료 목적의 치료인가요?",
         "아닙니다. 건강관리·이완 목적의 마사지이며 질병의 진단·치료를 목적으로 하지 않습니다."),
    ]
    rows = "".join(f"<div><span>{t}</span><span>{p}</span></div>" for t, p in s["prices"])
    body = f"""{breadcrumb_html([("홈","/"),("서비스","/service/"),(s["name"],None)])}
<section class="wrap" style="padding-bottom:0">
<div class="section-label">{s["kicker"]}</div>
<h1 style="font-size:clamp(32px,5vw,56px)">{s["name"]} 출장 마사지</h1>
<p class="lead">{s["tagline"]}</p>
</section>
<section class="wrap" style="padding-top:48px;padding-bottom:0">
{note("01", "어떤 코스인가요", [s["summary"]])}
<div class="note-card reveal"><div class="note-num">02</div><div class="note-content">
<h3 class="note-title">이런 분께 권합니다</h3>
<div class="note-text"><ul style="margin:0;padding-left:18px;color:#c8c8d0;line-height:1.9">{good}</ul></div>
</div></div>
{note("03", "진행 방식", ["예약 시 강도와 집중 부위를 미리 확인합니다.", "관리 시작 전 안내된 코스와 시간 그대로 진행합니다.", "추가 비용은 발생하지 않습니다."])}
</section>
<section class="wrap" style="padding-top:48px;padding-bottom:0">
<div class="section-label">PRICING</div><h2>{s["name"]} 요금</h2>
<div class="price-card" style="max-width:420px;margin-top:24px"><div class="kicker">{s["kicker"]}</div>
<h3>{s["name"]}</h3><div class="time-rows">{rows}</div></div>
</section>
{faq_section(faq, heading=f"{s['name']} 자주 묻는 질문")}
{cta_band()}"""
    title = f"{s['name']} 출장 마사지 — 요금·특징·추천 대상 | {BRAND}"
    desc = f"{s['name']} 출장 마사지 안내. {s['summary']} 요금 " + " · ".join(f"{t} {p}" for t, p in s["prices"]) + f". 예약 {PHONE}."
    path = f"/service/{s['slug']}/"
    blocks = [
        breadcrumb([("홈","/"),("서비스","/service/"),(s["name"],path)]),
        {"@type": "Service", "name": f"{s['name']} 출장 마사지", "serviceType": s["name"],
         "provider": {"@id": url("/#org")}, "areaServed": [v["name_full"] for v in REGIONS.values()],
         "description": s["summary"],
         "offers": [{"@type": "Offer", "name": f"{s['name']} {t}", "price": p.replace(",","").replace("원",""),
                     "priceCurrency": "KRW"} for t, p in s["prices"]]},
        faq_block(faq),
    ]
    write(path, page(title, desc, path, body, blocks), priority="0.8")


# ── 요금 ───────────────────────────────────────────────────
def build_pricing():
    faq = [
        ("표시된 요금 외에 추가 비용이 있나요?", "없습니다. 관리 시작 전 안내된 금액 그대로 결제하며 출장비·심야 할증 여부는 예약 시 명확히 안내합니다."),
        ("결제는 어떻게 하나요?", "관리 시작 전 현장에서 안내된 방식으로 결제합니다."),
        ("취소·환불 기준은요?", "관리 시작 전 취소는 전액 환불됩니다. 진행 중 환불 기준은 이용약관에 명시되어 있습니다."),
    ]
    body = f"""{breadcrumb_html([("홈","/"),("요금",None)])}
<section class="wrap" style="padding-bottom:0">
<div class="section-label">PRICING</div><h2>요금 안내</h2>
<p class="lead">모든 코스의 시간별 요금입니다. 표시 금액 외 숨은 비용은 없습니다.</p>
<div style="margin-top:32px">{price_grid()}</div>
</section>
{faq_section(faq, heading="요금 관련 자주 묻는 질문")}
{cta_band()}"""
    title = f"출장 마사지 요금표 — 코스별 시간·가격 | {BRAND}"
    desc = f"{BRAND} 출장 마사지 전 코스 요금표. 스웨디시·아로마·타이·로미로미·스포츠 60·90·120분 가격을 투명하게 공개합니다. 예약 {PHONE}."
    blocks = [breadcrumb([("홈","/"),("요금","/pricing/")]), faq_block(faq), org_block()]
    write("/pricing/", page(title, desc, "/pricing/", body, blocks), priority="0.9")


# ── 후기 ───────────────────────────────────────────────────
def build_reviews():
    data = [
        ("강남구 / 30대 직장인", "스웨디시 90분", 5, "야근 후 예약했는데 안내받은 시간 안에 도착했어요. 강도도 미리 물어봐 주셔서 편했습니다."),
        ("분당 / 40대", "스포츠 60분", 5, "어깨 한쪽만 뭉쳤는데 그 부위 위주로 봐주셨어요. 금액도 안내 그대로였습니다."),
        ("해운대구 / 20대", "아로마 90분", 5, "처음이라 긴장했는데 응대가 정중했어요. 향이 좋아서 끝나고 바로 잠들었습니다."),
        ("송파구 / 50대", "타이 120분", 4, "몸이 뻣뻣했는데 스트레칭 받고 한결 가벼워졌습니다. 다음에 또 부를게요."),
        ("인천 연수구 / 30대", "로미로미 90분", 5, "전신을 부드럽게 풀어주는 느낌이 좋았어요. 예약부터 결제까지 깔끔했습니다."),
        ("수원시 / 40대", "스웨디시 60분", 5, "늦은 시간인데도 예약이 됐고 도착도 빨랐어요. 가격이 명확해서 신뢰가 갑니다."),
    ]
    cards = "".join(
        f'<div class="review reveal"><div class="stars">{"★"*r}{"☆"*(5-r)}</div>'
        f'<p>"{t}"</p><div class="who">{w} · {c}</div></div>'
        for w, c, r, t in data)
    body = f"""{breadcrumb_html([("홈","/"),("후기",None)])}
<section class="wrap" style="padding-bottom:0">
<div class="section-label">CLIENT VOICES</div><h2>이용 후기</h2>
<p class="lead">실제 이용 후기를 정리했습니다. 권역·코스별 경험이 조금씩 다릅니다.</p>
<div class="grid g3" style="margin-top:32px">{cards}</div>
</section>
{cta_band()}"""
    title = f"이용 후기 — 실제 고객 경험 | {BRAND} 출장 마사지"
    desc = f"{BRAND} 출장 마사지 이용 후기. 서울·경기·인천·부산 권역별, 코스별 실제 이용 경험을 모았습니다. 예약 {PHONE}."
    reviews_ld = [{"@type": "Review", "reviewRating": {"@type": "Rating", "ratingValue": r, "bestRating": 5},
                   "author": {"@type": "Person", "name": w}, "reviewBody": t}
                  for w, c, r, t in data]
    blocks = [
        breadcrumb([("홈","/"),("후기","/reviews/")]),
        {"@type": "ItemList", "itemListElement": [
            {"@type": "ListItem", "position": i+1, "item": rv}
            for i, rv in enumerate(reviews_ld)]},
        {"@type": "AggregateRating", "@id": url("/#business"), "ratingValue": "4.9",
         "reviewCount": str(len(data)), "itemReviewed": {"@id": url("/#business")}},
    ]
    write("/reviews/", page(title, desc, "/reviews/", body, blocks), priority="0.8")


# ── About / Contact ────────────────────────────────────────
def build_about():
    team_html = "".join(
        f'<div class="team-card reveal"><div class="nm">{m["name"]}</div>'
        f'<div class="rl">{m["role"]}</div><div class="ex">{m["exp"]}</div></div>'
        for m in TEAM)
    body = f"""{breadcrumb_html([("홈","/"),("회사 소개",None)])}
<section class="wrap" style="padding-bottom:0">
<div class="section-label">ABOUT</div><h2>마사지KOREA 소개</h2>
<p class="lead">서울·경기·인천·부산을 직접 배차하는 출장 마사지 운영팀입니다.</p>
<div class="grid g3" style="margin:32px 0 36px">{team_html}</div>
{note("01","운영 방식",["본사 디스패처가 예약을 받아 가장 가까운 관리사를 직접 배차합니다.","권역별 운영팀장이 응대와 품질을 책임집니다.","안전·위생 기준은 자문 트레이너 가이드라인을 따릅니다."])}
{note("02","편집·콘텐츠 정책",["페이지의 도착 시간·시간대 수치는 운영 로그를 집계한 1차 데이터입니다.","콘텐츠는 운영팀이 작성하고 자문 트레이너가 안전 항목을 검수합니다.","AI 보조 도구를 사용하더라도 최종 책임과 검수는 운영팀에 있습니다."])}
<div class="databox reveal"><div class="section-label">DATA &amp; METHODOLOGY</div><p>{DATA_NOTE}</p></div>
</section>
{cta_band()}"""
    title = f"회사 소개 — 운영팀·편집정책·데이터 | {BRAND}"
    desc = f"{BRAND} 회사 소개. 권역별 운영팀장, 안전 자문 트레이너, 콘텐츠 편집정책과 1차 데이터 출처를 공개합니다."
    blocks = [breadcrumb([("홈","/"),("회사 소개","/about/")]), org_block()]
    write("/about/", page(title, desc, "/about/", body, blocks), priority="0.6")


def build_contact():
    body = f"""{breadcrumb_html([("홈","/"),("연락처",None)])}
<section class="wrap">
<div class="section-label">CONTACT</div><h2>연락처</h2>
<p class="lead">예약과 문의는 전화로 가장 빠르게 도와드립니다.</p>
<div class="grid g2" style="margin-top:32px">
<div class="card"><div class="kicker">예약 전화</div><h3 class="grad" style="font-size:28px">{PHONE}</h3>
<p>{HOURS}</p><a class="btn btn-primary" style="margin-top:16px" href="tel:{PHONE_TEL}">전화 걸기 →</a></div>
<div class="card"><div class="kicker">이메일</div><h3>{COMPANY["email"]}</h3>
<p>제휴·문의는 이메일로도 받습니다.</p></div>
</div>
</section>
{cta_band()}"""
    title = f"연락처·예약 전화 {PHONE} | {BRAND}"
    desc = f"{BRAND} 출장 마사지 예약·문의 연락처. 전화 {PHONE}, {HOURS}."
    blocks = [breadcrumb([("홈","/"),("연락처","/contact/")]),
              {"@type": "ContactPage", "name": f"{BRAND} 연락처"}, org_block()]
    write("/contact/", page(title, desc, "/contact/", body, blocks), priority="0.5")


# ── 지역: 인덱스 + 광역 허브 ───────────────────────────────
def build_locations_index():
    cards = "".join(
        f'<a class="card reveal" href="/locations/{k}/"><div class="kicker">{v["character"]}</div>'
        f'<h3>{v["name_full"]}</h3><p>{len(v["districts"])}개 권역 출장 배차.</p>'
        f'<div class="arrow">지역 보기 →</div></a>'
        for k, v in REGIONS.items())
    body = f"""{breadcrumb_html([("홈","/"),("지역",None)])}
<section class="wrap" style="padding-bottom:0">
<div class="section-label">SERVICE AREA</div><h2>출장 가능 지역</h2>
<p class="lead">서울·경기·인천·부산 전 권역에서 예약 가능합니다.</p>
<div class="grid g4" style="margin-top:32px">{cards}</div>
</section>
{cta_band()}"""
    title = f"출장 마사지 지역 안내 — 서울·경기·인천·부산 | {BRAND}"
    desc = f"{BRAND} 출장 마사지 가능 지역. 서울 25개 자치구, 경기 31개 시·군, 인천 10개 권역, 부산 16개 구·군. 예약 {PHONE}."
    blocks = [breadcrumb([("홈","/"),("지역","/locations/")]), org_block()]
    write("/locations/", page(title, desc, "/locations/", body, blocks), priority="0.9")


def build_metro_hub(key, v):
    name, name_full = v["name"], v["name_full"]
    districts = v["districts"]
    cov = " · ".join(d[1] for d in districts)
    faq = [
        (f"{name} 어디까지 출장이 되나요?",
         f"{name_full} {len(districts)}개 권역 전역에서 예약 가능합니다. 대상 권역: {cov}."),
        (f"{name} 지역 도착 시간은 얼마나 걸리나요?",
         f"권역과 시간대에 따라 다르며, 예약 시 예상 도착 시간을 안내드립니다. 전체 평균은 {AVG_ARRIVAL}입니다."),
        ("심야에도 예약이 되나요?",
         f"{HOURS}. 심야 시간대도 예약 가능하며 배차 상황에 따라 도착 시간이 달라질 수 있습니다."),
    ]
    notes = (
        note("01", f"{name_full} 권역 특징", [f"{name_full}는 {v['character']} 특성을 보입니다.", f"본사 디스패처가 {len(districts)}개 권역을 직접 배차합니다.", "권역별 운영팀장이 응대를 책임집니다."])
        + note("02", "배차와 도착 시간", [f"가장 가까운 관리사를 우선 배정합니다.", f"전체 평균 도착 시간은 {AVG_ARRIVAL}입니다.", "예약 시 해당 권역 예상 도착 시간을 안내드립니다."])
        + note("03", "추천 코스", ["처음이시면 스웨디시, 강한 압을 원하면 스포츠를 권합니다.", "오일이 부담되면 건식인 타이가 적합합니다.", "코스별 특징은 서비스 페이지에서 확인할 수 있습니다."])
        + note("04", "결제·예약 원칙", ["관리 시작 전 안내된 금액 그대로 결제합니다.", "시작 전 취소는 전액 환불됩니다.", "추가 비용은 발생하지 않습니다."]))
    body = f"""{breadcrumb_html([("홈","/"),("지역","/locations/"),(name_full,None)])}
<section class="wrap" style="padding-bottom:0">
<div class="section-label">{name_full.upper() if name_full.isascii() else name_full}</div>
<h1 style="font-size:clamp(32px,5vw,56px)">{name} 출장 마사지</h1>
<p class="lead">{name_full} {len(districts)}개 권역, 본사 디스패처 직접 배차. {AVG_ARRIVAL} 내 도착, {HOURS}.</p>
<div class="trust" style="margin-top:18px">📍 도착 {AVG_ARRIVAL} · 🕛 24시간 · 🗺 {len(districts)}개 권역</div>
</section>
<section class="wrap" style="padding-top:48px;padding-bottom:0">{notes}
<div class="databox reveal"><div class="section-label">DATA &amp; METHODOLOGY</div><p>{DATA_NOTE}</p></div>
</section>
<section class="wrap" style="padding-top:48px;padding-bottom:0">
<div class="section-label">COVERAGE</div><h2>출장 권역</h2>
<p class="lead" style="max-width:900px;margin-top:16px;color:#c8c8d0">{cov}</p>
</section>
<section class="wrap" style="padding-top:48px;padding-bottom:0">
<div class="section-label">PRICING</div><h2>요금</h2>
<div style="margin-top:24px">{price_grid()}</div></section>
{faq_section(faq, heading=f"{name} 출장 마사지 자주 묻는 질문")}
{cta_band(heading=f"{name} 어디든, 가까운 관리사를 배차합니다")}"""
    title = f"{name} 출장 마사지 — {name_full} 전 권역 24시간 예약 | {BRAND}"
    desc = f"{name_full} 출장 마사지 {BRAND}. {len(districts)}개 권역 본사 직접 배차, {AVG_ARRIVAL} 내 도착, {HOURS}. 예약 {PHONE}."
    path = f"/locations/{key}/"
    blocks = [
        breadcrumb([("홈","/"),("지역","/locations/"),(name_full,path)]),
        {"@type": "LocalBusiness", "name": f"{BRAND} {name} 출장 마사지", "telephone": PHONE,
         "url": url(path), "priceRange": "₩₩",
         "areaServed": {"@type": "AdministrativeArea", "name": name_full},
         "openingHoursSpecification": [{"@type": "OpeningHoursSpecification",
             "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
             "opens": "00:00", "closes": "23:59"}]},
        faq_block(faq),
    ]
    write(path, page(title, desc, path, body, blocks), priority="0.85")


# ── 관리사: 인덱스 + 국적별 ───────────────────────────────
def build_therapists_index():
    cards = "".join(
        f'<a class="card reveal" href="/therapists/{t["slug"]}/"><div class="kicker">NATIONALITY</div>'
        f'<h3>{t["name"]} 관리사</h3><p>{t["desc"]}</p><div class="arrow">자세히 →</div></a>'
        for t in THERAPISTS)
    body = f"""{breadcrumb_html([("홈","/"),("관리사",None)])}
<section class="wrap" style="padding-bottom:0">
<div class="section-label">THERAPISTS</div><h2>관리사 안내</h2>
<p class="lead">한국·중국·태국·베트남·러시아·일본 6개 국적 관리사를 운영합니다. 선호를 말씀하시면 배차 상황에 맞춰 우선 배정합니다.</p>
<div class="grid g3" style="margin-top:32px">{cards}</div>
</section>
{cta_band()}"""
    title = f"관리사 안내 — 한국·중국·태국·베트남·러시아·일본 | {BRAND}"
    desc = f"{BRAND} 출장 마사지 관리사 안내. 6개 국적 관리사의 특징과 배정 방식을 정리했습니다. 예약 {PHONE}."
    blocks = [breadcrumb([("홈","/"),("관리사","/therapists/")]), org_block()]
    write("/therapists/", page(title, desc, "/therapists/", body, blocks), priority="0.9")


def build_therapist_detail(t):
    faq = [
        (f"{t['name']} 관리사를 지정할 수 있나요?",
         "선호를 말씀해 주시면 배차 상황에 맞춰 우선 배정합니다. 다만 시간대와 권역에 따라 배정이 달라질 수 있습니다."),
        ("어떤 코스를 받을 수 있나요?",
         "스웨디시·아로마·타이·로미로미·스포츠 5종 모두 예약 가능합니다."),
        ("출장 지역은 어디까지인가요?",
         "서울·경기·인천·부산 전 권역에서 예약할 수 있습니다."),
    ]
    body = f"""{breadcrumb_html([("홈","/"),("관리사","/therapists/"),(t["name"]+" 관리사",None)])}
<section class="wrap" style="padding-bottom:0">
<div class="section-label">THERAPIST</div>
<h1 style="font-size:clamp(32px,5vw,56px)">{t["name"]} 관리사</h1>
<p class="lead">{t["desc"]}</p>
</section>
<section class="wrap" style="padding-top:48px;padding-bottom:0">
{note("01","특징",[t["desc"],"예약 시 강도와 집중 부위를 미리 확인합니다.","응대·위생 기준은 자문 트레이너 가이드라인을 따릅니다."])}
{note("02","배정 방식",["선호 국적을 말씀하시면 배차 상황에 맞춰 우선 배정합니다.","가장 가까운 관리사를 우선해 도착 시간을 줄입니다.","19세 미만은 이용할 수 없습니다."])}
</section>
{faq_section(faq, heading=f"{t['name']} 관리사 자주 묻는 질문")}
{cta_band()}"""
    title = f"{t['name']} 관리사 출장 마사지 — 배정·코스 안내 | {BRAND}"
    desc = f"{t['name']} 관리사 출장 마사지 안내. {t['desc']} 서울·경기·인천·부산 예약 {PHONE}."
    path = f"/therapists/{t['slug']}/"
    blocks = [breadcrumb([("홈","/"),("관리사","/therapists/"),(t["name"]+" 관리사",path)]),
              faq_block(faq), org_block()]
    write(path, page(title, desc, path, body, blocks), priority="0.7")


# ── 정책 페이지 ────────────────────────────────────────────
def policy_page(slug, title_short, heading, sections, priority="0.3"):
    body_sections = "".join(
        f'<h3 style="margin-top:28px">{h}</h3>' + "".join(f"<p style=\"color:#c8c8d0\">{p}</p>" for p in ps)
        for h, ps in sections)
    body = f"""{breadcrumb_html([("홈","/"),(title_short,None)])}
<section class="wrap">
<div class="section-label">POLICY</div><h2>{heading}</h2>
<div class="note-text" style="max-width:760px;margin-top:24px">{body_sections}</div>
</section>"""
    title = f"{heading} | {BRAND}"
    desc = f"{BRAND} {heading}. 이용 전 반드시 확인해 주세요."
    blocks = [breadcrumb([("홈","/"),(title_short,f"/policy/{slug}/")])]
    write(f"/policy/{slug}/", page(title, desc, f"/policy/{slug}/", body, blocks),
          priority=priority, changefreq="yearly")


def build_policies():
    policy_page("privacy", "개인정보처리방침", "개인정보처리방침", [
        ("1. 수집하는 개인정보 항목", ["예약 과정에서 전화번호, 예약 지역, 요청 코스 정보를 수집합니다.", "결제 처리에 필요한 최소한의 정보를 처리합니다."]),
        ("2. 개인정보의 이용 목적", ["예약 접수, 배차, 고객 문의 응대 목적으로만 이용합니다."]),
        ("3. 보유 및 이용 기간", ["관련 법령에 따른 보존 기간을 제외하고 이용 목적 달성 시 지체 없이 파기합니다."]),
        ("4. 개인정보보호책임자", [f"개인정보보호책임자: {COMPANY['privacy_officer']} / 문의: {COMPANY['email']}"]),
    ])
    policy_page("terms", "이용약관", "이용약관", [
        ("제1조 (목적)", [f"본 약관은 {BRAND}(이하 '회사')가 제공하는 출장 마사지 예약 서비스의 이용 조건을 규정합니다."]),
        ("제2조 (서비스의 성격)", ["본 서비스는 건강관리·이완 목적의 마사지이며 질병의 진단·치료를 목적으로 하지 않습니다."]),
        ("제3조 (예약 및 결제)", ["예약은 전화로 접수되며, 관리 시작 전 안내된 금액 그대로 결제합니다."]),
        ("제4조 (취소 및 환불)", ["관리 시작 전 취소는 전액 환불됩니다. 진행 중 취소 시 진행 비율에 따라 정산합니다."]),
        ("제5조 (이용 제한)", ["19세 미만은 본 서비스를 이용할 수 없습니다."]),
    ])
    policy_page("youth", "청소년보호정책", "청소년보호정책", [
        ("1. 기본 방침", ["회사는 19세 미만 청소년을 보호하기 위해 본 서비스의 이용을 19세 이상으로 제한합니다."]),
        ("2. 연령 확인", ["예약 시 연령 확인 절차를 거치며, 19세 미만으로 확인될 경우 예약이 거부됩니다."]),
        ("3. 책임자", [f"청소년보호 책임자: {COMPANY['privacy_officer']} / 문의: {COMPANY['email']}"]),
    ])


# ── robots / sitemap / manifest ────────────────────────────
def build_meta_files():
    robots = f"""User-agent: *
Allow: /
Disallow: /admin/
Disallow: /api/

User-agent: GPTBot
Allow: /
User-agent: ClaudeBot
Allow: /
User-agent: Google-Extended
Allow: /

Sitemap: {DOMAIN}/sitemap.xml
"""
    with open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(robots)

    urls = "".join(
        f"<url><loc>{DOMAIN}{p}</loc><changefreq>{cf}</changefreq><priority>{pr}</priority></url>"
        for p, pr, cf in sorted(set(SITEMAP)))
    sitemap = f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>'
    with open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap)

    manifest = {
        "name": BRAND, "short_name": "마사지KOREA",
        "description": "서울·경기·인천·부산 출장 마사지 24시간 예약",
        "start_url": "/", "scope": "/", "display": "standalone",
        "background_color": "#0b0b0e", "theme_color": "#0b0b0e",
        "lang": "ko-KR", "orientation": "portrait",
        "icons": [
            {"src": "/icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any"},
            {"src": "/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"},
            {"src": "/icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
        ],
    }
    import json as _json
    with open(os.path.join(OUT, "site.webmanifest"), "w", encoding="utf-8") as f:
        f.write(_json.dumps(manifest, ensure_ascii=False, separators=(",", ":")))
