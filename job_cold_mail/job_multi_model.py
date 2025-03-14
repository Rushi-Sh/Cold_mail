import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.memory import ConversationBufferMemory
from langchain.agents import AgentType, initialize_agent
from langchain.tools import Tool
from side_tools.ddg_search import website_content_search_agent

# Load API key from .env
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    raise ValueError("GROQ_API_KEY is missing. Please set it in your .env file.")

# Initialize LLM (Groq)
model = ChatGroq(model_name="llama3-70b-8192", temperature=0.7)

# Memory for conversation
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# 1️⃣ Website Content Search Agent
def website_search(inputs):
    return website_content_search_agent(inputs)

# 2️⃣ Role & Domain Agent
def role_domain_agent(inputs):
    prompt = f"Write a cold email targeting a {inputs['role']} in the {inputs['domain']} industry. Focus on their pain points and how our solution can help."
    return model.invoke(prompt).content

# 3️⃣ Personalization Agent
def personalized_agent(inputs):
    prompt = f"""
    Personalize this email for {inputs['hiring_manager']} (Hiring Manager) at {inputs['company']}.
    
    Job Location: {inputs.get('job_location', 'N/A')}
    Resume Highlights:
    {inputs.get('resume_content', 'No resume details provided')}

    Email Content:
    {inputs['email_content']}
    """
    return model.invoke(prompt).content.replace("*", "")  # Remove asterisks

# 4️⃣ Tone & Persuasion Agent
def tone_persuasion_agent(inputs):
    prompt = f"""
    Improve persuasion and professionalism in this email.
    Preferred Tone: {inputs.get('email_tone', 'Professional')}
    Key Resume Skills: {inputs.get('resume_highlights', 'Not specified')}

    Email Content:
    {inputs['email_content']}
    """
    return model.invoke(prompt).content.replace("*", "")

# 5️⃣ Critique & Refinement Agent
def critique_refinement_agent(inputs):
    prompt = f"""
    Critique and refine this cold email for better response rates.
    Unique Selling Point: {inputs.get('personal_message', 'Not provided')}
    Resume Summary: {inputs.get('resume_summary', 'No summary provided')}

    Email Content:
    {inputs['email_content']}
    """
    return model.invoke(prompt).content.replace("*", "")

# 6️⃣ Finalization Agent
def finalization_agent(inputs):
    prompt = f"""
    Finalize this email, fixing grammar, clarity, and structure.
    Ensure the contact details are included.

    Contact Details:
    Name: {inputs['your_name']}
    Phone: {inputs['your_contact']}

    Email Content:
    {inputs['email_content']}
    """
    return model.invoke(prompt).content.replace("*", "")

# Define Multi-Agent Tools
tools = [
    Tool(name="Website Content Search Agent", func=website_search, description="Fetches company details from the web."),
    Tool(name="Role & Domain Agent", func=role_domain_agent, description="Understands recipient's pain points."),
    Tool(name="Personalization Agent", func=personalized_agent, description="Personalizes the email."),
    Tool(name="Tone & Persuasion Agent", func=tone_persuasion_agent, description="Enhances persuasion and tone."),
    Tool(name="Critique & Refinement Agent", func=critique_refinement_agent, description="Reviews and refines the email."),
    Tool(name="Finalization Agent", func=finalization_agent, description="Fixes grammar, clarity, and ensures quality."),
]

# Initialize Multi-Agent System
multi_agent_system = initialize_agent(
    tools=tools,
    llm=model,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    memory=memory
)

# 📨 Function to Generate Cold Email
def generate_job_cold_email(user_data):
    """Generates a cold email using a multi-agent system with all user inputs, including resume content."""

    # Step 1: Fetch company details
    company_details = website_search({
        "company": user_data["company"], 
        "company_website": user_data["company_website"]
    })

    # Step 2: Generate initial email content based on role & domain
    initial_email = role_domain_agent({
        "role": user_data["job_title"],  
        "domain": user_data["job_domain"]
    })

    # Step 3: Personalize the email with user details, hiring manager, and extracted resume content
    personalized_email = personalized_agent({
        "email_content": initial_email, 
        "hiring_manager": user_data.get("hiring_manager", "Hiring Manager"),  # ✅ FIX: Include Hiring Manager Name
        "company": user_data["company"],
        "job_location": user_data.get("job_location", "N/A"),
        "resume_content": user_data.get("extracted_resume_data", "No resume details provided")
    })

    # Step 4: Improve persuasion and tone based on user preference
    refined_email = tone_persuasion_agent({
        "email_content": personalized_email, 
        "email_tone": user_data.get("email_tone", "Professional"),
        "resume_highlights": user_data.get("extracted_resume_data", {}).get("key_skills", "Not specified"),
    })

    # Step 5: Critique and refine the email for effectiveness
    critiqued_email = critique_refinement_agent({
        "email_content": refined_email, 
        "personal_message": user_data.get("personal_message", "No message provided"),
        "resume_summary": user_data.get("extracted_resume_data", {}).get("summary", "No summary provided"),
    })

    # Step 6: Finalize with grammar and clarity fixes and add sender's contact details
    final_email = finalization_agent({
        "email_content": critiqued_email,
        "your_name": user_data["your_name"],  # ✅ FIX: Ensure Your Name is in the Sender Section
        "your_contact": user_data["your_contact"],  # ✅ FIX: Ensure Contact Details are Included
    })

    return final_email  
