import streamlit as st
from dotenv import load_dotenv
import os

# 加载.env配置
load_dotenv()

# 首页布局
st.title("AI智能助手")
st.subheader("基于Python+LangChain+Streamlit开发")

# 显示当前配置（可选，让用户确认）
st.sidebar.title("配置信息")
st.sidebar.write(f"模型：{os.getenv('MODEL_NAME')}")
st.sidebar.write(f"温度：{os.getenv('TEMPERATURE')}")
st.sidebar.write(f"最大Token：{os.getenv('MAX_TOKENS')}")

# 引导到助手页面
st.markdown("→ 点击左侧菜单栏 **assistant** 开始对话")