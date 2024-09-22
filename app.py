import streamlit as st
from langchain import hub
from langchain.agents import create_openai_functions_agent
from langchain_openai.chat_models import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.runnables import RunnablePassthrough
from langchain_core.agents import AgentFinish
from langgraph.graph import END, Graph
import os
import uuid
from dotenv import load_dotenv
from firebase_auth import login, signup, logout, data_to_firebase
from datetime import datetime, timedelta
import pytz

load_dotenv()

st.set_page_config(page_title="AI-Powered Search Engine", layout="wide")


st.markdown("""
    <style>

    .big-font {
        font-size: 40px !important;
        font-weight: bold;
        color: #000000;
        text-align: center;
        margin-bottom: 30px;
    }
    .stApp {
        background-color: #f0f2f6;
    }
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        border-radius: 30px;
        padding: 15px 30px;
        font-size: 18px;
        transition: all 0.3s ease 0s;
        border: none;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stButton > button:hover {
        background-color: #45a049;
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
        transform: translateY(-2px);
    }
    .stButton > button:active {
        transform: translateY(0px);
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    .stRadio > label {
        background-color: #e1e5eb;
        padding: 12px;
        border-radius: 8px;
        margin-bottom: 12px;
        transition: all 0.2s ease 0s;
        cursor: pointer;
    }
    .stRadio > label:hover {
        background-color: #d0d4d9;
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stExpander {
        background-color: #ffffff;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    h1 {
        color: #2c3e50;
        font-size: 36px;
        font-weight: bold;
        margin-bottom: 20px;
    }
    h2, h3 {
        color: #34495e;
    }
    .stAlert {
        border-radius: 10px;
        font-weight: bold;
    }
    .stSpinner > div {
        border-color: #4CAF50 !important;
    }
    [data-testid="stAppViewContainer"] {
        background-image: url("https://img.freepik.com/free-photo/vivid-blurred-colorful-wallpaper-background_58702-3508.jpg?size=626&ext=jpg");
        background-size: cover;
    }
    [data-testid="stHeader"] {
        background-color: rgba(0,0,0,0);
    }
    [data-testid="stToolbar"] {
        right: 2rem;
        background-image: url("");
        background-size: cover;
    }
    [data-testid="stSidebarContent"] {
        background-image: url("https://img.freepik.com/free-vector/background-gradient-green-tones_23-2148382072.jpg");
        background-size: cover;
    }
    
    </style>
""", unsafe_allow_html=True)

# Get API keys from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")


if not OPENAI_API_KEY or not TAVILY_API_KEY:
    st.error("Please set OPENAI_API_KEY and TAVILY_API_KEY in your .env file")
    st.stop()

# Initialize tools and agent
tools = [TavilySearchResults(max_results=5)]
prompt = hub.pull("hwchase17/openai-functions-agent")
llm = ChatOpenAI(model="gpt-3.5-turbo")

agent_runnable = create_openai_functions_agent(llm, tools, prompt)

agent = RunnablePassthrough.assign(
    agent_outcome=agent_runnable
)

def execute_tools(data):
    agent_action = data.pop('agent_outcome')
    tools_to_use = {t.name: t for t in tools}[agent_action.tool]
    observation = tools_to_use.invoke(agent_action.tool_input)
    data['intermediate_steps'].append((agent_action, observation))
    return data

def should_continue(data):
    if isinstance(data['agent_outcome'], AgentFinish):
        return "exit"
    else:
        return "continue"

workflow = Graph()
workflow.add_node("agent", agent)
workflow.add_node("tools", execute_tools)
workflow.set_entry_point("agent")
workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "continue": "tools",
        "exit": END
    }
)
workflow.add_edge('tools', 'agent')

# Compile the chain
chain = workflow.compile()

# Function to summarize conversation
def summarize_conversation(messages):
    if not messages:
        return "New Conversation"
    
    first_message = messages[0]["content"]
    summary_prompt = f"Summarize the following message in 5 words or less: {first_message}"
    
    summary = llm.predict(summary_prompt)
    return summary.strip()

