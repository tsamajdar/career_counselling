import streamlit as st
import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI

# Load local .env if running locally
load_dotenv()

# Page Configuration
st.set_page_config(
    page_title="Career Counseling & Psychometric Guidance",
    page_icon="🧭",
    layout="wide"
)

st.title("🧭 Interactive Career Counseling & Psychometric Assessment Assistant")
st.markdown("Discover personalized career paths, skill-building roadmaps, and psychometric insights powered by **Google Gemini**.")

# Initialize Session State for Multi-Step Form
if "step" not in st.session_state:
    st.session_state.step = 1
if "profile" not in st.session_state:
    st.session_state.profile = {}

# ============================================================================
# MULTI-STEP ASSESSMENT FORM
# ============================================================================

if st.session_state.step == 1:
    st.subheader("Step 1: Background & Education")
    with st.form("step1_form"):
        name = st.text_input("Full Name", value=st.session_state.profile.get("name", ""))
        education = st.selectbox("Highest Qualification", ["High School", "Bachelor's Degree", "Master's Degree", "Doctorate / Ph.D.", "Diploma / Certification"], index=1)
        experience_years = st.slider("Years of Professional Experience", 0, 30, value=st.session_state.profile.get("experience_years", 2))
        current_focus = st.text_input("Current Role, Field of Study, or Primary Interest", value=st.session_state.profile.get("current_focus", "Computer Science & AI"))
        
        next_btn = st.form_submit_button("Next: Skills & Interests ➡️")
        if next_btn:
            st.session_state.profile.update({
                "name": name if name else "Candidate",
                "education": education,
                "experience_years": experience_years,
                "current_focus": current_focus
            })
            st.session_state.step = 2
            st.rerun()

elif st.session_state.step == 2:
    st.subheader("Step 2: Core Skills & Passions")
    with st.form("step2_form"):
        technical_skills = st.text_area("Key Technical / Professional Skills (comma-separated)", value=st.session_state.profile.get("technical_skills", "Python, SQL, Problem Solving"))
        passions = st.text_area("What tasks or subjects energize you the most?", value=st.session_state.profile.get("passions", "Building software, teaching, analyzing data"))
        preferred_domain = st.selectbox("Preferred Industry Domain", ["Software & AI", "Education & Training", "Data Analytics", "Management & Consulting", "Research & Development"], index=0)
        
        col1, col2 = st.columns(2)
        with col1:
            back_btn = st.form_submit_button("⬅️ Back")
        with col2:
            next_btn = st.form_submit_button("Next: Work Style ➡️")
            
        if back_btn:
            st.session_state.step = 1
            st.rerun()
        elif next_btn:
            st.session_state.profile.update({
                "technical_skills": technical_skills,
                "passions": passions,
                "preferred_domain": preferred_domain
            })
            st.session_state.step = 3
            st.rerun()

elif st.session_state.step == 3:
    st.subheader("Step 3: Work Style & Behavioral Preferences")
    with st.form("step3_form"):
        work_environment = st.radio("Preferred Work Environment", ["Remote / WFH", "Hybrid", "On-site / Office", "Entrepreneurial / Independent"], index=1)
        leadership_style = st.selectbox("Team Role Preference", ["Individual Contributor / Deep Specialist", "Team Leader / Project Manager", "Mentor / Instructor / Consultant", "Founder / Builder"], index=2)
        risk_appetite = st.select_slider("Risk Tolerance for Career Moves", options=["Low (Stability & Growth)", "Moderate (Calculated Pivots)", "High (Startups & High Growth)"], value="Moderate (Calculated Pivots)")
        
        col1, col2 = st.columns(2)
        with col1:
            back_btn = st.form_submit_button("⬅️ Back")
        with col2:
            generate_btn = st.form_submit_button("🚀 Generate Comprehensive Career Guidance Report")
            
        if back_btn:
            st.session_state.step = 2
            st.rerun()
        elif generate_btn:
            st.session_state.profile.update({
                "work_environment": work_environment,
                "leadership_style": leadership_style,
                "risk_appetite": risk_appetite
            })
            st.session_state.step = 4
            st.rerun()

# ============================================================================
# STEP 4: AI ANALYSIS & REPORT GENERATION
# ============================================================================
elif st.session_state.step == 4:
    st.subheader("📊 Your Personalized Career & Psychometric Guidance Report")
    
    profile = st.session_state.profile
    
    with st.spinner("Analyzing profile and synthesizing career roadmap with Google Gemini..."):
        try:
            # Initialize Gemini Model via LangChain
            llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3)
            
            prompt = ChatPromptTemplate.from_messages([
                ("system", "You are an expert Career Counselor, Psychologist, and Professional Mentor. Provide an empathetic, highly structured, and actionable guidance report based on the candidate's profile."),
                ("human", """
Analyze the following candidate profile and generate a comprehensive career counseling report:

- Name: {name}
- Education: {education}
- Years of Experience: {experience_years} years
- Current Focus: {current_focus}
- Technical/Professional Skills: {technical_skills}
- Passions & Energizers: {passions}
- Preferred Industry Domain: {preferred_domain}
- Work Environment Preference: {work_environment}
- Leadership/Team Role: {leadership_style}
- Risk Tolerance: {risk_appetite}

Your report must include:
1. **Psychometric & Behavioral Profile Summary**: Strengths, working style archetype, and innate drivers.
2. **Top 3 Aligned Career Paths**: Specific roles matching their background and preferences.
3. **Skill Gap Analysis**: Areas to develop for target roles.
4. **Actionable 12-Month Roadmap**: Milestone-based career development steps.
5. **Encouraging Closing Guidance**: Motivational advice tailored to their background.
""")
            ])
            
            chain = prompt | llm | StrOutputParser()
            
            report = chain.invoke({
                "name": profile.get("name"),
                "education": profile.get("education"),
                "experience_years": profile.get("experience_years"),
                "current_focus": profile.get("current_focus"),
                "technical_skills": profile.get("technical_skills"),
                "passions": profile.get("passions"),
                "preferred_domain": profile.get("preferred_domain"),
                "work_environment": profile.get("work_environment"),
                "leadership_style": profile.get("leadership_style"),
                "risk_appetite": profile.get("risk_appetite")
            })
            
            st.success("Assessment completed successfully!")
            st.markdown("---")
            st.markdown(report)
            
            st.download_button(
                label="Download Guidance Report as Markdown",
                data=report,
                file_name=f"{profile.get('name', 'candidate')}_career_guidance_report.md",
                mime="text/markdown"
            )
            
            if st.button("🔄 Start New Assessment"):
                st.session_state.step = 1
                st.session_state.profile = {}
                st.rerun()
                
        except Exception as e:
                st.error(f"Error connecting to Gemini API: {e}. Please ensure your GOOGLE_API_KEY is correctly set.")
                if st.button("⬅️ Back to Form"):
                    st.session_state.step = 3
                    st.rerun()
