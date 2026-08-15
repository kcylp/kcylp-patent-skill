# 实用新型结构辅助线稿（可选，默认关闭）

**合同**：`references/schemas/structure_lineart_brief.schema.yaml`  
**前置**：已有或本轮将写出的 `structure_schema.yaml` + `figure_plan.yaml`（见 `fill_structure_schema.md`）  
**性质**：交底**辅助**插图；**非**申报终稿；**禁止**无参考图纯文生图。  
**与外观分流**：外观用 `design_lineart_assist.md`；**禁止**用本流程处理外观，也禁止用外观流程给实用新型乱加「美感线稿无件号」当结构图。

## 开关

- **默认关闭**。未询问或用户未答 **是** 前：不得写 `structure_lineart_brief.yaml`，不得调用出图工具生成结构线稿。  
- 实用新型案件在填表/成文前，若已有结构相关图且缺干净线稿/CAD，可**一句反问**：是否开启实用新型结构辅助线稿？（请回 **是** / **否**）  
- 用户回 **否** 或跳过：仅用已有线稿/CAD/实拍走 Structure + figure_plan。  
- 用户回 **是**：再执行下文；可用环境变量 `PATENT_SKILL_STRUCTURE_LINEART=1` 或 `--enable-structure-lineart` 标记本轮已授权。

## 何时触发反问

- 专利类型 = **实用新型**，且材料中已有至少一张结构相关图（`figure_plan` 候选或 assets 实拍/结构图）。  
- **无任何图片**：不要反问「开启线稿」来绕过缺图；应要求补图或开启 STEP（若有）。无图则**禁止**本辅助流程。  
- 若已有清晰 `kind: lineart`/`cad` 入文图：可不反问；用户主动要求时再开。

## 确认「是」后的步骤

### 1. 读 YAML，联读多视 + 统一件号

1. **`Read`** `structure_schema.yaml`（或 json）与 `figure_plan.yaml`。  
2. 按 `figure_plan.relates_to` 联读总装/局部；**跨图同一 `parts.id`**。  
3. **`Write`** `structure_lineart_brief.yaml`：  
   - `structure_summary` / `parts_legend` 对齐 StructureSchema（`id`+`name` 不得改号）  
   - `callout_mode` 默认 **`overlay`**（轮廓与序号分层）  
   - 每个 `views[]`：至少填一个存在的 `source_paths`；`visible_part_ids` 为本视可见件  
   - `gen_prompt`：黑白结构线稿、无彩色无棚拍阴影、不发明未见结构；**默认不要**在提示里让模型自由编造序号（留给 overlay）  
   - `uncertain` 中的件不得列入本视必标序号

### 2. 门禁校验（推荐）

```bash
python ${CLAUDE_SKILL_DIR}/tools/shared/structure_lineart_gate.py --enable-structure-lineart \
  --case-dir "outputs/{案件标识}" --prepare-jobs
```

- 无授权旗标 → 拒绝。  
- 缺少 Structure / 无有效源图 / `visible_part_ids` 不在 `parts` → 拒绝。  
- 成功则写出 `lineart_assist/structure_lineart_jobs.json`。

### 3. 基于参考图出线稿（两层）

对 jobs 中每一 job：

1. **轮廓层**：以 `source_paths` / `reference_images` 为视觉参考生成线稿，写入 `output_path`。**禁止**纯文生图。  
2. **序号层**（`callout_mode: overlay`，推荐）：  
   - 使用 job 内 `callouts`（`id`+`name`）在轮廓图上叠加引出线与件号；  
   - 优先宿主标注 / 图层 / SVG / 人工核对，**不要**依赖模型一次性「猜位置猜编号」；  
   - 叠号结果写入 `callout_output_path`（若无则 `{stem}_callouts.png`）。  
3. **`in_prompt` 降级**：仅当无法叠图时，才在带参考图的条件下把「可见件号列表」写入提示；生成后必须对照 `parts_legend` 人工/自检，错号则重做或改 overlay。  
4. **`contour_only`**：只出无号轮廓；正文用部件表说明。

### 4. 回写 figure_plan

每张辅助线稿追加一条（**默认不入正文**）：

```yaml
- fig: null
  role: assembly          # 或 detail
  path: lineart_assist/….png   # 优先带 callouts 的路径（若已叠号）
  covers: ["1", "2", "总装"]
  kind: lineart
  score: 55
  use_in_disclosure: false
  reason: AI 辅助结构线稿（非申报终稿；件号对齐 StructureSchema）
  relates_to:
    - fig: 1
      relation: same_state
      note: 由图1辅助生成的结构线稿草稿
```

仅当用户明确要求「辅助线稿也写入交底」时，才 `use_in_disclosure: true` 并分配连续 `fig`。  
有总装+局部辅助对时，补写 `relates_to: detail_of`。

### 5. 成文纪律

- 正文附图说明以**原始结构图/CAD/已有线稿**为主；辅助线稿可一句「另附 AI 结构线稿草稿（件号对齐部件表）」。  
- **禁止**写成「已按国知局规范绘制的正式附图」。  
- 第三章部件表件号须与图上序号、`structure_schema.parts` 一致。

## 自检（内部）

- [ ] 本轮确有用户 **是**（或等价授权）  
- [ ] brief 每视均有真实 `source_paths`；未纯文生图  
- [ ] `parts_legend` / 图上件号与 StructureSchema 一致；跨图未改号  
- [ ] `uncertain` 件未画死序号  
- [ ] 优先 overlay；figure_plan 辅助条默认 `use_in_disclosure: false`  
- [ ] 未误用 `design_lineart_*`  
- [ ] **排版硬标准**：线稿为黑白（黑线白底）、SVG 最高清晰度、放大不失真、线条粗细适中（主线 0.5–1.0pt）、标注清晰可读  
- [ ] **图号对应**：所有部件序号与 `structure_schema.parts` 的 id 完全一致；跨图同一部件序号不改  
- [ ] **无重叠挤压**：各视图独立排版、间距充足、不重叠  
