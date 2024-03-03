import streamlit as st
import json
import re
import uuid
import platform
from urllib.parse import urlparse, urljoin
from streamlit.components.v1 import html
from streamlit_extras.add_vertical_space import add_vertical_space

from st_components.st_conversations import conversation_navigation

import os

OPEN_AI = 'OpenAI'
AZURE_OPEN_AI = 'Azure OpenAI'
OPEN_ROUTER = 'Open Router'
VERTEX_AI = 'Vertex AI'
LOCAL_AI = 'Local LLM'
OPEN_AI_MOCK = 'OpenAI Mock'


def st_sidebar():
    # try:
    with st.sidebar:
        # Select choice of API Server
        api_server = st.selectbox('Your API Server', [
                                  OPEN_AI, AZURE_OPEN_AI, OPEN_ROUTER, VERTEX_AI, LOCAL_AI, OPEN_AI_MOCK])

        # Set credentials based on choice of API Server
        if api_server == OPEN_AI:
            set_open_ai_credentials()
        elif api_server == AZURE_OPEN_AI:
            set_azure_open_ai_credentials()
        elif api_server == OPEN_ROUTER:
            set_open_router_credentials()
        elif api_server == VERTEX_AI:
            set_vertex_ai_credentials()
        elif api_server == LOCAL_AI:
            local_server_credentials()
        elif api_server == OPEN_AI_MOCK:
            st.warning('under construction')

        # Section dedicated to navigate conversations
        conversation_navigation()

        # Section dedicated to About Us
        about_us()

    # except Exception as e:
    #     st.error(e)


# About Us Section
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

# Setup OpenAI


def set_open_ai_credentials():
    with st.expander(label="Settings", expanded=(not st.session_state['chat_ready'])):
        openai_key = st.text_input('OpenAI Key:', type="password")
        os.environ['OPENAI_API_KEY '] = openai_key
        model = st.selectbox(
            label='🔌 models',
            options=list(st.session_state['models']['openai'].keys()),
            index=0,
            # disabled= not st.session_state.openai_key # Comment: Why?
        )
        context_window = st.session_state['models']['openai'][model]['context_window']

        temperature = st.slider('🌡 Tempeture', min_value=0.01, max_value=1.0
                               , value=st.session_state.get('temperature', 0.5), step=0.01)
        max_tokens = st.slider('📝 Max tokens', min_value=1, max_value=2000
                              , value=st.session_state.get('max_tokens', 512), step=1)

        num_pair_messages_recall = st.slider(
            '**Memory Size**: user-assistant message pairs', min_value=1, max_value=10, value=5)

        button_container = st.empty()
        save_button = button_container.button(
            "Save Changes 🚀", key='open_ai_save_model_configs')

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
            button_container.empty()  # Rerun does not allow it
            st.rerun()

# Setup Azure OpenAI


def set_azure_open_ai_credentials():
    with st.expander(label="Settings", expanded=(not st.session_state['chat_ready'])):
        azure_openai_key = st.text_input('Azure OpenAI Key:', type="password")
        azure_endpoint = st.text_input(
            'Azure endpoint', placeholder="https://{your-resource-name}.openai.azure.com")
        deployment_id = st.text_input(
            'deployment-id', help="The deployment name you choose when you deployed the model.")
        api_version = st.text_input(
            'api-version', help="The API version to use for this operation. This follows the YYYY-MM-DD format.")
        temperature = st.slider('🌡 Temperature', min_value=0.01, max_value=1.0
                               , value=st.session_state.get('temperature', 0.5), step=0.01)
        max_tokens = st.slider('📝 Max tokens', min_value=1, max_value=2000
                              , value=st.session_state.get('max_tokens', 512), step=1)
        num_pair_messages_recall = st.slider(
            '**Memory Size**: user-assistant message pairs', min_value=1, max_value=10, value=5)
        button_container = st.empty()
        save_button = button_container.button(
            "Save Changes 🚀", key='open_ai_save_model_configs')

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

# Setup Open Router


