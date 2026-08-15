#!/usr/bin/env python
"""
国知局专利全文获取模块 v1.0 · kcylp 定制版
============================================

功能：
  1. 通过公开号获取专利全文 PDF
  2. 解析 PDF 提取：权利要求、说明书、摘要、附图说明
  3. 结构化输出 JSON 供后续工具使用

数据源优先级：
  1. 国知局 epub.cnipa.gov.cn（Playwright 自动化）
  2. Google Patents CDN
  3. 备用 CDN 源

用法：
  python tools/crawl/cnipa_fulltext.py --pub CN112345678A -o ./output
  python tools/crawl/cnipa_fulltext.py --pub CN209861402U --format json
  python tools/crawl/cnipa_fulltext.py --batch input.jsonl -o ./batch_output

输入格式（batch 模式）：
  {"pub": "CN112345678A", "type": "invention"}
  {"pub": "CN209861402U", "type": "utility_model"}

输出：
  - {pub}/fulltext.pdf — 原始 PDF
  - {pub}/extracted.json — 结构化提取结果
  - {pub}/manifest.json — 元数据
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# 确保 tools 在路径中
_TOOLS_DIR = Path(__file__).resolve().parent.parent
_SHARED = _TOOLS_DIR / "shared"
for p in (_TOOLS_DIR, _SHARED):
    s = str(p)
    if s not in sys.path:
        sys.path.insert(0, s)

try:
    from patent_type import (
        infer_patent_type_from_pub,
        normalize_patent_type,
        normalize_pub_number,
    )
except ImportError:
    def infer_patent_type_from_pub(pub): return None
    def normalize_patent_type(t, default="all"): return default or "all"
    def normalize_pub_number(pub): return (pub or "").replace(" ", "").upper()


# ============================================================================
# 1. 国知局公开数据获取（Playwright）
# ============================================================================

def _get_playwright():
    try:
        from playwright.sync_api import sync_playwright
        return sync_playwright
    except ImportError:
        return None


def fetch_from_cnipa(pub: str, outdir: Path, *, headed: bool = False, timeout: int = 30) -> Dict[str, Any]:
    """
    通过 Playwright 从国知局 epub.cnipa.gov.cn 获取专利信息。

    返回：
      {
        "source": "cnipa",
        "url": "...",
        "html": "...",
        "patent_type": "invention|utility_model|design",
        "abstract": "...",
        "claims": ["权1...", "权2..."],
        "description_paragraphs": ["0001...", "0002..."],
        "biblio": {...},
        "error": None|str
      }
    """
    sync_playwright = _get_playwright()
    if not sync_playwright:
        return {
            "source": "cnipa",
            "error": "playwright 未安装: pip install -r tools/crawl/requirements-cnipa.txt && python -m playwright install chromium",
            "pub": pub,
        }

    result = {
        "source": "cnipa",
        "pub": pub,
        "url": "",
        "html": "",
        "patent_type": infer_patent_type_from_pub(pub),
        "abstract": "",
        "claims": [],
        "description_paragraphs": [],
        "biblio": {},
        "error": None,
    }

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=not headed,
                args=["--disable-blink-features=AutomationControlled", "--no-sandbox"],
            )
            context = browser.new_context(
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                ),
                locale="zh-CN",
                viewport={"width": 1280, "height": 900},
            )
            page = context.new_page()

            # 搜索专利
            page.goto("http://epub.cnipa.gov.cn/", wait_until="load", timeout=120_000)
            _wait_for_search_box(page, timeout=timeout)

            # 填入公开号搜索
            page.fill("#searchStr", pub)
            with page.expect_navigation(timeout=60_000, wait_until="commit"):
                form = page.query_selector("#indexForm")
                if form:
                    form.evaluate("el => el.submit()")

            # 等待结果页
            page.wait_for_function(
                """(titles) => {
                    const t = document.title.trim();
                    if (t === titles.noHit) return true;
                    if (t !== titles.result) return false;
                    const r = document.querySelector("#result");
                    if (!r) return false;
                    if (r.querySelector("div.item, h1.title")) return true;
                    const html = r.innerHTML;
                    return html.includes("无查询结果") || html.includes("没有找到") || html.includes("0条");
                }""",
                arg={"result": "专利查询结果展示", "noHit": "无查询结果"},
                timeout=60_000,
            )

            html = page.content()
            result["html"] = html

            # 提取摘要和基本著录
            result["abstract"] = _extract_abstract_from_html(html)
            result["biblio"] = _extract_biblio_from_html(html)

            # 尝试点击进入详情页获取更多信息
            detail_link = page.query_selector("div.item a[href*='detail']")
            if detail_link:
                detail_url = detail_link.get_attribute("href")
                if detail_url:
                    result["url"] = detail_url if detail_url.startswith("http") else f"http://epub.cnipa.gov.cn{detail_url}"

            context.close()
            browser.close()

    except Exception as e:
        result["error"] = str(e)

    return result


def _wait_for_search_box(page, timeout: int = 180):
    """等待搜索框出现。"""
    import time
    start = time.time()
    step = 3.0
    while time.time() - start < timeout:
        page.wait_for_timeout(int(step * 1000))
        if page.query_selector("#searchStr"):
            return
    raise TimeoutError(f"{timeout}s 内未出现搜索框")


def _extract_abstract_from_html(html: str) -> str:
    """从 HTML 中提取摘要。"""
    # 尝试匹配摘要区域
    patterns = [
        r'class=["\']abstract["\'][^>]*>([^<]+)',
        r'摘\s*要[：:]\s*([^<]+)',
        r'<p[^>]*>(?:本发明|本实用新型|本外观设计)(?:涉及|公开|提供)[^<]+</p>',
    ]
    for pat in patterns:
        m = re.search(pat, html, re.I)
        if m:
            text = re.sub(r'<[^>]+>', '', m.group(0)).strip()
            if len(text) > 20:
                return text[:500]
    return ""


def _extract_biblio_from_html(html: str) -> Dict[str, Any]:
    """从 HTML 中提取基本著录信息。"""
    biblio: Dict[str, Any] = {}

    # 申请号
    m = re.search(r'申请号[：:]\s*([A-Z0-9]+)', html)
    if m:
        biblio["application_number"] = m.group(1)

    # 申请日
    m = re.search(r'申请日[期]?[：:]\s*(\d{4}[-./年]\d{1,2}[-./月]\d{1,2}[日]?)', html)
    if m:
        biblio["filing_date"] = m.group(1)

    # 公开号
    m = re.search(r'(?:公开|公告)号[：:]\s*([A-Z0-9]+)', html)
    if m:
        biblio["publication_number"] = m.group(1)

    # IPC 分类
    ipc_matches = re.findall(r'(?:IPC|分类号)[：:]\s*([A-H]\d{2}[A-Z]\d+/\d+(?:\.\d+)?)', html)
    if ipc_matches:
        biblio["ipc_codes"] = list(set(ipc_matches))

    # 申请人/权利人
    assignee_match = re.search(r'(?:申请(人|权人)|权利人)[：:]\s*([^<\n]+)', html)
    if assignee_match:
        biblio["assignee"] = assignee_match.group(2).strip()

    # 发明人
    inventor_match = re.search(r'发明人[：:]\s*([^<\n]+)', html)
    if inventor_match:
        biblio["inventors"] = inventor_match.group(1).strip()

    return biblio


# ============================================================================
# 2. PDF 全文下载（Google Patents CDN）
# ============================================================================

def fetch_pdf_from_google_patents(pub: str, outdir: Path) -> Dict[str, Any]:
    """
    从 Google Patents 获取 PDF。
    返回：{"url": "...", "path": "...", "error": None|str}
    """
    import urllib.request
    import ssl

    result = {"url": "", "path": "", "error": None}

    # Google Patents URL 模式
    google_pub = pub.replace("CN", "").rstrip("ABUCS")
    urls_to_try = [
        f"https://patents.google.com/patent/CN{google_pub}A/en",
        f"https://patents.google.com/patent/CN{google_pub}B/en",
        f"https://patents.google.com/patent/CN{google_pub}U/en",
    ]

    # 已知的 Google Patents PDF CDN 模式
    pdf_urls = [
        f"https://patentimages.storage.googleapis.com/pdfs/CN{google_pub}.pdf",
    ]

    ssl_ctx = ssl.create_default_context()
    ssl_ctx.check_hostname = False
    ssl_ctx.verify_mode = ssl.CERT_NONE

    for pdf_url in pdf_urls:
        try:
            req = urllib.request.Request(pdf_url, headers={"User-Agent": "Mozilla/5.0"})
            resp = urllib.request.urlopen(req, timeout=30, context=ssl_ctx)
            if resp.status == 200:
                pdf_path = outdir / f"{pub}.pdf"
                pdf_path.write_bytes(resp.read())
                result["url"] = pdf_url
                result["path"] = str(pdf_path)
                return result
        except Exception:
            continue

    result["error"] = f"无法从 Google Patents 获取 {pub} 的 PDF"
    return result


# ============================================================================
# 3. PDF 文本提取（pymupdf）
# ============================================================================

def extract_text_from_pdf(pdf_path: Path) -> Dict[str, Any]:
    """
    从 PDF 提取结构化文本。
    返回：
      {
        "full_text": "...",
        "claims": ["权1...", "权2..."],
        "description": ["0001...", "0002..."],
        "abstract": "...",
        "figures": [{"page": 1, "caption": "图1..."}],
        "error": None|str
      }
    """
    result = {
        "full_text": "",
        "claims": [],
        "description": [],
        "abstract": "",
        "figures": [],
        "error": None,
    }

    try:
        import fitz  # pymupdf
    except ImportError:
        result["error"] = "pymupdf 未安装: pip install pymupdf"
        return result

    try:
        doc = fitz.open(str(pdf_path))
        full_text = ""
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text()
            full_text += text + "\n\n"

        result["full_text"] = full_text

        # 提取权利要求
        result["claims"] = _extract_claims(full_text)

        # 提取说明书段落
        result["description"] = _extract_description_paragraphs(full_text)

        # 提取摘要
        result["abstract"] = _extract_abstract(full_text)

        # 提取附图说明
        result["figures"] = _extract_figure_captions(full_text)

        doc.close()

    except Exception as e:
        result["error"] = str(e)

    return result


def _extract_claims(text: str) -> List[str]:
    """从全文中提取权利要求。"""
    claims = []
    # 匹配 "1. 一种..." 到下一个编号
    pattern = r'(?:权利要求书|权利要求)\s*(.*?)(?:说明书|具体实施方式|$)'
    m = re.search(pattern, text, re.DOTALL)
    if m:
        claims_text = m.group(1)
        # 按编号分割
        parts = re.split(r'\n\s*(\d+)\s*[.．、]', claims_text)
        for i in range(1, len(parts), 2):
            num = parts[i]
            content = parts[i + 1].strip() if i + 1 < len(parts) else ""
            if content:
                claims.append(f"{num}. {content[:300]}")
    return claims


def _extract_description_paragraphs(text: str) -> List[str]:
    """提取说明书段落。"""
    paragraphs = []
    # CNIPA 段落编号格式：[0001]
    pattern = r'\[(\d{4})\]\s*(.*?)(?=\[\d{4}\]|$)'
    for m in re.finditer(pattern, text, re.DOTALL):
        num = m.group(1)
        content = m.group(2).strip()
        if content and len(content) > 5:
            paragraphs.append(f"[{num}] {content[:200]}")
    return paragraphs[:100]  # 限制数量


def _extract_abstract(text: str) -> str:
    """提取摘要。"""
    patterns = [
        r'摘\s*要\s*(?:[:：])?\s*(.*?)(?:(?:说\s*明\s*书|权\s*利\s*要\s*求|附\s*图\s*说\s*明|具体实施方式)\s*$)',
        r'(?:本发明|本实用新型)(?:公开|提供|涉及|是)(?:了一种|一种)[^。]+。',
    ]
    for pat in patterns:
        m = re.search(pat, text, re.DOTALL | re.IGNORECASE)
        if m:
            abstract = m.group(0).strip()
            abstract = re.sub(r'\s+', ' ', abstract)
            if len(abstract) > 30:
                return abstract[:500]
    return ""


def _extract_figure_captions(text: str) -> List[Dict[str, Any]]:
    """提取附图说明。"""
    figures = []
    patterns = [
        r'图\s*(\d+)\s*[是为：:]\s*(.+?)(?:\n|$)',
        r'(?:附图说明|图面说明)\s*(.*?)(?:具体实施方式|$)',
    ]
    for pat in patterns:
        for m in re.finditer(pat, text, re.IGNORECASE):
            if m.lastindex and m.lastindex >= 2:
                fig_num = m.group(1)
                caption = m.group(2).strip()
                figures.append({"number": fig_num, "caption": caption[:100]})
            elif m.group(1):
                # 附图说明块
                for line in m.group(1).split('\n'):
                    line = line.strip()
                    if line and re.match(r'图\s*\d+', line):
                        parts = re.split(r'[是为：:]', line, maxsplit=1)
                        if len(parts) == 2:
                            figures.append({"number": parts[0].strip(), "caption": parts[1].strip()[:100]})
    return figures


# ============================================================================
# 4. 统一入口
# ============================================================================

def fetch_patent_fulltext(
    pub: str,
    outdir: Path,
    *,
    source: str = "auto",
    headed: bool = False,
) -> Dict[str, Any]:
    """
    统一获取专利全文。

    参数：
      pub: 公开号（如 CN112345678A）
      outdir: 输出目录
      source: "cnipa" | "google" | "auto"（默认 auto）
      headed: 是否显示浏览器窗口

    返回：
      {
        "pub": "...",
        "patent_type": "...",
        "source": "cnipa|google",
        "pdf_path": "...",
        "fulltext": {...},
        "biblio": {...},
        "error": None|str
      }
    """
    pub = normalize_pub_number(pub)
    outdir.mkdir(parents=True, exist_ok=True)

    result = {
        "pub": pub,
        "patent_type": infer_patent_type_from_pub(pub),
        "source": "",
        "pdf_path": "",
        "fulltext": {},
        "biblio": {},
        "error": None,
    }

    # 尝试 1: 国知局
    if source in ("auto", "cnipa"):
        cnipa_result = fetch_from_cnipa(pub, outdir, headed=headed)
        if not cnipa_result.get("error"):
            result["source"] = "cnipa"
            result["biblio"] = cnipa_result.get("biblio", {})
            # 如果拿到了 PDF URL，下载
            if cnipa_result.get("url"):
                pdf_result = fetch_pdf_from_google_patents(pub, outdir)
                if not pdf_result.get("error"):
                    result["pdf_path"] = pdf_result["path"]
                    result["fulltext"] = extract_text_from_pdf(Path(pdf_result["path"]))
            return result

    # 尝试 2: Google Patents
    if source in ("auto", "google"):
        pdf_result = fetch_pdf_from_google_patents(pub, outdir)
        if not pdf_result.get("error"):
            result["source"] = "google"
            result["pdf_path"] = pdf_result["path"]
            result["fulltext"] = extract_text_from_pdf(Path(pdf_result["path"]))
            return result

    result["error"] = f"无法获取 {pub} 的全文数据"
    return result


# ============================================================================
# 5. CLI 入口
# ============================================================================

def main(argv: Optional[List[str]] = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

    ap = argparse.ArgumentParser(description="国知局专利全文获取模块")
    ap.add_argument("--pub", help="公开号（如 CN112345678A）")
    ap.add_argument("-o", "--output", default="./output", help="输出目录")
    ap.add_argument("--source", choices=["auto", "cnipa", "google"], default="auto")
    ap.add_argument("--headed", action="store_true", help="显示浏览器窗口")
    ap.add_argument("--format", choices=["json", "text"], default="json")
    ap.add_argument("--batch", help="批量输入 JSONL 文件")
    args = ap.parse_args(argv)

    if args.batch:
        # 批量模式
        batch_input = Path(args.batch)
        if not batch_input.exists():
            print(f"错误: {batch_input} 不存在", file=sys.stderr)
            return 1

        outdir = Path(args.output)
        outdir.mkdir(parents=True, exist_ok=True)

        results = []
        for line in batch_input.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            try:
                item = json.loads(line)
                pub = item.get("pub", "")
                if pub:
                    result = fetch_patent_fulltext(
                        pub,
                        outdir / pub,
                        source=args.source,
                        headed=args.headed,
                    )
                    results.append(result)
            except json.JSONDecodeError:
                continue

        # 输出汇总
        summary = {
            "total": len(results),
            "success": sum(1 for r in results if not r.get("error")),
            "failed": sum(1 for r in results if r.get("error")),
            "results": results,
        }
        print(json.dumps(summary, ensure_ascii=False, indent=2))

    elif args.pub:
        # 单个模式
        outdir = Path(args.output) / args.pub
        result = fetch_patent_fulltext(
            args.pub,
            outdir,
            source=args.source,
            headed=args.headed,
        )

        if args.format == "json":
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            # 文本格式
            ft = result.get("fulltext", {})
            if result.get("error"):
                print(f"错误: {result['error']}")
            else:
                print(f"公开号: {result['pub']}")
                print(f"类型: {result['patent_type']}")
                print(f"来源: {result['source']}")
                print(f"PDF: {result['pdf_path']}")
                print(f"摘要: {ft.get('abstract', '未提取')[:200]}")
                print(f"权利要求数: {len(ft.get('claims', []))}")
                print(f"说明书段落数: {len(ft.get('description', []))}")

        return 0 if not result.get("error") else 1

    else:
        ap.print_help()
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
