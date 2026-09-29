"""Render the course list into the static page. Run after editing courses.json.

Terms use BIMSA's semester codes: 2025au is fall 2025, 2026sp is spring 2026.
Course listings: https://www.bimsa.cn/research/course/<term>/page_1.html?keyword=song+cheng
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECENT_FROM = 2024
courses = sorted(json.loads((ROOT / "content/courses.json").read_text()), key=lambda c: (c["term"][:4], c["term"][4:] == "au"), reverse=True)


def term_label(term):
    year, season = term[:4], term[4:]
    assert season in ("sp", "au"), f"Unknown term: {term}"
    return (f"Spring {year}", f"{year} 春季") if season == "sp" else (f"Fall {year}", f"{year} 秋季")


def render(course):
    e = html.escape
    en, zh = term_label(course["term"])
    return f'''<article class="course"><span class="course-term" data-en="{en}" data-zh="{zh}">{en}</span><h3><a href="{e(course['url'], quote=True)}" target="_blank" rel="noopener noreferrer"><span data-en="{e(course['title'], quote=True)}" data-zh="{e(course['title_zh'], quote=True)}">{e(course['title'])}</span> <span aria-hidden="true">↗</span></a></h3></article>'''


recent = [c for c in courses if int(c["term"][:4]) >= RECENT_FROM]
earlier = [c for c in courses if int(c["term"][:4]) < RECENT_FROM]
span = f"{earlier[-1]['term'][:4]}–{earlier[0]['term'][:4]}"
page = ROOT / "dist/index.html"
source = page.read_text()
source, count = re.subn(r"<!-- COURSES START -->.*?<!-- COURSES END -->", f'''<!-- COURSES START -->
        {chr(10).join(render(c) for c in recent)}
        <details class="paper-group earlier-courses"><summary><span data-en="Earlier courses, {span}" data-zh="更早的课程，{span}">Earlier courses, {span}</span></summary>{chr(10).join(render(c) for c in earlier)}</details>
        <!-- COURSES END -->''', source, flags=re.S)
if count != 1:
    raise ValueError("Expected one pair of course markers in dist/index.html")
page.write_text(source)
print(f"Rendered {len(courses)} courses.")
