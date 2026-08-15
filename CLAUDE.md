# 中国专利.skill · kcylp 定制版

基于 [handsomestWei/patent-disclosure-skill](https://github.com/handsomestWei/patent-disclosure-skill) (MIT) 深度定制。

## 快速开始

```bash
# 克隆到 Claude Code 技能目录
mkdir -p .claude/skills
git clone https://github.com/kcylp/patent-disclosure-skill.git .claude/skills/patent-disclosure-skill

# 安装 Python 依赖
pip install -r .claude/skills/patent-disclosure-skill/requirements.txt

# 安装 mermaid（用于框图渲染）
cd .claude/skills/patent-disclosure-skill/tools && npm install
```

## 触发方式

| 说 | 效果 |
|---|---|
| `专利挖掘` / `交底书` / `/交底书` | 启动交底书编写流程（发明/实用新型/外观设计） |
| `读专利` / `/读专利` + 公开号/PDF | 通俗解读专利，入库 Obsidian |
| `技能进化` / `政策雷达` / `/patent-evolve` | 联网嗅探国知局政策动向 |
| `审查答复` / `/oa` / `/审查答复` | 审查答复辅助（案例 RAG） |

## 四大模式

- **模式 A · 交底书编写** — 专利点挖掘 → 查新 → 成稿 → 迭代
- **模式 B · 专利通俗解读** — 全文/PDF → 通俗笔记 + Obsidian 知识图谱
- **模式 C · 技能进化旁路** — 政策动向嗅探（默认关，显式触发）
- **模式 D · 审查答复辅助** — 案例脱敏入库 → 标签+向量检索 → 答复草稿

## 详细文档

- [SKILL.md](SKILL.md) — 技能入口与 Agent 流程
- [INSTALL.md](INSTALL.md) — 完整安装说明
- [tools/README.md](tools/README.md) — 工具脚本详解
- [docs/obsidian-setup-guide.md](docs/obsidian-setup-guide.md) — Obsidian 库配置

## License

MIT · 原始版本 © handsomestWei · 定制版 © kcylp
