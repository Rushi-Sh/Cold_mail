import streamlit as st

def menu():
    st.sidebar.markdown(
        "<h2 style='text-align: center; color: #ffffff; background-color: #0073e6; padding: 10px; border-radius: 10px; margin-bottom : 40px'>📩 Cold Email Generator</h2>",
        unsafe_allow_html=True
    )
    
    menu_options = {
        "📄 Job Applications": "Job Applications",
        "🤝 Client Outreach": "Client Outreach",
        "🚀 Startup Pitches": "Startup Pitches"
    }

    choice = st.sidebar.selectbox(
        "Select an option",
        list(menu_options.keys()),
        index=0,
        format_func=lambda x: menu_options[x]
    )

    return menu_options[choice]
