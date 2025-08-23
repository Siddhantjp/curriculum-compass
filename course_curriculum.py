#!/usr/bin/env python3
"""
MIT OCW Prerequisite Scraper

This script scrapes MIT OpenCourseWare course pages to extract prerequisites
and maps them to human-readable course names using a provided course code mapping file.
"""

import requests
from bs4 import BeautifulSoup
import re
import json
import os
import pandas as pd
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Load course mappings
mapping_df = pd.read_csv("COURSE CODES.csv")
id_to_name = dict(zip(mapping_df["Course ID"].astype(str).str.strip(),
                      mapping_df["Course Name"].astype(str).str.strip()))

def map_course_code_to_name(code_or_name: str) -> str:
    """Map course codes to full course names using the CSV mapping."""
    if not isinstance(code_or_name, str):
        return code_or_name
    cleaned = code_or_name.strip()
    return id_to_name.get(cleaned, cleaned)

def get_course_data():
    """Define available courses for scraping."""
    courses = [
        {"id": 1, "title": "18.01SC Single Variable Calculus", "url": "https://ocw.mit.edu/courses/18-01sc-single-variable-calculus-fall-2010/pages/syllabus/"},
        {"id": 2, "title": "18.02SC Multivariable Calculus", "url": "https://ocw.mit.edu/courses/18-02sc-multivariable-calculus-fall-2010/pages/syllabus/"},
        {"id": 3, "title": "18.024 Multivariable Calculus with Theory", "url": "https://ocw.mit.edu/courses/18-024-multivariable-calculus-with-theory-spring-2011/pages/syllabus/"},
        {"id": 4, "title": "18.04 Complex Variables with Applications", "url": "https://ocw.mit.edu/courses/18-04-complex-variables-with-applications-fall-1999/pages/syllabus/"},
        {"id": 5, "title": "18.06SC Linear Algebra", "url": "https://ocw.mit.edu/courses/18-06sc-linear-algebra-fall-2011/pages/syllabus/"},
        {"id": 6, "title": "18.700 Linear Algebra", "url": "https://ocw.mit.edu/courses/18-700-linear-algebra-fall-2013/pages/syllabus/"},
        {"id": 7, "title": "18.03SC Differential Equations", "url": "https://ocw.mit.edu/courses/18-03sc-differential-equations-fall-2011/pages/syllabus/"},
        {"id": 8, "title": "18.05 Introduction to Probability and Statistics", "url": "https://ocw.mit.edu/courses/18-05-introduction-to-probability-and-statistics-spring-2022/pages/syllabus/"},
        {"id": 9, "title": "1.151 Probability and Statistics in Engineering", "url": "https://ocw.mit.edu/courses/1-151-probability-and-statistics-in-engineering-spring-2005/pages/syllabus/"},
        {"id": 10, "title": "8.04 Quantum Physics I", "url": "https://ocw.mit.edu/courses/8-04-quantum-physics-i-spring-2016/pages/syllabus/"},
        {"id": 11, "title": "8.02 Physics II: Electricity and Magnetism", "url": "https://ocw.mit.edu/courses/8-02-physics-ii-electricity-and-magnetism-spring-2007/pages/syllabus/"},
        {"id": 12, "title": "5.60 Thermodynamics & Kinetics", "url": "https://ocw.mit.edu/courses/5-60-thermodynamics-kinetics-spring-2008/pages/syllabus/"},
        {"id": 13, "title": "6.0001 Introduction to CS and Programming in Python", "url": "https://ocw.mit.edu/courses/6-0001-introduction-to-computer-science-and-programming-in-python-fall-2016/pages/syllabus/"},
        {"id": 14, "title": "6.0002 Intro to Computational Thinking and Data Science", "url": "https://ocw.mit.edu/courses/6-0002-introduction-to-computational-thinking-and-data-science-fall-2016/pages/syllabus/"},
        {"id": 15, "title": "6.S096 Introduction to C and C++", "url": "https://ocw.mit.edu/courses/6-s096-introduction-to-c-and-c-january-iap-2013/pages/syllabus/"},
        {"id": 16, "title": "6.006 Introduction to Algorithms", "url": "https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/pages/syllabus/"},
        {"id": 17, "title": "6.851 Advanced Data Structures", "url": "https://ocw.mit.edu/courses/6-851-advanced-data-structures-spring-2012/pages/syllabus/"},
        {"id": 18, "title": "6.042J Mathematics for Computer Science", "url": "https://ocw.mit.edu/courses/6-042j-mathematics-for-computer-science-fall-2005/pages/syllabus/"},
        {"id": 19, "title": "6.033 Computer System Engineering", "url": "https://ocw.mit.edu/courses/6-033-computer-system-engineering-spring-2018/pages/syllabus/"},
        {"id": 20, "title": "6.1810 Operating System Engineering", "url": "https://ocw.mit.edu/courses/6-1810-operating-system-engineering-fall-2023/pages/syllabus/"},
        {"id": 21, "title": "1.124J Foundations of Software Engineering", "url": "https://ocw.mit.edu/courses/1-124j-foundations-of-software-engineering-fall-2000/pages/syllabus/"},
        {"id": 22, "title": "6.035 Computer Language Engineering", "url": "https://ocw.mit.edu/courses/6-035-computer-language-engineering-spring-2010/pages/syllabus/"},
        {"id": 23, "title": "6.01SC Intro to EECS I", "url": "https://ocw.mit.edu/courses/6-01sc-introduction-to-electrical-engineering-and-computer-science-i-spring-2011/pages/syllabus/"},
        {"id": 24, "title": "6.011 Signals, Systems and Inference", "url": "https://ocw.mit.edu/courses/6-011-signals-systems-and-inference-spring-2018/pages/syllabus/"},
        {"id": 25, "title": "6.012 Microelectronic Devices and Circuits", "url": "https://ocw.mit.edu/courses/6-012-microelectronic-devices-and-circuits-fall-2009/pages/syllabus/"},
        {"id": 26, "title": "6.034 Artificial Intelligence", "url": "https://ocw.mit.edu/courses/6-034-artificial-intelligence-spring-2005/pages/syllabus/"},
        {"id": 27, "title": "6.036 Introduction to Machine Learning", "url": "https://ocw.mit.edu/courses/6-036-introduction-to-machine-learning-fall-2020/"},
        {"id": 28, "title": "6.867 Machine Learning", "url": "https://ocw.mit.edu/courses/6-867-machine-learning-fall-2006/pages/syllabus/"},
        {"id": 29, "title": "18.657 Mathematics of Machine Learning", "url": "https://ocw.mit.edu/courses/18-657-mathematics-of-machine-learning-fall-2015/pages/syllabus/"},
        {"id": 30, "title": "6.S191 Introduction to Deep Learning", "url": "https://ocw.mit.edu/courses/6-s191-introduction-to-deep-learning-january-iap-2020/"},
        {"id": 31, "title": "6.S897 Machine Learning for Healthcare", "url": "https://ocw.mit.edu/courses/6-s897-machine-learning-for-healthcare-spring-2019/pages/syllabus/"},
        {"id": 32, "title": "10.01 Ethics for Engineers: Artificial Intelligence", "url": "https://ocw.mit.edu/courses/10-01-ethics-for-engineers-artificial-intelligence-spring-2020/pages/syllabus/"},
        {"id": 33, "title": "6.5830 Database Systems", "url": "https://ocw.mit.edu/courses/6-5830-database-systems-fall-2023/"},
        {"id": 34, "title": "6.829 Computer Networks", "url": "https://ocw.mit.edu/courses/6-829-computer-networks-fall-2002/pages/syllabus/"},
        {"id": 35, "title": "6.263J Data Communication Networks", "url": "https://ocw.mit.edu/courses/6-263j-data-communication-networks-fall-2002/pages/syllabus/"},
        {"id": 36, "title": "6.837 Computer Graphics", "url": "https://ocw.mit.edu/courses/6-837-computer-graphics-fall-2012/pages/syllabus/"},
        {"id": 37, "title": "6.4210 Robotic Manipulation", "url": "https://ocw.mit.edu/courses/6-4210-robotic-manipulation-fall-2022/"},
        {"id": 38, "title": "2.017J Design of Electromechanical Robotic Systems", "url": "https://ocw.mit.edu/courses/2-017j-design-of-electromechanical-robotic-systems-fall-2009/pages/syllabus/"},
        {"id": 39, "title": "16.30 Feedback Control Systems", "url": "https://ocw.mit.edu/courses/16-30-feedback-control-systems-fall-2010/pages/syllabus/"},
        {"id": 40, "title": "2.04A Systems and Controls", "url": "https://ocw.mit.edu/courses/2-04a-systems-and-controls-spring-2013/pages/syllabus/"},
        {"id": 41, "title": "2.001 Mechanics & Materials I", "url": "https://ocw.mit.edu/courses/2-001-mechanics-materials-i-fall-2006/pages/syllabus/"},
        {"id": 42, "title": "3.032 Mechanical Behavior of Materials", "url": "https://ocw.mit.edu/courses/3-032-mechanical-behavior-of-materials-fall-2007/pages/syllabus/"},
        {"id": 43, "title": "3.012 Fundamentals of Materials Science", "url": "https://ocw.mit.edu/courses/3-012-fundamentals-of-materials-science-fall-2005/pages/syllabus/"},
        {"id": 44, "title": "3.020 Thermodynamics of Materials", "url": "https://ocw.mit.edu/courses/3-020-thermodynamics-of-materials-spring-2021/pages/syllabus/"},
        {"id": 45, "title": "2.25 Advanced Fluid Mechanics", "url": "https://ocw.mit.edu/courses/2-25-advanced-fluid-mechanics-fall-2013/pages/syllabus/"},
        {"id": 46, "title": "2.051 Introduction to Heat Transfer", "url": "https://ocw.mit.edu/courses/2-051-introduction-to-heat-transfer-fall-2015/pages/syllabus/"},
        {"id": 47, "title": "2.007 Design and Manufacturing I", "url": "https://ocw.mit.edu/courses/2-007-design-and-manufacturing-i-spring-2009/pages/syllabus/"},
        {"id": 48, "title": "2.00AJ Exploring Sea, Space, & Earth", "url": "https://ocw.mit.edu/courses/2-00aj-exploring-sea-space-earth-fundamentals-of-engineering-design-spring-2009/pages/syllabus/"},
        {"id": 49, "title": "1.012 Introduction to Civil Engineering Design", "url": "https://ocw.mit.edu/courses/1-012-introduction-to-civil-engineering-design-spring-2002/pages/syllabus/"},
        {"id": 50, "title": "1.040 Project Management", "url": "https://ocw.mit.edu/courses/1-040-project-management-spring-2009/pages/syllabus/"},
    ]
    return courses