def set_open_router_credentials():
    with st.expander(label="Settings", expanded=(not st.session_state['chat_ready'])):
        openrouter_key = st.text_input('Open Router Key:', type="password")
        openrouter_api_base = "https://openrouter.ai/api/v1/chat/completions"
        openrouter_headers = {
            # To identify your app. Can be set to e.g. http://localhost:3000 for testing
            "HTTP-Referer": "http://localhost:3000",
            "X-Title": "Open-Interpreter Gpt App",  # Optional. Shows on openrouter.ai
        }

        model = st.selectbox(
            label='🔌 models',
            options=list(st.session_state['models']['openrouter'].keys()),
            index=0,
            # disabled= not st.session_state.openai_key # Comment: Why?
        )
        context_window = st.session_state['models']['openrouter'][model]['context_window']

        temperature = st.slider('🌡 Tempeture', min_value=0.01, max_value=1.0
                               , value=st.session_state.get('temperature', 0.5), step=0.01)
        max_tokens = st.slider('📝 Max tokens', min_value=1, max_value=2000
                              , value=st.session_state.get('max_tokens', 512), step=1)

        num_pair_messages_recall = st.slider(
            '**Memory Size**: user-assistant message pairs', min_value=1, max_value=10, value=5)

        button_container = st.empty()
        save_button = button_container.button(
            "Save Changes 🚀", key='open_router_save_model_configs')

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

# Setup Vertex AI


def set_vertex_ai_credentials():

    def validate_json_content(data):
        required_keys = ['project_id', 'private_key', 'client_email']
        missing_keys = [key for key in required_keys if key not in data]
        if missing_keys:
            return False, f"The following keys are missing in the JSON file: {', '.join(missing_keys)}"
        else:
            return True, "JSON file contains all necessary elements"

    def save_validated_credentials(data):
        # Define the file path for the new JSON file
        json_file_name = f'{str(uuid.uuid4())}.json'

        output_path = os.path.join(os.getcwd(), json_file_name)
        with open(output_path, 'w', encoding='utf-8') as outfile:
            json.dump(json_dict, outfile, indent=2)

        return output_path

    def delete_json_file(json_file_name):
        try:
            os.remove(json_file_name)
            st.success(f"{json_file_name} has been deleted!")
        except FileNotFoundError:
            st.warning(f"{json_file_name} does not exist.")

    with st.expander(label="Settings", expanded=(not st.session_state['chat_ready'])):
        if 'ruta_saved' not in st.session_state:
            uploaded_file = st.file_uploader("Upload your JSON file credentials", type=["json"])
            if uploaded_file:
                bytes_data = uploaded_file.getvalue()
                json_string = bytes_data.decode('utf-8')
                json_dict = json.loads(json_string)
                # file_contents = uploaded_file.read()
                # json_dict = json.loads(file_contents)
                # Validate the JSON data
                is_valid, message = validate_json_content(json_dict)
                if is_valid:
                    st.write("Validation successful:", message)
                    # Save the loaded JSON under a new filename
                    ruta = save_validated_credentials(data=json_dict)
                    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = ruta
                    os.environ['VERTEXAI_PROJECT'] = json_dict['project_id']
                    st.session_state.ruta_saved = ruta
                    st.rerun()
                else:
                    st.error(f"Validation failed: {message}", icon='⚠️')

        else:
            # Create the Streamlit button to delete the JSON file
            st.success('JSON saved successfully')
            if st.button("Delete JSON file"):
                delete_json_file(json_file_name=st.session_state.ruta_saved)
                os.environ.pop('GOOGLE_APPLICATION_CREDENTIALS')
                os.environ.pop('VERTEXAI_PROJECT')
                if 'VERTEXAI_LOCATION' in os.environ:
                    os.environ.pop('VERTEXAI_LOCATION')
                del st.session_state.ruta_saved
                st.rerun()

        location = st.selectbox(
            label='Select Region',
            options=['Iowa (us-central1)', 'Northern Virginia (us-east4)', 'Oregon (us-west1)', 'Las Vegas (us-west4)', 'Montréal (northamerica-northeast1)', 'Belgium (europe-west1)', 'London (europe-west2)',
                     'Frankfurt (europe-west3)', 'Netherlands (europe-west4)', 'Paris (europe-west9)', 'Tokyo (asia-northeast1)', 'Seoul (asia-northeast3)', 'Singapore (asia-southeast1)'],
            index=0,
            help='The location of your Vertex AI resources.'
        )

        model = st.selectbox(
            label='🔌 models',
            options=list(st.session_state['models']['vertexai'].keys()),
            index=0
        )

        context_window = st.session_state['models']['vertexai'][model]['context_window']

        temperature = st.slider('🌡 Temperature', min_value=0.01, max_value=1.0
                               , value=st.session_state.get('temperature', 0.5), step=0.01)
        max_tokens = st.slider('📝 Max tokens', min_value=1, max_value=2000
                              , value=st.session_state.get('max_tokens', 512), step=1)

        num_pair_messages_recall = st.slider(
            '**Memory Size**: user-assistant message pairs', min_value=1, max_value=10, value=5)

        button_container = st.empty()
        save_button = button_container.button(
            "Save Changes 🚀", key='open_router_save_model_configs')

        if save_button and 'ruta_saved' in st.session_state:

            match = re.search(r'\((.*?)\)', location)
            if match:
                os.environ['VERTEXAI_LOCATION'] = match.group(1)

            st.session_state['api_choice'] = 'vertexai'
            st.session_state['model'] = f'vertex_ai/{model}'
            st.session_state['temperature'] = temperature
            st.session_state['max_tokens'] = max_tokens
            st.session_state['context_window'] = context_window

            st.session_state['num_pair_messages_recall'] = num_pair_messages_recall

            st.session_state['chat_ready'] = True
            button_container.empty()
            st.rerun()