def generate_three_line_summary(content):
    summary_prompt = f"Provide a three-line summary of the following content:\n\n{content}\n\nSummary:"
    summary = llm.predict(summary_prompt)
    return summary.strip()

# Function to format search results
def format_search_results(results):
    if not results:
        return "No search results found."
    
    formatted_results = "Top 5 Sources:\n\n"
    for i, result in enumerate(results[:5], 1):
        title = result.get('title')
        url = result.get('url', 'No URL available')
        content = result.get('content', 'No content available')
        
        if title:
            formatted_results += f"{i}. [{title}]({url})\n"
        else:
            formatted_results += f"{i}. [Reference {i}]({url})\n"
        
        summary = generate_three_line_summary(content)
        formatted_results += f"   {summary}\n\n"
    
    return formatted_results

def generate_overall_summary(results):
    if not results:
        return "No information available to summarize."
    
    combined_content = " ".join([result.get('content', '') for result in results[:5]])
    summary_prompt = f"Provide a concise overall summary of the following information:\n\n{combined_content}\n\nSummary:"
    summary = llm.predict(summary_prompt)
    return summary

def is_relevant_query(query, user_data):
    prompt = f"""
    Given the user's department: {user_data['department']}
    and interests: {', '.join(user_data['interests'])},
    is the following query relevant? Query: {query}
    Respond with 'Yes' or 'No'.
    """
    response = llm.predict(prompt)
    return response.strip().lower() == 'yes'

def get_recent_news(user_data, num_articles=10):
    interests = ", ".join(user_data['interests'])
    skills = ", ".join(user_data['skills'])

    current_date = datetime.now(pytz.utc).strftime("%Y-%m-%d")
    
    search_query = f"latest news as of {current_date} related to {interests} and {skills}"
    
    search_results = TavilySearchResults(
        max_results=20,
        include_domains=["bbc.com", "cnn.com", "reuters.com", "apnews.com", "bloomberg.com", "nytimes.com", "wsj.com"],
        exclude_domains=["wikipedia.org"],
        time_range="d"  # d for past day
    ).invoke(search_query)
    
    prompt = f"""
    Based on these search results, identify the 10 most recent and relevant news articles related to the user's interests ({interests}) and skills ({skills}).
    Today's date is {current_date}. Only include articles from the past week, prioritizing the most recent ones.
    For each article, provide:
    1. A concise title (max 15 words)
    2. A brief summary (2-3 sentences)
    3. The source URL
    4. The exact publication date and time (if available, in UTC)
    5. The source name

    Format the output as a list of dictionaries, each containing 'title', 'summary', 'url', 'date', and 'source' keys.
    Ensure the 'date' field is in the format 'YYYY-MM-DD HH:MM:SS UTC' if available, or 'YYYY-MM-DD' if only the date is known.
    If the exact date is not available, use 'Recent' as the date value.
    
    Sort the articles by date, with the most recent first.

    Search results:
    {search_results}
    """
    
    news_articles = eval(llm.predict(prompt))
    
    # Additional processing to ensure recency
    current_time = datetime.now(pytz.utc)
    filtered_articles = []
    for article in news_articles:
        try:
            if article['date'] != 'Recent':
                article_date = datetime.strptime(article['date'].split()[0], "%Y-%m-%d")
                article_date = pytz.utc.localize(article_date)
                if current_time - article_date <= timedelta(days=7):
                    filtered_articles.append(article)
            else:
                filtered_articles.append(article)
        except ValueError:
            # If date parsing fails, include the article anyway
            filtered_articles.append(article)
    
    return filtered_articles[:num_articles]

st.markdown('<p class="big-font">Advance AI Powered Search Engine 🤖</p>', unsafe_allow_html=True)

# Check if user is logged in
if "user_logged_in" not in st.session_state:
    st.session_state.user_logged_in = False

if "trending_topics" not in st.session_state:
    st.session_state.trending_topics = []


st.sidebar.title("User Management")
if st.session_state.user_logged_in:
    logout()
else:
    tab1, tab2 = st.sidebar.tabs(["Login", "Sign Up"])
    with tab1:
        if login():
            st.session_state.user_logged_in = True
            st.cache_data.clear()
            st.rerun()
    with tab2:
        if signup():
            st.session_state.user_logged_in = True
            st.rerun()


