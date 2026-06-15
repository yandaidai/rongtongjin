"""贵金属品种常量定义 — 唯一数据来源（DRY）

所有品种代码、名称、映射关系只在此定义。
引用方：akshare_service.py / quote_service.py / seed.py
"""

# ── 国内 SGE 品种 ──
DOMESTIC_PRODUCTS = [
    {"code": "Au99.99", "name": "黄金99.99", "unit": "元/克"},
    {"code": "Au99.95", "name": "黄金99.95", "unit": "元/克"},
    {"code": "Au100g",  "name": "黄金100克", "unit": "元/克"},
    {"code": "Pt99.95", "name": "铂金99.95", "unit": "元/克"},
    {"code": "Ag(T+D)", "name": "白银延期",  "unit": "元/千克"},
    {"code": "Au(T+D)", "name": "黄金延期",  "unit": "元/克"},
    {"code": "mAu(T+D)","name": "迷你黄金延期", "unit": "元/克"},
    {"code": "Ag99.99", "name": "白银99.99", "unit": "元/千克"},
]

# ── 国际品种 ──
INTERNATIONAL_PRODUCTS = [
    {"code": "XAU", "name": "国际现货黄金", "unit": "美元/盎司"},
    {"code": "XAG", "name": "国际现货白银", "unit": "美元/盎司"},
    {"code": "XPT", "name": "国际现货铂金", "unit": "美元/盎司"},
]

ALL_PRODUCTS = DOMESTIC_PRODUCTS + INTERNATIONAL_PRODUCTS

# ── 国内品种代码集合（用于 get_quotes_by_category 过滤）──
DOMESTIC_CODES = {p["code"] for p in DOMESTIC_PRODUCTS}

# ── 国际品种 → akshare 名称映射 ──
INTERNATIONAL_CODE_MAP: dict[str, str] = {
    "XAU": "COMEX黄金",
    "XAG": "COMEX白银",
    "XPT": "NYMEX铂金",
}

# ── SGE 品种 → akshare symbol 映射 ──
SGE_SYMBOLS: dict[str, str] = {p["code"]: p["code"] for p in DOMESTIC_PRODUCTS}
