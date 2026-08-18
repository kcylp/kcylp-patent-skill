# tools / 可选脚本

本目录按职责分子目录：

| 目录 | 内容 |
|------|------|
| **`crawl/`** | 国知局公布公告检索：`cnipa_epub_*.py`、`requirements-cnipa.txt` |
| **`shared/`** | 公用：`docx/pptx/md` 转换、`mermaid`/`math`/`math_to_omml`（OMML）、`formula_paradigms` / `check_formula_plan`、`iteration_dialog_log`、`patent_type.py`、**可选** STEP / 线稿门禁 |
| **`patent_reader/`** | 专利通俗解读：`shared/` · `extract/` · `analyze/` · `vault/`（见该目录 README） |
| **`oa/`** | 模式 D 审查答复：嵌入配置、sqlite-vec 入库/检索（见该目录 README） |

技能主流程以 `SKILL.md` 与 `prompts/` 为准。调用时请使用子目录完整路径（如 `tools/crawl/cnipa_epub_search.py`、`tools/shared/mermaid_render.py`）。

## 国知局公布公告检索（`crawl/`，Step 5 查新优先）

| 脚本 | 作用 |
|------|------|
| **`crawl/cnipa_epub_search.py`** | **（Step 5 优先）** 一步拉取+解析，不落盘；**`--type invention\|utility_model\|design\|all`** 对应首页四类勾选；Agent 分次一词并合并 JSON。 |
| **`crawl/cnipa_epub_crawler.py`** | 拉取并默认保存结果页 HTML；同样支持 `--type`。 |
| **`crawl/cnipa_epub_parse.py`** | 仅解析已保存 HTML。 |
| **`shared/patent_type.py`** | 类型别名、国知局 checkbox、Google Patents 查询提示；**`--pub` 按文献种类码推断类型**（解读 Schema 挂钩）。 |

依赖：`pip install -r tools/crawl/requirements-cnipa.txt` 与 `python -m playwright install chromium`。类型检索说明见 **`references/patent_type_search.yaml`**、**`prompts/disclosure/prior_art_search.md`**。

抓取失败时降级 **WebSearch**（Google 学术**无**专利类型过滤；Google Patents 支持 PATENT/DESIGN，实用新型靠关键词+国知局）。

---

## CAD / STEP（`shared/`，可选，默认关闭）

| 脚本 | 作用 |
|------|------|
| **`shared/cad_scan.py`** | 扫描 `.step`/`.stp` 与原生 CAD 后缀；输出 JSON（`ask_enable_step_parse` / `hint_export_step`）。**无重依赖**。 |
| **`shared/cad_formats.py`** | 后缀表与提示文案。 |
| **`shared/step_to_views.py`** | STEP → 多视角 PNG + `assembly_tree` / `figure_plan.seed` / `structure_schema.seed`。须 **`--enable-step-parse`**。 |
| **`shared/gen_demo_snap_step.py`** | 生成教学用 `demo_snap_plate.step`（无 CadQuery）。 |
| **`shared/requirements-step.txt`** | CadQuery + cairosvg；**仅用户确认后** `pip install`（建议 Py3.9–3.12）。 |

流程纪律见 **`prompts/disclosure/project_scan.md`**「CAD / STEP」：有 STEP 先反问；仅有原生 CAD 则对话末尾提示导出 STEP。

Windows 若无系统 Cairo，`cairosvg` 可能失败；`step_to_views` 会回退 **matplotlib 镶嵌投影** 出 PNG（仍写出 SVG）。建议 **Python 3.9–3.12** 隔离 venv 安装依赖（3.13 常无 CadQuery 轮子）。若全局 pip 配置了 `target` 指向共享目录，请对 venv 使用 `pip install --target <venv>/Lib/site-packages …`。

```bash
python tools/shared/cad_scan.py -r knowledge --json
pip install -r tools/shared/requirements-step.txt   # 用户确认后
python tools/shared/step_to_views.py --enable-step-parse -i a.step -o outputs/case/cad_views
```

---

## 发明公式范式（`shared/` + `references/formulas/`）

