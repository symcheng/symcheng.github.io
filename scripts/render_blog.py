"""Generate the bilingual blog as static HTML; no runtime or build dependency."""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "dist"
home = (PUBLIC / "index.html").read_text()
e = html.escape
posts = [json.loads(path.read_text()) for path in sorted((ROOT / "content/posts").glob("*.json"))]


def i18n(en, zh, tag="span", attrs=""):
    return f'<{tag}{attrs} data-en="{e(en, quote=True)}" data-zh="{e(zh, quote=True)}">{e(en)}</{tag}>'


def localized_meta(name, en, zh, attribute="name"):
    return f'<meta {attribute}="{name}" content="{e(en, quote=True)}" data-content-en="{e(en, quote=True)}" data-content-zh="{e(zh, quote=True)}">'


def adapt_links(markup, prefix):
    def replace(match):
        url = match[1]
        if url.startswith(("https:", "mailto:", "data:")):
            return match[0]
        if url.startswith("#"):
            url = f"index.html{url}"
        return f'href="{prefix}{url}"'
    return re.sub(r'href="([^"]*)"', replace, markup)


def render_page(body, prefix, title, description, kind, title_zh, description_zh):
    head = re.search(r"<head>.*?</head>", home, re.S)[0]
    head = re.sub(r"<title>.*?</title>", lambda m: i18n(f"{title} · Song Cheng", f"{title_zh} · 程嵩", "title"), head)
    head = re.sub(r'<meta name="description"[^>]*>', lambda m: localized_meta("description", description, description_zh), head)
    head = re.sub(r'<meta property="og:description"[^>]*>', lambda m: localized_meta("og:description", description, description_zh, "property"), head)
    head = re.sub(r'<meta property="og:title"[^>]*>', lambda m: localized_meta("og:title", title, title_zh, "property"), head)
    if kind == "article":
        head = head.replace('content="website"', 'content="article"')
    head = re.sub(r'src="([^"/]+\.js)"', lambda match: f'src="{prefix}{match[1]}"', head)
    head = adapt_links(head, prefix)

    header = re.search(r'<header class="site-header">.*?</header>', home, re.S)[0]
    header = header.replace('href="blog/index.html"', 'href="blog/index.html" aria-current="page"')
    header = adapt_links(header, prefix)
    footer = re.search(r'<footer class="site-footer">.*?</footer>', home, re.S)[0]
    return f'''<!doctype html>
<html lang="en" data-theme="dark">
{head}
<body class="blog-page {kind}-page">
{i18n("Skip to content", "跳至正文", "a", ' class="skip-link" href="#main"')}
{header}
<main id="main">{body}</main>
{footer}
</body>
</html>
'''


def index_entry(post, number):
    zh = post["translations"]["zh"]
    return f'''<article class="blog-entry">
      <div><p class="entry-meta">{i18n(post['category'], zh['category'])} <span>·</span> {i18n(f"{post['readingMinutes']} min read", f"约 {zh['readingMinutes']} 分钟")}</p>
      <h2><a href="{post['slug']}/index.html">{i18n(post['title'], zh['title'])}<span aria-hidden="true">↗</span></a></h2>
      {i18n(post['description'], zh['description'], 'p', ' class="entry-description"')}
      <a class="entry-link" href="{post['slug']}/index.html">{i18n('Read the article', '阅读全文')} <span aria-hidden="true">→</span></a></div>
    </article>'''


def video_figure(post):
    """Optional player at the top of an article; files live in dist/assets/video/."""
    video = post.get("video")
    if not video:
        return ""
    for name in (video["file"], video["poster"]):
        assert (PUBLIC / "assets/video" / name).is_file(), f"Missing video asset: {name}"
    src, poster = f'../../assets/video/{video["file"]}', f'../../assets/video/{video["poster"]}'
    minutes, seconds, size = video["minutes"], video["seconds"], video["sizeMB"]
    download = i18n(f"Download the video (MP4, {size} MB)", f"下载视频（MP4，{size} MB）", "a", f' href="{src}"')
    return f'''<figure class="film article-film"><div class="film-screen"><video controls preload="metadata" playsinline poster="{poster}" width="1920" height="1080" aria-describedby="film-description"><source src="{src}" type="video/mp4">{download}</video></div><figcaption>{i18n(video["caption"], post["translations"]["zh"]["videoCaption"], "p", ' id="film-description"')}{i18n(f"{minutes} min {seconds} s, made with Claude", f"{minutes} 分 {seconds} 秒，由 Claude 制作", "span", ' class="film-meta"')}</figcaption></figure>'''


