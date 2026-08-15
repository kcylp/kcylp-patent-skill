# 外观辅助线稿（可选，默认关闭）

**合同**：`references/schemas/design_lineart_brief.schema.yaml`  
**前置**：已有或本轮将写出的 `appearance_schema.yaml` + `figure_plan.yaml`（见 `fill_appearance_schema.md`）  
**性质**：交底**辅助**插图；**非**申报终稿；**禁止**无参考图纯文生图。

## 开关

- **默认关闭**。未询问或用户未答 **是** 前：不得写 `design_lineart_brief.yaml`，不得调用任何出图工具生成线稿。  
- 外观案件在填表/成文前可**一句反问**：是否开启外观辅助线稿？（请回 **是** / **否**）  
- 用户回 **否** 或跳过：仅用实拍/已有视图走 Appearance + figure_plan。  
- 用户回 **是**：再执行下文；可用环境变量 `PATENT_SKILL_DESIGN_LINEART=1` 或校验脚本 `--enable-design-lineart` 标记本轮已授权。

## 何时触发反问

- 专利类型 = **外观设计**，且扫描/材料中已有至少一张产品相关图（`figure_plan` 候选或 `assets` 实拍/效果图）。  
- **无任何图片**：不要反问「开启线稿」来绕过缺图；应要求补图。无图则**禁止**本辅助流程。

## 确认「是」后的步骤

### 1. 读 YAML，联读多视

1. **`Read`** `appearance_schema.yaml`（或 json）与 `figure_plan.yaml`。  
2. 按 `figure_plan.relates_to`（`same_state` / `alternate_view` / `detail_of`）联读多图；件名/造型特征跨图一致。  
3. **`Write`** `design_lineart_brief.yaml`：  
   - `overall_shape` / `design_points` / `uncertain` 对齐 AppearanceSchema  
   - 每个 `views[]`：**至少**填一个存在的 `source_paths`（来自 figure_plan.path 或 schema `views[].source_image` / `source_images`）  
   - `source_figs` / `relates_hint` 抄自 figure_plan  
   - `gen_prompt` 必须写明：黑白专利风格线稿、无彩色无棚拍阴影、不发明未见结构、保留可见轮廓与开口/倒角等要点、**以参考图为准**

### 2. 门禁校验（推荐）

```bash
python ${CLAUDE_SKILL_DIR}/tools/shared/design_lineart_gate.py --enable-design-lineart \
  --case-dir "outputs/{案件标识}" --prepare-jobs
```

- 无 `--enable-design-lineart`（且无环境变量）→ 拒绝。  
- 任一条 `views` 无有效图片路径 → 拒绝（**禁止纯文生图**）。  
- 成功则写出 `lineart_assist/design_lineart_jobs.json`（每条含 reference 路径与提示词）。

### 3. 基于参考图出线稿

对 `design_lineart_jobs.json` 中每一 job：

1. 使用**当前宿主环境**提供的图像生成能力完成出图（名称因客户端而异：可能是内置生图工具、图生图 API、本地模型或插件等）。**不要**写死某一产品的工具名。  
2. **硬性要求**：必须以该 job 的 `source_paths`（jobs 里亦作参考图列表）作为**视觉参考/条件输入**再生成；等价于「有参考图的图生图 / 图像条件生成」。  
3. **禁止**在未附带任何参考图的情况下，仅用 `gen_prompt` 做纯文生图。  
4. 提示词以 job 的 `gen_prompt` + brief 中 `design_points` 为准；多视 job 须同时参考 `relates_hint` 所涉源图，保持同一产品。  
5. 输出写到 job 的 `output_path`（默认 `lineart_assist/*.png`）。若宿主工具不能指定落盘路径，生成后须把结果**复制/保存**到该路径，再回写 figure_plan。

### 4. 回写 figure_plan

每张辅助线稿追加一条（**默认不入正文**）：

```yaml
- fig: null                    # 或分配序号但不入文
  role: reference              # 或与源图同 role
  path: lineart_assist/….png
  covers: ["立体图"]           # 对齐 view_name
  kind: lineart
  score: 50
  use_in_disclosure: false
  reason: AI 辅助线稿（非申报终稿）
  relates_to:
    - fig: 1                   # 源实拍/参考图 fig
      relation: same_state
      note: 由图1辅助生成的线稿草稿
```

仅当用户明确要求「辅助线稿也写入交底」时，才将对应条 `use_in_disclosure: true` 并分配连续 `fig`。

### 5. 成文纪律

- 正文视图说明以**实拍/原始参考图**为主；辅助线稿可一句带过「另附线稿草稿供代理人参考」。  
- **禁止**把 AI 线稿写成「已按国知局规范绘制的正式视图」。  
- `uncertain` 中的特征不得在线稿说明里写成既定设计要点。

## 自检（内部）

- [ ] 本轮确有用户 **是**（或等价授权）  
- [ ] `design_lineart_brief.yaml` 每视均有真实存在的 `source_paths`  
- [ ] 未做纯文生图  
- [ ] 多视参照了 `relates_to` / `relates_hint`  
- [ ] figure_plan 中辅助线稿默认 `use_in_disclosure: false`  
- [ ] **排版硬标准**：线稿为黑白（黑线白底）、SVG 最高清晰度、放大不失真、线条粗细适中（主线 0.5–1.0pt）、标注清晰可读  
- [ ] **图号对应**：线稿中所有标注数字与正文引用、figure_plan 编号一一对应  
- [ ] **无重叠挤压**：线稿各视图独立排版、间距充足、不重叠  
