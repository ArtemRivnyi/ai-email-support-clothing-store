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
st.set_page_config(page_title="AI Email Support Admin", layout="wide", page_icon="🤖")

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
    col1, col2, col3, col4 = st.columns(4)
    
    # Mock data for now (replace with real Redis/Prometheus queries later)
    queue_size = r.llen('emails') if r else 0
    emails_today = 142 # Placeholder
    success_rate = 94.5 # Placeholder
    avg_response_time = "2.3s" # Placeholder

    col1.metric("Queue Size", queue_size, "-2")
    col2.metric("Emails Today", emails_today, "+12")
    col3.metric("Success Rate", f"{success_rate}%", "+1.2%")
    col4.metric("Avg Response", avg_response_time, "-0.1s")

    # Charts
    st.subheader("Activity Overview")
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        # Mock data for chart
        df_hourly = pd.DataFrame({
            'Hour': range(24),
            'Emails': [5, 2, 1, 0, 0, 1, 8, 15, 25, 40, 35, 30, 28, 32, 38, 45, 40, 25, 15, 10, 8, 5, 3, 2]
        })
        fig_hourly = px.line(df_hourly, x='Hour', y='Emails', title='Emails per Hour')
        st.plotly_chart(fig_hourly, use_container_width=True)

    with chart_col2:
        df_status = pd.DataFrame({
            'Status': ['Success', 'Failed', 'Manual Review'],
            'Count': [850, 30, 20]
        })
        fig_pie = px.pie(df_status, values='Count', names='Status', title='Processing Status')
        st.plotly_chart(fig_pie, use_container_width=True)
    
    st.subheader("Recent Activity")
    st.dataframe(pd.DataFrame({
        'Time': ['10:01', '10:02', '10:05'],
        'Sender': ['alice@example.com', 'bob@example.com', 'charlie@example.com'],
        'Subject': ['Order status', 'Return policy', 'Wrong size'],
        'Status': ['Replied', 'Replied', 'Queued']
    }), use_container_width=True)

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
