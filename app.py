import streamlit as st
from multi_model import generate_cold_email

# Streamlit UI
st.set_page_config(page_title="Cold Email Generator", layout="centered")

st.title("📩 AI-Powered Cold Email Generator")
st.write("Generate highly optimized cold emails using a multi-agent AI system.")

# Input Fields
role = st.text_input("Target Role (e.g., CTO, VP of Marketing)", "CTO")
domain = st.text_input("Industry Domain (e.g., SaaS, Healthcare)", "SaaS")
name = st.text_input("Recipient Name", "John Doe")
company = st.text_input("Company Name", "TechCorp")

# Generate Button
if st.button("Generate Cold Email"):
    with st.spinner("Generating cold email... ⏳"):
        email_result = generate_cold_email(role, domain, name, company)
        st.subheader("📨 Generated Cold Email:")
        st.write(email_result)

# Footer
st.markdown("---")
st.markdown("👨‍💻 Built with **LangChain & Groq Llama-3**")
