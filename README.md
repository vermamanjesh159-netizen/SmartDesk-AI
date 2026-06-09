# 🤖 AI Assistant Pro

AI Assistant Pro is a premium, high-fidelity AI-powered web application built using **Streamlit**, **Groq API**, **OpenAI GPT OSS 120B**, and **Llama 4 Vision**. Designed with a clean, ChatGPT-like professional light-theme user interface, it supports real-time streaming, live web search, specialized task prompt engineering, and visual analysis.

---

## ✨ Features

### 1. 💬 ChatGPT-style Multi-Chat Threads
- **Isolated History Logs**: Maintain separate conversation history per chat thread.
- **Dynamic Thread Renaming**: The app automatically extracts the first few words of the initial prompt to rename the thread dynamically.
- **State Retention**: Selected tone, task dropdown indexes, and parameters are preserved per chat.
- **Creation & Deletion Actions**: Quickly create new threads or delete existing conversations from the sidebar registry.

### 2. ➕ Circular Plus Button Popover Menu
- **Interactive Overlay**: A grey, circular `+` button is placed directly to the left of the chat box. Clicking it displays a popover menu.
- **Select AI Task**: A dropdown menu offering distinct prompt templates (e.g. Summarize, Sentiment Analysis, Translator, Code Generator, Explainer).
- **📎 Image Attachment Dropzone**: A clean dropzone inside the popover to upload images (`PNG`, `JPG`, `JPEG`).
- **🌐 Web Search Toggle**: A checkbox inside the popover to enable/disable DuckDuckGo search retrieval.

### 4. 🧠 OpenAI GPT OSS 120B Model
- Powered by the fast Mixture-of-Experts (MoE) open-weights **`openai/gpt-oss-120b`** model hosted on Groq for state-of-the-art reasoning and speed.

### 4. 🎭 Persona Alignment (Tone Selection)
Align the response persona dynamically. Select from six curated system prompt configurations in the sidebar:
- **Professional**: Formal, polite, structured, and logical.
- **Friendly**: Warm, positive, engaging, with emojis.
- **Creative**: Brainstorming-focused, innovative, and out-of-the-box.
- **Technical**: Developer-centric, providing clean code blocks and architectures.
- **Marketing**: Persuasive, engaging, with high impact and clear calls-to-action.
- **Academic**: Rigorous, analytical, formal, and objective.

### 5. ⚡ Task Specialization (Prompt Engineering)
Boost your productivity with 12 preset specialized tasks. When a task is selected, the application automatically builds a prompt wrapper behind the scenes to optimize the LLM's output for:
- Summarize, Rewrite, Explain, Generate Ideas, Translate, Write Content, Improve Grammar, Generate Email, Create Blog Post, Create LinkedIn Post, Generate Hashtags, and Generate Marketing Copy.

---

## 🛠️ Technology Stack
- **Python 3.12+**
- **Streamlit** (Web Application Framework)
- **Groq API** (GPT OSS 120B / Llama 4 Vision Inference Engine)
- **DuckDuckGo Search** (Live Web Retrieval)
- **Custom CSS** (Cool light-theme layout)

---

## 🚀 Setup & Execution

### 1. Prerequisites
Ensure you have Python 3.10+ installed on your system.

### 2. Clone or Enter the Project Directory
```bash
cd /home/shanti/Test/ai-assistance
```

### 3. Setup Virtual Environment & Install Dependencies
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install ddgs
```

### 4. Set Environment Variables (Optional)
You can create a `.env` file in the root directory to automatically load your Groq API key:
```env
GROQ_API_KEY=your_groq_api_key_here
```

### 5. Launch the Streamlit Server
```bash
streamlit run app.py
```
Open your browser and navigate to `http://localhost:8501`.
