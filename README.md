# ColorQA - 性格色彩测试系统

这是一个高度工程化的前后端分离系统。

## 技术栈 (Modern Stack)

### 后端 (Backend)
- **框架**: FastAPI (异步高性能)
- **ORM**: SQLAlchemy 2.0 (采用 `Mapped` 类型安全模式)
- **验证**: Pydantic v2 (严谨的数据建模)
- **数据库**: SQLite

### 前端 (Frontend)
- **框架**: Vue 3 (Composition API)
- **构建**: Vite
- **状态管理**: Pinia
- **样式**: Tailwind CSS (原子化 CSS)
- **网络**: Axios

```text
ColorQA/
├── backend/                # 后端工程 (FastAPI)
│   ├── app/                # 核心逻辑
│   │   ├── api/            # 接口定义 (待实现: questions, records)
│   │   ├── core/           # 数据库连接与安全配置
│   │   ├── models/         # SQLAlchemy 数据库模型 (与设计稿 5 表对应)
│   │   └── schemas/        # Pydantic 数据验证
│   ├── main.py             # FastAPI 入口文件
│   ├── color_test.db       # 已生成的 SQLite 数据库 (30题已录入)
│   └── requirements.txt    # 后端依赖
├── frontend/               # 前端工程 (Vue 3 + Vite)
│   ├── src/                # 源代码
│   ├── package.json        # 前端依赖
│   └── vite.config.js      # Vite 配置
├── docs/                   # 项目文档与原始素材
│   └── 性格色彩测试题.md     # 题目与评分标准对照表
├── scripts/                # 运维与工具脚本 (如数据库初始化)
└── README.md
```

## 快速开始

### 1. 启动后端
```bash
cd backend
pip install -r requirements.txt
python main.py
```
后端 API 地址: `http://localhost:8000`
文档地址: `http://localhost:8000/docs` (FastAPI 自动生成)

### 2. 启动前端
```bash
cd frontend
npm install
npm run dev
```
前端开发地址: `http://localhost:5173`

## 开发准则
本项目遵循 **Karpathy Guidelines**:
1. **简洁优先**: 代码保持精简，避免过度封装。
2. **目标驱动**: 所有开发均围绕“答题-评分-展示结果”这一核心链路。
3. **精准修改**: 对现有数据库表结构的修改需同步更新 `backend/app/models/database.py`。
