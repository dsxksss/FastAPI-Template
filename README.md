# 🚀 企业级FastAPI后端模板

<div align="center">

**一个功能完整、架构清晰的企业级FastAPI后端模板，专为团队开发设计，开箱即用**

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Stars](https://img.shields.io/github/stars/JiayuXu0/FastAPI-Template?style=social)](https://github.com/JiayuXu0/FastAPI-Template/stargazers)
[![Forks](https://img.shields.io/github/forks/JiayuXu0/FastAPI-Template?style=social)](https://github.com/JiayuXu0/FastAPI-Template/network/members)

[![UV](https://img.shields.io/badge/📦_依赖管理-UV-blueviolet.svg)](https://github.com/astral-sh/uv)
[![Architecture](https://img.shields.io/badge/🏗️_架构-三层架构-orange.svg)](#)
[![RBAC](https://img.shields.io/badge/🔐_权限-RBAC-red.svg)](#)
[![Docker](https://img.shields.io/badge/🐳_容器-Docker-blue.svg)](https://www.docker.com/)

[📖 快速开始](#-快速开始) • [🏗️ 架构说明](#-架构说明) • [📚 开发指南](CLAUDE.md) • [🤝 贡献指南](CONTRIBUTING.md) • [🌟 给个Star!](https://github.com/JiayuXu0/FastAPI-Template)

</div>

---

## 🌟 为什么选择这个模板？

<div align="center">

| 🎯 **企业级标准** | ⚡ **开箱即用** | 🛡️ **安全可靠** | 📈 **性能优秀** |
|:---:|:---:|:---:|:---:|
| 三层架构设计<br/>规范清晰 | 5分钟启动项目<br/>零配置烦恼 | RBAC权限控制<br/>多重安全防护 | 异步高并发<br/>现代化技术栈 |

</div>

## ✨ 核心特性

### 🔐 认证与权限
- **JWT身份认证** - 基于HS256算法的安全token认证
- **RBAC权限控制** - 角色基础访问控制，支持细粒度API权限
- **用户管理** - 完整的用户注册、登录、权限分配功能
- **角色管理** - 灵活的角色定义和权限分配

### 🗂️ 数据管理
- **菜单管理** - 动态菜单配置，支持多级菜单结构
- **API管理** - 自动化API权限配置和管理
- **部门管理** - 组织架构管理，支持层级结构
- **文件管理** - 安全的文件上传、下载、存储功能

### 🛡️ 安全防护
- **文件安全** - 文件类型验证、大小限制、恶意文件检测
- **安全头** - 自动XSS、CSRF、点击劫持防护
- **CORS配置** - 严格的跨域访问控制
- **审计日志** - 完整的用户操作记录和追踪

### 🏗️ 架构设计
- **三层架构** - API → Service → Controller → Model 清晰分层
- **异步支持** - 全异步设计，高性能处理
- **数据库迁移** - 基于Aerich的版本化数据库管理
- **类型安全** - 完整的Python类型注解

## 🛠️ 技术栈

| 组件 | 技术选型 | 版本要求 |
|------|----------|----------|
| **语言** | Python | 3.11+ |
| **Web框架** | FastAPI | 0.100+ |
| **数据库ORM** | Tortoise ORM | 0.20+ |
| **数据库** | SQLite/PostgreSQL | - |
| **身份认证** | PyJWT | 2.8+ |
| **数据验证** | Pydantic | 2.0+ |
| **数据库迁移** | Aerich | 0.7+ |
| **包管理** | UV | latest |
| **日志** | Loguru | 0.7+ |

## 📁 项目结构

```
evoai-backend-template/
├── src/                          # 📦 源代码目录
│   ├── api/v1/                   # 🌐 API路由层 (轻量化路由)
│   │   ├── users/               # 👥 用户管理API
│   │   ├── roles/               # 👑 角色管理API
│   │   ├── menus/               # 📋 菜单管理API
│   │   ├── files/               # 📁 文件管理API
│   │   └── ...
│   ├── services/                 # 🔧 业务逻辑层 (核心业务)
│   │   ├── base_service.py      # 🏗️ 服务基类和权限服务
│   │   ├── user_service.py      # 👤 用户业务逻辑
│   │   ├── file_service.py      # 📄 文件业务逻辑
│   │   └── ...
│   ├── controllers/              # 🗄️ 数据访问层 (CRUD操作)
│   ├── models/                   # 📊 数据模型层
│   │   ├── admin.py             # 👨‍💼 用户角色模型
│   │   ├── base.py              # 🔷 基础模型类
│   │   └── enums.py             # 📝 枚举定义
│   ├── schemas/                  # ✅ 数据验证层
│   ├── core/                     # ⚙️ 核心功能
│   │   ├── dependency.py        # 🔗 依赖注入
│   │   ├── middlewares.py       # 🛡️ 中间件
│   │   └── init_app.py          # 🚀 应用初始化
│   ├── utils/                    # 🔧 工具函数
│   └── settings/                 # ⚙️ 配置管理
├── migrations/                   # 📈 数据库迁移文件
├── tests/                        # 🧪 测试文件
├── uploads/                      # 📂 文件上传目录
├── logs/                         # 📋 日志文件
├── pyproject.toml               # 📦 UV项目配置
├── .env                         # 🔐 环境变量配置
└── CLAUDE.md                    # 🤖 Claude开发指南
```

## 🚀 快速开始

### 1. 环境准备

```bash
# 安装UV包管理器
curl -LsSf https://astral.sh/uv/install.sh | sh

# 克隆项目
git clone <your-repo-url>
cd evoai-backend-template

# 安装依赖
uv sync
```

### 2. 🔐 环境配置

**复制环境配置文件：**
```bash
cp .env.example .env
```

**⚠️ 必须修改的安全配置：**

| 配置项 | 说明 | 生成方式 |
|--------|------|----------|
| `SECRET_KEY` | JWT签名密钥 | `openssl rand -hex 32` |
| `SWAGGER_UI_PASSWORD` | API文档访问密码 | 设置强密码 |
| `DB_PASSWORD` | 数据库密码 | 设置强密码 |

**配置示例：**
```bash
# 基础配置
SECRET_KEY=your_generated_secret_key_here
APP_TITLE=你的项目名称
PROJECT_NAME=YourProject

# 数据库配置 (开发环境推荐SQLite)
DB_ENGINE=sqlite
DB_PASSWORD=your_strong_password

# API文档保护
SWAGGER_UI_USERNAME=admin
SWAGGER_UI_PASSWORD=your_strong_password

# CORS配置
CORS_ORIGINS=http://localhost:3000,http://localhost:8080
```

### 3. 数据库初始化

```bash
uv run aerich init-db
```

### 4. 启动服务

```bash
# 开发模式
uv run uvicorn src:app --reload --host 0.0.0.0 --port 8000

# 生产模式
uv run uvicorn src:app --host 0.0.0.0 --port 8000 --workers 4
```

### 5. 访问服务

- **API文档**: http://localhost:8000/docs
- **替代文档**: http://localhost:8000/redoc
- **健康检查**: http://localhost:8000/api/v1/base/health

### 6. 默认账号

```
用户名: admin
密码: 123456
邮箱: admin@admin.com
```

**🚨 首次登录后立即修改密码！**

---

## 📊 项目统计

<div align="center">

![GitHub repo size](https://img.shields.io/github/repo-size/JiayuXu0/FastAPI-Template)
![GitHub code size](https://img.shields.io/github/languages/code-size/JiayuXu0/FastAPI-Template)
![Lines of code](https://img.shields.io/tokei/lines/github/JiayuXu0/FastAPI-Template)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/JiayuXu0/FastAPI-Template)

</div>

## 🎉 成功案例

> 💡 **已有多个团队使用此模板快速搭建生产级后端服务**

- 🏢 **企业管理系统** - 支持10万+用户的权限管理平台
- 🛒 **电商后台** - 高并发订单处理系统  
- 📱 **移动应用API** - 微服务架构的用户中心
- 🎯 **SaaS平台** - 多租户权限隔离系统

**👥 如果你也在使用这个模板，[告诉我们](https://github.com/JiayuXu0/FastAPI-Template/discussions)你的使用案例！**

## 🏗️ 架构说明

### 三层架构模式

```
┌─────────────────┐
│   API Layer     │  ← 路由分发、参数验证
│  (api/v1/)      │
├─────────────────┤
│  Service Layer  │  ← 业务逻辑、权限检查
│  (services/)    │
├─────────────────┤
│Controller Layer │  ← 数据库操作、CRUD
│ (controllers/)  │
├─────────────────┤
│  Model Layer    │  ← 数据模型定义
│   (models/)     │
└─────────────────┘
```

### 核心设计原则

1. **单一职责** - 每层只处理自己的逻辑
2. **依赖注入** - 通过FastAPI依赖系统管理
3. **类型安全** - 完整的Python类型注解
4. **异步优先** - 全异步设计，高并发支持
5. **安全第一** - 内置多重安全防护机制

## 📚 开发指南

### 添加新功能

1. **定义数据模型** (`models/`)
2. **创建数据Schema** (`schemas/`)
3. **实现Controller** (`controllers/`)
4. **编写Service业务逻辑** (`services/`)
5. **添加API路由** (`api/v1/`)
6. **生成数据库迁移** (`aerich migrate`)

详细步骤请参考 [CLAUDE.md](CLAUDE.md) 开发指南。

### 数据库操作

```bash
# 生成迁移文件
uv run aerich migrate --name "add_new_feature"

# 应用迁移
uv run aerich upgrade

# 查看迁移历史
uv run aerich history
```

### 测试

```bash
# 运行所有测试
uv run pytest

# 运行特定测试
uv run pytest tests/test_users.py

# 生成覆盖率报告
uv run pytest --cov=src --cov-report=html
```

## 🔒 安全最佳实践

### 生产环境安全检查

- [ ] **SECRET_KEY** 使用随机生成的64位字符串
- [ ] **密码强度** 所有密码至少12位，包含大小写字母、数字、特殊字符
- [ ] **DEBUG模式** 生产环境设置 `DEBUG=False`
- [ ] **CORS配置** 设置具体域名，不使用通配符 `*`
- [ ] **HTTPS** 生产环境启用HTTPS
- [ ] **数据库安全** 使用独立数据库账号，限制权限
- [ ] **日志安全** 确保日志中不包含敏感信息

### 文件上传安全

- 支持的文件类型白名单验证
- 文件大小限制 (默认500MB)
- 危险文件类型黑名单检测
- 安全的文件名生成机制
- 本地文件存储 (可扩展至云存储)

## 🔧 配置说明

### 环境变量

| 变量名 | 必填 | 默认值 | 说明 |
|--------|------|--------|------|
| `SECRET_KEY` | ✅ | - | JWT签名密钥 |
| `APP_TITLE` | ❌ | Vue FastAPI Admin | 应用标题 |
| `DB_ENGINE` | ❌ | postgres | 数据库类型 |
| `DB_HOST` | ❌ | localhost | 数据库主机 |
| `CORS_ORIGINS` | ❌ | localhost:3000 | 允许的CORS源 |
| `DEBUG` | ❌ | True | 调试模式 |

### 数据库支持

- **SQLite** - 适合开发和小型部署
- **PostgreSQL** - 推荐生产环境使用

## 📈 性能优化

- **异步处理** - 全异步架构，支持高并发
- **连接池** - 数据库连接池管理
- **中间件** - 请求压缩、缓存头设置
- **日志优化** - 结构化日志，性能监控

## 🤝 贡献指南

1. Fork 项目仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交改动 (`git commit -m 'Add some amazing feature'`)
4. 推送分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

### 代码规范

- 遵循 **PEP 8** 编码规范
- 使用 **Google风格** 文档字符串
- 添加 **类型注解** 到所有函数
- 编写 **单元测试** 覆盖关键功能

## 📄 许可证

本项目基于 [MIT License](LICENSE) 开源协议。

## 🔗 相关链接

- [FastAPI官方文档](https://fastapi.tiangolo.com/)
- [Tortoise ORM文档](https://tortoise.github.io/)
- [UV包管理器](https://github.com/astral-sh/uv)
- [Claude Code文档](https://docs.anthropic.com/en/docs/claude-code)

---

## 🆘 获取帮助

如果您在使用过程中遇到问题：

1. 📖 查看 [CLAUDE.md](CLAUDE.md) 详细开发指南
2. 🔍 查看 [Issues](../../issues) 查找类似问题
3. 💬 创建新的 [Issue](../../issues/new) 描述问题
4. 📧 联系维护者

**开箱即用，专业可靠的企业级FastAPI后端模板** 🚀

---

## 🏆 特色亮点

<div align="center">

### 🚀 快速上手
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
git clone https://github.com/JiayuXu0/FastAPI-Template.git
cd FastAPI-Template && uv sync && cp .env.example .env
uv run aerich init-db && uv run uvicorn src:app --reload
# 🎉 5分钟内即可启动完整的企业级后端服务！
```

### 💎 技术栈对比

| 传统方案 ❌ | 本模板 ✅ |
|:---:|:---:|
| 复杂的环境配置 | UV一键管理依赖 |
| 混乱的项目结构 | 清晰的三层架构 |
| 手动权限管理 | 完整RBAC系统 |
| 缺乏安全防护 | 多重安全机制 |
| 文档不完善 | 详细开发指南 |

</div>

## 🌟 社区支持

<div align="center">

**加入我们的开发者社区，一起打造更好的后端模板！**

[![GitHub Discussions](https://img.shields.io/github/discussions/JiayuXu0/FastAPI-Template?color=blue&logo=github)](https://github.com/JiayuXu0/FastAPI-Template/discussions)
[![GitHub Issues](https://img.shields.io/github/issues/JiayuXu0/FastAPI-Template?color=green&logo=github)](https://github.com/JiayuXu0/FastAPI-Template/issues)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/JiayuXu0/FastAPI-Template?color=orange&logo=github)](https://github.com/JiayuXu0/FastAPI-Template/pulls)

[💬 讨论交流](https://github.com/JiayuXu0/FastAPI-Template/discussions) • [🐛 报告问题](https://github.com/JiayuXu0/FastAPI-Template/issues) • [🔀 提交PR](https://github.com/JiayuXu0/FastAPI-Template/pulls) • [📧 联系作者](mailto:jiayuxu@example.com)

</div>

## 🎯 路线图

- [x] ✅ **v1.0** - 基础三层架构和RBAC系统
- [x] ✅ **v1.1** - UV包管理器集成
- [ ] 🚧 **v1.2** - GraphQL API支持
- [ ] 📅 **v1.3** - 微服务架构扩展
- [ ] 📅 **v1.4** - 实时通信 (WebSocket)
- [ ] 📅 **v2.0** - 云原生部署方案

[查看完整路线图 →](https://github.com/JiayuXu0/FastAPI-Template/projects)