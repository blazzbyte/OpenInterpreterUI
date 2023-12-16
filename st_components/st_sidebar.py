
import streamlit as st
from streamlit.components.v1 import html
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_option_menu import option_menu

from st_components.st_conversations import conversation_navigation

import os

OPEN_AI = 'OpenAI'
AZURE_OPEN_AI = 'Azure OpenAI'
OPEN_ROUTER = 'Open Router'
OPEN_AI_MOCK = 'OpenAI Mock'


def st_sidebar():
    # try:
        with st.sidebar:
            # Select choice of API Server
            api_server = st.selectbox('Your API Server', [OPEN_AI, AZURE_OPEN_AI, OPEN_ROUTER, OPEN_AI_MOCK])

            # Set credentials based on choice of API Server
            if api_server == OPEN_AI:
                set_open_ai_server_credentials()
            elif api_server == AZURE_OPEN_AI:
                set_azure_open_ai_server_credentials()
            elif api_server == OPEN_ROUTER:
                set_open_router_server_credentials()
            elif api_server == OPEN_AI_MOCK:
                st.warning('under construction')

            # Section dedicated to navigate conversations
            conversation_navigation()

            # Section dedicated to About Us
            about_us()


    # except Exception as e:
    #     st.error(e)

def about_us():
    add_vertical_space(8)
    html_chat = '<center><h5>🤗 Support the project with a donation for the development of new Features 🤗</h5>'
    st.markdown(html_chat, unsafe_allow_html=True)
    button = '<script type="text/javascript" src="https://cdnjs.buymeacoffee.com/1.0.0/button.prod.min.js" data-name="bmc-button" data-slug="blazzmocompany" data-color="#FFDD00" data-emoji=""  data-font="Cookie" data-text="Buy me a coffee" data-outline-color="#000000" data-font-color="#000000" data-coffee-color="#ffffff" ></script>'
    html(button, height=70, width=220)
    iframe = '<style>iframe[width="220"]{position: absolute; top: 50%;left: 50%;transform: translate(-50%, -50%);margin:26px 0}</style>'
    st.markdown(iframe, unsafe_allow_html=True)
    add_vertical_space(2)
    st.write('<center><h6>Made with ❤️ by <a href="mailto:blazzmo.company@gmail.com">BlazzByte</a></h6>',
            unsafe_allow_html=True)
    st.write('<center><h6>Contribution 🤝 by <a href="mailto:tranhoangnguyen03@gmail.com">Sergeant113</a></h6>',
            unsafe_allow_html=True)


def set_open_ai_server_credentials():
    with st.expander(label="Settings", expanded= (not st.session_state['chat_ready'])):
        openai_key = st.text_input('OpenAI Key:', type="password")
        os.environ['OPENAI_API_KEY '] = openai_key
        model = st.selectbox(
            label= '🔌 models',
            options= list(st.session_state['models']['openai'].keys()),
            index= 0,
            # disabled= not st.session_state.openai_key # Comment: Why?
        )
        context_window = st.session_state['models']['openai'][model]['context_window']

        temperature = st.slider('🌡 Tempeture', min_value=0.01, max_value=1.0, value=st.session_state.get('temperature', 0.5), step=0.01)
        max_tokens = st.slider('📝 Max tokens', min_value=1, max_value=2000, value=st.session_state.get('max_tokens', 512), step=1)

        num_pair_messages_recall = st.slider('**Memory Size**: user-assistant message pairs', min_value=1, max_value=10, value=5)

        button_container = st.empty()
        save_button = button_container.button("Save Changes 🚀", key='open_ai_save_model_configs')

        if save_button and openai_key:
            os.environ["OPENAI_API_KEY"] = openai_key
            st.session_state['api_choice'] = 'openai'
            st.session_state['openai_key'] = openai_key
            st.session_state['model'] = model
            st.session_state['temperature'] = temperature
            st.session_state['max_tokens'] = max_tokens
            st.session_state['context_window'] = context_window

            st.session_state['num_pair_messages_recall'] = num_pair_messages_recall

            st.session_state['chat_ready'] = True
            button_container.empty()
            st.rerun()