# Setup Local LLM
def local_server_credentials():

    def validate_local_host_link(link):
        prefixes = ['http://localhost', 'https://localhost',
                    'http://127.0.0.1', 'https://127.0.0.1']
        return any(link.startswith(prefix) for prefix in prefixes)

    def validate_provider(link, provider):
        return link if provider != 'Lmstudio' else link + '/v1' if not link.endswith('/v1') else link

    def parse_and_correct_url(url):
        parsed_url = urlparse(url)
        corrected_url = urljoin(parsed_url.geturl(), parsed_url.path)
        return corrected_url

    def submit():
        if platform.system() == 'Linux' and not validate_local_host_link(st.session_state.widget) and st.session_state.widget != '':
            link = validate_provider(
                link=st.session_state.widget, provider=local_provider)
            print('Linux')
            st.session_state.widget = parse_and_correct_url(link)

        else:
            print(platform.system() == 'Linux', validate_local_host_link(
                st.session_state.widget), st.session_state.widget != '')
            if platform.system() != 'Linux' and validate_local_host_link(st.session_state.widget) and st.session_state.widget != '':
                link = validate_provider(link=st.session_state.widget, provider=local_provider)
                print('here')
                st.session_state.widget = parse_and_correct_url(link)
            else:
                print('empty')
                st.session_state.widget = ''

    with st.expander(label="Settings", expanded=(not st.session_state['chat_ready'])):
        local_provider = st.selectbox(
            label='Local Provider',
            options=['Lmstudio', 'Ollama'],
            index=0,
        )
        api_base = st.text_input(
            label='Put here your Api Base Link', 
            value=st.session_state.get('api_base', ''),
            placeholder='http://localhost:1234/v1' if local_provider == 'Lmstudio' else 'http://localhost:11434', 
            key='widget', 
            on_change=submit)

        model = st.text_input(label='Model Name [get here](https://ollama.com/library)' if local_provider == 'Ollama' else 'Model Name [get here](https://huggingface.co/models?pipeline_tag=text-generation)',
                              value=st.session_state.get('model', 'mistral') if local_provider == 'Ollama' else 'openai/x', disabled=False if local_provider == 'Ollama' else True)
        context_window = st.selectbox(
            label='Input/Output token windows',
            options=['512', '1024', '2048', '4096', '8192', '16384', '32768'],
            index=0,
        )

        # context_window = st.slider('Input/Output token window', min_value=512, max_value=32768, value=st.session_state.get('context_window', st.session_state.get('window', 512)), step=st.session_state.get('window', 512)*2, key='window')
        temperature = st.slider('🌡 Temperature', min_value=0.01, max_value=1.0
                               , value=st.session_state.get('temperature', 0.5), step=0.01)
        max_tokens = st.slider('📝 Max tokens', min_value=1, max_value=2000
                              , value=st.session_state.get('max_tokens', 512), step=1)

        num_pair_messages_recall = st.slider(
            '**Memory Size**: user-assistant message pairs', min_value=1, max_value=10, value=5)

        button_container = st.empty()
        save_button = button_container.button("Save Changes 🚀", key='open_ai_save_model_configs')

        if save_button and api_base and model:
            st.session_state['provider'] = local_provider
            st.session_state['api_choice'] = 'local'
            st.session_state['api_base'] = api_base
            st.session_state['model'] = model
            st.session_state['temperature'] = temperature
            st.session_state['max_tokens'] = max_tokens
            st.session_state['context_window'] = context_window

            st.session_state['num_pair_messages_recall'] = num_pair_messages_recall

            st.session_state['chat_ready'] = True
            button_container.empty()
            st.rerun()