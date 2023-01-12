# STORY TIME WEB APP

# What will your software do? 
# The App will select 5 random words per day from a set of words. 
# The 5 selected words will be used in features described below to help babies learn to talk.

# What features will it have? 
# It will display selected words as images and use them in a chatGPT generated story for parents to read to their children. 

# How will it be executed?
# It will be executed as a web app using flask. 

# What new skills will you need to acquire? What topics will you need to research?
# I will need to figure out how to use chatGPT, how to display images of selected words, automate the process and keep the data in a database. 

# Import libraries to run flask app
import sys, os
import config
from flask import Flask, flash, redirect, render_template, request, session
from flask_session.__init__ import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
import openai
import jinja2
import sqlite3
# Import API class from pexels_api package
from pexels_api import API

global storiesInfo

"""def override_where():
     
    # change this to match the location of cacert.pem
    return os.path.abspath("cacert.pem")


# is the program compiled?
if hasattr(sys, "frozen"):
    import certifi.core

    os.environ["REQUESTS_CA_BUNDLE"] = override_where()
    certifi.core.where = override_where

    # delay importing until after where() has been replaced
    import requests.utils
    import requests.adapters
    # replace these variables in case these modules were
    # imported before we replaced certifi.core.where
    requests.utils.DEFAULT_CA_BUNDLE_PATH = override_where()
    requests.adapters.DEFAULT_CA_BUNDLE_PATH = override_where()"""

# List of common baby words
babyWords = ["baby", "milk", "cocomelon", "sleep", "nap", "eat", "drink", "poo", "wash", "milk", "food"]

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Type your Pexels API
PEXELS_API_KEY = config.pexelsKey
# Create API object
api = API(PEXELS_API_KEY)

# Make sure API key is set
#if not os.environ.get("API_KEY"):
#  raise RuntimeError("API_KEY not set")

# Connecting ChatGPT
openai.api_key = config.openAIKey 



@app.route("/", methods=["GET"])
def index():

    wordsList = []

    # create con object to connect 
    # the database words.db
    con = sqlite3.connect("words.db")
    #check_same_thread=False)

    # create the cursor object
    cur = con.cursor()
    # insertion cursor object
    insertCur = con.cursor()

    wordsListTest = cur.execute("select noun from words ORDER BY RANDOM() LIMIT 3")
    wordsListTest = cur.fetchall()
    cur.close()
    for element in wordsListTest:
        wordsList.append(element[0])

    wordOne = wordsList[0]
    wordTwo = wordsList[1]
    wordThree = wordsList[2]

    # print(wordOne)
    # print(wordTwo)
    # print(wordThree)
    
    imageInfo = {}

    # Search three photos of each keyword from list above
    for word in wordsList:

        imageInfo[word] = []

        api.search(word, page=1, results_per_page=3)
        # Get photo entries
        photos = api.get_entries()
        # Loop the three photos

        # List all relevant info for image
        for photo in photos:
            # Print photographer
            photographerInfo = photo.photographer
            # Print url
            imageUrl = photo.original

            imageInfo[word].append([photographerInfo, imageUrl])

    storyPrompt = (f"Write a night time story for children focused on keywords: {wordOne}, {wordTwo}, {wordThree}")

    # Generate a story
    response = openai.Completion.create(
           model="text-davinci-003",
           prompt=storyPrompt,
           max_tokens=4060,
           temperature=0.9,
           
       )
    
    
    story = response.choices[0].text
    # story = story.replace('.', '...')
    storyParagraphs = story.split('.')
    storyParagraphs = storyParagraphs[:-1]
    #print(storyParagraphs)

    # Insert story into database
    storyInsert = insertCur.execute("INSERT INTO stories (wordOne, wordTwo, wordThree, story) VALUES (?, ?, ?, ?)", (wordOne, wordTwo, wordThree, story))
    con.commit()

    con.close()
    return render_template("index.html", words=wordsList, imageInfo=imageInfo, story=storyParagraphs)


@app.route("/stories")
def stories():


    # create con object to connect 
    # the database words.db
    con = sqlite3.connect("words.db", check_same_thread=False)

    # create the cursor object
    cur = con.cursor()
    storiesInfo = cur.execute("select *, rowid from stories")

    storiesInfo = cur.fetchall()
    cur.close()
    con.close()
    # print(storiesInfo)

    return render_template("stories.html", storiesInfo=storiesInfo)


@app.route("/story")
def story():
    storyId = request.args.get('storyId')
    wordOne = request.args.get('wordOne')
    wordTwo = request.args.get('wordTwo')
    wordThree = request.args.get('wordThree')

    # create con object to connect 
    # the database words.db
    con = sqlite3.connect("words.db", check_same_thread=False)

    # create the cursor object
    cur = con.cursor()
    storyInfo = cur.execute("select story from stories where rowid=(?)", (storyId,))
    storySelected = cur.fetchone()
    storySelected = storySelected[0]
    storyParagraphs = storySelected.split('.')
    storyParagraphs = storyParagraphs[:-1]
    # print(storyParagraphs)
    
    cur.close()
    con.close()

    imageInfo = {}

    # Search three photos of each keyword from list above
    for word in [wordOne, wordTwo, wordThree]:

        imageInfo[word] = []

        api.search(word, page=1, results_per_page=3)
        # Get photo entries
        photos = api.get_entries()
        # Loop the three photos

        # List all relevant info for image
        for photo in photos:
            # Print photographer
            photographerInfo = photo.photographer
            # Print url
            imageUrl = photo.original

            imageInfo[word].append([photographerInfo, imageUrl])


    return render_template("story.html", wordOne=wordOne, wordTwo=wordTwo, wordThree=wordThree, story=storyParagraphs, imageInfo=imageInfo)



