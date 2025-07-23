# llm_handler.py
import os
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from prompts import make_question_prompt, check_relevance_prompt
from prompts import evaluate_the_answer_prompt, follow_up_prompt

# get secrets from .env
load_dotenv()

# this sets up the ai model
try:
    model1 = ChatOpenAI(
        model="mistralai/mistral-7b-instruct",
        openai_api_key=os.environ["OPENROUTER_API_KEY"],
        openai_api_base="https://openrouter.ai/api/v1",
        temperature=0.6,
        max_tokens=512,
    )
except Exception as e:
    print(f"oops, error happened: {e}")
    model1 = None


def get_the_questions(tech_stack):
    # check if model loaded
    if not model1:
        print("model is not working.")
        return None

    # geting the prompt
    prompt1 = make_question_prompt(tech_stack)

    try:
        # call the ai
        response_msg = model1.invoke(prompt1)
        response_text = response_msg.content

        # trying to parse the json
        try:
            questions = json.loads(response_text)

            # final check
            if isinstance(questions, list) and all(isinstance(q, str) for q in questions):
                return questions
            else:
                print(f"json warning: its not a list of strings")
                return None
        except json.JSONDecodeError:
            print(f"json thing didnt work. response: '{response_text}'")
            return None

    except Exception as e:
        print(f"some other error with the ai call: {e}")
        return None

def is_it_relevant(question_asked, user_answer):
    if not model1:
        print("model not working for relevance check")
        return True # just say its true

    prompt2 = check_relevance_prompt(question_asked, user_answer)
    try:
        response = model1.invoke(prompt2)
        response_text = response.content.strip().upper()

        # look for yes or no
        if "YES" in response_text:
            return True
        elif "NO" in response_text:
            return False
        else:
            # if we dont know, just say its ok
            print(f"weird response from relevance check: '{response_text}'")
            return True
    except Exception as e:
        print(f"error during relevance check: {e}")
        return True

def check_the_answer(question, answer):
    if not model1: return None
    prompt3 = evaluate_the_answer_prompt(question, answer)
    try:
        response = model1.invoke(prompt3)
        # get json from ai
        evaluation = json.loads(response.content)
        if isinstance(evaluation, dict) and "status" in evaluation and "reason" in evaluation:
            return evaluation
        return None
    except Exception as e:
        print(f"error when evaluating answer: {e}")
        return None

def make_follow_up_q(question, answer, reason):
    if not model1: return None
    prompt4 = follow_up_prompt(question, answer, reason)
    try:
        response = model1.invoke(prompt4)
        # return the text
        return response.content
    except Exception as e:
        print(f"error making follow up question: {e}")
        return None