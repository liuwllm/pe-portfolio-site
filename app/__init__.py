import os, datetime
from flask import Flask, render_template, request
from dotenv import load_dotenv
from peewee import *
from playhouse.shortcuts import model_to_dict

load_dotenv()
app = Flask(__name__)

if os.getenv("TESTING") == "true":
    print("Running in test mode")
    mydb = SqliteDatabase('file:memory?mode=memory&cache=shared', uri=True)
else:
    mydb = MySQLDatabase(os.getenv("MYSQL_DATABASE"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        host=os.getenv("MYSQL_HOST"),
        port=3306
    )

print(mydb)

class TimelinePost(Model):
    name= CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb

mydb.connect()
mydb.create_tables([TimelinePost])

PAGES = [
    {
        "name": "home",
        "endpoint": "index"
    },
    {
        "name": "hobbies",
        "endpoint": "hobbies"
    },
    {
        "name": "timeline",
        "endpoint": "timeline"
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

    return render_template('index.html', title="MLH Fellow", work_experience=work_experiences, education=education, url=os.getenv("URL"), pages=PAGES)

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

@app.route('/timeline')
def timeline():
    posts = [model_to_dict(p) for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())]

    return render_template('timeline.html', title='Timeline', url=os.getenv("URL"), reload_url=os.getenv("RELOAD_URL"), pages=PAGES, posts=posts)

@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    # Validate required fields
    if not request.form.get('name'):
        return "Invalid name", 400
    
    if not request.form.get('content'):
        return "Invalid content", 400
    
    # Basic email validation
    email = request.form.get('email')
    if '@' not in email or '.' not in email:
        return "Invalid email", 400
    
    name = request.form['name']
    content = request.form['content']
    timeline_post = TimelinePost.create(name=name, email=email, content=content)
    
    return model_to_dict(timeline_post)

@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    return {
        'timeline_posts': [
            model_to_dict(p)
            for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }
