# First
import openai 
import streamlit as st
import openai
import interpreter

if 'OpenAI_api_key' not in st.session_state:
    st.session_state.OpenAI_api_key = ''
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

st.set_page_config(
   page_title="Open-Interpreter Gpt App",
   page_icon="🤖",
   layout="wide",
   initial_sidebar_state="expanded",
)

st.title("💬 Open Interpreter")

with st.sidebar:
    def submit():
        try:
            st.session_state.OpenAI_api_key = st.session_state.widget
            openai.api_key = st.session_state.OpenAI_api_key
            respuesta = openai.ChatCompletion.create(
            model="gpt-4-0613",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Hello!"}
            ]
            )
            interpreter.api_key = st.session_state.OpenAI_api_key
        except Exception as e:
            print(e)
            # st.session_state.OpenAI_api_key = st.session_state.widget
            st.session_state.widget = ''
            # st.session_state.OpenAI_api_key = ''
            st.info("Please add your OpenAI API key Correctly to continue.")
            # st.stop()

    st.text_input('OpenAI API Key', key='widget', on_change=submit, type="password")


for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input(placeholder="Write here your message", disabled=not st.session_state.OpenAI_api_key):

    openai.api_key = st.session_state.OpenAI_api_key
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = interpreter.chat(prompt)
    st.session_state.messages.append(response)
    st.chat_message("assistant").write(response)