# 融通金 App

黄金回收/交易平台

## 技术栈

- **前端**: React Native (Expo) + TypeScript
- **后端**: FastAPI (Python)
- **数据库**: MySQL
- **测试**: pytest

## 项目结构

```
rongtongjin/
├── frontend/          # React Native 前端
├── backend/           # FastAPI 后端
└── docs/              # 文档
```

## 快速开始

### 后端

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# 配置数据库连接后
alembic upgrade head
uvicorn app.main:app --reload
```

### 前端

```bash
cd frontend
npm install
npx expo start
```
