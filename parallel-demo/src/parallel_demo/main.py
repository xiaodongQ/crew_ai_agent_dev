#!/usr/bin/env python3
"""
CrewAI 并行执行演示 - 主入口

使用方法:
    python -m parallel_demo.main [主题]
    
示例:
    python -m parallel_demo.main 人工智能技术
    python -m parallel_demo.main Python 编程入门
"""

import os
import sys

# 修复 sqlite3 问题
try:
    import pysqlite3
    sys.modules['sqlite3'] = pysqlite3
    sys.modules['sqlite3.dbapi2'] = pysqlite3.dbapi2
except ImportError:
    pass


def main():
    """主函数"""
    from parallel_demo.crew import run_parallel_demo
    
    # 读取命令行参数
    topic = sys.argv[1] if len(sys.argv) > 1 else "人工智能技术"
    
    # 加载环境变量
    env_file = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
    if os.path.exists(env_file):
        print(f"📖 加载环境变量：{env_file}")
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    if '=' in line:
                        key, value = line.split('=', 1)
                        os.environ.setdefault(key.strip(), value.strip())
    
    # 验证环境变量
    api_key = os.getenv('LLM_API_KEY')
    api_base = os.getenv('LLM_API_BASE')
    
    if not api_key:
        print("⚠️  警告：未设置 LLM_API_KEY")
        print("   请确保 .env 文件中包含 LLM_API_KEY=your-api-key")
        print()
    
    if not api_base:
        print("⚠️  警告：未设置 LLM_API_BASE")
        print("   建议设置：LLM_API_BASE=https://coding.dashscope.aliyuncs.com/v1")
        print()
    
    print("="*60)
    print("🔧 环境信息:")
    print(f"   LLM_API_KEY: {'已设置' if api_key else '❌ 未设置'}")
    print(f"   LLM_API_BASE: {api_base or '❌ 未设置'}")
    print(f"   LLM_MODEL: {os.getenv('LLM_MODEL', 'openai/qwen3.5-plus')}")
    print("="*60)
    print()
    
    # 执行并行演示
    result = run_parallel_demo(topic)
    
    return result


if __name__ == "__main__":
    main()
