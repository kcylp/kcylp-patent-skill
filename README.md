<div align="center">

# 中国专利.skill · kcylp 定制版

> 专利点挖掘与交底书（发明/实用/外观）编写，通俗解读专利，嗅探政策动向，辅助审查答复。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Node.js](https://img.shields.io/badge/Node.js-mermaid%2Fmmdc-339933.svg)](https://nodejs.org/)
[![AgentSkills](https://img.shields.io/badge/AgentSkills-Standard-green)](https://agentskills.io)

<br>

基于 **[handsomestWei/patent-disclosure-skill](https://github.com/handsomestWei/patent-disclosure-skill)** 深度定制。<br>
有设计文档和代码，但**专利点还没梳**？交底书要**框图 + 可改 Word**？<br>
定稿后还要**多轮补材料、纠错**并留下修改追溯？<br>
公开专利晦涩难懂，想**快速看懂权要与落地语境**？

[初衷](#初衷) · [运行效果](#运行效果) · [功能特性](#功能特性) · [定制增强](#定制增强) · [示例](#示例) · [安装说明](INSTALL.md) · [技能入口](SKILL.md)

</div>

---

## 初衷

### 专利交底书编写

> **做了多年核心研发，专利发明人那一栏从没写过我的名字。**

代码是自己敲的，方案是自己扛的，轮到交底书却卡在「专利点怎么挖、查新怎么写、框图和 Word 怎么一次交得出去」。本技能把这一环打通：覆盖发明 / 实用新型 / 外观设计，结构图与外观图都能读懂、写进交底；从项目材料梳出可申请的点，查新、脱敏、成文、迭代另存——让真正干活的人，也能把技术贡献写进可交付的交底书里。

### 专利通俗解读

> **不止一篇。**

公开专利常把阅读门槛抬得很高：权要绕、术语密、落地语境散落在说明书与附图里。本技能把单篇读成通俗笔记与图谱，并入库 Obsidian；依托双链、图谱、插件与 Bases 等生态，陆续解读的专利可以沉淀成**只属于自己的私有专利知识库**——权要、术语、线索与附图彼此勾连，越读越厚。再叠上 [Obsidian CLI](https://help.obsidian.md/cli) 与库内外连接能力，检索、批处理、和外部工具接力都更容易：从单篇通俗笔记，走向可检索、可关联、可继续生长的个人专利情报层，把沉睡在 PDF 里的技术细节重新点亮。库厚了之后，还能在这层之上做**专利比对、挖掘与分析**——同族对照、技术路线梳理、差异点扫描，把「读懂」推进到「用起来」。

---

## 运行效果

### 专利交底书编写

<table width="100%" border="1" cellpadding="12" cellspacing="0">
<tr>
<th width="50%" align="center">初版生成<br><sub>首次落盘交付</sub></th>
<th width="50%" align="center">迭代更新<br><sub>多版本并存 + 对话记录</sub></th>
</tr>
<tr>
<td width="50%" valign="top" align="center">
<img src="docs/效果例-初版生成.jpg" alt="初版生成：outputs 目录下的时间戳交底书、mermaid 图目录等" width="100%" />
</td>
<td width="50%" valign="top" align="center">
<img src="docs/效果例-迭代更新.jpg" alt="迭代更新：新时间戳文件与交底书修订对话记录" width="100%" />
</td>
</tr>
</table>

### 实用新型 / 外观 · 看图与出图

<table width="100%" border="1" cellpadding="12" cellspacing="0">
<tr>
<th width="33%" align="center">外观线稿<br><sub>从产品图自动提炼造型轮廓</sub></th>
<th width="33%" align="center">实用新型线稿<br><sub>从结构图自动生成轮廓与部件序号引出</sub></th>
<th width="34%" align="center">CAD 三维模型投影<br><sub>从工程模型自动提取等轴测等多视角</sub></th>
</tr>
<tr>
<td width="33%" valign="top" align="center">
<img src="docs/效果例-外观专利线稿.png" alt="外观辅助线稿：产品造型黑白线稿示意" width="100%" />
</td>
<td width="33%" valign="top" align="center">
<img src="docs/效果例-实用新型专利线稿含部件序号引出线.png" alt="实用新型辅助线稿：结构线稿与部件序号引出线" width="100%" />
</td>
<td width="34%" valign="top" align="center">
<img src="docs/效果例-cad提取等轴测投影图.png" alt="CAD 三维模型等轴测投影：从工程模型自动提取多视角示意" width="100%" />
</td>
</tr>
</table>

### 专利通俗解读

<table width="100%" border="1" cellpadding="12" cellspacing="0">
<tr>
<th width="50%" align="center">Obsidian 关系图<br><sub>知识图谱与多色节点</sub></th>
<th width="50%" align="center">解读 Canvas<br><sub>叙事故事线 · 术语 · 公开线索</sub></th>
</tr>
<tr>
<td width="50%" valign="top" align="center">
<img src="docs/效果例-obs图谱.jpg" alt="Obsidian 关系图：解读笔记、术语与 Canvas 知识图谱" width="100%" />
</td>
<td width="50%" valign="top" align="center">
<img src="docs/效果例-解读.jpg" alt="专利解读 Canvas：叙事、权要、术语与公开线索图谱" width="100%" />
</td>
</tr>
</table>

---

## 功能特性

### 专利交底书编写

支持 **发明**、**实用新型**、**外观设计** 三种专利类型（未指定时默认发明；材料偏结构/外观时可反问切换）。

<!-- 使用 HTML 表格：避免 GitHub 管道表把左列挤窄 -->
<table>
<colgroup>
<col width="1%">
<col>
</colgroup>
<thead>
<tr><th align="left" nowrap width="1%">能力</th><th align="left">说明</th></tr>
</thead>
<tbody>
<tr><td nowrap width="1%"><strong>专利类型</strong></td><td>发明 / 实用新型 / 外观设计<strong>分模板成文</strong>；实用与外观先填 Schema，再写 <code>figure_plan.yaml</code> 排序入文图（成文不扫全 assets 临场挑图）</td></tr>
<tr><td nowrap width="1%"><strong>项目扫描</strong></td><td>按优先级读文档 / 代码；<code>.docx</code> / <code>.pptx</code> 先转 Markdown 再扫；可选扫描 <code>.step</code>/<code>.stp</code> 与原生 CAD（<strong>默认不解析</strong>，遇 STEP 先反问再装依赖出多视图）（<code>project_scan.md</code>）</td></tr>
<tr><td nowrap width="1%"><strong>外观辅助线稿</strong></td><td>可选、默认关；用户确认后基于已有参考图生成描述与线稿草稿（禁止无图纯文生）；<strong>不</strong>画部件序号；默认不入正文（<code>design_lineart_assist.md</code>）</td></tr>
<tr><td nowrap width="1%"><strong>实用结构辅助线稿</strong></td><td>可选、默认关；用户确认后基于结构/参考图生成轮廓线稿，并按 <code>structure_schema.parts</code> 准备序号引出（推荐轮廓与序号分层 overlay，禁止自创件号）；默认不入正文（<code>structure_lineart_assist.md</code>）</td></tr>
<tr><td nowrap width="1%"><strong>专利点</strong></td><td>候选点讨论与融合（按类型：<code>invention|utility_model|design</code> 挖点文件）</td></tr>
<tr><td nowrap width="1%"><strong>查新</strong></td><td><strong>优先</strong> <a href="http://epub.cnipa.gov.cn/">国知局 · 中国专利公布公告</a>（<code>tools/crawl/cnipa_epub_search.py</code>，<code>--type</code> 对齐类型）；异常或无果时降级 WebSearch。著录写入第一章（<code>prior_art_search.md</code>）</td></tr>
<tr><td nowrap width="1%"><strong>交底书成稿</strong></td><td>脱敏模版；发明用 <strong>mermaid</strong> 框图；实用/外观按 <code>figure_plan</code> 嵌结构图或视图；定稿可出 <strong>.docx</strong></td></tr>
<tr><td nowrap width="1%"><strong>交付命名</strong></td><td><code>{案件名}_{YYYYMMDDHHmmss}.md</code> 与同名 <code>.docx</code>（<code>disclosure_builder.md</code> §7.3）</td></tr>
<tr><td nowrap width="1%"><strong>自检 / 迭代</strong></td><td>逻辑与公式自检（不写入正文）；合并 / 纠正另存新文件 + <code>交底书修订对话记录.md</code></td></tr>
</tbody>
</table>

怎么开口：自然语言即可（专利挖掘、交底书、查新等），或 `/交底书`、`/patent-disclosure-skill`；尽量带上**项目路径或技术主题**，并点明类型（未指定默认**发明**）。

| 类型 | 典型场景 | 触发示例 |
|------|----------|----------|
| **发明** | 方法 / 系统 / 算法流程 | 「按发明写交底」「项目路径 …」 |
| **实用新型** | 形状、构造、连接与装配 | 「实用新型」「一种…装置/结构」 |
| **外观设计** | 外形、图案、色彩或其结合 | 「外观设计」「设计说明 / 六视图」 |

已有交底上补材料或纠错时，按 `merger.md` / `correction_handler.md` 另存新稿（实用/外观改图或主题时同步 `figure_plan`）。细则见 [SKILL.md](SKILL.md)、`prompts/disclosure/intake.md`。

### 专利通俗解读

**强烈推荐安装 Obsidian**：索引、Canvas 知识图谱、术语网与 callout 配色依赖库内呈现，才能发挥本模式的完整体验。安装与可选社区插件见 [docs/obsidian-setup-guide.md](docs/obsidian-setup-guide.md)。

<table>
<colgroup>
<col width="1%">
<col>
</colgroup>
<thead>
<tr><th align="left" nowrap width="1%">能力</th><th align="left">说明</th></tr>
</thead>
<tbody>
<tr><td nowrap width="1%"><strong>取证解读</strong></td><td>全文 / PDF 抽取 → 权要树、术语表、特征—说明书—附图对照（<code>patent_plain_reader.md</code>）</td></tr>
<tr><td nowrap width="1%"><strong>叙述故事线</strong></td><td>一句话总览 + 连贯叙事：把权要与说明书「讲成人话」，降低首次通读成本</td></tr>
<tr><td nowrap width="1%"><strong>知识图谱</strong></td><td>单篇 <code>*_图谱.canvas</code>、多篇 <code>_专利关联.canvas</code>、术语双链与关系图配色；入库<strong>自动</strong>配置 CSS / Bases</td></tr>
<tr><td nowrap width="1%"><strong>公开线索辅助</strong></td><td>联网检索公开材料（≤3 条）；Agent 读 URL 写摘要；L1–L4 旁注与 <code>clues/</code> 落地，用行业语境辅助理解（<strong>非</strong>权要 / 说明书证据）</td></tr>
</tbody>
</table>

怎么开口：读专利、专利解读、`/读专利`、`/patent-read`，并给出**公开号或 PDF 路径**。配置库环境变量 `PATENT_READER_OBSIDIAN_VAULT` 体验更完整；无库时可降级到 `outputs/patent_reader/`。流程见 [tools/patent_reader/README.md](tools/patent_reader/README.md)、[SKILL.md](SKILL.md)。

### 政策感知与技能自进化

审查指南、智能审查口径一变，交底写法很容易「还按老习惯」。需要时可以说一声「技能进化 / 政策雷达 / 政策审查动向嗅探」：联网看看国知局等官网**近期政策与审查动向**，把观点和原文链接整理成**参考清单**（默认 `outputs/evolution/EVOL-*.md`；确认沉淀后再拷到 `docs/evolution/`），帮你判断技能该不该跟、怎么跟。也可 `/patent-evolve`、`/技能进化`。默认不开；你点头确认前，**不会**擅自改交底/解读流程。细则见 [SKILL.md](SKILL.md)「模式 C」与 `prompts/evolution/`。

### 审查答复辅助

审查意见一来，往往要翻旧案、对法条、想策略——经验散落在 PDF 和聊天记录里，很难复用。需要时可以说「审查答复 / 案例入库 / `/审查答复`」：**自动**完成「历史通知书与答复脱敏写入 Obsidian、打上法条/缺陷等标签以固化经验 → 对新通知书做标签过滤（向量模型可选；启用后叠加本地轻量向量相似度检索，相当于外挂一套属于自己的 RAG 知识库）→ 交大模型起草意见陈述」整条链路，提高召回精准度，让答复更贴你的历史口径，而不是凭空瞎编。向量可跳过，也可中途开启并重建索引；向量不可用时仍靠标签检索继续出草稿。默认不开；产出为草稿，须人审后再递交。细则见 [SKILL.md](SKILL.md)「模式 D」、[docs/oa/README.md](docs/oa/README.md)、[tools/oa/README.md](tools/oa/README.md)。

接入宿主、Python / Node、可选 STEP 等见 **[INSTALL.md](INSTALL.md)**。

---

## 示例

索引见 [examples/README.md](examples/README.md)。完整产物落在 **`outputs/`** 或 Obsidian 库。

<!-- 使用 HTML 表格：前两列 nowrap 防挤窄，后两列自动换行 -->
<table>
<colgroup>
<col width="1%">
<col width="1%">
<col>
<col>
</colgroup>
<thead>
<tr>
<th align="left" nowrap width="1%">示例</th>
<th align="left" nowrap width="1%">类型</th>
<th align="left">材料</th>
<th align="left">怎么开口</th>
</tr>
</thead>
<tbody>
<tr>
<td nowrap width="1%">批任务调度</td>
<td nowrap width="1%"><strong>发明</strong>交底</td>
<td><a href="examples/example_batch_job_scheduler/"><code>examples/example_batch_job_scheduler/</code></a>（扫 <code>knowledge/</code>）</td>
<td>「按发明写交底，项目路径 …/knowledge/」或 <code>/交底书</code></td>
</tr>
<tr>
<td nowrap width="1%">卡扣散热结构</td>
<td nowrap width="1%"><strong>实用新型</strong>交底</td>
<td><a href="examples/example_utility_model_snap_heatsink/"><code>examples/example_utility_model_snap_heatsink/</code></a></td>
<td>「实用新型交底，材料在 …/example_utility_model_snap_heatsink/」</td>
</tr>
<tr>
<td nowrap width="1%">折臂台灯</td>
<td nowrap width="1%"><strong>外观设计</strong>交底</td>
<td><a href="examples/example_design_desk_lamp/"><code>examples/example_design_desk_lamp/</code></a></td>
<td>「外观设计交底，材料在 …/example_design_desk_lamp/」</td>
</tr>
<tr>
<td nowrap width="1%">公开专利 PDF</td>
<td nowrap width="1%"><strong>通俗解读</strong></td>
<td><a href="examples/example_patent_reader/"><code>examples/example_patent_reader/</code></a>（PDF 本地自备）</td>
<td>「读专利」+ 公开号或 PDF；<code>/读专利</code>、<code>/patent-read</code></td>
</tr>
<tr>
<td nowrap width="1%">政策 / 审查动向</td>
<td nowrap width="1%"><strong>技能自进化</strong></td>
<td>无需本地样例（联网出清单 → <code>outputs/evolution/EVOL-*.md</code>）</td>
<td>「技能进化 / 政策雷达 / 政策审查动向嗅探：近 12 个月国知局动向，整理观点↔链接，先别改技能」；<code>/patent-evolve</code>、<code>/技能进化</code></td>
</tr>
<tr>
<td nowrap width="1%">审查答复样例</td>
<td nowrap width="1%"><strong>审查答复</strong></td>
<td><a href="examples/example_oa_response/"><code>examples/example_oa_response/</code></a>（2 历史案 + 1 待答复通知书）</td>
<td>「审查答复：先入库 <code>cases/</code>，再用 <code>pending/oa_notice_pending.md</code> 出草稿；向量可跳过」；<code>/审查答复</code>、<code>/oa</code></td>
</tr>
</tbody>
</table>

---

## 定制增强

本仓库基于 [handsomestWei/patent-disclosure-skill](https://github.com/handsomestWei/patent-disclosure-skill) (MIT) 深度定制，在原始版本基础上做了以下增强：

### 🚀 v1.0 定制内容（kcylp 版）

| 增强项 | 说明 |
|--------|------|
| **Obsidian 笔记模板** | 内置 `assets/obsidian/_专利解读索引.template.md`，首次入库自动配置 CSS、Bases、图谱配色 |
| **国知局优先查新** | `tools/crawl/cnipa_epub_search.py` 直连中国专利公布公告，支持 `--type` 按发明/实用/外观过滤 |
| **Mermaid → PNG → Word 全链路** | `mermaid_render.py` 一步完成公式渲染 + mermaid 生图 + Markdown 定稿 + Word 生成 |
| **LaTeX 公式 OMML 双轨** | 发明交底含公式时，优先 OMML（Word 可编辑公式），失败回退 PNG |
| **CAD/STEP 多视角提取** | 可选从 `.step` 工程文件自动提取等轴测/三视图 PNG，直接嵌入交底 |
| **辅助线稿生成** | 外观设计从产品图提炼造型轮廓；实用新型从结构图生成轮廓+部件序号引出 |
| **审查答复 RAG 案例库** | 向量+标签双轨检索历史答复案例，支持智谱/DashScope/MiniMax/OpenAI 向量模型 |
| **政策动向嗅探** | 联网扫国知局官网，出「观点↔信源 URL」清单，人工审核后才改技能 |
| **三专利类型独立模板** | 发明/实用新型/外观设计各有专属 builder + template，不混用 |
| **多轮迭代修订追溯** | 每轮修改自动追加 `交底书修订对话记录.md`，带时间戳+变更摘要 |

### 📊 原始版本 vs 定制版

| 能力 | 原始版 | 定制版 |
|------|--------|--------|
| 专利类型覆盖 | ✅ 发明/实用/外观 | ✅ 发明/实用/外观 + 独立模板 |
| 交底书成稿 | ✅ Markdown + mermaid | ✅ Markdown + mermaid + Word + OMML 公式 |
| 查新 | ✅ WebSearch 降级 | ✅ 国知局官方优先 + WebSearch 降级 |
| 通俗解读 | ✅ 权要树+术语表 | ✅ 权要树+术语表+Obsidian 知识图谱+Canvas |
| 辅助线稿 | ❌ | ✅ 外观轮廓+实用序号引出 |
| CAD/STEP | ❌ | ✅ 多视角 PNG 提取 |
| 审查答复 | ❌ | ✅ 向量 RAG 案例库 |
| 政策嗅探 | ❌ | ✅ 联网出清单，人审后才改技能 |
| Obsidian 集成 | 基础 | ✅ 自动配置 CSS/Bases/图谱配色/术语网 |
| 迭代追溯 | 无记录 | ✅ 修订对话记录（时间戳+摘要） |

---

## 致谢

本项目基于 [handsomestWei/patent-disclosure-skill](https://github.com/handsomestWei/patent-disclosure-skill) (MIT License) 定制开发。感谢原作者 [handsomestWei](https://github.com/handsomestWei/) 的出色工作。

---

## 参考文档

- [技能入口与 Agent 流程](SKILL.md)（交底 / 解读 / 进化 / 审查答复）
- [详细安装说明](INSTALL.md)
- [交底书：图示与转换 / 国知局工具](tools/README.md)
- [专利解读工具](tools/patent_reader/README.md)
- [审查答复 · 案例 RAG](tools/oa/README.md)
- [Obsidian 安装与可选社区插件（Windows）](docs/obsidian-setup-guide.md)
- [示例案件与原材料](examples/README.md)
- [交底书模版细则](prompts/disclosure/invention/template_reference.md)

---

<div align="center">

MIT License © [handsomestWei](https://github.com/handsomestWei/) · 定制版 © [kcylp](https://github.com/kcylp)

</div>
