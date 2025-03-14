import fitz
import re
import spacy

def extract_text_from_pdf(uploaded_file):
    """Extracts text from a PDF file."""
    text = ""
    if uploaded_file is not None:
        pdf_reader = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        for page in pdf_reader:
            text += page.get_text("text") + "\n"
    return text

def extract_details(text):

    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    
    # Extract email
    email = re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', text)
    email = email[0] if email else "Not Found"
    
    # Extract phone number
    phone = re.findall(r'\+?\d{10,13}', text)
    phone = phone[0] if phone else "Not Found"
    
    # Extract named entities (for Name, Education, Experience, etc.)
    name = "Not Found"
    education = []
    experience = []
    skills = []
    
    for ent in doc.ents:
        if ent.label_ == "PERSON" and name == "Not Found":
            name = ent.text
        elif ent.label_ in ["ORG", "EDUCATION"]:
            education.append(ent.text)
        elif ent.label_ == "WORK_OF_ART":
            experience.append(ent.text)
    
    # Extract skills (basic keyword matching, can be improved with embeddings)
    skill_keywords = ["Python", "Java", "C++", "Machine Learning", "AI", "Deep Learning", "Data Science", "SQL", "Django", "Flask", "React", "Node.js"]
    for word in text.split():
        if word in skill_keywords and word not in skills:
            skills.append(word)
    
    return {
        "Name": name,
        "Email": email,
        "Phone": phone,
        "Education": education,
        "Experience": experience,
        "Skills": skills
    }