# TalentScout AI Hiring Assistant

This is a smart AI chatbot that helps the "TalentScout" recruitment agency with initial interviews. This project shows how to use a Large Language Model (LLM) to build a solid app that's easy and smart to use.

## ✨ Key Features

* **Gathers All Info:** Gathers all the important info from a candidate, like their name, email, phone number, experience, and tech skills.
* **Smart Questions:** Uses a powerful AI (a Large Language Model) to create technical questions on the fly, based on the skills the candidate lists.
* **Stays on Topic:** It cleverly uses a second AI check to make sure the candidate's answers are relevant, keeping the conversation on track.
* **Asks Follow-up Questions:** The chatbot checks if a candidate's answer is clear. If it's too short or vague, it asks a smart follow-up question to get more details, just like a real interviewer.
* **Easy to Use:** You can end the conversation at any time by typing keywords like `exit`, `quit`, or `bye`.

##  Technical Stack

* **Language:** Python 3.9+
* **Framework:** Streamlit (to build the web interface)
* **AI Model Connection:** LangChain with OpenRouter.ai
* **Core AI Model:** `mistralai/mistral-7b-instruct`

## ⚙️ Installation & Setup

Follow these steps to get the project running on your computer.

### 1. Clone the Repository

```bash
git clone https://github.com/patelsourabh/Hiring-Assistant
```

### 2. Create a Virtual Environment (Recommended)

It's a good idea to keep this project's packages separate from your other Python projects.

```bash
# For macOS/Linux
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
.\venv\Scripts\activate.ps1
```

### 3. Install Dependencies

This command installs all the Python libraries needed for the project.

```bash
pip install -r requirements.txt
```

### 4. Set Up Your API Key (OpenRouter)

The project needs an API key to talk to the AI model via OpenRouter.

1.  Go to [OpenRouter.ai](https://openrouter.ai/) and sign up or log in.
2.  Go to your **Keys** page (click your profile icon in the top-right).
3.  Create a new key and copy it.
4.  In the project folder, create a new file and name it `.env`.
5.  Add the following line to the `.env` file, pasting your key where shown:
    ```
    OPENROUTER_API_KEY="your_secret_openrouter_api_key_here"
    ```
The app will now be able to use your key securely.

## ▶Usage

Once everything is set up, run this command in your terminal:

```bash
streamlit run app.py
```

A new tab should open in your web browser with the chatbot ready to go.

##  How It Works: Decisions & Prompts

### Architecture

The app's logic is built like a flowchart, known as a **Finite State Machine (FSM)**. This makes the conversation flow logical and easy to manage. The code is split into different files to keep things organized:

* `app.py`: Handles the user interface you see in the browser.
* `chatbot_logic.py`: The "brain" of the app; it decides what happens next in the conversation.
* `llm_handler.py`: Handles all the communication with the AI service.
* `prompts.py`: Keeps all the instructions (prompts) for the AI in one place, so they are easy to edit.

### Prompt Design

I used a few different types of prompts to talk to the AI reliably:

1.  **Question Generation Prompt:** This prompt gives very specific instructions to the AI to make sure it returns a clean list of questions in JSON format. This helps prevent errors.
2.  **Relevance Check Prompt:** This is a quick and cheap way to check if a user's answer is on-topic. It tells the AI to only answer "YES" or "NO".
3.  **"Evaluate -> Act" Prompt Chain:** To handle follow-up questions, it's a two-step process:
    * First, an **evaluation prompt** asks the AI to check if an answer is clear and return a simple status (`{"status": "UNCLEAR", "reason": "..."}`).
    * Then, if the answer was "UNCLEAR," a **follow-up prompt** uses this reason to ask a better, more specific question.

## Challenges & Solutions

### Challenge 1: Getting the AI to Cooperate

* **Problem:** Sometimes, AI models can give messy or unexpected answers instead of the clean data an app needs.
* **Solution:** I solved this by writing very clear instructions (prompts) for the AI. The code also includes `try-except` blocks to safely handle the AI's response and avoid crashes if the format isn't perfect.

### Challenge 2: Remembering the Conversation

* **Problem:** A challenge with Streamlit is that it refreshes the app with every click, which can make it forget what happened before.
* **Solution:** To solve this, I used `st.session_state` to store all the conversation details. It's like the app's short-term memory, so it remembers everything even when the app refreshes.
