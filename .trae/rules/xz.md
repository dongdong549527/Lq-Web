# 项目开发规范 (Vue 3 + FastAPI)

## 1. 技术栈概览
- **前端**: Vue 3, Vite, TypeScript, Pinia, Vue Router
- **后端**: FastAPI, Python 3.10+, Pydantic, SQLAlchemy (或 Tortoise-ORM), uv (包管理器)

## 2. 前端规范 (Vue 3)

### 代码风格
- **组件写法**: 必须使用 Composition API 和 `<script setup lang="ts">`。
- **命名**:
  - 文件名: 使用 PascalCase (如 `UserProfile.vue`)。
  - 目录名: 使用 kebab-case (如 `user-profile`).
- **样式**: 推荐使用 Scoped CSS 或 Tailwind CSS。

### 最佳实践
- **响应式数据**: 优先使用 `ref` 处理基本类型，`reactive` 处理对象，但保持一致性更重要（推荐统一用 `ref` 以避免解构丢失响应性）。
- **状态管理**: 使用 Pinia 而不是 Vuex。
- **API 调用**: 将 API 请求封装在 `src/api` 目录下的模块中，不要在组件内直接调用 `axios` 或 `fetch`。
- **类型定义**: 所有的 Props 和 Emits 都应定义 TypeScript 类型。

```vue
<script setup lang="ts">
import { ref } from 'vue';
import type { User } from '@/types';

interface Props {
  initialUser: User;
}

const props = defineProps<Props>();
const emit = defineEmits<{
  (e: 'update', user: User): void;
}>();
</script>
```

## 3. 后端规范 (FastAPI)

### 代码风格
- **类型提示**: 所有函数参数和返回值必须包含 Python 类型提示 (Type Hints)。
- **异步优先**: 路由处理函数 (`path operations`) 默认为 `async def`，除非涉及阻塞 IO 且库不支持异步。

### 最佳实践
- **依赖管理**: 强制使用 `uv` 进行包管理。
  - 安装依赖: `uv pip install -r requirements.txt` 或 `uv add <package>`
  - 运行: `uv run uvicorn app.main:app --reload`
- **数据验证**: 严格使用 Pydantic 模型 (`BaseModel`) 进行请求体和响应体的验证。
- **项目结构**:
  - `app/main.py`: 入口文件
  - `app/api/`: 路由定义 (endpoints)
  - `app/core/`: 核心配置 (config, security)
  - `app/models/`: 数据库模型 (ORM models)
  - `app/schemas/`: Pydantic 模式 (DTOs)
  - `app/services/`: 业务逻辑层
- **依赖注入**: 使用 `Depends` 处理数据库会话、当前用户验证等共享逻辑。

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import UserCreate, UserResponse
from app.services import user_service
from app.core.deps import get_db

router = APIRouter()

@router.post("/", response_model=UserResponse)
async def create_user(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    return await user_service.create(db, user_in)
```

## 4. 通用规范
- **注释**: 复杂逻辑需添加注释，API 接口需编写文档字符串 (Docstrings)。
- **Git 提交**: 使用 Conventional Commits 规范 (e.g., `feat: add user login`, `fix: resolve db connection error`).
