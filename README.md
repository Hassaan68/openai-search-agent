# 🔎 Web-Searching AI Agent (LangChain + OpenAI + Streamlit)

A minimal, open-source AI research assistant that searches the live web before answering questions. Built with **LangChain / LangGraph**, **OpenAI (`gpt-4o-mini`)**, **DuckDuckGo Search**, and **Streamlit**, and configured for one-click deployment on **Render.com**.

## Features

- **Live Web Search:** Uses DuckDuckGo (`ddgs`) so the agent can look up recent events, tech releases, and real-time facts without needing a separate search API key.
- **Conversational Memory:** Keeps track of your current session in Streamlit so you can ask follow-up questions naturally.
- **Provider-Agnostic Setup:** Uses OpenAI by default, with ready-to-uncomment examples in `app.py` for **Anthropic Claude** and **Google Gemini**.
- **Flexible Key Management:** Reads `OPENAI_API_KEY` from server environment variables in production, or lets users paste their own key directly in the sidebar.
- **Render-Ready:** Includes `.python-version` and a `render.yaml` Blueprint for hassle-free cloud hosting.

---

## Project Structure

```text
openai-search-agent/
├── app.py              # Streamlit UI and LangChain ReAct agent
├── requirements.txt    # Pinned Python dependencies
├── render.yaml         # Render.com Blueprint configuration
├── .python-version     # Pins Python 3.11.9 for consistent builds
├── .env.example        # Sample environment variables
├── .gitignore          # Git ignore rules
├── LICENSE             # MIT License
└── README.md           # Project documentation
```

---

## Run Locally

1. Clone the repository:

```bash
git clone https://github.com/Hassaan68/openai-search-agent.git
cd openai-search-agent
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Start the Streamlit app:

```bash
streamlit run app.py
```

5. Open `http://localhost:8501` in your browser and enter your OpenAI API key in the sidebar.

---

## Using Other LLMs (Claude, Gemini, etc.)

Because LangChain standardizes chat model interfaces, switching away from OpenAI takes only a few lines of code:

1. Uncomment the provider you want in `requirements.txt` (`langchain-anthropic` or `langchain-google-genai`) and install it.
2. Open `app.py` and uncomment the corresponding model block inside `load_agent()`:

```python
# Anthropic Claude
from langchain_anthropic import ChatAnthropic
llm = ChatAnthropic(model="claude-sonnet-4-6", temperature=0, api_key=api_key)

# Google Gemini
from langchain_google_genai import ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash", temperature=0, google_api_key=api_key)
```

---

## Deploy on Render.com

### Option 1: Deploy via Render Blueprint (`render.yaml`)

1. Push or fork this repository to your GitHub account.
2. In your [Render Dashboard](https://dashboard.render.com/), click **New + → Blueprint** and connect `openai-search-agent`.
3. Render automatically reads `render.yaml` and `.python-version`. Add your `OPENAI_API_KEY` when prompted (or leave it blank if you want visitors to input their own key in the sidebar).

### Option 2: Manual Web Service Setup

1. Click **New + → Web Service** in Render and connect your GitHub repo.
2. Set the **Build Command** to:

```bash
pip install -r requirements.txt
```

3. Set the **Start Command** to:

```bash
streamlit run app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true
```

4. (Optional) Add `OPENAI_API_KEY` under **Environment Variables** and click **Create Web Service**.

---

## License

This project is open-sourced under the [MIT License](LICENSE).
