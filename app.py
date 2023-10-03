# First
from streamlit.components.v1 import html
from streamlit_extras.add_vertical_space import add_vertical_space
import openai
# import json
import streamlit as st
import openai
import interpreter

if 'OpenAI_api_key' not in st.session_state:
    st.session_state.OpenAI_api_key = ''
if "messages" not in st.session_state:
    st.session_state["messages"] = []
    # [{"role": "assistant", "content": "How can I help you?"}]

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
            model="gpt-3.5-turbo-0613",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Hello!"}
            ]
            )
            interpreter.api_key = st.session_state.OpenAI_api_key
            interpreter.auto_run = True
        except Exception as e:
            print(e)
            st.session_state.widget = ''
            st.session_state.OpenAI_api_key = ''
            st.info("Please add your OpenAI API key Correctly to continue.")

    st.text_input('OpenAI API Key', key='widget', on_change=submit, type="password")

    add_vertical_space(29)
    html_chat = '<center><h5>🤗 Soporta el proyecto con una donación para el desarrollo de nuevas Características 🤗</h5>'
    st.markdown(html_chat, unsafe_allow_html=True)
    button = '<script type="text/javascript" src="https://cdnjs.buymeacoffee.com/1.0.0/button.prod.min.js" data-name="bmc-button" data-slug="blazzmocompany" data-color="#FFDD00" data-emoji=""  data-font="Cookie" data-text="Buy me a coffee" data-outline-color="#000000" data-font-color="#000000" data-coffee-color="#ffffff" ></script>'
    html(button, height=70, width=220)
    iframe = '<style>iframe[width="220"]{position: absolute; top: 50%;left: 50%;transform: translate(-50%, -50%);margin:26px 0}</style>'
    st.markdown(iframe, unsafe_allow_html=True)
    add_vertical_space(2)
    st.write('<center><h6>Hecho con ❤️ por <a href="mailto:blazzmo.company@gmail.com">AI-Programming</a></h6>',unsafe_allow_html=True)

# st.write(st.session_state)
for msg in st.session_state.messages:
    if msg["role"]=="user":
        st.chat_message(msg["role"]).text(msg["content"])
    elif msg["role"]=="assistant":
        st.chat_message(msg["role"]).markdown(msg["content"])

if prompt := st.chat_input(placeholder="Write here your message", disabled=not st.session_state.OpenAI_api_key):
    st.write(interpreter.messages)

    interpreter.model = "gpt-3.5-turbo"
    
    with st.chat_message("user"):
        st.text(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        # Initialize variables
        full_response = ""
        message_placeholder = st.empty()
        for chunk in interpreter.chat(prompt, display=False, stream=True):
            
            # Message
            if "message" in chunk:
                full_response += chunk["message"]
                if chunk['message'] == ":":
                    full_response += "\n"

            # Code
            if "code" in chunk:
              # Handle code lines
              if full_response.endswith("```"):
                full_response = full_response[:len(full_response)-3] + chunk['code'] + "```"
              else:
                full_response += f"```{chunk['code']}```"
            
            # Output
            if "executing" in chunk:
                # Handle code execution messages
                if full_response.endswith("```"):
                    full_response = full_response[:len(full_response)-3] + "\n```"
                full_response += f"\n\n```{chunk['executing']['language']}\n{chunk['executing']['code']}\n```"
            if "output" in chunk:
                # Handle output messages
                if chunk["output"] != "KeyboardInterrupt":
                    full_response += f"\n\n```text\n{chunk['output']}```\n"
            if "end_of_execution" in chunk:
                # Add a newline to separate executions
                full_response = full_response.strip()
                full_response += "\n"

            # Join the formatted messages
            # full_response += json.dumps(chunk)
            message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)

        st.session_state.messages.append({"role": "assistant", "content": full_response})

elif not st.session_state.OpenAI_api_key:
    st.info("👋 Hey , estamos muy felices por verte aqui 🤗")
    st.info("👉 Coloca tu OpenAI api key, para ser capaz to correr codigo mientras lo generas 🚀")
    st.error("👉 El objetivo de este proyecto es tu mostrar una facil implementacion del uso de Open Interpreter 🤗")