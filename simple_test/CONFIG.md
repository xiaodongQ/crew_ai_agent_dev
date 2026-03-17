# 项目配置规范

## 环境变量配置

本项目使用 `.env` 文件管理敏感配置信息，避免将 API Key 等机密信息硬编码到代码中。

### 创建 .env 文件

在项目根目录创建 `.env` 文件，格式如下：

```env
LLM_API_KEY=your-api-key-here
LLM_API_BASE=https://coding.dashscope.aliyuncs.com/v1
LLM_MODEL=openai/qwen3.5-plus
```

### .env 文件说明

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `LLM_API_KEY` | API 密钥 | 必填 |
| `LLM_API_BASE` | API 基础 URL | 阿里云 DashScope |
| `LLM_MODEL` | 模型名称 | openai/qwen3.5-plus |

### 使用方式

在 Python 代码中通过 `python-dotenv` 读取：

```python
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("LLM_API_KEY")
api_base = os.getenv("LLM_API_BASE")
model = os.getenv("LLM_MODEL", "openai/qwen3.5-plus")
```

### 安全提示

- `.env` 文件应被加入 `.gitignore`，**不要提交到版本控制**
- 生产环境使用环境变量直接注入，而非 `.env` 文件
