# 🤖 SmartDesk AI

SmartDesk AI is a premium, high-fidelity AI-powered web workspace built using **Streamlit**, **Groq API**, **OpenAI GPT OSS 120B**, and **Llama 4 Vision**. Designed with a clean, ChatGPT-like professional light-theme user interface, it supports real-time streaming, live web search, specialized task prompt engineering, and visual analysis.

---

## ✨ Features

### 1. 💬 ChatGPT-style Multi-Chat Threads
- **Isolated History Logs**: Maintain separate conversation history per chat thread.
- **Dynamic Thread Renaming**: The app automatically extracts the first few words of the initial prompt to rename the thread dynamically.
- **State Retention**: Selected tone, task dropdown indexes, and parameters are preserved per chat.
- **Unified Clear/Delete Actions**: Click the trash bin (`🗑️`) button next to any conversation in the sidebar list to delete the thread (or clear its message history if it's the last remaining thread).

### 2. ➕ Circular Plus Button Popover Menu
- **Interactive Overlay**: A grey, circular `+` button is placed directly to the left of the chat box. Clicking it displays a popover menu.
- **Select AI Task**: A dropdown menu offering distinct prompt templates (e.g. Normal Chat, Summarize, Sentiment Analysis, Translator, Code Generator, Explainer).
- **📎 Image Attachment Dropzone**: A clean dropzone inside the popover to upload images (`PNG`, `JPG`, `JPEG`).
- **🌐 Web Search Toggle**: A checkbox inside the popover to enable/disable DuckDuckGo search retrieval.

### 3. 📋 Clipboard Copy Button
- A ChatGPT-style copy button is placed below every bot response.
- Includes a secure browser check and a legacy clipboard API fallback (`document.execCommand('copy')`) to ensure it works over insecure networks (like local LAN IPs) and inside iframe embeddings.

### 4. 🧠 High-Performance Inference Models
- **Standard Text**: Powered by the fast Mixture-of-Experts (MoE) open-weights **`openai/gpt-oss-120b`** model hosted on Groq for state-of-the-art reasoning and speed.
- **Vision Tasks**: Automatically falls back to high-capability vision models when an image is attached.

### 5. 🎨 Custom Premium Aesthetics
- **Floating Panel Layout**: The chat workspace is rendered inside a beautiful floating page container with a white background, rounded corners (`16px`), and soft depth shadows.
- **Dark Teal / Dark Cyan Header**: A rich, modern teal gradient header spans the top of the chat area.
- **Dark Navy Blue User Bubbles**: High-contrast dark navy blue bubbles (`#0f172a`) with white text.
- **Light Gray Page Background**: Premium gray background canvas (`#f3f4f6`).

---

## 🛠️ Technology Stack
- **Python 3.12+**
- **Streamlit** (Web Application Framework)
- **Groq API** (GPT OSS 120B / Vision Inference Engine)
- **DuckDuckGo Search** (Live Web Retrieval)
- **Custom CSS** (Cool light-theme layout)

---

## 🚀 Setup & Local Execution

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

---

## ☁️ Deploying to Streamlit Community Cloud

Streamlit Community Cloud is the easiest way to deploy python apps for free. Follow these steps:

### 1. Push Code to GitHub
Ensure all code (except `.env` and `venv/`) is pushed to a public GitHub repository.

```bash
git add .
git commit -m "Configure SmartDesk AI for deployment"
git push -u origin main
```

### 2. Deploy on Streamlit Community Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io/) and log in with your GitHub account.
2. Click **New app**.
3. Select your repository (`SmartDesk-AI`), the branch (`main`), and the main file path (`app.py`).

### 3. Configure Secrets (API Keys)
To prevent hardcoding your `GROQ_API_KEY` in the public repository, define it as a Streamlit Secret:
1. Before clicking deploy, click **Advanced settings...** at the bottom of the page.
2. In the **Secrets** text area, paste your keys in TOML format:
   ```toml
   GROQ_API_KEY = "gsk_your_actual_groq_key_here"
   ```
3. Click **Save** and then **Deploy**.
4. Streamlit will build your app environment using `requirements.txt` and run it automatically!
