import streamlit as st
from resume_extractor.resume_extractor_agent import extract_details, extract_text_from_pdf

def job_inputs():
    
    st.subheader("🎯 Generate a Cold Email for Job Applications")
    your_name = st.text_input("👤 Your Name")
    your_contact = st.text_input("📞 Your Contact Number (Optional)")
    job_title = st.text_input("🎯 Job Title You're Applying For")
    
    # Dropdown for selecting the job domain
    job_domain = st.selectbox(
        "🏢 Job Domain / Industry",
        [
            "Software & IT", "Finance & Banking", "Healthcare", "Marketing & Sales",
            "Education", "Engineering", "Consulting", "Retail & E-commerce",
            "Government & Public Sector", "Other"
        ],
        index=0
    )
    
    company = st.text_input("🏢 Company Name")
    company_website = st.text_input("🌐 Company Website Link")
    hiring_manager = st.text_input("👤 Hiring Manager / Recruiter Name (If known)")
    job_location = st.text_input("🌍 Job Location")
    
    email_tone = st.selectbox(
        "🎭 Preferred Email Tone",
        ["Formal", "Friendly", "Persuasive", "Enthusiastic"],
        index=0
    )
    
    # Resume Upload
    resume_file = st.file_uploader("📄 Upload Your Resume (PDF)", type=["pdf"])
    extracted_resume_data = {}
    
    if resume_file:
        resume_text = extract_text_from_pdf(resume_file)
        extracted_resume_data = extract_details(resume_text)
    
    personal_message = st.text_area("📝 Personal Message / Unique Selling Point")
    
    # Validation Check - Ensure all required fields are filled
    all_fields_filled = all([
        your_name, job_title, job_domain, company, company_website, job_location, resume_file, personal_message
    ])
    
    if not all_fields_filled:
        st.warning("⚠️ Please fill out all required fields before generating the cold email.")
    
    user_data = {
        "your_name": your_name,
        "your_contact": your_contact,
        "job_title": job_title,
        "job_domain": job_domain,  # Added dropdown selection for job domain
        "company": company,
        "company_website": company_website,
        "hiring_manager": hiring_manager,
        "job_location": job_location,
        "email_tone": email_tone,
        "personal_message": personal_message,
        "all_fields_filled": all_fields_filled,
        "extracted_resume_data": extracted_resume_data 
    }
    
    # # Print all attributes after entering details
    # if all_fields_filled:
    #     st.write("### Entered Details:")
    #     for key, value in user_data.items():
    #         st.write(f"**{key}:** {value}")
    
    return user_data
