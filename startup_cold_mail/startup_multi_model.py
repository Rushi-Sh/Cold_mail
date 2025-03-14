import os
from langchain_groq import ChatGroq
from langchain.memory import ConversationBufferMemory
from langchain.agents import AgentType, initialize_agent
from langchain.tools import Tool
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    raise ValueError("GROQ_API_KEY is missing. Please set it in your .env file.")

# Initialize LLM (Groq)
model = ChatGroq(model_name="llama3-70b-8192", temperature=0.7)

# Memory for conversation
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Agent Functions
def role_domain_agent(inputs):
    prompt = f"Write a cold email targeting a {inputs['role']} in the {inputs['domain']} industry. Focus on their pain points and how our solution can help."
    return model.invoke(prompt)  # ✅ Using .invoke() instead of .predict()

def personalized_agent(inputs):
    prompt = f"Make this email more personal for {inputs['name']} at {inputs['company']}:\n\n{inputs['email_content']}"
    return model.invoke(prompt)

def tone_persuasion_agent(inputs):
    prompt = f"Improve this email's persuasion and professional tone:\n\n{inputs['email_content']}"
    return model.invoke(prompt)

def critique_refinement_agent(inputs):
    prompt = f"Critique this cold email and refine it to increase response rates:\n\n{inputs['email_content']}"
    return model.invoke(prompt)

def finalization_agent(inputs):
    prompt = f"Fix any grammar, clarity, and style issues in this email:\n\n{inputs['email_content']}"
    return model.invoke(prompt)

# Define Multi-Agent Tools
tools = [
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

# Function to run Multi-Agent Cold Email Generation
def generate_startup_cold_email(role, domain, name, company):
    """Generates a cold email using a multi-agent system."""
    
    # Step 1: Generate initial email content
    initial_email = role_domain_agent({"role": role, "domain": domain})
    
    # Step 2: Personalize the email
    personalized_email = personalized_agent({"email_content": initial_email, "name": name, "company": company})
    
    # Step 3: Improve persuasion and tone
    refined_email = tone_persuasion_agent({"email_content": personalized_email})
    
    # Step 4: Critique and refine the email
    critiqued_email = critique_refinement_agent({"email_content": refined_email})
    
    # Step 5: Finalize with grammar and clarity fixes
    final_email = finalization_agent({"email_content": critiqued_email})

    return final_email  # ✅ Returns the final optimized email

# # Example Usage
# if __name__ == "__main__":
#     result = generate_cold_email("CTO", "SaaS", "John Doe", "TechCorp")
#     print("\n🔹 Final Cold Email:\n", result)
