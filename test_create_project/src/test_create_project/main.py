#!/usr/bin/env python
import os
import sys
from test_create_project.crew import TestCreateProject

# 替换sqlite3以避免问题
sys.modules['sqlite3'] = __import__('pysqlite3')
sys.modules['sqlite3.dbapi2'] = __import__('pysqlite3.dbapi2')

def run():
    """
    Run the crew.
    """
    inputs = {
        'topic': '人工智能技术'
    }
    try:
        # 设置API密钥
        if os.path.exists('.env'):
            with open('.env', 'r') as f:
                for line in f:
                    if line.strip() and not line.startswith('#'):
                        key, value = line.strip().split('=', 1)
                        os.environ.setdefault(key, value)
        
        # 运行crew
        result = TestCreateProject().crew().kickoff(inputs=inputs)
        print(f"最终结果:\n{result}")
        return result
    except Exception as e:
        print(f"运行crew时发生错误: {e}")
        import traceback
        traceback.print_exc()

def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "人工智能技术"
    }
    try:
        TestCreateProject().crew().train(n_iterations=5, filename='training_data.json', inputs=inputs)
    except Exception as e:
        raise Exception(f"训练过程中发生错误: {e}")

def replay(task_id: str):
    """
    Replay the crew execution from a specific task.
    """
    try:
        TestCreateProject().crew().replay(task_id=task_id)
    except Exception as e:
        raise Exception(f"重放过程中发生错误: {e}")

def test():
    """
    Test the crew for a given number of iterations.
    """
    inputs = {
        "topic": "人工智能技术"
    }
    try:
        iterations = int(input("请输入测试迭代次数 (默认为1): ") or 1)
        TestCreateProject().crew().test(n_iterations=iterations, openai_model_name="gpt-4o", inputs=inputs)
    except Exception as e:
        raise Exception(f"测试过程中发生错误: {e}")

if __name__ == '__main__':
    run()