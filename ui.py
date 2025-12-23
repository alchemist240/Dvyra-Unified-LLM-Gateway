import streamlit as st
import yaml
import os
from openai import OpenAI
import time
import datetime

# ==========================================
# 1. CONFIGURATION & SETUP
# ==========================================
st.set_page_config(
    page_title="DVYRA | Gateway Command",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

def load_config():
    try:
        with open("config.yaml", "r") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        st.error("🚨 config.yaml not found!")
        return None

config_data = load_config()
available_models = [m['model_name'] for m in config_data['model_list']] if config_data else ["gemini-flash"]

# ==========================================
# 2. FUTURISTIC GLASS-MORPHISM CSS (FIXED FONTS)
# ==========================================
st.markdown("""
<style>
    /* 1. IMPORT POPPINS FONT */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

    /* MAIN BACKGROUND */
    .stApp {
        background-color: #050505;
        background-image: 
            radial-gradient(at 0% 0%, hsla(253,16%,7%,1) 0, transparent 50%), 
            radial-gradient(at 50% 0%, hsla(225,39%,30%,1) 0, transparent 50%), 
            radial-gradient(at 100% 0%, hsla(339,49%,30%,1) 0, transparent 50%);
        color: #e0e0e0;
        font-family: 'Poppins', sans-serif !important; 
    }
    
    /* Font overrides for specific elements */
    h1, h2, h3, h4, h5, h6, p, input, textarea {
        font-family: 'Poppins', sans-serif !important;
    }
    .stButton button {
        font-family: 'Poppins', sans-serif !important;
    }
    
    /* SCANLINE EFFECT */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        background: repeating-linear-gradient(
            0deg, transparent 0, transparent 2px, rgba(0, 255, 204, 0.02) 3px, rgba(0, 255, 204, 0.02) 4px
        );
        pointer-events: none;
        z-index: 0;
    }

    /* GLASS CONTAINERS */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
    }

    /* GLITCH TITLE */
    @keyframes glitch {
        0% { text-shadow: 2px 2px 0px #ff00ff, -2px -2px 0px #00ffcc; }
        2% { text-shadow: -2px 2px 0px #ff00ff, 2px -2px 0px #00ffcc; }
        100% { text-shadow: 2px 2px 0px #ff00ff, -2px -2px 0px #00ffcc; }
    }
    .glitch-text {
        animation: glitch 3s infinite alternate-reverse;
        font-weight: bold;
        letter-spacing: 2px; 
    }

    /* INPUT FIELD */
    .stTextInput > div > div > input {
        background-color: rgba(0, 0, 0, 0.3) !important;
        color: #00ffcc !important;
        border: 1px solid #333 !important;
        border-radius: 8px;
        font-family: 'Poppins', sans-serif !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #00ffcc !important;
        box-shadow: 0 0 15px rgba(0, 255, 204, 0.3);
    }
    
    /* CHAT BUBBLES */
    .user-msg {
        background: rgba(0, 255, 204, 0.05);
        border-right: 3px solid #00ffcc;
        padding: 15px;
        border-radius: 10px 0 0 10px;
        margin-bottom: 15px;
        text-align: right;
        margin-left: 20%;
        color: #e0e0e0;
        font-family: 'Poppins', sans-serif !important;
    }
    .bot-msg {
        background: rgba(255, 0, 255, 0.05);
        border-left: 3px solid #ff00ff;
        padding: 15px;
        border-radius: 0 10px 10px 0;
        margin-bottom: 15px;
        text-align: left;
        margin-right: 20%;
        color: #e0e0e0;
        font-family: 'Poppins', sans-serif !important;
    }
    
    /* FOOTER */
    .msg-footer {
        font-size: 0.7em;
        color: #666;
        margin-top: 10px;
        border-top: 1px solid rgba(255,255,255,0.1);
        padding-top: 5px;
        display: flex;
        justify-content: space-between;
        font-family: 'Poppins', sans-serif !important; 
    }

    /* TERMINAL LOGS */
    .terminal-box {
        background-color: #0c0c0c;
        border: 1px solid #333;
        font-family: 'Poppins', sans-serif !important;
        color: #00ff00;
        padding: 10px;
        font-size: 11px;
        height: 200px;
        overflow-y: auto;
        border-radius: 5px;
        box-shadow: inset 0 0 10px #000;
        line-height: 1.4;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .block-container { padding-top: 2rem; padding-bottom: 5rem; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. SESSION STATE
# ==========================================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "terminal_logs" not in st.session_state:
    st.session_state.terminal_logs = ["System Initialized...", "Waiting for inputs..."]

if "last_latency" not in st.session_state:
    st.session_state.last_latency = "--" 

# ==========================================
# 4. SIDEBAR
# ==========================================
with st.sidebar:
    st.markdown("## ⚙️ GATEWAY CONTROL")
    
    with st.expander("🔐 ENCRYPTED CONFIG", expanded=False):
        base_url = st.text_input("Gateway URL", value="https://dominator2414-unified-dvyra.hf.space")
        api_key = st.text_input("Master Key", type="password") 
    
    selected_model = st.selectbox("Active Route", available_models, index=0)
    
    st.markdown("---")
    st.markdown("### 📊 Status Monitor")
    
    c1, c2 = st.columns(2)
    with c1:
        st.metric("Latency", st.session_state.last_latency)
    with c2:
        st.metric("Uptime", "99.9%", delta="Stable")
    
    st.markdown("---")
    st.markdown("### 📟 SYSTEM LOGS")
    
    log_placeholder = st.empty()

    def update_logs(new_entry=None):
        if new_entry:
            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            st.session_state.terminal_logs.append(f"[{timestamp}] {new_entry}")
            if len(st.session_state.terminal_logs) > 20:
                st.session_state.terminal_logs.pop(0)
        
        log_content = "<br>".join([f"> {line}" for line in st.session_state.terminal_logs])
        log_placeholder.markdown(f'<div class="terminal-box">{log_content}</div>', unsafe_allow_html=True)

    update_logs()

    if st.button("🗑️ Clear Context"):
        st.session_state.messages = []
        st.session_state.terminal_logs = ["Logs cleared."]
        st.session_state.last_latency = "--"
        st.rerun()

# ==========================================
# 5. MAIN INTERFACE
# ==========================================

st.markdown("""
    <h1 style='text-align: center; color: white; margin-bottom: 30px;'>
        DVYRA <span style='font-size: 0.5em; color: #888;'>// UNIVERSAL LLM GATEWAY</span>
    </h1>
""", unsafe_allow_html=True)

history_container = st.container()

# === RENDER HISTORY LOOP ===
with history_container:
    for msg in st.session_state.messages:
        if "html_content" in msg:
             st.markdown(msg["html_content"], unsafe_allow_html=True)
        elif msg["role"] == "user":
            st.markdown(f'<div class="user-msg"><b>Kshitij:</b><br>{msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bot-msg"><b>DVYRA_NET:</b><br>{msg["content"]}</div>', unsafe_allow_html=True)

# ==========================================
# 6. INPUT & LOGIC
# ==========================================
prompt = st.chat_input("Enter command or prompt...")

if prompt:
    # A. Display User Msg
    with history_container:
        st.markdown(f'<div class="user-msg"><b>Kshitij:</b><br>{prompt}</div>', unsafe_allow_html=True)

    st.session_state.messages.append({"role": "user", "content": prompt})
    update_logs(f"INPUT RECEIVED: {len(prompt)} chars")

    if not api_key:
        st.error("🔒 ACCESS DENIED: Please enter your Master Key in the sidebar.")
        update_logs("ERROR: MISSING AUTH KEY")
    else:
        try:
            client = OpenAI(api_key=api_key, base_url=base_url)
            
            update_logs(f"ROUTING TO: {selected_model}...")
            st.toast(f"Establishing uplink to {selected_model}...", icon="🔄")
            time.sleep(0.2) 
            
            with history_container:
                with st.spinner(f"⚡ Uplink active..."):
                    start_time = time.time()
                    
                    api_messages = [
                        {"role": m["role"], "content": m["content"]} 
                        for m in st.session_state.messages
                    ]
                    
                    response = client.chat.completions.create(
                        model=selected_model,
                        messages=api_messages
                    )
                    end_time = time.time()
            
            bot_raw_text = response.choices[0].message.content
            actual_model = response.model
            
            # --- FIXED LOGIC START ---
            # 1. Get the 'Technical ID' expected for the selected dropdown name
            # We look through config_data to find the matching entry
            target_tech_id = selected_model # Default to selection
            if config_data:
                for item in config_data['model_list']:
                    if item['model_name'] == selected_model:
                        target_tech_id = item['litellm_params']['model']
                        break
            
            # 2. Smart Comparison (Does Actual contain Target? Or Target contain Actual?)
            # This handles cases where 'gemini/gemini-flash' matches 'gemini-flash'
            is_fallback = True
            
            # Check A: Exact Match
            if actual_model == selected_model:
                is_fallback = False
            # Check B: Tech ID contains Actual (e.g. config has 'gemini/flash', response has 'flash')
            elif actual_model in target_tech_id:
                is_fallback = False
            # Check C: Actual contains Tech ID
            elif target_tech_id in actual_model:
                 is_fallback = False

            if is_fallback:
                update_logs(f"⚠️ PRIMARY ROUTE FAILED")
                update_logs(f"✅ FALLBACK SUCCESS: {actual_model}")
                st.toast(f"⚠️ Primary Route Failed! Switched to {actual_model}", icon="🚨")
            else:
                update_logs(f"✅ CONNECTION STABLE: {actual_model}")
                st.toast("Data packet received successfully.", icon="✅")
            # --- FIXED LOGIC END ---

            # Token Usage
            usage = response.usage
            t_in = usage.prompt_tokens if usage else 0
            t_out = usage.completion_tokens if usage else 0
            t_total = usage.total_tokens if usage else 0
            
            bot_html_display = f"""
            <div class="bot-msg">
                <b>DVYRA_NET [{actual_model}]:</b><br>{bot_raw_text}
                <div class="msg-footer">
                    <span>⚡ IN: {t_in} | OUT: {t_out}</span>
                    <span>TOT: {t_total}</span>
                </div>
            </div>
            """

            latency_val = round((end_time - start_time) * 1000)
            st.session_state.last_latency = f"{latency_val}ms"
            update_logs(f"DATA PACKET RECEIVED. LATENCY: {latency_val}ms")
            
            st.session_state.messages.append({
                "role": "assistant",
                "content": bot_raw_text,
                "html_content": bot_html_display
            })
            
            st.rerun()

        except Exception as e:
            error_msg = str(e)
            st.error(f"❌ CONNECTION FAILURE: {error_msg}")
            
            if "429" in error_msg:
                update_logs("ERR 429: RESOURCE EXHAUSTED")
            elif "401" in error_msg:
                update_logs("ERR 401: AUTH FAILED")
            else:
                update_logs("FATAL CONNECTION ERROR")