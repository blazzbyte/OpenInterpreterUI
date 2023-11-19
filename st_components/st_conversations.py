
# Database
from src.data.database import create_tables, get_all_conversations, get_chats_by_conversation_id, save_conversation, save_chat, delete_conversation
from src.data.models import Conversation, Chat
import uuid

# Streamlit
import streamlit as st
from streamlit_option_menu import option_menu

def init_conversations():
    #DATABASE
    create_tables()
    conversations = list(reversed(get_all_conversations(st.session_state.user_id)))
    conversation_options = [f"{conversation['name']}" for conversation in conversations]
    return conversations, conversation_options

def conversation_navigation():    
    conversations, conversation_options = init_conversations()
    with st.expander(label="Conversation Nav", expanded=False):
        create_conversation(conversation_options)
        navigate_past_conversations(conversations, conversation_options)
        delete_current_conversation()


def create_conversation(conversation_options):
    new_conversation_name = st.text_input("Enter New Conversation Name:")
    if st.button("Add New Conversation") and new_conversation_name.strip() != "":
        if new_conversation_name in conversation_options:
            st.warning("Conversation with that name already exists. Please choose a different name.")
        else:
            conversation_id = str(uuid.uuid4())
            user_id = st.session_state.user_id
            new_conversation = Conversation(conversation_id, user_id, new_conversation_name)
            save_conversation(new_conversation)
            st.success(f"Conversation '{new_conversation_name}' added successfully!")
            st.rerun()

def navigate_past_conversations(conversations, conversation_options):
    if len(conversation_options) > 0:
        icons_conversations = ['chat-right-dots-fill'] * len(conversation_options)
        selected_conversation = option_menu(
            "Conversations", conversation_options , 
            default_index=0, menu_icon='chat', 
            icons=icons_conversations,
            styles={
                "icon": {"color": "#FEFEFE", "font-size": "12px"}, 
                "nav-link": {"font-family":"Source Sans Pro, sans-serif", "font-size": "12px", "text-align": "left", "margin":"0px", "--hover-color": "#151515", "color": "#FEFEFE"},
                "nav-link-selected": {"background-color": "#1E1E1E", "color": "#FEFEFE","font-weight":"400"},
            },
            key='menu'
        )

        if(selected_conversation):
            for element in conversations:
                if element.get("name") == selected_conversation:
                    st.session_state['current_conversation'] = element
                    break
            st.session_state.messages = get_chats_by_conversation_id(st.session_state['current_conversation']["id"])
    
def delete_current_conversation():
    if 'current_conversation' in st.session_state and st.button("Delete Current Conversation", type='primary'):
        delete_conversation(st.session_state['current_conversation']["id"])
        del st.session_state['current_conversation']
        st.rerun()