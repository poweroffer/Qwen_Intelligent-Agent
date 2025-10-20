import requests
import subprocess
import sys
from typing import Optional, Dict, Any
from mcp.server.fastmcp import FastMCP
from mcp import Tool
import PIL
import pyautogui
import logging
USER_AGENT = "weather-app/1.0"
mcp = FastMCP("tools",port=8087)


 # 也可以换成百度/谷歌

@mcp.tool()
async def get_url_content(url:str)->str:
    '''
    传入一个百度笔记的连接获取该链接中的内容
    :param url: 百度笔记的链接
    :return: （字符串）链接的内容
    '''
    service = Service(executable_path=r"D:\tools\chromedriver-win64\chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            // 覆盖navigator.webdriver为undefined（模拟正常浏览器）
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
            // 修复window.chrome属性（部分检测会检查这个）
            window.chrome = {
                runtime: {},
                // 其他需要的属性可根据网页检测逻辑补充
            };
            // 修复屏幕分辨率和颜色深度（避免异常值）
            Object.defineProperty(screen, 'width', {get: () => 1920});
            Object.defineProperty(screen, 'height', {get: () => 1080});
            Object.defineProperty(screen, 'colorDepth', {get: () => 24});
        """
    })
    note_tab = None
    try:
        note_tab = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.CLASS_NAME, 'content')
            )
        )
    except:
        try:
            note_tab = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable(
                    (By.ID, 'scroll-area')
                )
            )
        except:
            pass
    if note_tab is None:
        return "None"
    res = note_tab.text
    return res

@mcp.tool()
def get_RAG_konwledge(question: str) -> str:
    """
    传入问题可以获得问题相关的知识（仅包括全国各地的风俗，习惯，特色，特点。）
    :param question: 问题
    :return: 搜索到的结果
    """
    embbing_question = model.encode(f"{question}").tolist()
    search_params = {
        "metric_type": "COSINE",  # 也可以是 IP、COSINE
        "params": {"nprobe": 10}
    }
    results = collection.search(
        data=[embbing_question],  # 查询向量
        anns_field="embedding",  # 向量字段名
        param=search_params,
        limit=30,  # 返回前5个
        output_fields=["id", "text"]  # 额外返回的标量字段
    )
    contents = []
    for hits in results:
        for hit in hits:
            contents.append(hit.entity.get("text"))

    data = {
        "model": "/bge-reranker-base",
        "query": question,
        "documents": contents
    }
    url = "http://192.168.175.1:8009/rerank"
    header = {
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=data, headers=header).json()
    lis = []
    num = 0

    for j in response['results']:
        lis.append(j['document']['text'])
        num += 1
        if num >= 5 or j['relevance_score'] < 0.6:
            break
    return "\n".join(lis)
@mcp.tool()
async def get_weather(city: str) -> str:
    """
    Get weather for a city.
    :param city: 城市名 或者 城市编码
    :return: 天气消息
    """
    key = "650f7b3e859077d9257fadfdcf09700d"
    weather = requests.get(
        f"https://restapi.amap.com/v3/weather/weatherInfo?key={key}&city={city}&extensions=all"
    )
    print("天气信息：", weather.json())
    # 拼接为字符串
    result = f"{city}的天气信息如下： {str(weather.json()["forecasts"])}"
    # for k, v in weather.json()["lives"][0].items():
    #     result += f"{k}: {v}\n"
    return result
# @mcp.tool()
# async def write_code(code: str, save_path: str) -> str:
#     """
#     将代码写入指定路径
#     :param code: 代码
#     :param save_path: 保存路径
#     :return: 工具调用结果
#     """
#     with open(save_path, "w", encoding="utf-8") as f:
#         f.write(code)
#     return f"工具调用成功：代码已保存到{save_path}"
# @mcp.tool()
# def run_python_file(
#     file_path: str,
#     timeout: Optional[float] = 10.0,
#     python_path: Optional[str] = None,
# ) -> Dict[str, Any]:
#     """
#     在独立子进程中执行一个已有的 .py 文件（单线程安全）。
#
#     :param file_path: Python 文件路径
#     :param timeout: 超时时间（秒）
#     :param python_path: 指定 Python 解释器，不填则用当前解释器
#     :return: dict 包含 stdout / stderr / exit_code / timed_out
#     """
#     python_exe = python_path or sys.executable
#     try:
#         completed = subprocess.run(
#             [python_exe, file_path],
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE,
#             text=True,
#             encoding="utf-8",
#             timeout=timeout,
#             check=False
#         )
#         return {
#             "stdout": completed.stdout,
#             "stderr": completed.stderr,
#             "exit_code": completed.returncode,
#             "timed_out": False
#         }
#
#     except subprocess.TimeoutExpired as e:
#         return {
#             "stdout": e.stdout,
#             "stderr": e.stderr,
#             "exit_code": None,
#             "timed_out": True
#         }

if __name__ == "__main__":
    print("MY HTTP MCP Server 已启动，监听客户端请求...")
    mcp.run(transport="streamable-http")