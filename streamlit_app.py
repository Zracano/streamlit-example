import streamlit as st
import psycopg2
from psycopg2 import sql

# Set up a connection to the PostgreSQL database
DATABASE_URL = "postgres://enqlthhf:l6_JolzJ2pQhvgGWITGB2rtWjTKLE2Zr@bubble.db.elephantsql.com/enqlthhf"
conn = psycopg2.connect(DATABASE_URL)
c = conn.cursor()

# Create tables if they don't exist
c.execute('''
    CREATE TABLE IF NOT EXISTS survey_data (
        email TEXT,
        looking_for_job TEXT,
        industry TEXT,
        job_role TEXT,
        cognitive_answers TEXT,
        emotional_answers TEXT,
        social_answers TEXT,
        behavioral_answers TEXT
    )
''')
conn.commit()
conn.close()

def matrix_question(title, rows):
    st.subheader(title)
    options = ["Strongly Disagree", "Disagree", "Somewhat Disagree", "Neither Disagree Nor Agree", "Somewhat Agree",
               "Agree", "Strongly Agree"]
    answers = {}
    for row in rows:
        answer = st.radio(row, options)
        answers[row] = answer
    return answers

# Navigation setup
if 'page' not in st.session_state:
    st.session_state.page = 0

# Initialize session state attributes
if 'email' not in st.session_state:
    st.session_state.email = ""
if 'looking_for_job' not in st.session_state:
    st.session_state.looking_for_job = "No"
if 'industry' not in st.session_state:
    st.session_state.industry = []
if 'job_role' not in st.session_state:
    st.session_state.job_role = "CEO (Chief Executive Officer)"
if 'cognitive_answers' not in st.session_state:
    st.session_state.cognitive_answers = {}
if 'emotional_answers' not in st.session_state:
    st.session_state.emotional_answers = {}
if 'social_answers' not in st.session_state:
    st.session_state.social_answers = {}
if 'behavioral_answers' not in st.session_state:
    st.session_state.behavioral_answers = {}

pages = [
    "General Information",
    "Cognitive Experience",
    "Emotional Experience",
    "Social Experience",
    "Behavioral Experience",
]

st.title(pages[st.session_state.page])

# General Information
if st.session_state.page == 0:
    st.session_state.email = st.text_input("Email Address", st.session_state.email)
    st.session_state.looking_for_job = st.radio(
        "Are you looking for a new job or a different role in your company?",
        ["Yes", "No"], index=(0 if st.session_state.looking_for_job == "Yes" else 1)
    )
    st.session_state.industry = st.multiselect(
        "Industry",
        [
            "Agriculture",
            "Fishing and Aquaculture",
            "Forestry",
            "Mining",
            "Oil and Gas Extraction",
            "Construction",
            "Manufacturing",
            "Energy Production",
            "Retail",
            "Wholesale",
            "Transportation and Logistics",
            "Tourism and Hospitality",
            "Health Care",
            "Education",
            "Information Technology",
            "Telecommunications",
            "Financial Services",
            "Real Estate",
            "Professional Services",
            "Media and Entertainment",
            "Public Administration and Defense"
        ], default=st.session_state.industry
    )
    st.session_state.job_role = st.selectbox(
        "Job Role",
        [
            "CEO (Chief Executive Officer)",
            "CTO (Chief Technology Officer)",
            "CIO (Chief Information Officer)",
            "CFO (Chief Financial Officer)",
            "COO (Chief Operating Officer)",
            "CMO (Chief Marketing Officer)",
            "Data Scientist",
            "Machine Learning Engineer",
            "Software Developer",
            "DevOps Engineer",
            "Research Scientist",
            "Product Manager",
            "Project Manager",
            "Business Analyst",
            "Data Analyst",
            "QA Engineer (Quality Assurance)",
            "UX/UI Designer",
            "Technical Writer",
            "Information Security Analyst",
            "Sales Engineer",
            "Customer Success Manager",
            "Human Resources Manager",
            "Legal Advisor",
            "Compliance Officer"
        ],
        index=[
            "CEO (Chief Executive Officer)",
            "CTO (Chief Technology Officer)",
            "CIO (Chief Information Officer)",
            "CFO (Chief Financial Officer)",
            "COO (Chief Operating Officer)",
            "CMO (Chief Marketing Officer)",
            "Data Scientist",
            "Machine Learning Engineer",
            "Software Developer",
            "DevOps Engineer",
            "Research Scientist",
            "Product Manager",
            "Project Manager",
            "Business Analyst",
            "Data Analyst",
            "QA Engineer (Quality Assurance)",
            "UX/UI Designer",
            "Technical Writer",
            "Information Security Analyst",
            "Sales Engineer",
            "Customer Success Manager",
            "Human Resources Manager",
            "Legal Advisor",
            "Compliance Officer"
        ].index(st.session_state.job_role)
    )

# Cognitive Experience
elif st.session_state.page == 1:
    st.session_state.cognitive_answers = matrix_question(
        "Cognitive Experience",
        ["Improve my skills", "Gain new knowledge/expertise", "Test my talent/capabilities",
         "Keep up with new ideas and innovations", "Come up with new ideas"]
    )

# Emotional Experience
elif st.session_state.page == 2:
    st.session_state.emotional_answers = matrix_question(
        "Emotional Experience",
        ["Have a pleasurable work experience", "Have fun at work", "Enjoy what I am doing",
         "Feel more satisfied with my work"]
    )

# Social Experience
elif st.session_state.page == 3:
    st.session_state.social_answers = matrix_question(
        "Social Experience",
        ["Have better interactions with my colleagues", "Expand my personal/social network",
         "Strengthen my affiliation with my organization", "Feel I belong to my organization",
         "Meet others with whom I share similar interests at work", "Make a good impression on my colleagues"]
    )

# Behavioral Experience
elif st.session_state.page == 4:
    st.session_state.behavioral_answers = matrix_question(
        "Behavioral Experience",
        ["Make a better contribution", "Improve the impact of my work", "Control the quality of my work",
         "Have a positive impact on other’s work"]
    )

# Navigation buttons
if st.session_state.page > 0:
    if st.button('Back'):
        st.session_state.page -= 1

if st.session_state.page < len(pages) - 1:
    if st.button('Next'):
        st.session_state.page += 1

# Submit button on the last page
if st.session_state.page == len(pages)-1:
    if st.button('Submit'):
        conn = psycopg2.connect(DATABASE_URL)
        c = conn.cursor()
        # Insert data into the database using parameterized queries to prevent SQL injection
        query = sql.SQL('''
            INSERT INTO survey_data (
                email,
                looking_for_job,
                industry,
                job_role,
                cognitive_answers,
                emotional_answers,
                social_answers,
                behavioral_answers
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ''')
        data = (
            st.session_state.email,
            st.session_state.looking_for_job,
            str(st.session_state.industry),
            st.session_state.job_role,
            str(st.session_state.cognitive_answers),
            str(st.session_state.emotional_answers),
            str(st.session_state.social_answers),
            str(st.session_state.behavioral_answers)
        )

        c.execute(query, data)
        conn.commit()
        conn.close()

        st.write("Survey Submitted. Thank you!")
        st.session_state.page = 0
