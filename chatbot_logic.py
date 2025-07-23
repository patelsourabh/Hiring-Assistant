# chatbot_logic.py
import streamlit as st
import re
from llm_handler import (
    get_the_questions,
    is_it_relevant,
    check_the_answer,
    make_follow_up_q
)

def get_last_assistant_question(messages):
    for msg in reversed(messages):
        if msg["role"] == "assistant":
            return msg["content"]
    return ""

EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
PHONE_REGEX = r'^\+?1?\d{9,15}$'

# main chat function
def chat_logic_func(s_state, user_text):
    c_state = s_state.current_state

    # cheking if the user is on topic
    RELEVANCE_CHECK_STATES = {'GATHERING_EXPERIENCE', 'GATHERING_POSITION', 'GATHERING_LOCATION', 'GATHERING_TECH_STACK'}
    if c_state in RELEVANCE_CHECK_STATES:
        last_q = get_last_assistant_question(s_state.messages)
        if not is_it_relevant(last_q, user_text):
            fallback_msg = f"I'm sorry, I didn't quite understand your response in relation to my question. Could we please return to the topic? {last_q}"
            s_state.messages.append({"role": "assistant", "content": fallback_msg})
            return

    # conversation states
    if c_state == 'GREETING':
        s_state.user_info['full_name'] = user_text
        s_state.current_state = 'GATHERING_EMAIL'
        bot_reply = f"Nice to meet you, {user_text}! What is your email address?"
        s_state.messages.append({"role": "assistant", "content": bot_reply})

    elif c_state == 'GATHERING_EMAIL':
        # cheking the email
        if not re.match(EMAIL_REGEX, user_text):
            bot_reply = "That doesn't look like a valid email. Please provide a correct email address."
        else:
            s_state.user_info['email'] = user_text
            s_state.current_state = 'GATHERING_PHONE'
            bot_reply = "Thank you. What is your phone number?"
        s_state.messages.append({"role": "assistant", "content": bot_reply})

    elif c_state == 'GATHERING_PHONE':
        clean_phone = user_text.replace(" ", "").replace("-", "")
        if not re.match(PHONE_REGEX, clean_phone):
            bot_reply = "That doesn't seem to be a valid phone number. Please enter a number like +1234567890."
        else:
            s_state.user_info['phone_number'] = user_text
            s_state.current_state = 'GATHERING_EXPERIENCE'
            bot_reply = "Great. How many years of professional experience do you have?"
        s_state.messages.append({"role": "assistant", "content": bot_reply})

    elif c_state == 'GATHERING_EXPERIENCE':
        s_state.user_info['years_experience'] = user_text
        s_state.current_state = 'GATHERING_POSITION'
        bot_reply = "Understood. What position or positions are you interested in?"
        s_state.messages.append({"role": "assistant", "content": bot_reply})

    elif c_state == 'GATHERING_POSITION':
        s_state.user_info['desired_position'] = user_text
        s_state.current_state = 'GATHERING_LOCATION'
        bot_reply = "Noted. And what is your current location (e.g., City)?"
        s_state.messages.append({"role": "assistant", "content": bot_reply})

    elif c_state == 'GATHERING_LOCATION':
        s_state.user_info['location'] = user_text
        s_state.current_state = 'GATHERING_TECH_STACK'
        bot_reply = "Perfect. Now, please list your primary tech stack, separated by commas (e.g., Python, React, SQL)."
        s_state.messages.append({"role": "assistant", "content": bot_reply})

    elif c_state == 'GATHERING_TECH_STACK':
        s_state.user_info['tech_stack'] = user_text
        with st.spinner("🧠 Analyzing your tech stack and generating questions..."):
            q_list = get_the_questions(user_text)

        if q_list:
            s_state.tech_questions = q_list
            s_state.current_state = 'CONDUCTING_TEST'
            bot_reply = "Excellent, thank you. I have a few questions for you.\n\n**Question 1:** " + q_list[0]
        else:
            s_state.current_state = 'END_CONVERSATION'
            bot_reply = "Thank you. I had an issue generating questions at this moment, but a recruiter will review your profile and be in touch soon!"
        s_state.messages.append({"role": "assistant", "content": bot_reply})

    elif c_state == 'CONDUCTING_TEST':
        q_index = s_state.question_index
        current_q = s_state.tech_questions[q_index]

        with st.spinner("Analyzing answer..."):
            eval_result = check_the_answer(current_q, user_text)

        already_followed_up = q_index in s_state.follow_ups_asked

        if eval_result and eval_result.get("status") == "UNCLEAR" and not already_followed_up:
            # answer is unclear, ask a follow up
            with st.spinner("Thinking of a follow-up question..."):
                follow_up = make_follow_up_q(
                    current_q, user_text, eval_result.get("reason")
                )
            
            if follow_up:
                s_state.follow_ups_asked.append(q_index)
                bot_reply = follow_up
            else:
                # if follow up fails, just move on
                bot_reply = "Okay, let's move to the next question."
                s_state.question_index += 1
        else:
            # answer is clear, move on
            s_state.question_index += 1
        
        # figure out what to say next
        if s_state.question_index < len(s_state.tech_questions):
            if 'bot_reply' not in locals():
                next_q = s_state.tech_questions[s_state.question_index]
                bot_reply = f"Thank you. **Question {s_state.question_index + 1}:** {next_q}"
        else:
            # end of test
            s_state.current_state = 'END_CONVERSATION'
            bot_reply = "Thank you for answering! That's all I need. Our team will review your profile and contact you with the next steps."
            
        s_state.messages.append({"role": "assistant", "content": bot_reply})