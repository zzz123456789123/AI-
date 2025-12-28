import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage
import tiktoken
import time
import os

# 初始化配置
load_dotenv()
model = ChatOpenAI(
    api_key=os.getenv("API_KEY"),
    base_url=os.getenv("BASE_URL"),
    model=os.getenv("MODEL_NAME"),
    temperature=float(os.getenv("TEMPERATURE")),
    max_tokens=int(os.getenv("MAX_TOKENS"))
)


# Token计数器（按模型适配）
def count_tokens(messages):
    encoding = tiktoken.encoding_for_model(os.getenv("MODEL_NAME"))
    total = 0
    for msg in messages:
        total += len(encoding.encode(msg.content))
    return total


# 初始化对话历史（Streamlit会话存储）
if "messages" not in st.session_state:
    st.session_state.messages = [SystemMessage(content="你是一个实用的AI助手")]

# 页面布局
st.title("AI对话助手")

# 提示词自定义（侧边栏）
st.sidebar.title("提示词设置")
system_prompt = st.sidebar.text_area(
    "系统提示词（自定义AI角色）",
    value=st.session_state.messages[0].content,
    key="system_prompt"
)
# 更新系统提示词
if st.sidebar.button("应用提示词"):
    st.session_state.messages[0] = SystemMessage(content=system_prompt)
    st.rerun()

# 显示对话历史
for msg in st.session_state.messages[1:]:  # 跳过系统提示词（不显示）
    role = "user" if isinstance(msg, HumanMessage) else "assistant"
    with st.chat_message(role):
        st.markdown(msg.content)

# 实时统计信息（侧边栏）
token_count = count_tokens(st.session_state.messages)
st.sidebar.subheader("实时统计")
st.sidebar.write(f"已用Token：{token_count}/{os.getenv('MAX_TOKENS')}")

# 用户输入与模型响应
if user_input := st.chat_input("请输入你的问题..."):
    # 添加用户消息到历史
    user_msg = HumanMessage(content=user_input)
    st.session_state.messages.append(user_msg)
    with st.chat_message("user"):
        st.markdown(user_input)

    # 模型响应（流式输出+耗时统计）
    start_time = time.time()
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        # 流式调用模型
        for chunk in model.stream(st.session_state.messages):
            full_response += chunk.content
            response_placeholder.markdown(full_response + "▌")
        response_placeholder.markdown(full_response)
    end_time = time.time()

    # 添加助手消息到历史
    st.session_state.messages.append(AIMessage(content=full_response))

    # 显示耗时
    st.sidebar.write(f"响应耗时：{end_time - start_time:.2f}秒")

# 清空对话历史（侧边栏）
if st.sidebar.button("清空对话"):
    st.session_state.messages = [SystemMessage(content=system_prompt)]
    st.rerun()