def scrape_prerequisites(url):
    """Scrape prerequisites from MIT OCW course page."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Look for prerequisites section with better targeting
        prereq_header = soup.find(
            ['h2', 'h3', 'h4', 'strong', 'b'],
            string=re.compile(r'^\s*Prerequisites\s*$', re.IGNORECASE)
        )
        
        if prereq_header:
            prereq_content = []
            for sibling in prereq_header.find_next_siblings():
                if sibling.name in ['h2', 'h3', 'h4']:
                    break
                if hasattr(sibling, 'get_text'):
                    text = sibling.get_text(strip=True)
                    if text:
                        prereq_content.append(text)
            return "\n\n".join(prereq_content) if prereq_content else "Found 'Prerequisites' heading but no text."
        else:
            return "Prerequisites section not found."
    except requests.exceptions.RequestException as e:
        return f"Error fetching page: {e}"

def extract_prereqs(course_name, text):
    """Use Groq's LLaMA model to parse prerequisite text into structured format."""
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": """
You are a parser that extracts course prerequisites from MIT syllabus text.
Always respond ONLY with valid JSON in the format:
{"course": "<COURSE NAME>", "prerequisites": ["<CODE1>", "<CODE2>", ...]}.

Rules:
- "course" must be the FULL course name (not just the number).
- If no prerequisites are found, return an empty list [].
- Include non-course requirements like 'Java Proficiency' as plain text in the list.
"""},
            {"role": "user", "content": f"Course: {course_name}\nText: {text}"}
        ],
        temperature=0
    )
    output = response.choices[0].message.content.strip()
    try:
        parsed = json.loads(output)
        parsed["course"] = map_course_code_to_name(parsed.get("course", course_name))
        parsed["prerequisites"] = [map_course_code_to_name(pr) for pr in parsed.get("prerequisites", [])]
        return parsed
    except Exception:
        return {"course": course_name, "prerequisites": []}

def main():
    """Main function to run the scraper."""
    try:
        courses = get_course_data()
        print("Curriculum Compass - MIT OCW Prerequisite Scraper")
        print("=" * 50)
        
        while True:
            print("\nAvailable courses:")
            for course in courses:
                print(f"{course['id']:2d}. {course['title']}")
            
            choice = input(f"\nEnter the course number you want to scrape (1-{len(courses)}) or type 'exit' to quit: ").strip()
            
            if choice.lower() == "exit":
                print("Exiting program.")
                break
                
            if not choice.isdigit():
                print("Please enter a valid number or 'exit'.")
                continue
            
            choice = int(choice)
            selected = next((c for c in courses if c["id"] == choice), None)
            if not selected:
                print("Invalid course number.")
                continue
            
            print(f"\nScraping prerequisites for: {selected['title']}")
            print("=" * 50)
            
            try:
                prereq_text = scrape_prerequisites(selected["url"])
                print(f"Raw prerequisite text: {prereq_text[:200]}...")
                
                parsed = extract_prereqs(selected["title"], prereq_text)
                
                print("\n" + "=" * 50)
                print("RESULT:")
                print(json.dumps(parsed, indent=4))
                
            except Exception as e:
                print(f"Error scraping course: {e}")
            
            # Ask if they want to try another course
            again = input("\nDo you want to try another course? (y/n): ").strip().lower()
            if again != "y":
                print("Exiting program.")
                break
        
    except Exception as e:
        print(f"Error: {e}")
        print("Please make sure you have:")
        print("1. Set up your GROQ_API_KEY in the .env file")
        print("2. Installed all required dependencies (pip install -r requirements.txt)")
        print("3. Placed the COURSE CODES.csv file in the same directory")

if __name__ == "__main__":
    main()