blog_dir = PUBLIC / "blog"
blog_dir.mkdir(exist_ok=True)
entries = '\n'.join(index_entry(post, number) for number, post in enumerate(posts, 1)) or i18n('No articles yet.', '暂无文章。', 'p', ' class="blog-empty"')
index_body = f'''<section class="blog-intro">{i18n('Ideas, explanations and research', '想法、科普与研究', 'p', ' class="eyebrow"')}<h1>{i18n('Blog', '博客')}<span class="name-period">.</span></h1><div class="blog-intro-bottom">{i18n('Notes on tensor networks, quantum computing, and the ideas that connect them.', '关于张量网络、量子计算及其相互联系的研究随笔。', 'p')}{i18n(f'{len(posts)} articles', f'{len(posts)} 篇文章', 'span', ' class="blog-count"')}</div></section>
<section class="blog-list" aria-label="Articles" data-aria-label-en="Articles" data-aria-label-zh="文章列表">{entries}</section>
<div class="blog-bottom">{i18n('Questions or thoughts?', '欢迎交流问题与想法。')}<a href="mailto:chengsong@bimsa.cn">chengsong@bimsa.cn ↗</a></div>'''
(blog_dir / "index.html").write_text(render_page(index_body, "../", "Blog", "Research notes and accessible introductions to tensor networks, quantum computing, and machine learning.", "blog-index", "博客", "关于张量网络、量子计算与机器学习的研究随笔和科普介绍。"))

for post in posts:
    zh = post["translations"]["zh"]
    assert len(post["sections"]) == len(zh["sections"]), f"Incomplete translation: {post['slug']}"
    paired_sections = list(zip(post["sections"], zh["sections"]))
    toc = ''.join(f'<li><a href="#section-{i}">{i18n(section["heading"], translated["heading"])}</a></li>' for i, (section, translated) in enumerate(paired_sections, 1))
    sections = []
    for i, (section, translated) in enumerate(paired_sections, 1):
        assert len(section["paragraphs"]) == len(translated["paragraphs"]), f"Incomplete paragraph translation: {post['slug']}, section {i}"
        paragraphs = ''.join(i18n(paragraph, chinese, 'p') for paragraph, chinese in zip(section["paragraphs"], translated["paragraphs"]))
        sections.append(f'<section id="section-{i}" class="article-section">{i18n(section["heading"], translated["heading"], "h2")}{paragraphs}</section>')
    sources = ''.join(f'<li><a href="{e(source["url"], quote=True)}" target="_blank" rel="noopener noreferrer">{e(source["label"])} <span aria-hidden="true">↗</span></a></li>' for source in post["sources"])
    related = ''.join(f'<a href="../{item["slug"]}/index.html">{i18n(item["category"], item["translations"]["zh"]["category"])}<strong>{i18n(item["title"], item["translations"]["zh"]["title"])} <span aria-hidden="true">↗</span></strong></a>' for item in posts if item != post)
    body = f'''<article class="blog-article">
      <header class="article-header"><a class="back-link" href="../index.html">← {i18n('All articles', '全部文章')}</a><p class="entry-meta">{i18n(post['category'], zh['category'])} <span>·</span> {i18n(f"{post['readingMinutes']} min read", f"约 {zh['readingMinutes']} 分钟")}</p>{i18n(post['title'], zh['title'], 'h1')}{i18n(post['description'], zh['description'], 'p', ' class="article-description"')}<div class="article-byline">{i18n('Song Cheng', '程嵩')}{i18n('BIMSA · Research notes', 'BIMSA · 研究随笔')}</div></header>
      <div class="article-layout"><aside class="article-toc"><nav aria-label="In this article" data-aria-label-en="In this article" data-aria-label-zh="本文目录">{i18n('In this article', '本文目录', 'p')}<ol>{toc}</ol></nav></aside><div class="article-body">{video_figure(post)}{''.join(sections)}<section class="article-sources" aria-labelledby="sources-heading">{i18n('Papers & further reading', '论文与延伸阅读', 'h2', ' id="sources-heading"')}<ol>{sources}</ol></section></div></div>
      <nav class="related-articles" aria-label="More articles" data-aria-label-en="More articles" data-aria-label-zh="更多文章">{i18n('Continue reading', '继续阅读', 'p', ' class="eyebrow"')}<div>{related}</div></nav>
    </article>'''
    destination = blog_dir / post["slug"]
    destination.mkdir(exist_ok=True)
    (destination / "index.html").write_text(render_page(body, "../../", post["title"], post["description"], "article", zh["title"], zh["description"]))
print(f"Rendered blog index and {len(posts)} articles.")