def set_azure_open_ai_server_credentials():
    with st.expander(label="Settings", expanded=(not st.session_state['chat_ready'])):
        azure_openai_key = st.text_input(
            'Azure OpenAI Key:',
            type="password")
        azure_endpoint = st.text_input(
            'Azure endpoint',
            placeholder="https://{your-resource-name}.openai.azure.com")
        deployment_id = st.text_input(
            'deployment-id',
            help="The deployment name you chose when you deployed the model.")
        api_version = st.text_input(
            'api-version',
            help="The API version to use for this operation. This follows the YYYY-MM-DD format.")
        temperature = st.slider('🌡 Temperature', min_value=0.01, max_value=1.0,
                                value=st.session_state.get('temperature', 0.5), step=0.01)
        max_tokens = st.slider('📝 Max tokens', min_value=1, max_value=2000,
                               value=st.session_state.get('max_tokens', 512), step=1)
        num_pair_messages_recall = st.slider('**Memory Size**: user-assistant message pairs', min_value=1, max_value=10,
                                             value=5)
        button_container = st.empty()
        save_button = button_container.button("Save Changes 🚀", key='open_ai_save_model_configs')

        if save_button and azure_openai_key:
            st.session_state['api_choice'] = 'azure_openai'
            st.session_state['openai_key'] = azure_openai_key
            st.session_state['model'] = f"azure/{deployment_id}"
            st.session_state['azure_endpoint'] = azure_endpoint
            st.session_state['api_version'] = api_version
            st.session_state['temperature'] = temperature
            st.session_state['max_tokens'] = max_tokens
            st.session_state['num_pair_messages_recall'] = num_pair_messages_recall
            st.session_state['chat_ready'] = True
            button_container.empty()
            st.rerun()


def set_open_router_server_credentials():
    with st.expander(label="Settings", expanded=(not st.session_state['chat_ready'])):
        openrouter_key = st.text_input('Open Router Key:', type="password")
        openrouter_api_base = "https://openrouter.ai/api/v1/chat/completions"
        openrouter_headers = {
            "HTTP-Referer": "http://localhost:3000", # To identify your app. Can be set to e.g. http://localhost:3000 for testing
            "X-Title": "Open-Interpreter Gpt App", # Optional. Shows on openrouter.ai
        }

        model = st.selectbox(
            label= '🔌 models',
            options= list(st.session_state['models']['openrouter'].keys()),
            index= 0,
            # disabled= not st.session_state.openai_key # Comment: Why?
        )
        context_window = st.session_state['models']['openrouter'][model]['context_window']

        temperature = st.slider('🌡 Tempeture', min_value=0.01, max_value=1.0, value=st.session_state.get('temperature', 0.5), step=0.01)
        max_tokens = st.slider('📝 Max tokens', min_value=1, max_value=2000, value=st.session_state.get('max_tokens', 512), step=1)

        num_pair_messages_recall = st.slider('**Memory Size**: user-assistant message pairs', min_value=1, max_value=10, value=5)

        button_container = st.empty()
        save_button = button_container.button("Save Changes 🚀", key='open_router_save_model_configs')

        if save_button and openrouter_key:
            os.environ["OPENROUTER_API_KEY"] = openrouter_key
            os.environ["OR_SITE_URL"] = openrouter_headers["HTTP-Referer"]
            os.environ["OR_APP_NAME"] = openrouter_headers["X-Title"]
            st.session_state['api_choice'] = 'openrouter'
            st.session_state['openrouter_key'] = openrouter_key
            st.session_state['openrouter_api_base'] = openrouter_api_base
            st.session_state['openrouter_headers'] = openrouter_headers
            st.session_state['model'] = f'openrouter/{model}'
            st.session_state['temperature'] = temperature
            st.session_state['max_tokens'] = max_tokens
            st.session_state['context_window'] = context_window

            st.session_state['num_pair_messages_recall'] = num_pair_messages_recall

            st.session_state['chat_ready'] = True
            button_container.empty()
            st.rerun()