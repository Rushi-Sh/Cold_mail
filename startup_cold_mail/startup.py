import streamlit as st

def startup_inputs():
    st.subheader("🚀 Generate a Cold Email for Startup Pitches")
    founder_name = st.text_input("👤 Your Name")
    startup_name = st.text_input("🏢 Startup Name")
    investor_name = st.text_input("💼 Investor / VC Name")
    problem_solved = st.text_area("🔥 Problem Your Startup Solves")
    business_model = st.text_area("📈 Business Model & Revenue Strategy")
    funding_needs = st.text_area("💰 Funding Requirements & Use Cases")


    all_fields_filled = all([
        founder_name, startup_name, investor_name, problem_solved, business_model, funding_needs
    ])

    if not all_fields_filled:
        st.warning("⚠️ Please fill out all required fields before generating the cold email.")

    return {
        "founder_name": founder_name,
        "startup_name": startup_name,
        "investor_name": investor_name,
        "problem_solved": problem_solved,
        "business_model": business_model,
        "funding_needs": funding_needs,
        "all_fields_filled": all_fields_filled  # Flag to indicate completion
    }
