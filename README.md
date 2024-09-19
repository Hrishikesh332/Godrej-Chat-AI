<br />
<div align="center">
  <h3 align="center">Godrej AI Chat Application</h3>
  <p align="center">
    Advance Search with Personalization
    <br />
    <a href="https://github.com/Hrishikesh332/Godrej-Chat-AI"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://godrej-chat-ai.streamlit.app/">View Demo</a>
    ·
    <a href="https://github.com/Hrishikesh332/Godrej-Chat-AI/issues">Report Bug</a>
    ·
    <a href="https://github.com/Hrishikesh332/Godrej-Chat-AI/issues">Request Feature</a>
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

The thread conversation management is also been applied to store the conversation of the user, for now it's kept in the vanishing mode and it is maintain as per the session state.

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

## Features

- **AI-Powered Conversations** - OpenAI model for intelligent responses.
- **Custom Search** - Uses Tavily Search for searching relevant content from web.
- **Personalization** - User skill and interest info is taken into the account 
- **User Authentication** - Secure login and signup functionality powered by Firebase.
- **Responsive UI** - Interactive chat UI built with Streamlit.
- **Multi-agent System** - Supports multiple agents for diverse AI functionalities.

## Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python, OpenAI, Langchain, Langchain-openai, LangGraph, Langchain-community
- **Deployment**: Streamlit Cloud
- **Authentication**: Firebase Authentication

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


## Feedback

If you have any feedback, please reach out to us at **hriskikesh.yadav332@gmail.com**


## License

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)


