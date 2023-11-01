import streamlit as st

from st_components.st_interpreter import setup_interpreter
# Database
from src.data.database import save_chat
from src.data.models import Chat

def chat_with_interpreter():
    
    # GENERATE MESSAGES
    if prompt := st.chat_input(placeholder="Write here your message", disabled=not st.session_state['chat_ready']):
    
        setup_interpreter()

        handle_user_message(prompt)

        handle_assistant_response(prompt)

def handle_user_message(prompt):
    with st.chat_message("user"):
        st.markdown(f'<p>{prompt}</p>', True)
        st.session_state.messages.append({"role": "user", "content": prompt})
        user_chat = Chat(st.session_state['current_conversation']["id"], "user", prompt)
        save_chat(user_chat)

def add_memory(prompt):
    look_back = -2*st.session_state['num_pair_messages_recall']
    memory = '\n'.join(
            [f"{i['role'].capitalize()}: {i['content']}" for i in st.session_state['messages'][look_back:]]
        ).replace('User', '\nUser' 
    )
    prompt_with_memory = f"user's request:{prompt}. --- \nBelow is the transcript of your past conversation with the user: {memory} ---\n"
    return prompt_with_memory

def handle_assistant_response(prompt):
    with st.chat_message("assistant"):
        # Initialize variables   
        prompt_with_memory = add_memory(prompt)
        codeb = True
        outputb = False
        full_response = ""
        message_placeholder = st.empty()
        with st.spinner('thinking'):
            for chunk in st.session_state['interpreter'].chat(message=add_memory(prompt_with_memory), display=False, stream=True):  
                full_response, codeb, outputb = format_response(chunk, full_response, codeb, outputb)
                
                # Join the formatted messages
                message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
        
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        assistant_chat = Chat(st.session_state['current_conversation']["id"], "assistant", full_response)
        save_chat(assistant_chat)
        st.session_state['mensajes'] = st.session_state['interpreter'].messages

def format_response(chunk, full_response, codeb, outputb):
    # Handle message chunks (copy-paste from original)
    if "message" in chunk:
        full_response += chunk["message"]
        if chunk['message'] == ":":
            full_response += "\n"

    # Handle code chunks (copy-paste from original)
    if "code" in chunk:
        if full_response.endswith("```"):
            if chunk['code'].find("\n") != -1 and codeb:
                partido = full_response[:len(full_response)-3].split("```")[-1]
                full_response = full_response.replace(
                    "```" + partido, "\n```\n" + partido + chunk['code'])
                codeb = False
            else:
                full_response = full_response[:len(full_response) - 3] + chunk['code'] + "```"
        else:
            full_response += f"```{chunk['code']}```"
    
    # (copy-paste from original # Output)
    # Handle code execution chunks 
    if "executing" in chunk:
        if full_response.endswith("```") and full_response[:len(full_response)-3].split("```")[-1].find("\n") != -1:
            full_response = full_response[:len(full_response)-3] + "\n```"
        full_response += f"\n\n```{chunk['executing']['language']}\n{chunk['executing']['code']}\n```"

    # Handle output chunks
    if "output" in chunk:
        if chunk["output"] != "KeyboardInterrupt" and outputb:
            full_response = full_response[:len(
                full_response)-4] + chunk['output'] + "\n```\n"
        elif chunk["output"] != "KeyboardInterrupt":
            full_response += f"\n\n```text\n{chunk['output']}```\n"
            outputb = True
        codeb = True

    # Handle end of execution chunks
    if "end_of_execution" in chunk:
        full_response = full_response.strip()
        full_response += "\n"

    return full_response, codeb, outputb
