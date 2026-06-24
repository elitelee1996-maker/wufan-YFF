# 平安快运 · 项目计划与进度管控系统

Standard模式：FastAPI + React + PostgreSQL

## 项目结构

```
pingan_pm/
├── backend/
│   ├── main.py              # FastAPI入口
│   ├── config/
│   │   ├── settings.py      # 环境配置
│   │   └── field_mapping.json # 字段映射表(Phase 3回填)
│   ├── services/
│   │   ├── jdy_client.py    # 简道云API客户端
│   │   ├── field_mapper.py  # 字段映射服务
│   │   ├── cpm_engine.py    # CPM调度引擎
│   │   ├── wbs_calculator.py # WBS编码计算
│   │   ├── schedule_service.py # 进度排程服务
│   │   ├── template_importer.py # 模板导入服务
│   │   ├── resource_scheduler.py # 资源调度服务
│   │   └── baseline_manager.py # 基线管理服务
│   ├── api/
│   │   ├── auth_api.py      # 认证API
│   │   ├── template_api.py  # 模板管理API
│   │   ├── wbs_api.py       # WBS编制API
│   │   ├── schedule_api.py  # 进度排程API
│   │   ├── resource_api.py  # 资源管理API
│   │   └── monitoring_api.py # 执行监控API
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── App.jsx          # 路由配置
│   │   ├── pages/           # 页面组件
│   │   └── services/api.js  # API客户端
│   ├── package.json
│   └── vite.config.js
├── static/                  # Phase 2原型(生产页面)
└── docs/                    # 项目文档
```

## 快速启动

```bash
# 后端
cd backend
cp .env.example .env  # 填入JDY_API_KEY
pip install -r requirements.txt
uvicorn main:app --reload

# 前端
cd frontend
npm install
npm run dev
```

## 健康检查

```bash
curl http://localhost:8000/api/health
```
