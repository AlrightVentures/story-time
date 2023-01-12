# Title: Story time
# Video Demo:  https://www.youtube.com/watch?v=4cl-ngBlMws
# Description:

## Overview
This project called 'STORY TIME' is a Flask web app focused on creation of children stories. 
I built this project for my 8-month old daughter. I would like her to learn some vocabulary through night time stories that I could read to her. Story creation takes time so I decided to make the process automated with ChatGPT.  


## How it works
1. When the app is launched (or '/' page reloaded) the app selects 3 random words from a words table in the words.db database. 
2. 3 words as used as keywords for a night time story.
3. Pexels platform is searched for the 3 keywords and the web app displays 3 images per keyword on the page, i.e. 9 images in total (3 for the first word, 3 for the second, and 3 for the third word)
4. A prompt to generate a night time story for children is sent to ChatGPT via API. The story generated by ChatGPT has to focus on the 3 keywords.
5. The web app receives the response ('a story') which is displayed on the homepage. 
6. The story displayed on the homepage is added to the stories table in the words.db database. 
7. All stories are displayed on 'Past stories' page. 
8. Users can access individual story pages by clicking one of the tiles on the 'Past stories' page
9. When user clicks on the tile, the web app gets the story string from the words.db database and new request is sent to Pexels platform to display corresponding images. 


## The work process
1. I searched the web for some common English words, copy/pasted them to an Excel file. I saved the Excel file as .csv and uploaded it to sql database - added ~1500 words to a words.db database. 
2. I created flask app skeleton using existing Finance app (cs50 week 9).
3. I decided it would be good to show some example images for keywords so that a baby can associate a word with an image of what it represents. For that I searched Google for some image platforms and decided to select Pexels as their API was easy to use and understand. 
4. I set up Pexels account and got their API. 
5. I created ChatGPT account and learned about their API. I created API key for the use in the web app. 
6. I connected up ChatGPT and Pexels APIs to the webapp and created structure to display ChatGPT-generated stories and images pulled from Pexels. 
7. I needed to find a way to store stories created by ChatGPT to a) capture stories in case I'd like to reuse them and b) save up tokens as you need to pay for ChatGPT use. For that I created a table in words.db to store story info like rowid, keywords used (selected 3 words per story) and story string. 
8. I created a 'Past stories' page to display all available stories. I then created a template 'story' page to display individual stories. This was sort of necessary as I wanted to maintain the functionality to display images from Pexels for all individual stories, i.e. to keep the functionality consistent across all stories. 
9. Finished the app with Bootstrap formatting.
10. Tested functionality in Google Chrome and Safari browsers. 


## What each of the files contains and does
1. App.py - this file imports all necessary libraries; it configures the flask app; it connects to Pexels and ChatGPT APIs; it defines all routes of the flask app. In '/' we connect to sqlite3 database to select 3 random keywords, send a prompt to ChatGPT and receive a response that is then rendered on the page. We insert the response into the sqlite3 database and close the database connection. 
In '/stories' route we connect to sqlite3 database and select all info related to existing stories, which is then displayed on a page as tiles that users can click on to get to individual story pages. In '/story' route we get user-selected story info e.g. keywords and story id using request.args.get. Then we render a story for user's selection by selecting a story matching story id and render images from Pexels. 
2. Config.py - includes all API keys that I don't want to upload to Github.
3. .gitignore - list of all files to be excluded from git repository.
4. Static folder - styles.css contains modifications to Bootstrap styles 
5. Templates folder - there are index.html, layout.html, stories.html, and story.html files. I used layout.html for templating and other html files extend that template file. Jinja is used to display variables, e.g. data from the database without hardcoding into html. 
6. Requirements.txt - lists the correct versions of the required Python libraries to run the Python code used in the web app. 


## Design choices to debate 
1. Which image platform to use - I went with Pexels as I could understand how to use their API, it worked and the images provided matched the keywords. I tried some other platforms but I couldn't get the API to work. 
2. What info to focus on to make it a product I want to use, i.e. what is my MVP. Is it a text-to-speech tool with less stories? Should I be the one reading stories to my child? Should I include images? Decided to go ahead with images to make it visual for a child as it should be easier to understand the meaning of a word by seeing it. MVP does not include text-to-speech as I would initially aim to read the stories myself. 
3. How many keywords to focus on per day. Initially started with 10 keywords however decided to reduce it to 5, then further down to 3 keywords. More keywords meant more complexity in terms of page layout management and APIs - more keywords meant more images had to be loaded and it was slower. I decided that 3 keywords still make a story exciting and instead of displaying 10 images of individual keywords I went with 3 images per keyword to provide some variety for a child to better understand that e.g. 'bottle' can mean a plastic blue bottle, a glass transparent bottle, or some different bottle with a label etc. 


## Potential project expansions
1. Account creation for individual users.
2. Text-to-speech functionality to read story text aloud. 
3. Creation of stories based on user-provided keywords. 
4. Generation of story-specific images using e.g. DALL-E
