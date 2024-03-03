import streamlit as st

def setup_interpreter():
    try:
        st.session_state['interpreter'].reset()
    except:
        pass
        
    st.session_state['interpreter'].conversation_filename = st.session_state['current_conversation']["id"]
    st.session_state['interpreter'].conversation_history = True
    st.session_state['interpreter'].messages = st.session_state.get(
        'messages',
        st.session_state.get('mensajes',[])
    )
    st.session_state['interpreter'].llm.model = st.session_state['model']
    st.session_state['interpreter'].llm.temperature = st.session_state['temperature']
    st.session_state['interpreter'].llm.max_tokens = st.session_state['max_tokens']
    st.session_state['interpreter'].llm.system_message = st.session_state['system_message']
    st.session_state['interpreter'].auto_run = True

    st.session_state['interpreter'].computer.emit_images = True

    if st.session_state['api_choice'] == 'openrouter':
        st.session_state['interpreter'].llm.api_key = st.session_state['openrouter_key']
        st.session_state['interpreter'].llm.context_window = st.session_state['context_window']
    elif st.session_state['api_choice'] == 'openai':
        st.session_state['interpreter'].llm.api_key = st.session_state['openai_key']
        st.session_state['interpreter'].llm.context_window = st.session_state['context_window']
    elif st.session_state['api_choice'] == 'azure_openai':
        st.session_state['interpreter'].llm.api_key = st.session_state['openai_key']
        st.session_state['interpreter'].llm.api_base = st.session_state['azure_endpoint']
        st.session_state['interpreter'].llm.api_version = st.session_state['api_version']
    elif st.session_state['api_choice'] == 'vertexai':
        st.session_state['interpreter'].llm.context_window = st.session_state['context_window']
    elif st.session_state['api_choice'] == 'local':
        st.session_state['interpreter'].llm.context_window = st.session_state['context_window']
        st.session_state['interpreter'].offline = True
        if st.session_state['provider']=='Lmstudio':
            st.session_state['interpreter'].llm.model = "openai/x" # Tells OI to send messages in OpenAI's format
            st.session_state['interpreter'].llm.api_key = "fake_key" # LiteLLM, which we use to talk to LM Studio, requires this
            st.session_state['interpreter'].llm.api_base = st.session_state.get('api_base') # Point this at any OpenAI compatible server
        else:
            st.session_state['interpreter'].llm.model = f"ollama_chat/{st.session_state.get('model')}"
            st.session_state['interpreter'].llm.api_base = st.session_state.get('api_base')

    # Debug
    # st.write(interpreter.__dict__)
    # st.write(f'{interpreter.conversation_history_path=}')
    # st.write(f'{interpreter.conversation_filename =}')