| 脚本 / 文档 | 作用 |
|-------------|------|
| **`references/formulas/paradigms.yaml`** | 默认可扩展范式库 |
| **`references/schemas/formula_plan.schema.yaml`** | 案件 `formula_plan.yaml` 合同 |
| **`shared/formula_paradigms.py`** | `list` / `show` / `combos`（支持案件目录覆盖） |
| **`shared/check_formula_plan.py`** | 校验选题 id、禁装饰音、数值例 |

```bash
python tools/shared/formula_paradigms.py list
python tools/shared/check_formula_plan.py -i outputs/case/formula_plan.yaml
```

成文纪律见 **`prompts/disclosure/invention/disclosure_builder.md` §7.7**。

## 外观辅助线稿（`shared/`，可选，默认关闭）

| 脚本 / 文档 | 作用 |
|-------------|------|
| **`prompts/shared/design_lineart_assist.md`** | Agent 流程：确认「是」→ 写 brief → 门禁 → **参考图**出线稿 |
| **`shared/design_lineart_gate.py`** | 默认关；无源图拒绝；`--prepare-jobs` 写出 `lineart_assist/design_lineart_jobs.json` |
| **`references/schemas/design_lineart_brief.schema.yaml`** | 描述合同 |

```bash
python tools/shared/design_lineart_gate.py --print-confirm
python tools/shared/design_lineart_gate.py --enable-design-lineart --case-dir outputs/case --prepare-jobs
```

**禁止**纯文生图；辅助线稿默认 `use_in_disclosure: false`。

## 实用新型结构辅助线稿（`shared/`，可选，默认关闭）

| 脚本 / 文档 | 作用 |
|-------------|------|
| **`prompts/shared/structure_lineart_assist.md`** | Agent 流程：确认「是」→ 写 brief → 门禁 → **参考图**出轮廓 → 按 Structure 叠件号 |
| **`shared/structure_lineart_gate.py`** | 默认关；无源图 / 无 Structure 拒绝；`--prepare-jobs` 写出 `lineart_assist/structure_lineart_jobs.json` |
| **`references/schemas/structure_lineart_brief.schema.yaml`** | 描述合同（与外观 `design_lineart_*` 分文件） |

```bash
python tools/shared/structure_lineart_gate.py --print-confirm
python tools/shared/structure_lineart_gate.py --enable-structure-lineart --case-dir outputs/case --prepare-jobs
```

**禁止**纯文生图与自创件号；推荐 `callout_mode: overlay`；辅助线稿默认 `use_in_disclosure: false`。

## Office / mermaid（`shared/`）

用 **`shared/docx_to_md.py`**、**`shared/pptx_to_md.py`**、**`shared/mermaid_render.py`** 等。

## mermaid_render.py — mermaid：图示 → PNG + 定稿 Markdown + **默认生成 Word**

