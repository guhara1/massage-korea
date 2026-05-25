# -*- coding: utf-8 -*-
"""빌드 후 미니파이. dist/*.html 의 인라인 CSS·HTML 공백을 안전하게 축소.

- CSS: <style> 내부 주석 제거 + 공백 축소
- HTML: 태그 사이 공백 제거(>\\s+<) + 다중 공백 1칸
- JS/JSON-LD는 줄바꿈을 보존(다중 공백만 축소)하므로 // 주석·구문 안전
- <pre>/<textarea> 는 이 사이트에 없으므로 별도 보호 불필요
"""

import os
import re
import glob


def minify_css(css: str) -> str:
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    css = re.sub(r"\s*([{}:;,>+~])\s*", r"\1", css)
    css = re.sub(r"\s+", " ", css)
    css = re.sub(r";}", "}", css)
    return css.strip()


def minify_html(html: str) -> str:
    # 1) <style> 내부만 CSS 미니파이
    html = re.sub(r"<style[^>]*>(.*?)</style>",
                  lambda m: f"<style>{minify_css(m.group(1))}</style>",
                  html, flags=re.S)
    # 2) <script> 보호: 잠시 치환
    scripts = []
    def _stash(m):
        scripts.append(m.group(0))
        return f"\x00SCRIPT{len(scripts)-1}\x00"
    html = re.sub(r"<script[^>]*>.*?</script>", _stash, html, flags=re.S)
    # 3) 태그 사이 공백 제거 + 다중 공백 축소 (텍스트/속성 내 단일 공백은 보존)
    html = re.sub(r">\s+<", "><", html)
    html = re.sub(r"[ \t]{2,}", " ", html)
    html = re.sub(r"\n\s*\n", "\n", html)
    # 4) <script> 복원 (다중 공백만 축소, 줄바꿈 보존 → // 주석 안전)
    def _restore(m):
        s = scripts[int(m.group(1))]
        return re.sub(r"[ \t]{2,}", " ", s)
    html = re.sub(r"\x00SCRIPT(\d+)\x00", _restore, html)
    return html.strip()


def run(out_dir):
    total_before = total_after = 0
    for f in glob.glob(os.path.join(out_dir, "**", "*.html"), recursive=True):
        src = open(f, encoding="utf-8").read()
        out = minify_html(src)
        total_before += len(src.encode("utf-8"))
        total_after += len(out.encode("utf-8"))
        open(f, "w", encoding="utf-8").write(out)
    pct = (1 - total_after / total_before) * 100 if total_before else 0
    print(f"미니파이: {total_before:,}B → {total_after:,}B ({pct:.1f}% 감소)")
