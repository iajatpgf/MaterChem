import streamlit as st
from langchain.memory import ConversationBufferMemory
from utils import get_chat_response

st.title("克隆ChatGPT")

with st.sidebar:
    openai_api_key = st.text_input("请输入OpenAI API Key：", type="password")
    st.markdown("[获取OpenAI API key](https://platform.openai.com/account/api-keys)")
    st.subheader('请选择所要使用的模型')
    "温馨提示，默认使用gpt-3.5模型，若想得到更好的回复，请选择gpt-4模型，但是更贵，约4分/字"
    selected_model = st.sidebar.selectbox('选择一个模型', ['gpt-3.5-turbo', 'gpt-4-0125-preview'], key='selected_model')

if "memory" not in st.session_state:
    st.session_state["memory"] = ConversationBufferMemory(return_messages=True)
    st.session_state["messages"] = [{"role": "ai",
                                     "content": "你好，我是你的AI助手，有什么可以帮你的吗？"}]

with st.sidebar:# 添加一个按钮，点击后重新设置会话状态
    if st.button('重新开始'):
        st.session_state["memory"] = ConversationBufferMemory(return_messages=True)
        st.session_state["messages"] = [{"role": "ai",
                                     "content": "你好，我是你的AI助手，有什么可以帮你的吗？"}]

for message in st.session_state["messages"]:
    st.chat_message(message["role"]).write(message["content"])
    if (len(st.session_state["messages"])) == 1:
        st.write("""你可以这样问我:
        
        '你是一个广告公司的创意总监，帮我的产品写一段宣传语，产品是xxx，特点是xxx'
        
        '你是一个大学教授，帮我写一篇英文文章的摘要，主题是xxx'
        
        '扩写一下这个主题，300字左右，要求立意深刻’
        
        ‘帮我润色以下这段内容，内容部分以3个#隔开，###here is your content###'""")

prompt = st.chat_input()
if prompt:
    if not openai_api_key:
        st.info("请输入你的OpenAI API Key")
        st.stop()
    st.session_state["messages"].append({"role": "human", "content": prompt})
    st.chat_message("human").write(prompt)

    with st.spinner("AI正在思考中，请稍等..."):
        response = get_chat_response(selected_model, prompt, st.session_state["memory"],
                                     openai_api_key)
    msg = {"role": "ai", "content": response}
    st.session_state["messages"].append(msg)
    st.chat_message("ai").write(response)