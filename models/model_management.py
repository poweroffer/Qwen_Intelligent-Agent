from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()


# 创建一个模型管理类
class LLMModel:
    # 创建一个模型变量
    _llm = None

    # 构造函数
    def __init__(self):
        # 获取模型名称
        self._llm_name = os.getenv("LLM_NAME")

    # 加载千问模型
    def get_line_model(self):
        # 懒加载机制
        if self._llm is None:
            self._llm = ChatOpenAI(model=self._llm_name)
        return self._llm

if __name__ == '__main__':
    model = LLMModel()
    llm = model.get_line_model()
    res = llm.invoke("hello world, 用一句中文诗词回答，只返回答案，不要解释。")
    print(res.content)