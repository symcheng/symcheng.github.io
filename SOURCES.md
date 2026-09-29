# 内容来源与核验记录

核验日期：2026-09-26。没有从未提供的历史记忆中补造个人经历。

## 基本资料

- [BIMSA 官方个人页面](https://www.bimsa.cn/detail/songcheng.html)：现职、研究方向、公开工作邮箱、办公室、任职与教育年份、截至 2026 年的论文。
- 父目录 `CV-SongCheng.pdf`：文件元数据日期 2025-11-19；任职月份、教育经历、课程与论文的补充资料。
- 父目录 `main.jpeg`：用户提供的首屏肖像（实为 PNG），2026-09-29 起替换 `343FFF2A-…_c.jpeg`；缩放为 1024×768 JPEG 后保存为 `dist/assets/song-cheng.jpeg`，未做其他编辑。
- 研究方向的介绍为以上资料的简洁改写；中文课程名为对应英文课程名的翻译。

## 版本与取舍

- 当前职位：BIMSA Quantum Symmetry Group 副教授，2025 年 10 月至今。
- 网站论文包含 2026 年新内容。2026-09-29 起网站不再提供 CV 下载，公开版 PDF 已从 `dist/assets/` 删除（仍保留在 git 历史中）。
- 教学栏仅展示 CV 中的三门近期课程，不宣称是 2026 年最新或全部开课记录。
- 未展示 CV 中相互冲突的累计引用数，也未猜测 Google Scholar、ORCID、GitHub 或社交账号。
- 手机号码已从公开版 PDF 通过真正 PDF redaction 删除，原始文件保留在网站目录之外。

## 论文处理

每项的一手链接存放在 `content/publications.json`。同一工作的预印本与期刊正式版分列两项，不合并，全部按日期倒序排列（2026-09-29 调整）：

- 期刊版日期取 Crossref 登记的上线日期；*物理* 46(7) 在 Crossref 无记录，按卷期记为 2017-07。
- 预印本日期取 arXiv 首次提交（v1）日期，题名取 arXiv 当前版本的题名，因此可能与期刊版不同。例如 [arXiv:2510.22311](https://arxiv.org/abs/2510.22311) 的 v1 题名为 *Pauli Propagation: Simulating Quantum Spin Dynamics via Operator Complexity*，当前题名为 *Characterizing Pauli Propagation via Operator Complexity*。
- *Efficient construction of stabilizer codes via ZX-calculus*（Academia Quantum 3(2)，2026）与 *A ZX-Calculus Approach for the Construction of Graph Codes*（[arXiv:2304.08363](https://arxiv.org/abs/2304.08363)）作者和内容高度一致，但两边未明确相互登记；现各自独立列出，不标注对应关系。
- Communications Physics 条目暂不补造卷号或文章号。

共 24 项，不宣称这是个人总论文数。

## 字体

DM Sans 与 Libre Caslon Display 来自 [Google Fonts](https://github.com/google/fonts)，字体文件本地托管，许可证在 `licenses/` 下。网站不对用户提供的插画或 CV 作开源授权。

## Blog

三篇文章均为配合 `../video_promo/` 中三部短片撰写的稿件，提供完整英文版与逐节逐段对应的中文翻译。文章依据各片的旁白脚本和片中引用的文献写成，在旁白基础上补充了适用条件和结论边界；短片中无法独立核实的具体数字，文中改为定性描述或注明出自短片。所有 DOI 与 arXiv 编号均已于 2026-09-29 核对可解析，且指向所列论文。完整稿件保存在 `content/posts/`。

- 张量网络机器学习：面积律只在一维有能隙系统中被严格证明；互信息上界 log₂ D 针对 MPS 玻恩机；PEPS 的归一化一般只能近似缩并；生成模型的似然只说“接近”而非“超过”最好的深度模型。
- 张量网络与量子纠错：10.9% 与 18.9% 注明为码容量阈值（不含测量错误）；XZZX 码的 50% 为纯退相位极限；LDPC 译码只说张量网络能处理部分回路。
- 高温超导：声子机制的 Tc 上限写作经验预期而非严格上限；RVB、自旋涨落配对注明尚未证实或未获普遍接受；纯哈伯德模型不超导的结论限定在所研究的参数区；室温超导说法未经受住检验。

2026-09-29 之前的三篇旧稿已删除，可从 git 历史找回。
