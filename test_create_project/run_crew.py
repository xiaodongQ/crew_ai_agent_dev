#!/usr/bin/env python
"""
技术自媒体专家系统运行脚本
用于替代crewai run命令，解决sqlite3版本兼容性问题
"""
import os
import sys

# 添加pysqlite3以替换内置的sqlite3
try:
    import pysqlite3
    sys.modules['sqlite3'] = pysqlite3
    sys.modules['sqlite3.dbapi2'] = pysqlite3.dbapi2
except ImportError:
    print("警告: 未安装pysqlite3，请运行 'pip install pysqlite3-binary' 安装")

# 设置环境变量
if os.path.exists('.env'):
    with open('.env', 'r') as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ.setdefault(key, value)

# 设置API密钥
os.environ['OPENAI_API_KEY'] = os.environ.get('LLM_API_KEY', '')
os.environ['OPENAI_BASE_URL'] = os.environ.get('LLM_API_BASE', 'https://coding.dashscope.aliyuncs.com/v1')

def run_crew():
    """运行技术自媒体专家系统"""
    from test_create_project.crew import TestCreateProject
    
    inputs = {
        'topic': '人工智能技术',
        'platform': '微信、小红书、抖音'
    }
    
    print("启动技术自媒体专家系统...")
    print("正在分析人工智能技术在各大社交平台的运营策略...")
    
    try:
        result = TestCreateProject().crew().kickoff(inputs=inputs)
        print("\n任务完成！")
        print(f"结果: {result}")
        return result
    except Exception as e:
        print(f"运行过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    run_crew()