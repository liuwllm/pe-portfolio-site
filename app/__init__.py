import os
from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)


@app.route('/')
def index():
    work_experiences = [
        {
            "picture": "streamforge.jpg",
            "title": "Software Engineer Intern",
            "company": "Streamforge",
            "date": "Apr 2023 - Aug 2023",
            "description": "Developed POC projects for new and existing data pipelines and managed influencer advertising campaigns for Remnant II and Sea of Stars, generating thousands of clickthroughs"
        },
        {
            "picture": "cafezia.jpg",
            "title": "UX Intern",
            "company": "Cafezia Coffee",
            "date": "Nov 2022 - Apr 2023",
            "description": "Provided improvements to user experience, search engine optimization, and customer engagementProvided improvements to user experience, search engine optimization, and customer engagement"
        }
    ]

    education = [
        {
            "picture": "western.jpg",
            "name": "Western University",
            "degree": "HBSc. in Computer Science & HBA in Business Administration",
            "date": "Sep 2022 - Apr 2027"
        }
    ]

    return render_template('index.html', title="William's Portfolio", work_experience=work_experiences, education=education, url=os.getenv("URL"))

@app.route('/hobbies')
def hobbies():
    return render_template('hobbies.html', title="Hobbies", url=os.getenv("URL"))