将 fenced **mermaid**（`` ```mermaid`` ``）逐块交给 **`mmdc`** 渲染为 PNG；输出 `.md` 中**保留** mermaid 围栏源码，并追加 ``<!-- ![图示 n](mermaid_figures/…) -->`` 供 **`md_to_docx.py`** 嵌入 Word（Word **仅**嵌 PNG，不写 mermaid 代码块）。**3.2 系统框图**与 **3.4 流程图**均用 mermaid（`flowchart` / `subgraph` 等），交底书正文**不再**要求单独的文字框图或 PlantUML。

**生图失败降级**：某一围栏 `mmdc` 失败时**不中断**——该处**保留**原 `` ```mermaid`` … `` ``` `` 源码；其余块照常出图。仍写出定稿 `.md`，并**照常尝试**生成 Word（未出图块在 Word 中为 **Consolas 代码块**，与 `md_to_docx` 行为一致）。

### 依赖：mermaid（须 Node.js + `mmdc`）

| 方式 | 安装 | 说明 |
|------|------|------|
| **本地 npm（推荐）** | **Node.js** + 本目录 `npm install`（见 `package.json`） | 优先使用 `tools/node_modules/.bin/mmdc`，避免每次 npx 拉包 |
| **npx** | 未执行 `npm install` 时由脚本调用 `npx -y @mermaid-js/mermaid-cli mmdc` | 首次可能较慢 |
| **全局 npm** | `npm install -g @mermaid-js/mermaid-cli` | 提供 **PATH** 上的 `mmdc` |

mermaid 脚本按顺序查找：`tools/node_modules/.bin/mmdc` → **PATH** 上的 `mmdc` → `npx`。

生成 Word 仍需：`pip install -r requirements.txt`（与上表无关）。

**npm 推荐（本地 CLI）**：

```bash
cd tools
npm install
```

`package.json` 已包含 **`puppeteer`**（`@mermaid-js/mermaid-cli` 的 peer）。**Puppeteer 23+** 可能不会在 `npm install` 时自动下载浏览器；若自检或 `mmdc` 报错 **Could not find Chrome**，在 **`tools/`** 再执行：

```bash
npx puppeteer browsers install chrome-headless-shell
```

> **⚠️ Node 20 下 `npm install` 报 `EBADENGINE ... chevrotain ... required node >=22`？**
> 你在用 v26.08.17 或更早的版本（旧 lockfile 锁死了要求 Node ≥22 的 chevrotain 12），v26.08.18 已修复。升级：**更新仓库 → 删掉 `tools/node_modules` → 重新 `npm install`**（不删 node_modules 旧包会残留）：
>
> ```powershell
> rmdir /s /q tools\node_modules
> cd tools
> npm install
> npx mmdc --version   # 验证
> ```

（或按报错提示选用 `chrome` 等；详见 [Puppeteer 文档](https://pptr.dev/)。）

### mermaid CLI 与手动试转

**`mermaid_render.py` 与 11.x 一致**：在 **`mmdc -i <.mmd> -o <.png> -b white`** 基础上默认追加 **`-s 2 -w 1400 -H 1050`**（更高像素密度与视口，系统框图在 Word 中更清晰）。需要再锐化可 **`--mmdc-scale 3`**（PNG 更大）；恢复接近旧版可 **`--mmdc-scale 1 --mmdc-width 800 --mmdc-height 600`**。  
若某处写的是 `npx -y @mermaid-js/mermaid-cli -i …`，**少了子命令 `mmdc`**，参数会错位；正确示例：

```bash
npx -y @mermaid-js/mermaid-cli mmdc -i sample.mmd -o sample.png -b white
```

可自建极简 `sample.mmd`（如一行 `flowchart LR; A-->B`）试转；能出 PNG 则说明 **mmdc + Chrome** 正常，否则按上文安装 **`puppeteer` 浏览器**。

### 用法

```bash
# 写出定稿 .md，并在同目录生成同名 .docx（默认）；-o 须为「案件名_YYYYMMDDHHmmss.md」（见 prompts/disclosure/invention/disclosure_builder.md §7.3 第 5 点）
python tools/shared/mermaid_render.py -i draft.md -o "一种XXX方法及系统_20260408143025.md"

# 指定 .docx 路径（.md 主名仍须含时间戳）
python tools/shared/mermaid_render.py -i draft.md -o out/一种XXX方法及系统_20260408143025.md --docx out/一种XXX方法及系统_20260408143025.docx

# 仅 Markdown，不要 Word
python tools/shared/mermaid_render.py -i draft.md -o "一种XXX方法及系统_20260408143025.md" --no-docx

# 更高清晰度（可选）
python tools/shared/mermaid_render.py -i draft.md -o "…定稿.md" --mmdc-scale 3 --mmdc-width 1600 --mmdc-height 1200

