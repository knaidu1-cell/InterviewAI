import streamlit as st
import requests
import json
import os
import sqlite3
import pandas as pd

# CONFIGURATION

OLLAMA_BASE_URL = os.getenv('OLLAMA_BASE_URL', 'http://10.230.100.240:17020')
# Change default from 'gpt-oss:20b' to 'llama3.1'
OLLAMA_CHAT_MODEL = os.getenv('OLLAMA_CHAT_MODEL', 'llama3.1')

# Style
st.markdown("""
<style>
.stChatMessage[data-testid="chat-message-user"] {
    background-color: #0039a6;
    color: white;
}
.stChatMessage[data-testid="chat-message-assistant"] {
    background-color: #f0f2f6;
    color: black;
}
</style>
""", unsafe_allow_html=True)

# DATABASE LOGIC
def init_db():
    conn = sqlite3.connect('interview_history.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS history
                 (role TEXT, content TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

def save_message(role, content):
    conn = sqlite3.connect('interview_history.db')
    c = conn.cursor()
    c.execute("INSERT INTO history (role, content) VALUES (?, ?)", (role, content))
    conn.commit()
    conn.close()

# AI LOGIC (Streaming)
def call_ollama_stream(prompt):
    """Sends request to Ollama and yields chunks of text."""
    try:
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json={
                "model": OLLAMA_CHAT_MODEL, 
                "prompt": prompt, 
                "stream": True,
                "options": {"temperature": 0.7}
            },
            stream=True
        )
        for line in response.iter_lines():
            if line:
                chunk = json.loads(line)
                if "response" in chunk:
                    yield chunk["response"]
                if chunk.get("done", False):
                    break
    except Exception as e:
        yield f"Error connecting to AI: {e}"

def construct_system_prompt(user_input, history):
    """Builds the brain of the tutor."""
    # Convert list of dicts to string for context
    history_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in history[-5:]])
    
    return f"""
    You are an expert Behavioral Interview Coach. 
    
    TASK:
    1. Analyze the User's input: "{user_input}"
    2. Select the Best Framework:
       - STAR (Situation, Task, Action, Result) for standard stories.
       - SOAR (Situation, Obstacle, Action, Result) for failures or strategy.
    3. Provide a sample answer structure.
    
    CONTEXT:
    {history_text}
    
    USER INPUT: {user_input}
    
    RESPONSE FORMAT:
    **Framework:** [Name]
    **Why:** [Reason]
    **Answer:** [Structure]
    """

# MAIN APP UI 
st.title("AI Interview Tutor")
st.write("Practice your STAR and SOAR stories.")

# 1. Initialize DB and Session State
init_db()
if "messages" not in st.session_state:
    st.session_state.messages = []

# 2. Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# 3. Handle User Input
if prompt := st.chat_input("Paste a job description or interview question..."):
    # Add User Message to State & UI
    st.session_state.messages.append({"role": "user", "content": prompt})
    save_message("user", prompt)
    with st.chat_message("user"):
        st.write(prompt)

    # Generate AI Response
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        
        system_prompt = construct_system_prompt(prompt, st.session_state.messages)
        
        # Stream the result
        for chunk in call_ollama_stream(system_prompt):
            full_response += chunk
            response_placeholder.write(full_response + "▌")
            
        response_placeholder.write(full_response)
    
    # Save AI Message
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    save_message("assistant", full_response)