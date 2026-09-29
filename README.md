# Song Cheng · 程嵩

学术个人主页，英文默认，可切换中文。Blog 目录、文章正文、视频说明、目录导航和相关文章均有中英文版本。纯静态 HTML、CSS 和 JavaScript；字体、插画与视频均在本地，不依赖第三方 CDN。

右上角的月亮／太阳按钮可切换深浅色模式。首次访问默认深色，之后记住访客的选择；本地文件预览也会通过站内链接保持主题。

网站计划发布在 <https://symcheng.github.io/>，发布方式见文末。

## 预览

在本目录运行：

```sh
python3 -m http.server 4173 --bind 127.0.0.1 --directory dist
```

打开 <http://127.0.0.1:4173/>。中文预览为 <http://127.0.0.1:4173/?lang=zh>。停止服务器后需要重新运行命令。

也可以直接双击 `dist/index.html` 预览。站内页面链接均显式包含 `index.html`，不依赖服务器自动打开目录首页。

## 文件

- `dist/index.html`：首页，所有学术内容预渲染，禁用 JavaScript 也可阅读。
- `dist/styles.css`：主题与响应式样式。
- `dist/script.js`：中英文切换，通过 URL 保留当前语言。
- `dist/theme-init.js`、`dist/theme.css`：首屏主题初始化、深色配色与切换按钮。
- `dist/blog/`：独立博客目录与三篇双语文章，每篇配一部视频（张量网络机器学习、张量网络与量子纠错、高温超导）；没有文章时目录页显示“暂无文章”。
- `dist/blog.css`：博客和阅读页样式。
- `content/posts/`：双语文章源数据，每篇一个 JSON，按文件名排序（文件名前缀数字决定顺序）；可选的 `video` 字段在正文开头插入播放器，视频说明的中文在 `translations.zh.videoCaption`；英文字段保持在顶层，中文译文在 `translations.zh`，章节及段落逐一对应。
- `scripts/render_blog.py`：生成博客目录、文章、目录导航和相关文章。
- `dist/assets/`：原始插画的副本、自托管字体。网站不提供 CV 下载。
- `dist/assets/illustrations/`：首页研究方向使用的三张蜡笔插画（神经网络、量子噪声、环面码），由 `output/imagegen/quantum-crayon-series/` 的 PNG 压缩为 800px JPEG。
- 博客目录不配图片，新文章默认同样没有图片。
- `dist/assets/video/`：首页“视频”一节的张量网络科普短片，以及三篇博客文章的视频，均已烧录字幕，并各附一张封面帧。它们是 `../video_promo/` 中成片的原样副本：`tensor_networks_promo.mp4`、`tnml/tnml_promo.mp4`、`qec/tn_qec_promo.mp4`、`htsc/htsc_promo.mp4`。重新渲染后需再次复制，并用 ffmpeg 重新截取封面（首页取第 5 秒，文章取第 7 秒）。
- `content/publications.json`：论文目录，按年份排序；将已核验的正式版和预印本链接放在同一项。
- `scripts/render_publications.py`：将论文数据更新到 HTML。
- `content/courses.json`：课程列表，`term` 使用 BIMSA 学期代码（如 `2025au` 为 2025 秋季、`2026sp` 为 2026 春季），链接指向 BIMSA 课程详情页。
- `scripts/render_courses.py`：将课程数据更新到 HTML；新学期只需在 JSON 中加一项后运行。
- `scripts/check_site.py`：检查本地资源、页面锚点与论文链接。
- `.github/workflows/pages.yml`：仅允许手动触发的 GitHub Pages 发布流程，依次重新生成论文、课程与博客并检查后发布 `dist/`。
- `SOURCES.md`：资料出处及需要注意的版本差异。
- `licenses/`：字体的 SIL Open Font License。

网站不提供 CV 下载；父目录中的原始 CV 与原图不属于网站内容，不会发布。

## 更新

编辑个人简介、联系方式、经历、科研项目（Grants，资料来自父目录 CV）时，修改 `dist/index.html` 中的可见英文文本与对应 `data-en`、`data-zh` 两个属性。论文的正式标题保留原文。

更新论文后运行：

```sh
python3 scripts/render_publications.py
python3 scripts/render_courses.py
python3 scripts/render_blog.py
python3 scripts/check_site.py
node --check dist/script.js
```

## 发布到 GitHub Pages

源码在私有仓库 `symcheng/homepage_mine` 中维护；公开网站使用独立的公开仓库 `symcheng/symcheng.github.io`，其根目录即本目录 `site/` 的内容。

首次发布：

1. 在 GitHub 上创建公开仓库 `symcheng.github.io`（可为空仓库）。
2. 在私有仓库根目录运行 `./publish-site.sh`。脚本只导出 `site/` 中已提交的文件，不带私有仓库的历史，也不包含父目录的原始 CV、原图和视频工程。
3. 在公开仓库的 Settings → Pages 中，将 Source 设为 GitHub Actions。
4. 在公开仓库的 Actions 中手动运行 “Publish personal website”。

之后更新：在私有仓库提交改动后，再运行一次 `./publish-site.sh`，然后手动运行上述工作流。

工作流没有 `push` 触发器，因此推送到公开仓库不会自动上线，需要手动运行一次。站内文件使用相对路径，也兼容 `https://用户名.github.io/仓库名/` 形式。

工作流依据 [GitHub Pages 官方自定义工作流文档](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages) 配置。
