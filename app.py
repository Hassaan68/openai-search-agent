import os
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_community.tools import DuckDuckGoSearchRun
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage, AIMessage

st.set_page_config(page_title="Web Search AI Agent", page_icon="🔎", layout="centered")
st.title("🔎 Web-Searching AI Agent")
st.caption("Built with LangChain, OpenAI, DuckDuckGo, and Streamlit")

# Sidebar setup for the API key and chat reset
with st.sidebar:
    st.header("Settings")
    env_api_key = os.getenv("OPENAI_API_KEY", "")
    api_key = st.text_input(
        "OpenAI API Key",
        value=env_api_key,
        type="password",
        placeholder="sk-...",
        help="Paste your OpenAI key here, or set OPENAI_API_KEY in your server environment.",
    )
    st.markdown("---")
    if st.button("Clear Conversation"):
        st.session_state.messages = []
        st.rerun()

if not api_key:
    st.info("👈 Drop your OpenAI API key in the sidebar to get started.")
    st.stop()


# Cache the agent so we don't rebuild it on every user message
@st.cache_resource
def load_agent(api_key: str):
    # Default LLM: OpenAI
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        api_key=api_key,
    )

    # --- Want to use a different LLM? ---
    # Because LangChain uses a unified chat model interface, you can swap OpenAI
    # for Claude, Gemini, or any other supported provider by changing just a few lines:
    #
    # Option A: Anthropic Claude (requires `pip install langchain-anthropic`)
    # from langchain_anthropic import ChatAnthropic
    # llm = ChatAnthropic(
    #     model="claude-sonnet-4-6",
    #     temperature=0,
    #     api_key=api_key,  # or set ANTHROPIC_API_KEY in your environment
    # )
    #
    # Option B: Google Gemini (requires `pip install langchain-google-genai`)
    # from langchain_google_genai import ChatGoogleGenerativeAI
    # llm = ChatGoogleGenerativeAI(
    #     model="gemini-3.5-flash",
    #     temperature=0,
    #     google_api_key=api_key,  # or set GOOGLE_API_KEY in your environment
    # )

    search_tool = DuckDuckGoSearchRun()

    system_prompt = (
        "You are a sharp, helpful research assistant. "
        "Whenever a user asks about current events, recent releases, or anything you aren't 100% sure about, "
        "use the web search tool to look it up first. Keep answers clear and mention your sources."
    )

    return create_react_agent(llm, [search_tool], prompt=system_prompt)


agent = load_agent(api_key)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        AIMessage(
            content="Hey! Ask me anything—if I don't know it offhand, I'll search the web for you."
        )
    ]

# Display previous messages
for msg in st.session_state.messages:
    role = "user" if isinstance(msg, HumanMessage) else "assistant"
    with st.chat_message(role):
        st.markdown(msg.content)

# Handle new user input
if user_query := st.chat_input(
    "Ask about today's news, tech updates, or anything else..."
):
    st.session_state.messages.append(HumanMessage(content=user_query))
    with st.chat_message("user"):
        st.markdown(user_query)

    with st.chat_message("assistant"):
        with st.spinner("Searching the web..."):
            try:
                result = agent.invoke({"messages": st.session_state.messages})
                reply = result["messages"][-1].content
                st.markdown(reply)
                st.session_state.messages.append(AIMessage(content=reply))
            except Exception as e:
                st.error(f"Something went wrong: {e}")
