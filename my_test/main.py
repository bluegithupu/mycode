import streamlit as st

# 创建一个文本输入框
user_input = st.text_input("请输入一些文本：", "")

# 创建一个按钮
if st.button("显示输入"):
    # 当按钮被点击时，显示用户输入的内容
    st.write("你输入了：", user_input)