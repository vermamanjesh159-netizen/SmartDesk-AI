import os
import base64
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="SmartDesk AI",
    page_icon="favicon.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load and inject custom CSS styling
def local_css(file_name):
    if os.path.exists(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style.css")

# --- DATA DICTIONARIES ---

# Tone System Prompts
TONE_SYSTEM_PROMPTS = {
    "Professional": "You are a professional AI assistant. Provide structured, formal, polite, and precise answers. Focus on clear, logical reasoning, and avoid colloquialisms.",
    "Friendly": "You are a friendly, warm, and conversational AI assistant. Use encouraging, positive language, be approachable, and feel free to use appropriate emojis to make the interaction engaging.",
    "Creative": "You are a highly creative brainstorming assistant. Offer innovative, diverse, out-of-the-box ideas. Encourage lateral thinking, use rich analogies, and explore unique angles.",
    "Technical": "You are a senior software engineer and technical expert. Provide clean, well-explained code snippets, use technical terms accurately, explain architectural concepts, and suggest best practices.",
    "Marketing": "You are an expert marketer, copywriter, and brand strategist. Focus on persuasive language, brand voice, psychological triggers, high engagement, and clear calls to action (CTAs).",
    "Academic": "You are an academic researcher and scholar. Use analytical, objective, and scholarly language. Structure your responses formally, cite concepts or methodologies where applicable, and maintain deep intellectual rigor."
}

# Task Guidelines & Prompt Engineering Templates
TASK_DETAILS = {
    "Normal Chat": {
        "description": "Standard conversational chat without task prompt wrappers.",
        "template": "{user_input}"
    },
    "Summarize": {
        "description": "Summarize the text, highlighting main ideas and key takeaways.",
        "template": "Please summarize the following text. Capture the main ideas, key takeaways, and present it clearly (with bullet points if appropriate):\n\n---\n{user_input}\n---"
    },
    "Rewrite": {
        "description": "Rewrite the text to improve clarity, flow, and professional appeal.",
        "template": "Please rewrite the following text to improve its clarity, flow, tone, and overall quality while keeping the original meaning intact:\n\n---\n{user_input}\n---"
    },
    "Explain": {
        "description": "Break down complex concepts into simple, easy-to-understand terms.",
        "template": "Please explain the following concept or text in simple, easy-to-understand terms. Use analogies if helpful and break down complex jargon:\n\n---\n{user_input}\n---"
    },
    "Generate Ideas": {
        "description": "Brainstorm a list of creative ideas and strategies.",
        "template": "Please generate a list of creative, actionable ideas and strategies based on the following input:\n\n---\n{user_input}\n---"
    },
    "Translate": {
        "description": "Translate the input text to a target language.",
        "template": "Please translate the following text. (If a target language is not specified in the text, please translate it to English or detect the context to provide the best translation):\n\n---\n{user_input}\n---"
    },
    "Write Content": {
        "description": "Draft high-quality structured content like essays, articles, or reports.",
        "template": "Please write high-quality, structured content based on the following instructions or outline:\n\n---\n{user_input}\n---"
    },
    "Improve Grammar": {
        "description": "Fix grammar, punctuation, spelling, and style errors.",
        "template": "Please review the following text for grammar, punctuation, spelling, and stylistic errors. Provide the corrected text and briefly explain the changes made:\n\n---\n{user_input}\n---"
    },
    "Generate Email": {
        "description": "Write a professional email based on details provided.",
        "template": "Please write a professional, well-structured email based on the following requirements or bullet points:\n\n---\n{user_input}\n---"
    },
    "Create Blog Post": {
        "description": "Draft a comprehensive, SEO-friendly blog post with headers.",
        "template": "Please draft a comprehensive, engaging, and SEO-friendly blog post based on the following topic or outline. Include an eye-catching title, structured subheadings (H2, H3), and a strong conclusion:\n\n---\n{user_input}\n---"
    },
    "Create LinkedIn Post": {
        "description": "Write an engaging LinkedIn post with structured paragraphs and hashtags.",
        "template": "Please create an engaging LinkedIn post based on the following information. Structure it with short, punchy paragraphs, relevant emojis to make it readable, a call-to-action, and relevant hashtags at the bottom:\n\n---\n{user_input}\n---"
    },
    "Generate Hashtags": {
        "description": "Produce relevant, trending hashtags for social media platforms.",
        "template": "Please generate a set of relevant, high-impact hashtags for social media based on the following content or topic. Categorize them by reach (broad, niche, industry-specific) if appropriate:\n\n---\n{user_input}\n---"
    },
    "Generate Marketing Copy": {
        "description": "Draft persuasive ad copy, product descriptions, or sales pitches.",
        "template": "Please draft persuasive marketing copy, product descriptions, or sales pitches based on the following specifications. Focus on benefits, emotional hooks, and a strong call-to-action:\n\n---\n{user_input}\n---"
    }
}

# Prompt Templates for sidebar selection
PROMPT_TEMPLATES = {
    "None": "",
    "Professional Email": "Write a formal email asking for an update on the project timeline. Mention that the client is requesting progress details.",
    "Creative Pitch": "Create a 3-sentence pitch for a smart water bottle that tracks hydration levels and syncs with fitness apps.",
    "Code Refactoring": "Refactor the following Python code to make it more Pythonic and optimize its performance:\n\ndef find_elements(arr):\n    result = []\n    for i in range(len(arr)):\n        if arr[i] % 2 == 0:\n            result.append(arr[i])\n    return result",
    "Meeting Summary": "Summarize the key decisions and actions from this meeting transcript:\n- John proposed shifting the launch date to Oct 15.\n- Sarah agreed to check dev team capacity.\n- Budget increase of 10% was approved.",
    "Translation Request": "Translate the following Spanish paragraph into fluent French:\n\n'La inteligencia artificial está transformando la forma en que trabajamos y nos comunicamos cotidianamente.'"
}

# Supported Models
GROQ_MODELS = {
    "GPT OSS 120B (OpenAI / Groq)": "openai/gpt-oss-120b"
}

# --- SESSION STATE INITIALIZATION ---

import time

if "chats" not in st.session_state:
    st.session_state.chats = {
        "chat_1": {
            "title": "New Chat",
            "messages": [],
            "tone": "Professional",
            "task": "Normal Chat"
        }
    }
    st.session_state.current_chat_id = "chat_1"

# Dynamically fetch the current active chat details
current_chat = st.session_state.chats[st.session_state.current_chat_id]

# Keep st.session_state.messages linked to current chat messages
st.session_state.messages = current_chat["messages"]

if "chat_input" not in st.session_state:
    st.session_state.chat_input = ""

# Try to get API key from environment variable
env_api_key = os.environ.get("GROQ_API_KEY", "")

with st.sidebar:
    # Title Header (Mockup)
    st.markdown('<div class="sidebar-header">🌐 SmartDesk AI</div>', unsafe_allow_html=True)
    
    # Powered by GPT OSS 120B green pill (Mockup)
    st.markdown('<div class="llama-badge">🚀 Powered by GPT OSS 120B</div>', unsafe_allow_html=True)
    
    # New Chat Action Button
    st.markdown('<div class="new-chat-btn">', unsafe_allow_html=True)
    if st.button("➕ New Chat", use_container_width=True):
        new_chat_num = len(st.session_state.chats) + 1
        new_chat_id = f"chat_{new_chat_num}_{int(time.time())}"
        st.session_state.chats[new_chat_id] = {
            "title": f"Chat {new_chat_num}",
            "messages": [],
            "tone": "Professional",
            "task": "Normal Chat"
        }
        st.session_state.current_chat_id = new_chat_id
        st.session_state.chat_input = ""
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # List of conversation threads
    st.markdown("<div style='margin-top: 1rem; margin-bottom: 0.5rem; font-weight: 600; color: #2563eb;'>💬 Conversations</div>", unsafe_allow_html=True)
    
    for chat_id, chat in list(st.session_state.chats.items()):
        is_active = (chat_id == st.session_state.current_chat_id)
        btn_class = "chat-thread-btn-active" if is_active else "chat-thread-btn"
        
        col1, col2 = st.columns([0.80, 0.20])
        with col1:
            st.markdown(f'<div class="{btn_class}">', unsafe_allow_html=True)
            if st.button(f"💬 {chat['title']}", key=f"select_{chat_id}", use_container_width=True):
                st.session_state.current_chat_id = chat_id
                st.session_state.chat_input = ""
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="chat-thread-del">', unsafe_allow_html=True)
            if st.button("🗑️", key=f"del_{chat_id}", help="Delete or Clear this conversation"):
                if len(st.session_state.chats) > 1:
                    del st.session_state.chats[chat_id]
                    if chat_id == st.session_state.current_chat_id:
                        st.session_state.current_chat_id = list(st.session_state.chats.keys())[0]
                else:
                    # Reset the single remaining chat
                    st.session_state.chats[chat_id]["messages"] = []
                st.session_state.chat_input = ""
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<hr style='border-color: rgba(0,0,0,0.05); margin: 1rem 0;'>", unsafe_allow_html=True)
    
    # API Credentials & Settings
    st.markdown("### 🔑 API Configuration")
    api_key_input = st.text_input(
        "Groq API Key",
        value=env_api_key,
        type="password",
        placeholder="gsk_...",
        help="Get your API key from console.groq.com"
    )
    
    model_friendly_name = st.selectbox(
        "Select Model",
        options=list(GROQ_MODELS.keys()),
        index=0
    )
    selected_model_id = GROQ_MODELS[model_friendly_name]
    
    with st.expander("⚙️ Advanced Parameters"):
        temperature = st.slider("Temperature", min_value=0.0, max_value=2.0, value=0.7, step=0.1)
        max_tokens = st.slider("Max Tokens", min_value=128, max_value=8192, value=4096, step=128)
    
    st.markdown("<hr style='border-color: rgba(0,0,0,0.05); margin: 1rem 0;'>", unsafe_allow_html=True)
    
    # AI Tone Selection (Requirement 2 & Mockup)
    tone_options = list(TONE_SYSTEM_PROMPTS.keys())
    saved_tone = current_chat.get("tone", "Professional")
    tone_idx = tone_options.index(saved_tone) if saved_tone in tone_options else 0
    
    selected_tone = st.selectbox(
        "Select AI Tone",
        options=tone_options,
        index=tone_idx
    )
    current_chat["tone"] = selected_tone



# --- MAIN WORKSPACE ---

st.markdown(
    f'<div class="chat-header-card">'
    f'  <div class="chat-header-title">🌐 SmartDesk AI</div>'
    f'  <div class="chat-header-subtitle">Powered by GPT OSS 120B & Llama 4 Vision</div>'
    f'</div>',
    unsafe_allow_html=True
)

# Connection Status Badge
is_connected = bool(api_key_input)
if not is_connected:
    st.warning("⚠️ Please provide a Groq API Key in the sidebar to run tasks.")

# 1. Render the Conversation History (from oldest to newest)
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(
            f'<div class="output-bubble-user">{msg["content"]}</div>',
            unsafe_allow_html=True
        )
        # Render uploaded image in history if it exists
        if msg.get("image_base64"):
            st.image(
                f"data:{msg['image_type']};base64,{msg['image_base64']}",
                caption="Uploaded Image",
                width=150
            )
    else:
        # If this assistant message used web search, render the search results first
        if msg.get("search_results"):
            with st.expander("🔍 Web Search Results Used", expanded=False):
                for idx, res in enumerate(msg["search_results"]):
                    st.markdown(f"**[{idx+1}] [{res.get('title')}]({res.get('href')})**")
                    st.write(res.get('body'))

        # Encode assistant response for safe copy to clipboard using JavaScript
        encoded_content = base64.b64encode(msg["content"].encode('utf-8')).decode('utf-8')
        
        st.markdown(
            f'<div class="assistant-bubble-container">'
            f'  <div class="output-bubble-assistant">{msg["content"]}</div>'
            f'  <div class="bubble-actions">'
            f'    <button class="copy-btn" onclick="'
            f'      const b64 = this.getAttribute(\'data-text\');'
            f'      const decoded = decodeURIComponent(escape(window.atob(b64)));'
            f'      if (navigator.clipboard && window.isSecureContext) {{'
            f'        navigator.clipboard.writeText(decoded);'
            f'      }} else {{'
            f'        const textArea = document.createElement(\'textarea\');'
            f'        textArea.value = decoded;'
            f'        textArea.style.position = \'fixed\';'
            f'        textArea.style.opacity = \'0\';'
            f'        document.body.appendChild(textArea);'
            f'        textArea.focus();'
            f'        textArea.select();'
            f'        try {{ document.execCommand(\'copy\'); }} catch (err) {{}}'
            f'        document.body.removeChild(textArea);'
            f'      }}'
            f'      const originalInner = this.innerHTML;'
            f'      this.innerHTML = \'<svg stroke=&quot;currentColor&quot; fill=&quot;none&quot; stroke-width=&quot;2&quot; viewBox=&quot;0 0 24 24&quot; stroke-linecap=&quot;round&quot; stroke-linejoin=&quot;round&quot; class=&quot;copy-icon&quot; height=&quot;1em&quot; width=&quot;1em&quot; xmlns=&quot;http://www.w3.org/2000/svg&quot;><polyline points=&quot;20 6 9 17 4 12&quot;></polyline></svg> Copied!\';'
            f'      this.classList.add(\'copied\');'
            f'      setTimeout(() => {{'
            f'          this.innerHTML = originalInner;'
            f'          this.classList.remove(\'copied\');'
            f'      }}, 2000);'
            f'    " data-text="{encoded_content}">'
            f'      <svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round" class="copy-icon" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path><rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect></svg> Copy'
            f'    </button>'
            f'  </div>'
            f'</div>',
            unsafe_allow_html=True
        )

# 2. Render the Chat Input at the bottom of the page inside columns (with circular popover button)
with st.container(key="sticky-chat-bar"):
    col_plus, col_input = st.columns([0.08, 0.92])

    with col_plus:
        with st.popover("➕", help="AI Settings & Attachments"):
            st.markdown("### 🛠️ Options & Attachments")
            
            # Select AI Task Dropdown
            task_options = list(TASK_DETAILS.keys())
            saved_task = current_chat.get("task", "Normal Chat")
            task_idx = task_options.index(saved_task) if saved_task in task_options else 0
            selected_task = st.selectbox(
                "Select AI Task",
                options=task_options,
                index=task_idx
            )
            current_chat["task"] = selected_task
            
            # Upload Image
            uploaded_file = st.file_uploader("📎 Upload Image", type=["png", "jpg", "jpeg"])
            
            # Web Search Toggle
            web_search_enabled = st.checkbox("🌐 Enable Web Search (DuckDuckGo)", value=current_chat.get("web_search", False))
            current_chat["web_search"] = web_search_enabled
            
            st.info("💡 **Tip**: After configuration, type your message in the chat input and press Enter to search.")

    with col_input:
        prompt_response = st.chat_input(
            placeholder="Message SmartDesk AI...",
            key="chat_input"
        )

# 3. Handle submission
if prompt_response:
    user_prompt_text = prompt_response.strip()
    
    if not api_key_input:
        st.error("⚠️ Error: Please enter your Groq API Key in the sidebar.")
    elif not user_prompt_text and uploaded_file is None:
        st.warning("⚠️ Please enter a prompt or upload an image before generating a response.")
    else:
        # Default prompt if user only uploaded an image
        final_prompt = user_prompt_text if user_prompt_text else "Analyze this image and describe what you see."

        # Fetch web search results if enabled
        search_context = ""
        search_results = []
        if web_search_enabled:
            with st.spinner("Searching the web for latest information..."):
                try:
                    from ddgs import DDGS
                    with DDGS() as ddgs:
                        search_results = [r for r in ddgs.text(final_prompt, max_results=5)]
                    
                    if search_results:
                        context_parts = []
                        for idx, res in enumerate(search_results):
                            context_parts.append(
                                f"[{idx+1}] Title: {res.get('title')}\n"
                                f"URL: {res.get('href')}\n"
                                f"Snippet: {res.get('body')}\n"
                            )
                        search_context = "\n".join(context_parts)
                except Exception as search_err:
                    st.warning(f"⚠️ Web search error: {str(search_err)}. Proceeding without search results.")

        # Encode image to base64 if uploaded
        image_base64 = None
        image_type = None
        if uploaded_file is not None:
            image_type = uploaded_file.type
            file_bytes = uploaded_file.getvalue()
            image_base64 = base64.b64encode(file_bytes).decode("utf-8")

        # Append User message to session state
        st.session_state.messages.append({
            "role": "user",
            "content": final_prompt,
            "image_base64": image_base64,
            "image_type": image_type
        })
        
        # Dynamically set chat title based on the first prompt
        if len(st.session_state.messages) == 1 or current_chat["title"].startswith("Chat ") or current_chat["title"] == "New Chat":
            words = final_prompt.split()
            title_candidate = " ".join(words[:4])
            if len(title_candidate) > 25:
                title_candidate = title_candidate[:25] + "..."
            if not title_candidate:
                title_candidate = "Visual Prompt"
            current_chat["title"] = title_candidate
        
        # Render the User prompt immediately while streaming the response
        st.markdown(
            f'<div class="output-bubble-user">{final_prompt}</div>',
            unsafe_allow_html=True
        )
        if image_base64:
            st.image(
                f"data:{image_type};base64,{image_base64}",
                caption="Uploaded Image",
                width=150
            )

        # Build Groq Messages payload
        system_prompt = TONE_SYSTEM_PROMPTS[selected_tone]
        groq_messages = [{"role": "system", "content": system_prompt}]
        
        # Load previous history
        for msg in st.session_state.messages[:-1]:
            if msg.get("image_base64"):
                content_list = [
                    {"type": "text", "text": msg["content"]},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{msg['image_type']};base64,{msg['image_base64']}"
                        }
                    }
                ]
                groq_messages.append({"role": msg["role"], "content": content_list})
            else:
                groq_messages.append({"role": msg["role"], "content": msg["content"]})
            
        # Apply the Task engineering template to current input
        task_wrapper_template = TASK_DETAILS[current_chat["task"]]["template"]
        wrapped_user_prompt = task_wrapper_template.format(user_input=final_prompt)
        
        # If web search results were found, inject them as a RAG context
        if search_context:
            wrapped_user_prompt = (
                f"You have access to the following live web search results to answer the query:\n\n"
                f"{search_context}\n\n"
                f"Please write a comprehensive response based on these results. Cite your sources using [1], [2], etc.\n\n"
                f"Query: {wrapped_user_prompt}"
            )
            
        # Format the current user query according to presence of an image
        if image_base64:
            current_user_content = [
                {"type": "text", "text": wrapped_user_prompt},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:{image_type};base64,{image_base64}"
                    }
                }
            ]
            groq_messages.append({"role": "user", "content": current_user_content})
        else:
            groq_messages.append({"role": "user", "content": wrapped_user_prompt})
        
        # Show search results in an expander if search was successful
        if search_results:
            with st.expander("🔍 Web Search Results Used", expanded=False):
                for idx, res in enumerate(search_results):
                    st.markdown(f"**[{idx+1}] [{res.get('title')}]({res.get('href')})**")
                    st.write(res.get('body'))
        
        # Determine whether this is a vision conversation requiring the Vision Model
        is_vision_query = any(msg.get("image_base64") for msg in st.session_state.messages) or (image_base64 is not None)
        active_model_id = "meta-llama/llama-4-scout-17b-16e-instruct" if is_vision_query else selected_model_id
        
        # Display response area
        response_container = st.empty()
        
        spinner_msg = "Llama 4 Vision is analyzing..." if is_vision_query else "GPT OSS 120B is analyzing..."
        with st.spinner(spinner_msg):
            try:
                # Initialize Groq client
                client = Groq(api_key=api_key_input)
                
                # Fetch streamed response
                chat_completion = client.chat.completions.create(
                    messages=groq_messages,
                    model=active_model_id,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    stream=True
                )
                
                full_response = ""
                for chunk in chat_completion:
                    content_chunk = chunk.choices[0].delta.content
                    if content_chunk:
                        full_response += content_chunk
                        response_container.markdown(
                            f'<div class="output-bubble-assistant">{full_response}</div>', 
                            unsafe_allow_html=True
                        )
                        
                # Append assistant reply to session state
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": full_response,
                    "model_used": active_model_id,
                    "search_results": search_results
                })
                
                # Rerun to show the message instantly inside chronological history
                st.rerun()
                
            except Exception as e:
                error_msg = f"❌ Groq API Error: {str(e)}"
                response_container.markdown(
                    f'<div class="output-bubble-assistant" style="color: #dc2626; border-color: #fca5a5;">'
                    f'<strong>An error occurred:</strong><br>{error_msg}</div>',
                    unsafe_allow_html=True
                )
