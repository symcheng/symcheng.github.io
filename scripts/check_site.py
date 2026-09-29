"""Dependency-free checks for static files and internal navigation."""
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "dist"


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.references = []
        self.headings = 0

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag == "h1":
            self.headings += 1
        for name in ("src", "href"):
            if attrs.get(name):
                self.references.append(attrs[name])
        if tag == "img":
            assert "alt" in attrs, "Image missing alt text"
        if "data-en" in attrs:
            assert attrs.get("data-zh"), "Missing Chinese translation"


pages = {}
for path in PUBLIC.rglob("*.html"):
    page = Page()
    page.feed(path.read_text())
    assert page.headings == 1, f"Expected one primary heading: {path}"
    assert len(page.ids) == len(set(page.ids)), f"Duplicate element IDs: {path}"
    pages[path.resolve()] = page

references = 0
for path, page in pages.items():
    for reference in page.references:
        references += 1
        parsed = urlsplit(reference)
        if parsed.scheme or parsed.netloc:
            continue
        target = path
        if parsed.path:
            assert not parsed.path.startswith("/"), f"Root-relative URL breaks project Pages: {reference}"
            target = (path.parent / unquote(parsed.path)).resolve()
            assert not target.is_dir(), f"Link targets a directory instead of a page: {reference} in {path}"
            assert target.is_relative_to(PUBLIC.resolve()) and target.is_file(), f"Missing local asset: {reference} in {path}"
        if parsed.fragment:
            assert target in pages and parsed.fragment in pages[target].ids, f"Missing anchor: {reference} in {path}"

for font in re.findall(r"url\(['\"]?([^'\")]+)", (PUBLIC / "styles.css").read_text()):
    assert (PUBLIC / font).is_file(), f"Missing CSS asset: {font}"

papers = json.loads((ROOT / "content/publications.json").read_text())
# A preprint and its journal version may share a title, so entries are unique by link and dated in order.
links = [link for paper in papers for _, link in paper["links"]]
assert len(links) == len(set(links)), "Duplicate paper links"
assert all(re.fullmatch(r"\d{4}-\d{2}(-\d{2})?", paper["date"]) for paper in papers), "Paper dates must be YYYY-MM or YYYY-MM-DD"
assert len(papers) == (PUBLIC / "index.html").read_text().count('class="publication"'), "Render publications after updating JSON"
for paper in papers:
    assert "Song Cheng" in paper["authors"] or "程嵩" in paper["authors"]
    for _, link in paper["links"]:
        assert urlsplit(link).scheme == "https", f"Invalid paper URL: {link}"

assert (PUBLIC / ".nojekyll").is_file()
posts = list((ROOT / "content/posts").glob("*.json"))
for post in posts:
    data = json.loads(post.read_text())
    article = (PUBLIC / "blog" / data["slug"] / "index.html").read_text()
    translated = data["translations"]["zh"]
    for key in ("title", "description", "category"):
        assert translated[key].strip(), f"Missing Chinese {key}: {post}"
    assert len(translated["sections"]) == len(data["sections"]), f"Incomplete translated sections: {post}"
    for section, chinese in zip(data["sections"], translated["sections"]):
        assert section["paragraphs"], f"Empty article section: {post}"
        assert chinese["heading"].strip(), f"Missing translated heading: {post}"
        assert len(chinese["paragraphs"]) == len(section["paragraphs"]), f"Incomplete translated paragraphs: {post}"
        assert all(text.strip() for text in chinese["paragraphs"]), f"Empty translated paragraph: {post}"
    assert 'class="language-toggle"' in article, "Missing language control"
print(f"PASS: {len(pages)} pages, {references} references, {len(papers)} publications, {len(posts)} bilingual articles, translations, anchors, and local assets.")
