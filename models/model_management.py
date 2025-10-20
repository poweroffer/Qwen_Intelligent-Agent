from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()


# 创建一个模型管理类
class MyModel:
    # 创建一个模型变量
    _llm = None
    # 创建一个词嵌入变量
    _asr = None
    # 构造函数
    def __init__(self):
        # 获取模型名称
        self._llm_name = os.getenv("LLM_NAME")
        self._asr_name = os.getenv("ASR_NAME")


    # 加载千问模型
    def get_line_model(self):
        # 懒加载机制
        if self._llm is None:
            self._llm = ChatOpenAI(model=self._llm_name)
        return self._llm

    # 加载ASR模型
    def get_asr_model(self):
        if self._asr is None:
            self._asr = ChatOpenAI(model=self._asr_name)
        return self._asr

if __name__ == '__main__':
    model = MyModel()
    llm = model.get_line_model()
    res = llm.invoke("hello world, 用一句中文诗词回答，只返回答案，不要解释。")
    print(res.content)
    asr = model.get_asr_model()
    res = asr.invoke()