import sqlite3
import uuid
from contextlib import contextmanager
from src.data.models import Conversation, Chat

DATABASE_PATH = "chats.db"

@contextmanager
def create_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    try:
        yield cursor
    finally:
        connection.commit()
        connection.close()

def create_tables():
    with create_connection() as cursor:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id TEXT PRIMARY KEY,
                user_id TEXT,
                name TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chats (
                id TEXT PRIMARY KEY,
                conversation_id TEXT,
                role TEXT,
                content TEXT,
                FOREIGN KEY (conversation_id) REFERENCES conversations(id)
            )
        ''')

def save_conversation(conversation):
    with create_connection() as cursor:
        cursor.execute("INSERT INTO conversations (id, user_id, name) VALUES (?, ?, ?)", (conversation.id, conversation.user_id, conversation.name))

def save_chat(chat):
    with create_connection() as cursor:
        cursor.execute("INSERT INTO chats (id, conversation_id, role, content) VALUES (?, ?, ?, ?)", (str(uuid.uuid4()), chat.conversation_id, chat.role, chat.content))

def get_all_conversations(user_id):
    with create_connection() as cursor:
        cursor.execute("SELECT id, user_id, name FROM conversations WHERE user_id=?", (user_id,))
        result = cursor.fetchall()
        conversations = [Conversation(*row) for row in result]
        return [conversation.to_dict() for conversation in conversations]

def get_conversation_by_id(conversation_id):
    with create_connection() as cursor:
        cursor.execute("SELECT id, name FROM conversations WHERE id=?", (conversation_id,))
        result = cursor.fetchone()
        return Conversation(*result) if result else None

def get_chats_by_conversation_id(conversation_id):
    with create_connection() as cursor:
        cursor.execute("SELECT conversation_id, role, content FROM chats WHERE conversation_id=?", (conversation_id,))
        result = cursor.fetchall()
        chats = [Chat(conversation_id, *row[1:]) for row in result]
        return [chat.to_dict() for chat in chats]

def delete_conversation(conversation_id):
    with create_connection() as cursor:
        cursor.execute("DELETE FROM chats WHERE conversation_id=?", (conversation_id,))
        cursor.execute("DELETE FROM conversations WHERE id=?", (conversation_id,))