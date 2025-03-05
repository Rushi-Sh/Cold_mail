import streamlit as st
from multi_model import generate_cold_email
import json

# Streamlit UI Config
st.set_page_config(page_title="Cold Email Generator", layout="centered")

# Title & Description
st.title("📩 AI-Powered Cold Email Generator")
st.write("Generate highly optimized cold emails using a multi-agent AI system.")

# User Input Fields
role = st.text_input("🎯 Target Role", "CTO")
domain = st.text_input("🏢 Industry Domain", "SaaS")
name = st.text_input("👤 Recipient Name", "John Doe")
company = st.text_input("🏢 Company Name", "TechCorp")

# Generate Button
if st.button("🚀 Generate Cold Email"):
    with st.spinner("Generating cold email... ⏳"):
        email_result = generate_cold_email(role, domain, name, company)
        
        # Extract raw content (assuming AIMessage object)
        email_content = email_result.content if hasattr(email_result, "content") else str(email_result)

        # Extract response metadata if available
        response_metadata = getattr(email_result, "response_metadata", {})
        token_usage = response_metadata.get("token_usage", {})
        model_name = response_metadata.get("model_name", "Unknown")

        # Extract additional suggestions from email content
        suggestions = "No additional suggestions provided."
        if "Additional Suggestions:" in email_content:
            suggestions_index = email_content.find("Additional Suggestions:")
            suggestions = email_content[suggestions_index:]
            email_content = email_content[:suggestions_index]

        # Display Generated Email
        st.subheader("📨 Generated Cold Email:")
        email_template = f"""
        **Subject:** A Solution for {company} - Let's Connect 🚀  

        **Dear {name},**  

        {email_content}  

        Looking forward to your thoughts. Let’s connect!  

        **Best Regards,**  
        *[Your Name]*  
        *[Your Company]*  
        *[Your Contact Info]*  
        """
        st.markdown(email_template, unsafe_allow_html=True)

        # Display Additional Suggestions
        if suggestions:
            st.subheader("📝 Additional Suggestions:")
            st.markdown(suggestions, unsafe_allow_html=True)

        # Display Token Usage
        st.subheader("📊 Token Usage & Model Details:")
        st.json({
            "Model Used": model_name,
            "Completion Tokens": token_usage.get("completion_tokens", 0),
            "Prompt Tokens": token_usage.get("prompt_tokens", 0),
            "Total Tokens": token_usage.get("total_tokens", 0),
            "Completion Time (s)": token_usage.get("completion_time", 0),
        })

# Footer
st.markdown("---")
st.markdown("👨‍💻 Built By **Rushi Shah**")