if st.session_state.user_logged_in:


    tab1, tab2 = st.tabs(["💬 Chat", "🔥 Trending Topics"])

    with tab1:
        # current_user_chat=get_data_to_firebase()
        # print(current_user_chat)
        # Initialize session state for conversations
        if "conversations" not in st.session_state:
            st.session_state.conversations = {}

        if "current_conversation_id" not in st.session_state:
            st.session_state.current_conversation_id = None


        # Sidebar for conversation management
        st.sidebar.title("Conversations")

        # New conversation button
        if st.sidebar.button("New Conversation"):

            new_id = str(uuid.uuid4())
            st.session_state.conversations[new_id] = {
                "title": "New Conversation",
                "messages": []
            }
            st.session_state.current_conversation_id = new_id
        #Chat History with Inside Div Overflow

    
        for conv_id, conv_data in st.session_state.conversations.items():
            # Update summary title
            if conv_data["messages"]:
                conv_data["title"] = summarize_conversation(conv_data["messages"])
            
            if st.sidebar.button(conv_data["title"], key=conv_id):
                st.session_state.current_conversation_id = conv_id


        if st.session_state.current_conversation_id:
            conversation = st.session_state.conversations[st.session_state.current_conversation_id]
            

            for message in conversation["messages"]:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

            if prompt := st.chat_input("What would you like to search for?"):
                st.chat_message("user").markdown(prompt)
                conversation["messages"].append({"role": "user", "content": prompt})

                if len(conversation["messages"]) == 1:
                    conversation["title"] = summarize_conversation(conversation["messages"])

                if is_relevant_query(prompt, st.session_state.user_data):
                    try:
                        response = chain.invoke({"input": prompt, "intermediate_steps": []})
                        
                        if response.get('intermediate_steps') and response['intermediate_steps']:
                            search_results = response['intermediate_steps'][0][1]
                        else:
                
                            search_tool = TavilySearchResults(max_results=5)
                            search_results = search_tool.invoke(prompt)
                        
                        formatted_results = format_search_results(search_results)
                        overall_summary = generate_overall_summary(search_results)
                        
                        ai_response = f"{response['agent_outcome'].return_values['output']}\n\n{formatted_results}\nOverall Summary:\n{overall_summary}"
                    except Exception as e:
                        st.error(f"An error occurred while processing the search results: {str(e)}")
                        ai_response = "I apologize, but I encountered an error while processing the search results. Please try your query again or rephrase it."
                else:
                    ai_response = "I apologize, but this query doesn't seem to be related to your department or interests. Would you like to rephrase your question or ask something more relevant?"

                with st.chat_message("assistant"):
                    st.markdown(ai_response)
    
                conversation["messages"].append({"role": "assistant", "content": ai_response})
                data_to_firebase(prompt, ai_response, conversation["title"])

                st.rerun()
        else:
            st.info("Please create or select a conversation from the sidebar to start chatting.")
    
    with tab2:
            st.title("Latest News")
            
            if "recent_news" not in st.session_state:
                st.session_state.recent_news = []

            if st.button("🔄 Refresh Latest News", key="refresh_news_button"):
                with st.spinner("Fetching the latest news..."):
                    st.session_state.recent_news = get_recent_news(st.session_state.user_data)
                st.success("News updated with the latest articles!")

            col1, col2 = st.columns(2)

            if st.session_state.recent_news:
                for i, article in enumerate(st.session_state.recent_news):
                    with (col1 if i % 2 == 0 else col2).expander(f"📰 {article['title']}"):
                        st.markdown(f"**{article['summary']}**")
                        st.markdown(f"Source: {article['source']}")
                        st.markdown(f"Published: {article['date']}")
                        st.markdown(f"[Read Full Article]({article['url']})")
            else:
                st.info("Click 'Refresh Latest News' to load the most recent articles.")

            st.caption("News articles are tailored to your interests and skills, focusing on the most recent publications. Click 'Refresh Latest News' for up-to-the-minute updates.")


else:
    st.info("Please log in or sign up to access the chat interface.")
