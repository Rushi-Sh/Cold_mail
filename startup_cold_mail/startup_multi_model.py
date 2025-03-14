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

# Initialize LLM (Groq) with Multi-Model Support
def initialize_model(model_name="llama3-70b-8192", temperature=0.7):
    return ChatGroq(model_name=model_name, temperature=temperature)

# Memory for conversation
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# 1️⃣ Problem-Solution Agent
def problem_solution_agent(inputs, model):
    prompt = f"""
    Write a cold email to {inputs['investor_name']} introducing {inputs['startup_name']}.
    Explain how it solves {inputs['problem_solved']} and why this problem is critical.
    """
    return model.invoke(prompt)

# 2️⃣ Business Model Agent
def business_model_agent(inputs, model):
    prompt = f"""
    Enhance the email by detailing the business model for {inputs['startup_name']}:
    {inputs['business_model']}. Make it clear how revenue is generated.
    """
    return model.invoke(prompt)

# 3️⃣ Funding & Growth Agent
def funding_growth_agent(inputs, model):
    prompt = f"""
    Strengthen the email by including funding requirements and use cases:
    {inputs['funding_needs']}. Showcase how funds will be allocated.
    """
    return model.invoke(prompt)

# 4️⃣ Persuasion & Credibility Agent
def persuasion_agent(inputs, model):
    prompt = f"""
    Improve persuasion by emphasizing the startup's traction, uniqueness, or market potential.
    {inputs['email_content']}
    """
    return model.invoke(prompt)

# 5️⃣ Finalization Agent
def finalization_agent(inputs, model):
    prompt = f"""
    Finalize the email for clarity, conciseness, and professionalism:
    {inputs['email_content']}
    """
    return model.invoke(prompt)

# Define Multi-Agent Tools
def get_tools(model):
    return [
        Tool(name="Problem-Solution Agent", func=lambda x: problem_solution_agent(x, model), description="Explains problem and solution."),
        Tool(name="Business Model Agent", func=lambda x: business_model_agent(x, model), description="Details revenue strategy."),
        Tool(name="Funding & Growth Agent", func=lambda x: funding_growth_agent(x, model), description="Includes funding requirements."),
        Tool(name="Persuasion & Credibility Agent", func=lambda x: persuasion_agent(x, model), description="Enhances persuasion and credibility."),
        Tool(name="Finalization Agent", func=lambda x: finalization_agent(x, model), description="Refines grammar, clarity, and tone."),
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

# 📨 Function to Generate Investor Cold Email
def generate_startup_cold_email(user_data):
    model = initialize_model()
    
    initial_email = problem_solution_agent(user_data, model)
    enhanced_email = business_model_agent({"email_content": initial_email, **user_data}, model)
    funding_email = funding_growth_agent({"email_content": enhanced_email, **user_data}, model)
    persuasive_email = persuasion_agent({"email_content": funding_email, **user_data}, model)
    final_email = finalization_agent({"email_content": persuasive_email, **user_data}, model)

    return final_email