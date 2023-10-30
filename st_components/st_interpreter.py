import streamlit as st
import interpreter

def setup_interpreter(interpreter):
    interpreter.reset()
        
    if st.session_state['api_choice'] == 'openrouter':    
        interpreter.api_key = st.session_state['openrouter_key'] 
        interpreter.api_base = st.session_state['openrouter_api_base']     
        interpreter.headers = st.session_state['openrouter_headers'] 
         
    if st.session_state['api_choice'] == 'openapi':     
        interpreter.api_key = st.session_state['openai_key']
    
    interpreter.messages = st.session_state.get('messages',[])
    interpreter.model = st.session_state['model']
    interpreter.context_window = st.session_state['context_window']
    interpreter.temperature = st.session_state['temperature']
    interpreter.max_tokens = st.session_state['max_tokens']
    interpreter.system_message = st.session_state['system_message']
    interpreter.auto_run = True

    return interpreter
