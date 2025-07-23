# app.py
import streamlit as st
import re
from chatbot_logic import chat_logic_func

# page setup
st.set_page_config(
    page_title="TalentScout AI Assistant",
    page_icon="🤖",
    layout="centered"
)

# words to end the chat
EXIT_KEYWORDS = {"quit", "exit", "bye", "goodbye", "stop"}

st.title("🤖 TalentScout Hiring Assistant")

# starting the session
if 'current_state' not in st.session_state:
    st.session_state.current_state = 'GREETING'
    st.session_state.user_info = {}
    st.session_state.tech_questions = []
    st.session_state.question_index = 0
    st.session_state.follow_ups_asked = []
    st.session_state.messages = [
        {"role": "assistant", "content": "Welcome! I'm an AI assistant from TalentScout. To begin, what is your full name?"}
    ]

# show the chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# main loop
if st.session_state.current_state != 'END_CONVERSATION':
    if user_reply := st.chat_input("Your response..."):
        # add user message to history
        st.session_state.messages.append({"role": "user", "content": user_reply})
        with st.chat_message("user"):
            st.markdown(user_reply)

        # check for exit words
        if user_reply.lower().strip() in EXIT_KEYWORDS:
            st.session_state.current_state = 'END_CONVERSATION'
        
        else:
            # run the main logic
            chat_logic_func(st.session_state, user_reply)

        # refresh the screen
        st.rerun()

# handle the end of the chat
if st.session_state.current_state == 'END_CONVERSATION':
    if not st.session_state.get('summary_sent', False):
        user_name = st.session_state.user_info.get('full_name', 'there')
        final_msg = f"Thank you for your time, {user_name}. The session has now ended. The TalentScout team will be in touch if your profile is a match."
        st.session_state.messages.append({"role": "assistant", "content": final_msg})
        st.session_state.summary_sent = True
        st.rerun() # refresh one last time
    
    st.chat_input(disabled=True, placeholder="This chat has ended.")
    st.balloons()