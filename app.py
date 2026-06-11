import streamlit as st

st.set_page_config(
    page_title="AdPulse AI",
    page_icon="📈",
    layout="wide"
)

st.title("AdPulse AI: Marketing Diagnostics & Analytics")

st.markdown("""
Welcome to **AdPulse AI**!

This platform enables your marketing teams to:
- Navigate performance metrics efficiently
- Determine the most responsive audience
- Forecast conversion volumes 
- Generate natural language insights from your data

Please select a dashboard from the **sidebar** to get started.
""")

# Setup sidebar
st.sidebar.success("Select a dashboard above.")
