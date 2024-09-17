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

# Load environment variables from .env file
load_dotenv()

# Get API keys from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# Ensure API keys are set
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

# Set up the workflow
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

# Function to generate a three-line summary
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

# Function to generate overall summary
def generate_overall_summary(results):
    if not results:
        return "No information available to summarize."
    
    combined_content = " ".join([result.get('content', '') for result in results[:5]])
    summary_prompt = f"Provide a concise overall summary of the following information:\n\n{combined_content}\n\nSummary:"
    summary = llm.predict(summary_prompt)
    return summary

# Streamlit UI
st.title("AI-Powered Search Engine")

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

# Display and select conversations
for conv_id, conv_data in st.session_state.conversations.items():
    # Generate or update summary title
    if conv_data["messages"]:
        conv_data["title"] = summarize_conversation(conv_data["messages"])
    
    if st.sidebar.button(conv_data["title"], key=conv_id):
        st.session_state.current_conversation_id = conv_id

# Main chat interface
if st.session_state.current_conversation_id:
    conversation = st.session_state.conversations[st.session_state.current_conversation_id]
    
    # Display chat messages from history on app rerun
    for message in conversation["messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("What would you like to search for?"):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        conversation["messages"].append({"role": "user", "content": prompt})

        # Update conversation title after first message
        if len(conversation["messages"]) == 1:
            conversation["title"] = summarize_conversation(conversation["messages"])

        # Generate AI response
        try:
            response = chain.invoke({"input": prompt, "intermediate_steps": []})
            
            # Check if there are any intermediate steps
            if response.get('intermediate_steps') and response['intermediate_steps']:
                search_results = response['intermediate_steps'][0][1]
            else:
                # If no intermediate steps, perform a direct search
                search_tool = TavilySearchResults(max_results=5)
                search_results = search_tool.invoke(prompt)
            
            formatted_results = format_search_results(search_results)
            overall_summary = generate_overall_summary(search_results)
            
            ai_response = f"{response['agent_outcome'].return_values['output']}\n\n{formatted_results}\nOverall Summary:\n{overall_summary}"
        except Exception as e:
            st.error(f"An error occurred while processing the search results: {str(e)}")
            ai_response = "I apologize, but I encountered an error while processing the search results. Please try your query again or rephrase it."

        # Display AI response in chat message container
        with st.chat_message("assistant"):
            st.markdown(ai_response)
        # Add AI response to chat history
        conversation["messages"].append({"role": "assistant", "content": ai_response})

        # Force a rerun to update the display with the new messages
        st.rerun()
else:
    st.info("Please create or select a conversation from the sidebar to start chatting.")

# Add a sidebar with additional information
st.sidebar.title("About")
st.sidebar.info(
    "This is an AI-powered search engine that uses LangChain and OpenAI's GPT model. "
    "It can answer questions and provide information on a wide range of topics. "
    "You can create multiple conversations and switch between them using the sidebar."
)

# Add a footer
st.markdown(
    """
    ---
    Created with ❤️ using Streamlit, LangChain, and OpenAI
    """
)