# 指定 mermaid 图片子目录（相对输出 .md）
python tools/shared/mermaid_render.py -i draft.md -o out/一种XXX方法及系统_20260408143025.md --assets-dir figures/mermaid
```

**Word 生成失败**（缺依赖、版式报错等）时：脚本仍以退出码 **0** 结束（Markdown 已成功）；stderr 会打印 **`md_to_docx.py` 的手动命令**，请复制执行。

Windows 上若仅装 Node 未执行 `npm install`，脚本会通过 `npx -y @mermaid-js/mermaid-cli mmdc` 调用（首次可能较慢）。

### 与交底书约定

- 技能要求定稿**同时**交付 **Markdown + Word**，且 **`-o` 主文件名须含 `_{YYYYMMDDHHmmss}`**（`prompts/disclosure/invention/disclosure_builder.md` §7.3 第 5 点，含首次定稿）；**3.2 系统框图**与 **3.4 流程图**均用 fenced mermaid，**不要** ASCII 文字流程图或框图。
- 交付代理人前：运行 `mermaid_render.py` 一步即可（默认再调 `md_to_docx.py`）；若 Word 失败，按 stderr 提示手动执行 `md_to_docx.py`。

---

## math_to_omml.py — LaTeX → 可编辑 Office Math

``latex2mathml`` → MathML → Word ``m:oMath`` / ``m:oMathPara``。不依赖本机 TeX。由 **`md_to_docx.py`** 默认调用。

```bash
pip install latex2mathml   # 已写入根目录 requirements.txt
```

---

## math_render.py — LaTeX 公式 → PNG（OMML 回退）

将 Markdown 中的 **LaTeX 公式**用 **matplotlib mathtext** 渲染为 PNG；**保留 LaTeX 原文**，图片引用写入 HTML 注释，供 **`md_to_docx.py`** 在 **OMML 失败时**嵌入。

**Mermaid 框图**：``mermaid_render.py`` **保留** `` ```mermaid`` 源码，并追加 ``<!-- ![图示 n](mermaid_figures/...) -->``。

**mathtext 兼容**：``\ge``→``\geq`` 等；``\tag{1}`` 转式末 ``(1)``。

**Word 主路径**：默认 **OMML 优先**；PNG 仅回退。``--no-omml`` 可强制旧行为。

### 依赖

```bash
pip install -r requirements.txt   # 含 matplotlib
```

### 用法

```bash
python tools/shared/math_render.py -i draft.md -o draft_with_math.md
python tools/shared/math_render.py -i draft.md -o out.md --assets-dir math_figures
```

定稿流水线：**``mermaid_render.py`` 默认先跑公式再跑 mermaid**（可用 ``--no-math`` 跳过）。单独转 Word 时 **`md_to_docx.py` 也会自动尝试公式渲染**（``--no-math-render`` 可关闭）。

---

## md_to_docx.py — Markdown → Word

将交底书 Markdown 转为 `.docx`，**`#`–`######` 映射为 Word 内置「标题 1」–「标题 9」**，正文为宋体 10.5pt，代码块为 Consolas，便于交给代理人或所内用 Word 修订。

