# Principal
from streamlit.components.v1 import html
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_option_menu import option_menu
import streamlit as st
import interpreter
import uuid
import json
import os
# Database
from src.data.database import create_tables, get_all_conversations, get_chats_by_conversation_id, save_conversation, save_chat, delete_conversation
from src.data.models import Conversation, Chat

# st components
from st_components.st_init import set_style
from st_components.st_session_states import init_session_states
from st_components.st_sidebar import st_sidebar
from st_components.st_main import st_main

#validation
from litellm import completion
from openai import Model

set_style()

st.title("💬 Open Interpreter")

init_session_states()

st_sidebar()
st.write( os.environ['OPENAI_API_KEY '])
st_main(interpreter)
