import streamlit as st
import logging
from menu.menu import menu
from job_cold_mail.job import job_inputs
from client_cold_mail.client import client_inputs
from startup_cold_mail.startup import startup_inputs
from job_cold_mail.job_multi_model import generate_job_cold_email
from client_cold_mail.client_multi_model import generate_client_cold_email
from startup_cold_mail.startup_multi_model import generate_startup_cold_email

# Configure Streamlit Page
st.set_page_config(page_title="Cold Email Generator", layout="centered")

# Load Menu Selection
selected_option = menu()

st.title("📝 AI-Powered Cold Email Generator")

# Dictionary to Store User Inputs
user_data = {}

# Select Input Form Based on User Choice
if selected_option == "Job Applications":
    user_data = job_inputs()
elif selected_option == "Client Outreach":
    user_data = client_inputs()
elif selected_option == "Startup Pitches":
    user_data = startup_inputs()

# Logging Setup
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler('cold_email_generator.log')
stream_handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

# Ensure Required Fields Are Filled
if user_data and "all_fields_filled" in user_data and user_data["all_fields_filled"]:
    if st.button("🚀 Generate Cold Email"):
        with st.spinner("Generating cold email... ⏳"):
            try:
                logger.info(f"Generating cold email for {user_data.get('name', 'User')} at {user_data.get('company', 'Unknown Company')}...")
                
                if selected_option == "Job Applications":
                    email_content = generate_job_cold_email(user_data)
                elif selected_option == "Client Outreach":
                    email_content = generate_client_cold_email(user_data)
                elif selected_option == "Startup Pitches":
                    email_content = generate_startup_cold_email(user_data)

                
                logger.info("Cold email generation successful.")
                st.text_area("📧 Generated Cold Email", email_content, height=250)

            except Exception as e:
                logger.error(f"Error generating cold email: {str(e)}")
                st.error("⚠️ An error occurred while generating the email. Please try again.")
else:
    st.button("🚀 Generate Cold Email", disabled=True)  # Disable button if required fields are missing

st.markdown("---")
st.markdown("👨‍💻 Built By **Rushi Shah**")