**图示**：定稿应用 **`mermaid_render.py`** 将 mermaid 转为 PNG；若个别块生图失败被降级保留围栏，本脚本会将**仍存在的** `` ```mermaid`` 块按**代码块**写入 Word。本脚本不调用 `mmdc`。

### 依赖

```bash
pip install -r requirements.txt
```

依赖为 `python-docx` + 可选 `latex2mathml`（见仓库根目录 `requirements.txt`）。缺 `latex2mathml` 时自动回退 PNG/原文。

### 用法

```bash
python tools/shared/md_to_docx.py --input path/to/交底书.md --output path/to/交底书.docx
python tools/shared/md_to_docx.py -i a.md -o a.docx --no-omml   # 仅 PNG/原文
```

图片 `![](相对路径.png)`：默认相对 **Markdown 文件所在目录**；也可指定根目录：

```bash
python tools/shared/md_to_docx.py -i ./outputs/case/disclosure.md -o ./outputs/case/disclosure.docx --base-dir ./outputs/case
```

**插图**：对 PNG/GIF/JPEG 会读取像素尺寸，在默认 **最大宽 5.5" × 最大高 8.2"** 内**等比缩放**并同时指定 `width`/`height`，避免竖长流程图仅按宽度放大后**高度超出版心**、打印或阅读时像被裁切。可按纸张边距调整，例如：

```bash
python tools/shared/md_to_docx.py -i a.md -o a.docx --image-max-width-inches 6 --image-max-height-inches 9
```

在 Claude Code 中可将 `tools` 换为 `${CLAUDE_SKILL_DIR}/tools`。

### 支持的 Markdown 子集

| 元素 | 行为 |
|------|------|
| `#`–`######` | Word 标题 1–9 |
| 段落 | 宋体正文，支持 `**粗体**`、`` `行内代码` ``；**相邻非空行（中间无空行）各自成段**，「（1）…（2）…」会分行显示 |
| `-` / `*` 列表 | 项目符号列表 |
| `1.` 列表 | 编号列表 |
| ` ``` ` 围栏 | 等宽代码块 |
| `\| 表格 \|` | 简单表格（Table Grid）；单元格内 ``\\(...\\)``、``$...$``、``<!-- -->`` 及 ``\\|`` 中的 ``|`` **不会**被当作列分隔符 |
| `> ` | 左缩进引用 |
| `---` 等 | 浅色分隔线 |
| `![](path)` | 嵌入图片（路径需存在；默认宽/高上限内等比缩放；公式图与正文混排） |
| `$` / `\\(...\\)` / `$$` / `\\[...\\]` LaTeX | **优先 OMML（可编辑公式）** → 失败则 **PNG** → 再失败则 **原文**；``--no-omml`` 跳过 OMML |

**未完整支持**：复杂嵌套列表、HTML 块、**未预渲染的** mermaid 围栏（仍为代码块）、脚注、任务列表等。定稿前请运行 **`mermaid_render.py`**；若仅用外部工具导出 PNG，可直接写 `![](...)`。

### 版式说明（md_to_docx）

- 不同语言 Word 中「标题 1」显示名可能为「Heading 1」或「标题 1」，样式仍为大纲级别标题，可用导航窗格与目录域。
- 若需所内固定模版（页眉、首页不同），可在本脚本生成后套用单位 `.dotx`，或后续扩展 `python-docx` 打开模版再写入。

---

## iteration_dialog_log.py — 修订对话记录（迭代用）

每轮 **`prompts/disclosure/merger.md` / `correction_handler.md`** 交付后，在**案件目录**追加一条 **`交底书修订对话记录.md`**：含**本地时间与 UTC**、用户说明摘要、本轮交付文件名、合并/纠正摘要摘录。规则见 **`prompts/disclosure/iteration_context.md`**。

**依赖**：仅标准库。

```bash
python tools/shared/iteration_dialog_log.py --case-dir outputs/某案件 --kind merge \
  --user "补充了调度装置资料，合并进第三章" \
  --summary "已扩写 3.4，并更新实施例；未改保护点表述。" \
  --artifacts "一种XXX方法及系统_20260408143025.md,一种XXX方法及系统_20260408143025.docx"
