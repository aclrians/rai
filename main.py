import praw
import os
from dotenv import load_dotenv

# Transferring keys
load_dotenv()
reddit = praw.Reddit(
    client_id = os.getenv("CLIENT_ID"),
    client_secret = os.getenv("CLIENT_SECRET"),
    password = os.getenv("PASSWORD"),
    username = os.getenv("USERNAME"),
    user_agent = os.getenv("USER_AGENT"),

)


subName = input("Hello, enter the name of the subreddit you'd like to post in :\n")
title = input("Now, name your post :\n")
body = input("Enter your body of text: ")


subreddit = reddit.subreddit(subName)
post = subreddit.submit(title=title,selftext=body)

print("Post submitted! Here is the URL: " , post.url)