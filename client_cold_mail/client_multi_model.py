import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.memory import ConversationBufferMemory
from langchain.agents import AgentType, initialize_agent
from langchain.tools import Tool

# Load API key from .env
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    raise ValueError("GROQ_API_KEY is missing. Please set it in your .env file.")

# Initialize LLM (Groq) ✅ Multi-Model Support
def initialize_model(model_name="llama3-70b-8192", temperature=0.7):
    return ChatGroq(model_name=model_name, temperature=temperature)

# Memory for conversation
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# 1️⃣ Role & Domain Agent
def role_domain_agent(inputs, model):
    prompt = f"Write a cold email targeting a {inputs['role']} in the {inputs['domain']} industry. Focus on their pain points and how our solution can help."
    return model.invoke(prompt)  

# 2️⃣ Personalization Agent
def personalized_agent(inputs, model):
    prompt = f"Make this email more personal for {inputs['client_name']} at {inputs['client_company']}:\n\n{inputs['email_content']}"
    return model.invoke(prompt)

# 3️⃣ Tone & Persuasion Agent
def tone_persuasion_agent(inputs, model):
    prompt = f"Improve this email's persuasion and professional tone:\n\n{inputs['email_content']}"
    return model.invoke(prompt)

# 4️⃣ Critique & Refinement Agent
def critique_refinement_agent(inputs, model):
    prompt = f"Critique this cold email and refine it to increase response rates:\n\n{inputs['email_content']}"
    return model.invoke(prompt)

# 5️⃣ Finalization Agent
def finalization_agent(inputs, model):
    prompt = f"Fix any grammar, clarity, and style issues in this email:\n\n{inputs['email_content']}"
    return model.invoke(prompt)

# Define Multi-Agent Tools
def get_tools(model):
    return [
        Tool(name="Role & Domain Agent", func=lambda x: role_domain_agent(x, model), description="Understands recipient's pain points."),
        Tool(name="Personalization Agent", func=lambda x: personalized_agent(x, model), description="Personalizes the email."),
        Tool(name="Tone & Persuasion Agent", func=lambda x: tone_persuasion_agent(x, model), description="Enhances persuasion and tone."),
        Tool(name="Critique & Refinement Agent", func=lambda x: critique_refinement_agent(x, model), description="Reviews and refines the email."),
        Tool(name="Finalization Agent", func=lambda x: finalization_agent(x, model), description="Fixes grammar, clarity, and ensures quality."),
    ]

# Initialize Multi-Agent System
def initialize_multi_agent(model):
    return initialize_agent(
        tools=get_tools(model),
        llm=model,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        memory=memory
    )

# 📨 Function to Generate Client Cold Email
def generate_client_cold_email(user_data):
    """Generates a cold email using a multi-agent system with all user inputs."""
    model = initialize_model()
    
    # Step 1: Generate initial email content
    initial_email = role_domain_agent({
        "role": user_data["client_role"],  
        "domain": user_data["client_domain"]
    }, model)

    # Step 2: Personalize the email with user & client details
    personalized_email = personalized_agent({
        "email_content": initial_email, 
        "client_name": user_data["client_name"],  
        "client_company": user_data["client_company"],
        "service_offered": user_data["service_offered"],
        "unique_value": user_data["unique_value"]
    }, model)

    # Step 3: Improve persuasion and tone
    refined_email = tone_persuasion_agent({
        "email_content": personalized_email
    }, model)

    # Step 4: Critique and refine the email for effectiveness
    critiqued_email = critique_refinement_agent({
        "email_content": refined_email
    }, model)

    # Step 5: Finalize with grammar and clarity fixes
    final_email = finalization_agent({
        "email_content": critiqued_email
    }, model)

    return final_email 