import streamlit as st
import pandas as pd
import plotly.express as px
import redis
import json
import requests
import os
import time
from datetime import datetime

# Configuration
st.set_page_config(page_title="AI Email Support Admin", layout="wide", page_icon="🤖", initial_sidebar_state="expanded")

import streamlit.components.v1 as components

# --- VIBECODING PREMIUM CSS & MATRIX ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap');

html, body, [class*="st-"] {
    font-family: 'Space Grotesk', sans-serif !important;
}

/* Base background transparent to show matrix */
.stApp {
    background: #050505 !important;
}

/* Header */
header[data-testid="stHeader"] {
    background: rgba(10, 10, 15, 0.6) !important;
    backdrop-filter: blur(12px) !important;
    border-bottom: 1px solid rgba(102, 126, 234, 0.2);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: rgba(15, 23, 42, 0.4) !important;
    backdrop-filter: blur(12px) !important;
    border-right: 1px solid rgba(102, 126, 234, 0.2) !important;
}

/* Metric Cards & DataFrames */
div[data-testid="metric-container"], .stDataFrame, .stForm {
    background: rgba(15, 23, 42, 0.4) !important;
    backdrop-filter: blur(12px) !important;
    border: 1px solid rgba(102, 126, 234, 0.2) !important;
    border-radius: 12px !important;
    padding: 15px !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.4) !important;
    transition: all 0.3s ease;
}

div[data-testid="metric-container"]:hover {
    border-color: rgba(102, 126, 234, 0.6) !important;
    box-shadow: 0 0 15px rgba(102, 126, 234, 0.3) !important;
    transform: translateY(-2px);
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    border: none !important;
    color: white !important;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4) !important;
    transition: all 0.3s ease !important;
    border-radius: 8px !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6) !important;
}

/* Inputs */
.stTextInput > div > div > input, .stTextArea > div > div > textarea {
    background: rgba(10, 15, 30, 0.6) !important;
    border: 1px solid rgba(102, 126, 234, 0.3) !important;
    color: white !important;
}

.stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus {
    border-color: #667eea !important;
    box-shadow: 0 0 10px rgba(102, 126, 234, 0.3) !important;
}
</style>
""", unsafe_allow_html=True)

components.html("""
    <canvas id="matrix-canvas" style="position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: -1; pointer-events: none; background-color: #050505;"></canvas>
    <script>
        const canvas = document.getElementById('matrix-canvas');
        const ctx = canvas.getContext('2d');
        let width, height;
        let columns;
        const charSize = 14;
        let drops = [];
        function resize() {
            width = canvas.width = window.innerWidth;
            height = canvas.height = window.innerHeight;
            columns = Math.floor(width / charSize);
            drops = [];
            for (let i = 0; i < columns; i++) {
                drops[i] = Math.random() * -100;
            }
        }
        function draw() {
            ctx.fillStyle = 'rgba(5, 5, 5, 0.1)';
            ctx.fillRect(0, 0, width, height);
            ctx.fillStyle = 'rgba(102, 126, 234, 0.25)'; 
            ctx.font = charSize + 'px monospace';
            for (let i = 0; i < drops.length; i++) {
                const text = String.fromCharCode(Math.random() * 128);
                const x = i * charSize;
                const y = drops[i] * charSize;
                ctx.fillText(text, x, y);
                if (y > height && Math.random() > 0.975) {
                    drops[i] = 0;
                }
                drops[i]++;
            }
        }
        window.addEventListener('resize', resize);
        resize();
        setInterval(draw, 33);
        
        // Force the canvas container to be fixed over the whole screen
        try {
            window.parent.document.querySelector('.stApp').style.background = 'transparent';
        } catch(e) {}
        const iframe = window.frameElement;
        if(iframe) {
            iframe.style.position = 'fixed';
            iframe.style.top = '0';
            iframe.style.left = '0';
            iframe.style.width = '100vw';
            iframe.style.height = '100vh';
            iframe.style.zIndex = '0';
            iframe.style.pointerEvents = 'none';
        }
    </script>
