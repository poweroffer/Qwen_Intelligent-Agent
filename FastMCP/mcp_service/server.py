from fastmcp import FastMCP
from email_service.email_service import send_email_tool
from database_service.neo4j_service import neo4j_tool_pool
from database_service.sql_service import sql_tool_pool
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# 1.定义mcp应用程序
mcp = FastMCP(
    name="mcp服务",
    version="0.1.0",
)
# 2.定义mcp工具

@mcp.tool(name="neo4j_tool",description="neo4j工具,执行cypher语句")
def neo4j_tool(query: str) -> str:
    """
    cypher语句查询
    :param query: cypher语句
    :return: 答案
    """
    rs = neo4j_tool_pool(query)
    return rs

@mcp.tool(name="sql_tool_pool",description="sql工具,执行sql语句")
def sql_tool(query: str) -> str:
    """
    sql语句查询
    :param query: sql语句
    :return: 答案
    """
    rs = sql_tool_pool(query)
    return rs

@mcp.tool(name="send_email_tool",description="邮件发送工具")
def send_email(to_email: str, content: str, subject: str) -> str:
    """
    邮件发送
    :param to_email: 收件人邮箱
    :param subject: 邮件主题
    :param content: 邮件内容
    :return: 答案
    """
    rs = send_email_tool(to_email, subject, content)
    return rs

if __name__ == '__main__':
    mcp.run(
        host="0.0.0.0", # 监听所有ip
        port=8008,
        transport="sse" # sse传输方式
    )