<br />
<div align="center">
  <h3 align="center">Godrej AI Chat Application</h3>
  <p align="center">
    Advance Search with Personalization
  </p>
</div>

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about">About</a></li>
    <li><a href="#features">Features</a></li>
    <li><a href="#tech-stack">Tech Stack</a></li>
    <li><a href="#instructions-on-running-project-locally">Instructions on running project locally</a></li>
    <li><a href="#usecases">Usecases</a></li>
    <li><a href="#feedback">Feedback</a></li>
  </ol>
</details>

------

## About

The Godrej AI Chat is specifically built with the multi agent workflow, to provide the result in a desired format. The user can search about any information form LLM which is connected to the web, it also provide the top 5 best sources, and even summarizing them which saves a lot of time.

The thread conversation management is also been applied to store the conversation of the user, the conversation is stored in the Firebase Real Time Database.

The personalization for the chat is provided by taking the information of the skill, department and the interest of the user and taking use of it for the search.
 

## Demonstration

Try the Application Now -

<a href="https://godrej-chat-ai.streamlit.app/" target="_blank" style="
    display: inline-block;
    padding: 12px 24px;
    font-size: 18px;
    font-weight: bold;
    color: #ffffff;
    background-color: #007bff;
    border: none;
    border-radius: 8px;
    text-align: center;
    text-decoration: none;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    transition: background-color 0.3s, box-shadow 0.3s;
">
    Godrej AI Chat
</a>


## Worflow Architecture

![https://github.com/Hrishikesh332/Godrej-Chat-AI/blob/main/src/worflow-recent-news.png](https://github.com/Hrishikesh332/Godrej-Chat-AI/blob/main/src/worflow-recent-news.png)


## Features

- **AI-Powered Conversations** - LLM model for intelligent responses.
- **Custom Search** - Uses Tavily Search for searching relevant content from web.
- **Personalization** - User skill, interest and Interaction info is taken into the account to provide the latest news and updates.
- **User Authentication** - Secure login and signup functionality powered by Firebase Auth.
- **Responsive UI** - Interactive chat UI built with Streamlit.
- **Multi-agent Workflow** - Supports multiple agents for diverse AI functionalities with the help of Langgraph.


## Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python, OpenAI, Langchain, Langchain-openai, LangGraph, Langchain-community, Tavily, Langchain.agents
- **Deployment**: Streamlit Cloud
- **Authentication**: Firebase Authentication, Firebase Real Time Database


## User Journey of Application

![https://github.com/Hrishikesh332/Godrej-Chat-AI/blob/main/src/user-journey.png](https://github.com/Hrishikesh332/Godrej-Chat-AI/blob/main/src/user-journey.png)


## Instructions on running project locally

To run the YouTube Chapter Highlight Generator locally, follow these steps -

### Step 1 - Clone the project

```bash
git clone https://github.com/Hrishikesh332/Godrej-Chat-AI.git


Step 2  -

Install dependencies:

```bash
 cd Godrej-Chat-AI
 
 pip install -r requirements.txt
```

Step 3 - 

Set up your env -

```
OPENAI_API_KEY=your_openai_api_key
TAVILY_API_KEY=your_tavily_api_key
```


Step 4 -

Run the Streamlit application

```bash
  streamlit run app.py
```

Step 7 - 

Run the Server -

```bash
  http://localhost:8501/
```

If you wanna try with the other credentials, without signning, you can try with

mail - hriskikesh.yadav332@gmail.com
psswd - test123


## Full Fledge Approach for Organization Adoption

![https://github.com/Hrishikesh332/Godrej-Chat-AI/blob/main/src/vision-workflow.png](https://github.com/Hrishikesh332/Godrej-Chat-AI/blob/main/src/vision-workflow.png)

## Data Store In Firebase
```bash
{
  "users": {
    "YvkgYtJ582Z8UTCgch1xycnvmG72": {
      "2024-09-19T232234": {
        "email": "hriskikesh.yadav332@gmail.com",
        "status": "success",
        "timestamp": "2024-09-19T232234"
      },
      "2024-09-19T233211": {
        "email": "hriskikesh.yadav332@gmail.com",
        "status": "success",
        "timestamp": "2024-09-19T233211"
      },
      "2024-09-19T233648": {
        "email": "hriskikesh.yadav332@gmail.com",
        "status": "success",
        "timestamp": "2024-09-19T233648"
      },
      "2024-09-19T233846": {
        "email": "hriskikesh.yadav332@gmail.com",
        "status": "success",
        "timestamp": "2024-09-19T233846"
      },
      "2024-09-19T234305": {
        "email": "hriskikesh.yadav332@gmail.com",
        "status": "success",
        "timestamp": "2024-09-19T234305"
      },
      "2024-09-19T235402": {
        "email": "hriskikesh.yadav332@gmail.com",
        "status": "success",
        "timestamp": "2024-09-19T235402"
      },
      "department": "IT",
      "interests": [
        "Technology"
      ],
      "skills": [
        "Data"
      ]
    }
  }
}
```
## Feedback

If you have any feedback, please reach out to us at **hriskikesh.yadav332@gmail.com**


## License

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)


