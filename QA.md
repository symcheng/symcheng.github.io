# Preview validation

Checked locally on 2026-09-26. No GitHub repository has been created or changed, and no deployment has run.

> Update 2026-09-29: the original three articles were replaced by three new video articles (tensor-network machine learning, quantum error correction, high-temperature superconductivity), and the homepage video was replaced with the latest render. Article-specific checks below refer to the old articles. For the new ones: `check_site.py` passes for 5 pages; all four videos load with the expected durations and all covers return HTTP 200; English and Chinese versions were checked; no horizontal overflow at 375 CSS pixels.

- All five HTML routes respond locally: the homepage, blog index, and three articles.
- Static validation passes for 165 references, local assets, fragment links, unique IDs, and one main heading per page. Relative paths support both GitHub user pages and project pages.
- Homepage tested at 320, 768, and 1280 CSS pixels without document-level horizontal overflow. Blog index and article layouts also inspected at mobile and desktop widths; the noisy-circuit article passed the same three viewport checks.
- English homepage checked for remaining Chinese body text: none. The language button remains visible. Chinese translation and return to English work.
- Blog index and all three articles switch between complete English and Chinese versions. Titles, summaries, categories, reading times, bylines, table of contents, all 35 body paragraphs, diagram descriptions/captions, related links and page metadata follow the language button. Original source-paper titles remain unchanged. The document language follows the selected language.
- Chinese article layout checked at 320, 390 and 1280 CSS pixels without document-level horizontal overflow. English restoration and Chinese preference propagation through related-article links pass.
- The eight earlier publications expand and collapse with the Enter key.
- Blog links, table-of-contents anchors, and related-article links work. Each article has five sections and links to original papers.
- Images and local fonts load successfully. Public CV returns HTTP 200. No browser console warnings or errors were observed during the checked flows.
- Public CV redaction was verified using extracted text, metadata, PDF objects and rendered pages; source PDF is untouched.
- Three article drafts received a scientific review. The MPS description distinguishes a uniform bond dimension from a translation-invariant uniform MPS and states the single-bond open-chain condition for its Schmidt-rank bound.

The local server must remain running for the preview links to work. Deployment can be reviewed after the user approves the preview and confirms the GitHub destination.

## Theme switching

- Light mode retains the original colors. Dark mode covers the homepage, blog index, article text, contact area and embedded tensor diagram.
- New visitors start in dark mode. An isolated JavaScript check confirms that explicit URL choices and saved light-mode preferences take precedence, while absent/invalid preferences and unavailable storage fall back to dark mode.
- Theme selection persists across navigation and reloads, including a fresh URL without a theme parameter.
- Both language settings and keyboard activation work. The button announces its next action with a localized accessible name.
- Header layout checked at 320, 375, 760, 761, 1024 and 1280 CSS pixels: no horizontal overflow or displaced theme button.
- A local JavaScript check exercised file and HTTPS URLs with unavailable browser storage and restricted file history; theme and language still propagate in links, while PDF, email and external links remain intact.
