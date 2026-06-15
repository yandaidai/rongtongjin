# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Backend (Python 3.14, uv-based)

```bash
cd backend/

# Run server with scheduler (行情定时任务)
python run.py

# Run server without scheduler (development)
uvicorn app.main:app --reload

# Seed database with precious-metal products + default spread configs
python seed.py
python seed.py --sqlite   # For local SQLite testing

# Run all tests
pytest

# Run only unit tests (mocked service layer)
pytest tests/unittest/ -m unit

# Run only integration tests (SQLite-backed, full request→DB cycle)
pytest tests/integration/ -m integeation  # yes, the typo is intentional in pyproject.toml

# Run a single test file
pytest tests/integration/test_auth.py -v

# Type check (with strict mode)
mypy app/ --strict

# Alembic migrations (if they exist)
alembic upgrade head
alembic revision --autogenerate -m "description"
```

### Frontend (React Native / Expo SDK 52)

```bash
cd frontend/
npm install
npx expo start          # Start Expo dev server
npx expo start --ios    # iOS-specific
npx expo start --android
```

## Project Architecture

### Layered Backend (FastAPI)

```
app/main.py                   ← FastAPI app, CORS, route registration
├── app/api/v1/*.py           ← Routes (thin: parse params, delegate)
│   auth.py                   │  /auth/* (login, register, user info)
│   products.py               │  /products/*
│   quotes.py                 │  /quotes/* (实时行情 + 销售/回购价)
│   klines.py                 │  /klines/*
│   global_config.py          │  /global/config/*
│   user_config.py            │  /user/config/*
│   warns.py                  │  /user/warn/*
├── app/services/*.py         ← Business logic
│   akshare_service.py        │  akshare 贵金属行情获取 (SGE + COMEX/NYMEX)
│   quote_service.py          │  行情 + 点差计算 (销售价/回购价)
│   scheduler.py              │  APScheduler 定时刷新行情 (每分钟)
│   auth_service.py           │  用户认证
│   config_service.py         │  点差配置
│   kline_service.py          │  K线数据
│   product_service.py        │  品种管理
│   warn_service.py           │  价格预警
├── app/models/*.py           ← SQLAlchemy 2.0 ORM (7 tables)
├── app/schemas/*.py          ← Pydantic v2 request/response DTOs
├── app/core/                 ← Cross-cutting: JWT, dependencies
├── app/config.py             ← pydantic-settings (DB/JWT/app)
├── app/database.py           ← SQLAlchemy engine + get_db dependency
├── app/utils/helpers.py      ← Utilities
└── tests/
    ├── unittest/             ← Mocked service layer (fast, no DB)
    │   conftest.py           │  Minimal TestClient fixture
    │   test_api/test_auth.py │  14 tests with patched AuthService
    └── integration/          ← SQLite-backed (real DB, slower)
        conftest.py           │  Full fixture: e2e on test.db
        test_auth.py          │  14 tests (login, register, profile, password...)
        test_configs.py       │
        test_klines.py        │
        test_products.py      │
        test_quotes.py        │
        test_warns.py         │
```

### Key Design Decisions

- **QuoteService** computes sell_price = market_price + sell_add_spread, buy_back_price = market_price - buy_back_sub_spread
- **Spread priority**: user-config > global-config > hardcoded default (sell 3.0, buy 2.0)
- **Scheduler** runs independently via APScheduler (not tied to uvicorn lifecycle). Creates its own DB engine — currently a new engine per tick; consider refactoring to reuse the app's engine
- **Market data source**: akshare library (SGE for domestic, futures_global_spot_em for international)
- **Auth**: phone + SMS-code, JWT Bearer token, 24h expiry. Dev mode uses hardcoded code 123456
- **Product codes** are defined in 3 places (akshare_service.py / quote_service.py / seed.py) — a known duplication risk

### Frontend (React Native)

```
frontend/
├── App.tsx                 ← Root: AuthProvider + Navigator
├── app.json                ← Expo config (icon, splash, plugins)
├── src/
│   ├── api/client.ts       ← ApiClient class (fetch wrapper, token management)
│   ├── types/index.ts      ← TypeScript interfaces (User, MetalQuote, etc.)
│   ├── store/AuthContext.tsx ← React Context for auth state
│   ├── navigation/AppNavigator.tsx ← Stack + Tab navigation
│   ├── screens/            ← 9 screens (Login, Products, Quotes, Kline, Profile, Config, Warn)
│   └── components/         ← Shared UI: KlineChart, ProductCard, QuoteCard, Loading
```

### Database (MySQL via SQLAlchemy 2.0)

7 tables centered on `metal_product` as hub:

```
users ──┬── metal_user_config ← metal_product ──→ metal_global_config
        │                                          metal_quote
        └── metal_warn                              metal_kline
```

Key indexes: `ix_metal_quote_product_time(product_id, quote_time)` on metal_quote.

### Data Flow — Market Price Refresh

```
akshare → APScheduler (every 1min) → metal_quote table (+ metal_kline)
                                              ↓
                                     FastAPI → JSON → React Native UI
```

## Important Notes

- **MySQL must be running** on localhost:3306 with database `rongtongjin` for full backend
- **SECRET_KEY** in config.py has a weak default (`your-secret-key-change-in-production`) — must be overridden for production
- **No alembic migration files** exist yet (only env.py). Tables are created by SQLAlchemy `Base.metadata.create_all()` at app startup or via seed.py
- **Integration tests** use SQLite (`test.db`), not MySQL
- **Unit tests** mock the entire service layer — fast but only covers auth currently
- `.env` file can be placed at project root for configuration overrides
