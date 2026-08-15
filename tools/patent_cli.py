#!/usr/bin/env python
"""
专利技能统一 CLI 入口 v1.0 · kcylp 定制版
=========================================

一个命令完成所有专利工作流：
  disclosure  — 交底书编写（发明/实用新型/外观）
  read        — 专利通俗解读 + Obsidian 入库
  search      — 国知局/Google Patents 查新
  formula     — 公式验证/计算/渲染/同步检查（永不错误）
  extract     — PDF/STEP/CAD 提取
  lineart     — 辅助线稿生成（外观轮廓/实用结构）
  oa          — 审查答复辅助（案例 RAG）
  evolve      — 政策/审查动向嗅探
  version     — 版本信息

用法：
  python tools/patent_cli.py disclosure --type invention --case-dir ./my_case
  python tools/patent_cli.py read --pub CN112345678A
  python tools/patent_cli.py search --keywords "批任务 调度" --type invention
  python tools/patent_cli.py formula validate -i formula_plan.yaml
  python tools/patent_cli.py formula compute -i formula_plan.yaml --given "s0=0.8"
  python tools/patent_cli.py extract pdf --pub CN112345678A -o ./output
  python tools/patent_cli.py lineart --type design --case-dir ./my_case
  python tools/patent_cli.py oa ingest -i case.md
  python tools/patent_cli.py oa search --query "创造性 区别特征"
  python tools/patent_cli.py evolve --topic "审查指南"
  python tools/patent_cli.py version
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# 确保 tools 在路径中
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def _ensure_utf8():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")


# ============================================================================
# Sub-commands
# ============================================================================

def cmd_disclosure(args):
    """交底书编写入口。"""
    print("=" * 60)
    print("专利交底书编写")
    print("=" * 60)
    print(f"  类型: {args.type}")
    print(f"  案件目录: {args.case_dir}")

    if args.type == "invention":
        print("\n流程: intake → project_scan → patent_points_analyzer → prior_art_search → disclosure_builder → self_check")
        print("  系统框图 & 流程图: mermaid → PNG → Word")
        print("  公式: formula_plan.yaml → OMML/PNG 双轨 → Word")
    elif args.type == "utility_model":
        print("\n流程: intake → project_scan → patent_points → fill_structure_schema → figure_plan → disclosure_builder → self_check")
        print("  结构线稿: structure_lineart_assist（默认关，需确认）")
        print("  CAD/STEP: cad_scan → step_to_views（默认关，需确认）")
    elif args.type == "design":
        print("\n流程: intake → project_scan → patent_points → fill_appearance_schema → figure_plan → disclosure_builder → self_check")
        print("  外观线稿: design_lineart_assist（默认关，需确认）")
        print("  视图: figure_plan.yaml 排序入文图")
    else:
        print(f"\n⚠ 未知类型: {args.type}")
        return 1

    print("\n详细步骤提示:")
    print("  1. Read prompts/disclosure/intake.md")
    print("  2. Read prompts/disclosure/project_scan.md")
    print("  3. Read 对应类型 patent_points + builder + template")
    print("  4. Read prompts/disclosure/prior_art_search.md")
    print("  5. Read prompts/disclosure/disclosure_self_check.md")
    print("\n查看 SKILL.md 获取完整流程说明。")
    return 0


def cmd_read(args):
    """专利通俗解读入口。"""
    print("=" * 60)
    print("专利通俗解读")
    print("=" * 60)

    if args.pub:
        from tools.shared.patent_type import infer_patent_type_from_pub
        ptype = infer_patent_type_from_pub(args.pub)
        print(f"  公开号: {args.pub}")
        print(f"  推断类型: {ptype or '未知'}")
        print("\n流程: fetch_patent_pdf → extract_patent_text → build_context_anchor → write_patent_obsidian_note")
        print("  详见 prompts/reader/patent_plain_reader.md")
    else:
        print("  请提供 --pub 公开号 或 --pdf 文件路径")

    return 0


def cmd_search(args):
    """查新入口。"""
    print("=" * 60)
    print("专利查新")
    print("=" * 60)
    print(f"  关键词: {args.keywords}")
    print(f"  类型: {args.type}")

    from tools.shared.patent_type import normalize_patent_type, EPUB_TYPE_CHECKBOXES

    ptype = normalize_patent_type(args.type)
    checkboxes = EPUB_TYPE_CHECKBOXES.get(ptype, {})

    print(f"\n国知局 epub.cnipa.gov.cn 查询:")
    print(f"  checkbox: {checkboxes}")
    print(f"\n执行:")
    cmd = f'python tools/crawl/cnipa_epub_search.py --type {ptype} "{args.keywords}"'
    print(f"  {cmd}")
    print("\n或降级 WebSearch:")
    from tools.shared.patent_type import google_patents_websearch_query
    gpq = google_patents_websearch_query(args.keywords, ptype)
    print(f'  WebSearch: "{gpq}"')

    return 0


def cmd_formula(args):
    """公式引擎子命令。"""
    from tools.shared.formula_engine import FormulaEngine
    from pathlib import Path

    engine = FormulaEngine()

    if args.formula_cmd == "validate":
        result = engine.validate(Path(args.input))
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result.get("ok") else 1

    elif args.formula_cmd == "compute":
        result = engine.compute(Path(args.input), args.given)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result.get("all_ok") else 1

    elif args.formula_cmd == "render":
        plan = engine._load_plan(Path(args.input))
        output_dir = Path(args.input).parent / "formula_renders"
        output_dir.mkdir(exist_ok=True)
        result = engine.renderer.render_all(plan, output_dir)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if not result["errors"] else 1

    elif args.formula_cmd == "check-omml":
        result = engine.check_omml(Path(args.input))
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result.get("ok") else 1

    elif args.formula_cmd == "sync":
        result = engine.sync(Path(args.input), Path(args.disclosure))
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result.get("ok") else 1

    else:
        print(f"未知公式子命令: {args.formula_cmd}")
        return 1


def cmd_extract(args):
    """提取入口。"""
    print("=" * 60)
    print(f"提取: {args.extract_type}")
    print("=" * 60)

    if args.extract_type == "pdf":
        if args.pub:
            print(f"  公开号: {args.pub}")
            print(f"  输出: {args.output}")
            cmd = f'python tools/patent_reader/extract/fetch_patent_pdf.py --pub {args.pub} -o {args.output}'
            print(f"\n  执行: {cmd}")
        elif args.input:
            print(f"  输入: {args.input}")
            print("  执行: python tools/patent_reader/extract/extract_patent_text.py")
        else:
            print("  需要 --pub 或 --input")
            return 1

    elif args.extract_type == "step":
        if args.input:
            cmd = f'python tools/shared/step_to_views.py --enable-step-parse -i {args.input} -o {args.output or "./cad_views"}'
            print(f"  执行: {cmd}")
        else:
            print("  需要 --input <file.step>")
            return 1

    elif args.extract_type == "cad":
        cmd = f'python tools/shared/cad_scan.py -r {args.directory or "."} --json'
        print(f"  执行: {cmd}")

    return 0


def cmd_lineart(args):
    """辅助线稿入口。"""
    print("=" * 60)
    print(f"辅助线稿: {args.lineart_type}")
    print("=" * 60)
    print(f"  案件目录: {args.case_dir}")

    if args.lineart_type == "design":
        print("\n流程:")
        print("  1. 确认有产品参考图")
        print("  2. design_lineart_gate.py --print-confirm")
        print("  3. design_lineart_assist.md → 生成描述 + 线稿草稿")
        print("  注意: 禁止纯文生图；辅助线稿默认不入正文")
    elif args.lineart_type == "structure":
        print("\n流程:")
        print("  1. 确认有结构参考图 + structure_schema")
        print("  2. structure_lineart_gate.py --print-confirm")
        print("  3. structure_lineart_assist.md → 生成轮廓 + 件号引出")
        print("  注意: 件号对齐 parts；推荐 overlay；禁止自创件号")
    else:
        print(f"\n⚠ 未知线稿类型: {args.lineart_type}")
        return 1

    return 0


def cmd_oa(args):
    """审查答复入口。"""
    print("=" * 60)
    print("审查答复辅助")
    print("=" * 60)

    if args.oa_cmd == "ingest":
        print(f"  入库: {args.input}")
        print(f"  执行: python tools/oa/ingest_case.py -i {args.input}")
    elif args.oa_cmd == "search":
        print(f"  检索: {args.query}")
        print(f"  缺陷类型: {args.defect or '全部'}")
        print(f"  执行: python tools/oa/search_cases.py --query \"{args.query}\" --defect {args.defect or 'all'} --top-k {args.top_k or 5}")
    elif args.oa_cmd == "config":
        print("  配置向量模型:")
        print("    python tools/oa/config.py recommend")
        print("    python tools/oa/config.py set --preset zhipu|dashscope|minimax|local|openai|skip-vector")
        print("    python tools/oa/config.py status")
    else:
        print(f"  未知子命令: {args.oa_cmd}")
        return 1

    return 0


def cmd_evolve(args):
    """技能进化入口。"""
    print("=" * 60)
    print("技能进化旁路 · 政策/审查动向嗅探")
    print("=" * 60)
    print(f"  主题: {args.topic or '近 12 个月国知局动向'}")
    print("\n流程:")
    print("  1. Read prompts/evolution/intake.md")
    print("  2. Read prompts/evolution/research.md → WebSearch + 官网抓取")
    print("  3. Read prompts/evolution/emit_backlog.md → 写 EVOL-*.md")
    print("  4. 人审闸门 → 确认后才 apply_after_confirm.md")
    print("\n  注意: 默认关；须显式触发。清单含观点↔信源 URL 表。")

    return 0


def cmd_version(args):
    """版本信息。"""
    print("=" * 60)
    print("中国专利.skill · kcylp 定制版")
    print("=" * 60)
    print(f"  版本: 26.08.15")
    print(f"  原始: handsomestWei/patent-disclosure-skill (MIT)")
    print(f"  定制: https://github.com/kcylp/patent-disclosure-skill")
    print()
    print("  功能模块:")
    print("    A. 交底书编写  发明/实用新型/外观设计")
    print("    B. 专利通俗解读  Obsidian 知识图谱")
    print("    C. 技能进化旁路  政策动向嗅探（默认关）")
    print("    D. 审查答复辅助  向量 RAG 案例库（默认关）")
    print("    +  公式引擎 v1.0  数值验证/渲染/同步检查")
    print("    +  国知局全文获取  多源专利数据提取")
    print("    +  统一 CLI 入口  所有功能单命令接入")
    print("    +  多平台兼容     Claude Code / Codex / Cursor / Windsurf")
    print()

    try:
        from tools.shared.patent_type import CANONICAL_TYPES, TYPE_LABEL_ZH
        print("  支持的专利类型:")
        for t in CANONICAL_TYPES:
            print(f"    {t}: {TYPE_LABEL_ZH[t]}")
    except ImportError:
        pass

    return 0


# ============================================================================
# Main parser
# ============================================================================

def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(
        prog="patent_cli",
        description="专利技能统一 CLI · 交底书 / 解读 / 查新 / 公式 / 提取 / 线稿 / 审查答复 / 进化",
    )

    sub = ap.add_subparsers(dest="command")

    # disclosure
    p_disc = sub.add_parser("disclosure", help="交底书编写")
    p_disc.add_argument("--type", choices=["invention", "utility_model", "design"], default="invention",
                        help="专利类型（默认发明）")
    p_disc.add_argument("--case-dir", default="./outputs", help="案件目录")
    p_disc.set_defaults(func=cmd_disclosure)

    # read
    p_read = sub.add_parser("read", help="专利通俗解读")
    p_read.add_argument("--pub", help="公开号（如 CN112345678A）")
    p_read.add_argument("--pdf", help="PDF 文件路径")
    p_read.set_defaults(func=cmd_read)

    # search
    p_search = sub.add_parser("search", help="查新")
    p_search.add_argument("--keywords", required=True, help="搜索关键词")
    p_search.add_argument("--type", default="invention", help="专利类型")
    p_search.set_defaults(func=cmd_search)

    # formula (sub-sub-commands)
    p_formula = sub.add_parser("formula", help="公式引擎")
    formula_sub = p_formula.add_subparsers(dest="formula_cmd")

    p_fv = formula_sub.add_parser("validate", help="验证 formula_plan")
    p_fv.add_argument("-i", "--input", required=True)

    p_fc = formula_sub.add_parser("compute", help="计算公式数值")
    p_fc.add_argument("-i", "--input", required=True)
    p_fc.add_argument("--given", required=True, help="变量赋值，如 's0=0.8,alpha=0.3'")

    p_fr = formula_sub.add_parser("render", help="渲染公式为 OMML/PNG")
    p_fr.add_argument("-i", "--input", required=True)

    p_fo = formula_sub.add_parser("check-omml", help="检查 Word 中的 OMML 公式")
    p_fo.add_argument("-i", "--input", required=True)

    p_fs = formula_sub.add_parser("sync", help="检查 formula_plan 与正文同步")
    p_fs.add_argument("-i", "--input", required=True)
    p_fs.add_argument("-d", "--disclosure", required=True)

    p_formula.set_defaults(func=cmd_formula)

    # extract (sub-sub-commands)
    p_extract = sub.add_parser("extract", help="提取 PDF/STEP/CAD")
    extract_sub = p_extract.add_subparsers(dest="extract_type")

    p_ep = extract_sub.add_parser("pdf", help="获取专利 PDF")
    p_ep.add_argument("--pub", help="公开号")
    p_ep.add_argument("--input", help="输入文件路径")
    p_ep.add_argument("-o", "--output", default="./output")

    p_es = extract_sub.add_parser("step", help="STEP → 多视角 PNG")
    p_es.add_argument("--input", required=True)
    p_es.add_argument("-o", "--output", default="./cad_views")

    p_ec = extract_sub.add_parser("cad", help="扫描 CAD 文件")
    p_ec.add_argument("-r", "--directory", default=".")

    p_extract.set_defaults(func=cmd_extract)

    # lineart
    p_lineart = sub.add_parser("lineart", help="辅助线稿生成")
    p_lineart.add_argument("--type", choices=["design", "structure"], required=True)
    p_lineart.add_argument("--case-dir", default="./outputs")
    p_lineart.set_defaults(func=cmd_lineart)

    # oa (sub-sub-commands)
    p_oa = sub.add_parser("oa", help="审查答复")
    oa_sub = p_oa.add_subparsers(dest="oa_cmd")

    p_oi = oa_sub.add_parser("ingest", help="案例入库")
    p_oi.add_argument("-i", "--input", required=True)

    p_os = oa_sub.add_parser("search", help="检索案例")
    p_os.add_argument("--query", required=True)
    p_os.add_argument("--defect", help="缺陷类型标签")
    p_os.add_argument("--top-k", type=int, default=5)

    p_oc = oa_sub.add_parser("config", help="向量模型配置")
    p_oc.set_defaults(func=cmd_oa)

    p_oa.set_defaults(func=cmd_oa)

    # evolve
    p_evolve = sub.add_parser("evolve", help="技能进化/政策嗅探")
    p_evolve.add_argument("--topic", help="嗅探主题")
    p_evolve.set_defaults(func=cmd_evolve)

    # version
    sub.add_parser("version", help="版本信息").set_defaults(func=cmd_version)

    return ap


def main(argv: Optional[list] = None) -> int:
    _ensure_utf8()
    ap = build_parser()
    args = ap.parse_args(argv)

    if not args.command:
        ap.print_help()
        return 0

    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
