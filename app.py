import os
import json
import streamlit as st
from typing import Optional

# Reuse existing logic from the backend script
from course_curriculum import (
    get_course_data,
    scrape_prerequisites,
    extract_prereqs,
)

st.set_page_config(page_title="Curriculum Compass", page_icon="🎓", layout="wide")

st.title("Curriculum Compass")
st.caption("MIT OCW prerequisite extractor with AI-powered parsing")

# Get API key from Streamlit secrets
try:
    groq_api_key = st.secrets["api_keys"]["groq"]
    os.environ["GROQ_API_KEY"] = groq_api_key
except:
    st.error(
        "⚠️ Groq API key not found in Streamlit secrets!\n\n"
        "**For Local Development:**\n"
        "1. Create a `.streamlit/secrets.toml` file\n"
        "2. Add: `[api_keys]\ngroq = 'your_api_key_here'`\n\n"
        "**For Streamlit Cloud:**\n"
        "Add the secret in your app's settings"
    )
    st.stop()

# Sidebar controls
st.sidebar.header("Course Selection")
courses = get_course_data()
course_titles = [course["title"] for course in courses]

mode = st.sidebar.radio(
    "Choose input mode",
    ("Pick from list", "Enter OCW syllabus URL"),
    index=0,
)

selected_course = None
input_url: Optional[str] = None

if mode == "Pick from list":
    choice = st.sidebar.selectbox("Course", course_titles, index=0)
    selected_course = next(c for c in courses if c["title"] == choice)
    st.sidebar.write(f"Selected: {selected_course['title']}")
else:
    input_url = st.sidebar.text_input(
        "Paste a MIT OCW syllabus URL",
        placeholder="https://ocw.mit.edu/courses/.../pages/syllabus/",
    )

col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("Extraction")
    run = st.button("Extract Prerequisites", type="primary")

    if run:
        try:
            if mode == "Pick from list":
                url = selected_course["url"]
                course_name = selected_course["title"]
            else:
                if not input_url:
                    st.error("Please enter a valid OCW syllabus URL.")
                    st.stop()
                url = input_url.strip()
                course_name = "Custom Course"

            with st.spinner("Fetching syllabus page..."):
                prereq_text = scrape_prerequisites(url)

            if not prereq_text:
                st.info("No prerequisite text found on the page.")
                st.stop()

            st.success("Page fetched successfully.")

            with st.spinner("Parsing prerequisites with AI (Groq LLaMA 3.1)..."):
                parsed = extract_prereqs(course_name, prereq_text)

            st.subheader("Result")
            st.json(parsed, expanded=True)

            # Download button
            st.download_button(
                label="Download JSON",
                data=json.dumps(parsed, indent=2),
                file_name="prerequisites.json",
                mime="application/json",
            )
        except Exception as e:
            st.error(f"Error: {e}")

with col_right:
    st.subheader("Options")
    show_raw = st.checkbox("Show raw prerequisite text")

    if show_raw and (mode == "Pick from list" or (mode == "Enter OCW syllabus URL" and input_url)):
        try:
            url_preview = selected_course["url"] if mode == "Pick from list" else input_url
            raw_text_preview = scrape_prerequisites(url_preview)
            st.text_area("Raw Text", raw_text_preview or "", height=300)
        except Exception:
            st.info("Raw text preview unavailable.")

st.divider()
st.caption("Note: Parsing quality depends on the syllabus page structure and available prerequisite sections.")
