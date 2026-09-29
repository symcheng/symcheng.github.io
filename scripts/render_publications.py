"""Render bibliography into the static page. Run after editing publications.json."""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# Journal versions and preprints are separate entries, newest first by publication or submission date.
papers = sorted(json.loads((ROOT / "content/publications.json").read_text()), key=lambda paper: paper["date"], reverse=True)
RECENT_FROM = 2023


def render(paper, previous=None):
    e = html.escape
    year = paper['date'][:4]
    # Print each year once; repeated years stay available to screen readers.
    year_class = 'publication-year' if previous is None or previous['date'][:4] != year else 'publication-year repeated-year'
    authors = ", ".join(f"<strong>{e(name)}</strong>" if name in ("Song Cheng", "程嵩") else e(name) for name in paper["authors"])
    links = "".join(f'<a class="paper-link" href="{e(url, quote=True)}" target="_blank" rel="noopener noreferrer">{e(label)}</a>' for label, url in paper["links"])
    return f'''<article class="publication"><span class="{year_class}">{year}</span><div class="publication-content"><h3><a href="{e(paper['links'][0][1], quote=True)}" target="_blank" rel="noopener noreferrer">{e(paper['title'])} <span aria-hidden="true">↗</span></a></h3><p class="authors">{authors}</p><div class="paper-links"><span class="publication-venue">{e(paper['venue'])}</span>{links}</div></div></article>'''


page = ROOT / "dist/index.html"
source = page.read_text()
def render_list(group):
    return '\n'.join(render(paper, group[i - 1] if i else None) for i, paper in enumerate(group))


recent = [paper for paper in papers if int(paper['date'][:4]) >= RECENT_FROM]
earlier = [paper for paper in papers if int(paper['date'][:4]) < RECENT_FROM]
span = f"{earlier[-1]['date'][:4]}–{earlier[0]['date'][:4]}"
full_span = f"{papers[-1]['date'][:4]}–{papers[0]['date'][:4]}"
source, count = re.subn(r'<!-- PUBLICATIONS START -->.*?<!-- PUBLICATIONS END -->', f'''<!-- PUBLICATIONS START -->
      <details class="paper-group all-papers" open><summary><span data-en="Journal articles &amp; preprints, {full_span}" data-zh="期刊论文与预印本，{full_span}">Journal articles &amp; preprints, {full_span}</span></summary>
      <div class="publication-list" id="recent-publications">{render_list(recent)}</div>
      <details class="paper-group earlier-papers"><summary><span data-en="Earlier publications, {span}" data-zh="早期论文，{span}">Earlier publications, {span}</span></summary><div class="publication-list">{render_list(earlier)}</div></details>
      </details>
      <!-- PUBLICATIONS END -->''', source, flags=re.S)
if count != 1:
    raise ValueError("Expected one pair of bibliography markers in dist/index.html")
page.write_text(source)
print(f"Rendered {len(papers)} publications.")
