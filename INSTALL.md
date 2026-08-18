# 安装说明

本技能遵循 [AgentSkills](https://agentskills.io) 常见布局：仓库根目录即技能根目录，内含 `SKILL.md`。

## Claude Code

在 **git 仓库根目录** 下安装：

```bash
mkdir -p .claude/skills
git clone <本仓库 URL> .claude/skills/patent-disclosure-skill
```

或使用本地路径复制到 `.claude/skills/patent-disclosure-skill`。

运行时环境通常会设置 **`CLAUDE_SKILL_DIR`** 指向该技能目录；`SKILL.md` 中的 `${CLAUDE_SKILL_DIR}/prompts/...` 即解析到此路径。

## Cursor

Cursor 支持 [Agent Skills](https://www.cursor.com/docs/context/skills) 约定：每个技能是一个**子文件夹**，内含根级 `SKILL.md`（`name` 字段须与文件夹名一致，本仓库为 `patent-disclosure-skill`）。可将**本仓库完整内容**（含 `prompts/`、`tools/` 等）放在下列位置之一，重启 Cursor 后在 **Settings → Rules** 中查看是否已被发现；亦可用 Agent 输入 `/` 后选择技能名。

### 用户主目录（全局，所有项目可用）

| 系统 | 推荐路径 |
|------|----------|
| Windows | `%USERPROFILE%\.cursor\skills\patent-disclosure-skill\`（即 `C:\Users\<用户名>\.cursor\skills\patent-disclosure-skill\`） |
| macOS / Linux | `~/.cursor/skills/patent-disclosure-skill/` |

示例（将仓库克隆到全局技能目录）：

```bash
mkdir -p ~/.cursor/skills
git clone <本仓库 URL> ~/.cursor/skills/patent-disclosure-skill
```

Windows（PowerShell）：

```powershell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.cursor\skills"
git clone <本仓库 URL> "$env:USERPROFILE\.cursor\skills\patent-disclosure-skill"
```

### 项目目录（仅当前仓库）

将本技能放在当前工作区下的：

`<项目根>/.cursor/skills/patent-disclosure-skill/`

（同样需包含完整仓库文件树，且 **`SKILL.md` 中 `name: patent-disclosure-skill` 与文件夹名一致**。）

### 与「仅打开文件夹」等价关系

若未使用上述 `skills/` 布局，也可**直接用 Cursor 打开本仓库根目录**作为工作区；此时将 **`CLAUDE_SKILL_DIR`** 理解为「包含 `SKILL.md` 的目录」。分步指令在：

- `prompts/disclosure/`（交底；含 `invention/`、`utility_model/`、`design/`）
- `prompts/reader/`（通俗解读）
- `prompts/shared/`（Structure / Appearance 填表）

与 `SKILL.md` 中的 **`${CLAUDE_SKILL_DIR}/prompts/...`** 同义。

Cursor 也会扫描 **`~/.claude/skills/`**、项目内 **`.claude/skills/`** 等路径；详见 Cursor 官方文档与当前版本设置项。

## 可选依赖

若仅使用交底书 Markdown 流程，不必安装 Python。

若需使用 **`tools/shared/md_to_docx.py`**（Markdown → Word）、**`tools/shared/docx_to_md.py`**（Word → Markdown + 图片）或 **`tools/shared/pptx_to_md.py`**（PPT → Markdown + 图片，供扫描）：

```bash
pip install -r requirements.txt
```

**发明**交底定稿须同时产出 **.md + .docx**，且将 **mermaid**（**3.2 系统框图**与 **3.4 流程图**）经 **`tools/shared/mermaid_render.py`** 转为 PNG 嵌入。**mermaid** 须 **Node.js**（`@mermaid-js/mermaid-cli` 要求 `^18.19 || >=20.0`，Node 20 / 24 已实测兼容）：在 **`tools/`** 执行 **`npm install`**（含 **`puppeteer`**）；若 **`mmdc`** 报找不到 Chrome，再执行 **`npx puppeteer browsers install chrome-headless-shell`**。详见 **`tools/README.md`**。

> **⚠️ 故障排除：`npm install` 报 `EBADENGINE ... chevrotain ... required node >=22`**
> 说明你在用 **v26.08.17 或更早** 的版本（旧 lockfile 锁死了 chevrotain 12，它要求 Node ≥22）。v26.08.18 已修复。升级步骤：
> 1. 重新下载本仓库 zip（或 `git pull`）拿到新版 `tools/package.json` + `tools/package-lock.json`
> 2. **删掉 `tools/node_modules` 整个文件夹**（不删则旧的 chevrotain 12 仍残留）：
>    ```powershell
>    rmdir /s /q tools\node_modules
>    ```
> 3. 重新安装：
>    ```powershell
>    cd tools
>    npm install
>    ```
> 装完可运行 `npx mmdc --version` 验证。

**实用新型 / 外观**定稿以各类型 `prompts/disclosure/utility_model|design/disclosure_builder.md` 为准：填表产出 `structure_schema`/`appearance_schema` + **`figure_plan.yaml`**，成文只嵌清单入文图（结构图或视图；docx 对实用建议、对外观可选）。

## 可选：STEP 多视角解析（默认关闭）

扫描发现 **`.step` / `.stp`** 时，Agent 会**先反问**是否开启；确认前**不安装**下列依赖。仅有 SolidWorks 等原生 CAD、无 STEP 时，只会提示导出中性格式。

```bash
pip install -r tools/shared/requirements-step.txt
python tools/shared/cad_scan.py -r knowledge --json
python tools/shared/step_to_views.py --check-deps
python tools/shared/step_to_views.py --enable-step-parse -i model.step -o outputs/{案件}/cad_views
```

与主 `requirements.txt` **独立**。细则见 `prompts/disclosure/project_scan.md`「CAD / STEP」、`tools/README.md`。

## 可选：外观辅助线稿（默认关闭）

有产品图的外观案件可反问是否开启；确认前不生成。流程见 `prompts/shared/design_lineart_assist.md`。

```bash
python tools/shared/design_lineart_gate.py --print-confirm
python tools/shared/design_lineart_gate.py --enable-design-lineart --case-dir outputs/{案件} --prepare-jobs
```

**禁止**无参考图纯文生图；产出为交底辅助草稿，非申报终稿。

## 可选：实用新型结构辅助线稿（默认关闭）

有结构图的实用新型案件可反问是否开启；确认前不生成。流程见 `prompts/shared/structure_lineart_assist.md`（件号对齐 StructureSchema；推荐轮廓与序号分层）。

```bash
python tools/shared/structure_lineart_gate.py --print-confirm
python tools/shared/structure_lineart_gate.py --enable-structure-lineart --case-dir outputs/{案件} --prepare-jobs
```

**禁止**无参考图纯文生图与自创件号；产出为交底辅助草稿，非申报终稿。

## 可选：国知局公布公告站抓取（Step 5 查新优先路径）

若需使用 **`tools/crawl/cnipa_epub_search.py`**（一步，推荐）或 **`tools/crawl/cnipa_epub_crawler.py`** / **`tools/crawl/cnipa_epub_parse.py`**（[epub.cnipa.gov.cn](http://epub.cnipa.gov.cn/)，见 `prompts/disclosure/prior_art_search.md`）：

```bash
pip install -r tools/crawl/requirements-cnipa.txt
python -m playwright install chromium
# 按类型（与 intake 一致）：invention | utility_model | design | all
python tools/crawl/cnipa_epub_search.py --type utility_model 卡扣
```

**Windows 终端中文**：`cnipa_epub_search.py` / `cnipa_epub_crawler.py` 已对 stdout/stderr 尝试 **UTF-8**（`reconfigure`）。若仍乱码，可在运行前执行 **`chcp 65001`**，或设置环境变量 **`PYTHONUTF8=1`**，以便复制 **`EPUB_HITS_JSON:`** 一行给 Agent 时不误判为失败。

与主流程 `requirements.txt` **独立**；未安装时 Step 5 仍可按该 prompt 降级为 **WebSearch**（如 Google 学术）。

## 可选：审查答复案例库（模式 D，默认关闭）

显式触发「审查答复 / 案例入库 / `/oa`」后使用。配置与向量库默认在操作系统**文档**目录：`{Documents}/patent-disclosure-skill/oa/`（`PATENT_OA_HOME` 可覆盖）。**推荐**智谱 `embedding-3`；亦支持 DashScope / MiniMax / 本地 / OpenAI（`config.py set --preset …`）。

```bash
pip install -r tools/oa/requirements-oa.txt
# 例：智谱
# 环境变量 ZHIPUAI_API_KEY=…
python tools/oa/config.py recommend
python tools/oa/config.py set --preset zhipu
# 其他：--preset dashscope|minimax|local|openai
python tools/oa/ingest_case.py -i path/to/case.md
python tools/oa/refresh_vault.py   # 刷新 oa 索引 / Bases / 关联 Canvas
python tools/oa/search_cases.py --query "创造性 区别特征" --defect inventiveness --top-k 5
```

Obsidian 案例落在 `{vault}/oa/cases/history/`（另有 `pending/`、`drafts/`）。与主依赖**独立**。细则见 `prompts/oa/`、`tools/oa/README.md`、[SKILL.md](SKILL.md) 模式 D。

## 强烈建议：专利通俗解读 + Obsidian 库

**强烈建议安装并配置 Obsidian**，才能完整体验索引、Canvas 知识图谱、术语网、关系图配色与公开线索旁注。无库时可降级到 `outputs/patent_reader/`，效果会弱一截。

对话开始前由 Agent 运行探测（也可手动）：

```bash
python tools/patent_reader/vault/check_obsidian_env.py
# 自动接受唯一/当前打开的库：
python tools/patent_reader/vault/check_obsidian_env.py --auto-accept
# 手动指定并持久化（+ Windows 用户环境变量）：
python tools/patent_reader/vault/check_obsidian_env.py --set "C:\Users\你\Documents\Obsidian Vault" --setx
```

亦可仅设会话变量：

```bash
# Windows PowerShell
$env:PATENT_READER_OBSIDIAN_VAULT = "D:\Obsidian\你的库"
# 可选：库内目录，默认 Research/Patents
$env:PATENT_READER_PAPERS_DIR = "Research/Patents"
$env:PATENT_READER_GLOSSARY_DIR = "Research/术语"
```

```bash
pip install -r tools/patent_reader/requirements.txt   # PDF：pymupdf
```

**首次使用**：解读**入库时会自动**初始化库（CSS、Bases、索引、关系图配色）。用户只需安装 Obsidian、配置库路径，并（可选）在社区插件市场安装 Dataview 等——步骤与插件清单见 **`docs/obsidian-setup-guide.md`**。交付后 Agent 按 **`prompts/reader/obsidian_plugin_guide.md`** 引导可选插件。

工具链分层见 **`tools/patent_reader/README.md`**（`shared/` · `extract/` · `analyze/` · `vault/`）。常用入口：

```bash
python tools/patent_reader/extract/fetch_patent_pdf.py --pub CN… -o tmp/patent_reader/RUN
python tools/patent_reader/vault/write_patent_obsidian_note.py --help
```