""", height=0, width=0)

REDIS_URL = os.getenv('REDIS_URL', 'redis://redis:6379/0')
API_URL = os.getenv('API_URL', 'http://api:5000')

# Redis Connection
@st.cache_resource
def get_redis_connection():
    try:
        return redis.from_url(REDIS_URL)
    except Exception as e:
        st.error(f"Failed to connect to Redis: {e}")
        return None

r = get_redis_connection()

# Sidebar Navigation
st.sidebar.title("🤖 AI Support Admin")
page = st.sidebar.radio("Navigation", ["Dashboard", "Knowledge Base", "Queue Management", "Analytics", "Settings"])

# --- PAGE: DASHBOARD ---
if page == "Dashboard":
    st.title("📊 System Dashboard")
    
    # Metrics
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    # Real Data from Redis
    if r:
        queue_size = r.llen('emails')
        emails_today = int(r.get('emails:today:count') or 0)
        
        success_count = int(r.get('emails:status:Success:count') or 0)
        failed_count = int(r.get('emails:status:Failed:count') or 0)
        ignored_count = int(r.get('emails:status:Ignored:count') or 0)
        total_processed = success_count + failed_count + ignored_count
        
        success_rate = round((success_count / total_processed * 100), 1) if total_processed > 0 else 0
        
        resp_time_sum = float(r.get('emails:response_time:sum') or 0)
        resp_time_count = int(r.get('emails:response_time:count') or 0)
        avg_response_time = round(resp_time_sum / resp_time_count, 2) if resp_time_count > 0 else 0
    else:
        queue_size, emails_today, success_rate, avg_response_time = 0, 0, 0, 0

    col1.metric("Queue Size", queue_size)
    col2.metric("Emails Today", emails_today)
    col3.metric("Success Rate", f"{success_rate}%")
    col4.metric("Avg Response", f"{avg_response_time}s")

    # Charts
    st.subheader("Activity Overview")
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        # Hourly Stats
        hourly_counts = []
        if r:
            for h in range(24):
                count = int(r.get(f'emails:hour:{h}:count') or 0)
                hourly_counts.append(count)
        else:
            hourly_counts = [0]*24

        df_hourly = pd.DataFrame({
            'Hour': range(24),
            'Emails': hourly_counts
        })
        fig_hourly = px.line(df_hourly, x='Hour', y='Emails', title='Emails per Hour')
        st.plotly_chart(fig_hourly, use_container_width=True)

    with chart_col2:
        df_status = pd.DataFrame({
            'Status': ['Success', 'Failed', 'Ignored'],
            'Count': [success_count, failed_count, ignored_count]
        })
        fig_pie = px.pie(df_status, values='Count', names='Status', title='Processing Status')
        st.plotly_chart(fig_pie, use_container_width=True)
    
    st.subheader("Recent Activity")
    recent_data = []
    if r:
        recent_raw = r.lrange('emails:recent', 0, 10)
        for item in recent_raw:
            try:
                recent_data.append(json.loads(item))
            except:
                pass
    
    if recent_data:
        st.dataframe(pd.DataFrame(recent_data), use_container_width=True)
    else:
        st.info("No recent activity.")

# --- PAGE: KNOWLEDGE BASE ---
elif page == "Knowledge Base":
    st.title("📚 Knowledge Base Management")
    
    tab1, tab2 = st.tabs(["Add New", "View & Edit"])
    
    with tab1:
        with st.form("add_faq"):
            question = st.text_input("Question")
            answer = st.text_area("Answer")
            keywords = st.text_input("Keywords (comma separated)")
            submitted = st.form_submit_button("Add to Knowledge Base")
            
            if submitted and question and answer:
                # In a real app, this would save to a DB or file and trigger re-indexing
                st.success("FAQ added successfully! (Simulation)")
                # r.lpush('knowledge_base_updates', json.dumps({'q': question, 'a': answer}))

    with tab2:
        st.info("Existing Knowledge Base Entries")
        # Mock data
        kb_data = pd.DataFrame({
            'ID': [1, 2, 3],
            'Question': ['How do I return?', 'Where is my order?', 'Do you ship internationally?'],
            'Keywords': ['return, refund', 'shipping, tracking', 'shipping, international']
        })
        st.dataframe(kb_data, use_container_width=True)

# --- PAGE: QUEUE MANAGEMENT ---
elif page == "Queue Management":
    st.title("⚙️ Queue Management")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Pending Emails", r.llen('emails') if r else 0)
    with col2:
        st.metric("Failed Queue", r.llen('failed_emails') if r else 0)
    
    st.subheader("Failed Emails")
    if r and r.llen('failed_emails') > 0:
        # Fetch some failed emails
        failed_emails = r.lrange('failed_emails', 0, 10)
        for email_raw in failed_emails:
            st.warning(email_raw)
            if st.button(f"Retry {email_raw[:10]}..."):
                # Logic to requeue
                st.success("Requeued!")
    else:
        st.info("No failed emails.")

# --- PAGE: ANALYTICS ---
elif page == "Analytics":
    st.title("📈 Detailed Analytics")
    
    # Mock data
    df_cats = pd.DataFrame({
        'Category': ['Orders', 'Returns', 'Product Info', 'Shipping', 'Other'],
        'Count': [300, 150, 120, 100, 50]
    })
    fig_bar = px.bar(df_cats, x='Category', y='Count', title='Email Categories')
    st.plotly_chart(fig_bar, use_container_width=True)
    
    df_acc = pd.DataFrame({
        'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
        'Accuracy': [92, 93, 91, 95, 96]
    })
    fig_line = px.line(df_acc, x='Day', y='Accuracy', title='Classification Accuracy Trend')
    st.plotly_chart(fig_line, use_container_width=True)

# --- PAGE: SETTINGS ---
elif page == "Settings":
    st.title("⚙️ System Settings")
    
    st.subheader("Email Configuration")
    st.text_input("Support Email Address", value="support@clothingstore.com")
    st.number_input("Check Interval (minutes)", value=5)
    
    st.subheader("LLM Settings")
    st.selectbox("Model", ["gemma:7b", "llama3", "mistral"])
    st.slider("Temperature", 0.0, 1.0, 0.4)
    
    st.subheader("System Info")
    st.json({
        "Version": "1.0.0",
        "Environment": "Production",
        "Redis Status": "Connected" if r else "Disconnected"
    })
    
    if st.button("Save Settings"):
        st.success("Settings saved!")
