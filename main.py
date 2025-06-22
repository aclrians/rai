import praw
import os
from dotenv import load_dotenv
from openai import OpenAI 
import sqlite3
from datetime import datetime

def insert_into_db(title, post):

    todayDate = datetime.today().strftime('%Y-%m-%d')
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS Post(date TEXT, title TEXT , body TEXT)")
    # Inserting
    cur.execute("INSERT INTO Post (date, title, body) VALUES (?,?,?)" , (todayDate,title,post))
    con.commit()
    # Closing
    con.close()
    print("Logged into database\n")


load_dotenv()
# Loading reddit API key
reddit = praw.Reddit(
    client_id = os.getenv("CLIENT_ID"),
    client_secret = os.getenv("CLIENT_SECRET"),
    password = os.getenv("PASSWORD"),
    username = os.getenv("USERNAME"),
    user_agent = os.getenv("USER_AGENT"),

)

# Loading openai API key
client = OpenAI(api_key=os.getenv("OPEN_AI_KEY"))

# process content through openAI
# have the model know if the title or body are waiting to be modified
def aiRevision(content, is_title = False):
    typeSelector = "title" if is_title else "body"
    prompt = f"This is a {typeSelector}:\n{content}"
    response = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages = [
                {"role":"system", "content": "You are an expert marketing editor. The user will provide EITHER a title or a body. Improve ONLY that section. Do not return anything else. For titles, keep it under 100 characters, no hashtags or quotes."},
                {"role":"user","content": prompt}
        ],
        temperature = 0.7,
        max_tokens = 500
    )   
    # Returning the ai response
    revisedWork = (response.choices[0].message.content)
    return revisedWork

def publishing(sub,userBody,revisedBody,userTitle,revisedTitle):
    subreddit = reddit.subreddit(sub)
    # If title changes
    if userBody == revisedBody and userTitle != revisedTitle:
        post = subreddit.submit(title = revisedTitle  , selftext = userBody)
        print("Post submitted! Here is the URL:\n " , post.url)
        insert_into_db(revisedTitle,userBody)
    # If body changes
    elif userBody != revisedBody and userTitle == revisedTitle:
        post = subreddit.submit(title = userTitle , selftext = revisedBody)
        print("Post submitted! Here is the URL: " , post.url)
        insert_into_db(userTitle,revisedBody)
    # If both title and body have been changed
    elif userBody != revisedBody and userTitle != revisedTitle:
        post = subreddit.submit(title = revisedTitle , selftext = revisedBody)
        print("Post submitted! Here is the URL: " , post.url)
        insert_into_db(revisedTitle,revisedBody)
    # If none changed
    else:
        post = subreddit.submit(title = userTitle , selftext = userBody)
        print("Post submitted! Here is the URL: " , post.url)
        insert_into_db(userTitle,userBody)




subName = input("Hello, enter the name of the subreddit you'd like to post in :\n")
title = input("Now, name your post :\n")
body = input("Enter you the main idea of your post here:\n")

aiBody = body
aiTitle = title

userDecision = input("\nWould you like to revise the content using ai?\n").lower()

'''
So I wrote to senf multiple variables because we needed a system to see which content was being changed, will explain better in future
'''
if userDecision == "yes":
    aiRev = True
    while aiRev == True:
        userPick = input("\nWhat would you like to transform, the title or the body content?\n").lower()
        if userPick == "body":
            aiBody= aiRevision(body, is_title = False)
            print(f"\nHere is the revised content : {aiBody}")
            # Publishing the content
            publishing(subName,body,aiBody,title,aiTitle)
            aiRev = False
        if userPick == "title":
            aiTitle = aiRevision(title, is_title = True)
            print(f"\nHere is the revised content : {aiTitle}")
            publishing(subName,body,aiBody,title,aiTitle)
            aiRev = False


    