```

- `--kind`：`merge` 或 `correct`。  
- `--log-name`：可选，默认 `交底书修订对话记录.md`；英文环境可改用 `disclosure_revision_log.md`。  
- 无法执行脚本时，由 Agent 按同结构手工追加。

---

## docx_to_md.py — Word → Markdown + 抽取图片

将 **.docx**（Word / WPS 等另存为 docx）转为 **Markdown**，并把文档内嵌图片落到磁盘，便于 **`Read` 与 Step 2 扫描**（与直接读二进制 .docx 相比更稳）。**Step 2** 对扫描树内**每一个** `.docx` 都应先转换再读产出 `.md`，见 `prompts/disclosure/project_scan.md`。

### 依赖

与 `md_to_docx` 共用根目录 `requirements.txt`（`python-docx` + **`mammoth`**）。

```bash
pip install -r requirements.txt
```

### 用法

```bash
python tools/shared/docx_to_md.py --input path/to/设计说明.docx --output outputs/case/design.md
```

- 默认图片目录：`outputs/case/design_media/`，Markdown 内为相对路径 `![](design_media/img_0001.png)`。
- 自定义图片目录：

```bash
python tools/shared/docx_to_md.py -i ./raw/spec.docx -o ./knowledge/spec.md --media-dir ./knowledge/spec_assets
```

转换警告（如部分样式、WMF 图）会输出到 **stderr**，仍可能生成可用 `.md`。

### 局限（mammoth）

- 仅 **`.docx`**（OOXML）；老版 **`.doc`** 不支持。
- **Markdown 输出在 mammoth 侧标记为 deprecated**，复杂排版可能弱于「先导出 HTML 再转 MD」；专利扫描一般足够。若版式崩坏，建议所内 **另存为 PDF 或纯文本** 再扫。
- **WMF/EMF** 等 Windows 图元可能需单独处理（见 [mammoth WMF 配方](https://github.com/mwilliamson/python-mammoth)）。

在 Claude Code 中可将 `tools` 换为 `${CLAUDE_SKILL_DIR}/tools`。

---

## pptx_to_md.py — PowerPoint → Markdown + 抽取图片

将 **.pptx** / **.ppsx** 按**幻灯片页**导出为 Markdown，并抽取幻灯片中的**嵌入位图**（`PICTURE` 形状），便于 **`Read` 与 Step 2 扫描**。**Step 2** 对扫描树内**每一个** `.pptx` 均应先转换再读 `.md`，见 `prompts/disclosure/project_scan.md`。

### 依赖

根目录 `requirements.txt` 中的 **`python-pptx`**。

```bash
pip install -r requirements.txt
```

### 用法

```bash
python tools/shared/pptx_to_md.py --input path/to/评审材料.pptx --output outputs/case/review.md
```

- 默认图片目录：`outputs/case/review_media/`，文件名形如 `slide03_img0001.png`。
- 自定义图片目录：

```bash
python tools/shared/pptx_to_md.py -i ./raw/deck.pptx -o ./knowledge/deck.md --media-dir ./knowledge/deck_media
```

每页输出二级标题 `## 第 N 页`，其后为该页形状中的**文本与表格**（简化为管道表）及图片引用；若存在**演讲者备注**，以「**备注**」小节附于该页末尾。

### 局限（python-pptx）

- 仅 **`.pptx` / `.ppsx`**（OOXML）；**`.ppt`** 不支持，请先另存。
- **图表、SmartArt、嵌入 OLE** 等若未以普通图片形状存在，**不会**自动栅格化为 PNG；可先在 PowerPoint 中另存为图片或导出 PDF 作补充材料。
- 文本按形状遍历顺序输出，与视觉阅读顺序可能略有差异。

在 Claude Code 中可将 `tools` 换为 `${CLAUDE_SKILL_DIR}/tools`。

---

## 专利通俗解读（阅读模式）

脚本与说明见 **[`patent_reader/README.md`](patent_reader/README.md)**。

```bash
pip install -r tools/patent_reader/requirements.txt

# 发明/实用新型全文 PDF
python tools/patent_reader/extract/fetch_patent_pdf.py --pub CN… -o RUN

# 外观设计视图（常无 PDF CDN；需 Playwright，同国知局爬虫依赖）
pip install -r tools/crawl/requirements-cnipa.txt && python -m playwright install chromium
python tools/patent_reader/extract/fetch_design_views.py --pub CN…S -o RUN
```

---

## 审查答复案例库（`oa/`，可选，默认关闭）

| 脚本 | 作用 |
|------|------|
| **`oa/config.py`** | `recommend` / `skip-vector` / `enable-vector` / `status` / `set` |
| **`oa/pdf_text.py`** | 审查通知书/答复 PDF→文本（pymupdf） |
| **`oa/ingest_case.py`** | 脱敏入库；无向量亦可；支持 `--pdf` |
| **`oa/search_cases.py`** | 标签检索 + 可选向量；失败回退；支持 `--pdf` |
| **`oa/rebuild_vectors.py`** | 用户确认后扫描 oa/cases 重建向量 |

依赖：`pip install -r tools/oa/requirements-oa.txt`。说明见 **`tools/oa/README.md`**、**`docs/oa/README.md`**。

---

## 扩展其它脚本时

- Word / PPT 转换依赖写在 `requirements.txt`。
- 在 `SKILL.md`「工具与数据来源」表中增加一行调用说明。
- 勿将密钥写入仓库；配置使用环境变量或用户主目录。
