# ColorQA - 专业性格色彩测试系统

这是一个高度工程化的专业性格测评系统，基于 FPA (Four-colors Personality Analysis) 性格色彩学理论开发。

## 🌟 核心特性

- **专业性**: 完整录入 30 道专业测评题，包含情感、社交、工作等维度的深度分析。
- **高性能**: 后端采用 FastAPI 异步框架，响应极快。
- **现代化 UI**: 前端使用 Vue 3 + Tailwind CSS，配合流畅的交互动画。
- **数据驱动**: 完整的数据库设计，支持用户信息存储与历史测试记录回溯。

---

## 🛠️ 技术栈

### 后端 (Backend)
- **框架**: FastAPI (异步高性能)
- **数据库**: SQLite (本地存储)
- **ORM**: SQLAlchemy 2.0 (Mapped 类型安全)
- **数据验证**: Pydantic v2

### 前端 (Frontend)
- **框架**: Vue 3 (Composition API)
- **构建**: Vite
- **状态管理**: Pinia
- **交互**: Axios (已配置 Vite Proxy 代理)

---

## 📂 项目结构

```text
ColorQA/
├── backend/                # 后端工程 (FastAPI)
│   ├── app/                # 核心业务代码
│   │   ├── api/            # 路由定义 (题目加载、结果提交)
│   │   ├── core/           # 数据库配置 (SQLAlchemy)
│   │   ├── models/         # 数据库模型
│   │   └── schemas/        # Pydantic 响应与请求模型
│   ├── main.py             # 服务入口 (运行在 8000 端口)
│   ├── color_test.db       # SQLite 数据库文件
│   └── requirements.txt    # 后端依赖
├── frontend/               # 前端工程 (Vue 3)
│   ├── src/                # 源代码 (Views, Components, Stores)
│   ├── vite.config.js      # 配置了 /api 代理转发
│   └── package.json        # 前端依赖
├── scripts/                # 工具脚本
│   └── setup_db_v2.py      # 数据库初始化与数据导入脚本
└── docs/                   # 素材文档
    └── 性格色彩测试题.md      # 原始题目素材
```

---

## 🚀 快速开始

### 1. 准备环境
确保本地已安装 Python 3.8+ 和 Node.js 环境。

### 2. 初始化数据库 (可选)
如果需要重新生成或初始化题库数据：
```bash
python scripts/setup_db_v2.py
```

### 3. 启动后端
```bash
# 安装依赖
pip install -r backend/requirements.txt

# 运行后端 (默认 8000 端口)
python backend/main.py
```
API 文档访问: `http://localhost:8000/docs`

### 4. 启动前端
```bash
cd frontend

# 安装依赖
npm install

# 运行前端 (默认 5173 端口)
npm run dev
```
访问地址: `http://localhost:5173`

---

## 📝 开发备注
- **本地代理**: 前端开发环境下，所有发往 `/api` 的请求均会由 Vite 代理转发至 `localhost:8000`。
- **数据安全**: 数据库采用异步驱动 `aiosqlite`，确保高并发下的稳定性。
