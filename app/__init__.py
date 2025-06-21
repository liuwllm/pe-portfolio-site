import os
from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

PAGES = [
    {
        "name": "home",
        "endpoint": "index"
    },
    {
        "name": "hobbies",
        "endpoint": "hobbies"
    }
]

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

    return render_template('index.html', title="William's Portfolio", work_experience=work_experiences, education=education, url=os.getenv("URL"), pages=PAGES)

@app.route('/hobbies')
def hobbies():
    hobbies = [
        {
            "picture": "gaming.jpg",
            "title": "Gaming",
            "description": "I'm an avid gamer who loves playing all sorts of games! I typically play a lot of multiplayer games like Valorant or Teamfight Tactics. Some other favourites include Nintendo games like Fire Emblem and Pokemon. I've also played my fair share of indie games, with some of my favourites being Hades, Celeste, and Return of the Obra Dinn.",
        },
        {
            "picture": "japanese.jpg",
            "title": "Learning Japanese",
            "description": "I'm currently learning Japanese, mostly through immersion and flashcards (Anki).",
        },
        {
            "picture": "guitar.jpg",
            "title": "Playing Guitar",
            "description": "I recently bought a guitar as an impulse purchase of sorts. It's been a lot of fun fiddling around with it, though, and I'm hoping to progress my way to learning full songs soon.",
        }
    ]


    return render_template('hobbies.html', title="Hobbies", hobbies=hobbies, url=os.getenv("URL"), pages=PAGES)