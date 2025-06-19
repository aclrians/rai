import praw
import os
from dotenv import load_dotenv
from openai import OpenAI 

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

# Sending a message 
response = client.chat.completions.create(
    model = "gpt-3.5-turbo",
    messages = [
        {"role":"system", "content": "You are an experienced poster on Reddit. You know how to spot virality and trends which you use to enhance your posts"},
        {"role":"user","content": "Write a reddit post about the dangers of increased screen time in less than 4 paragraphs"}

    ],
    temperature = 0.7,
    max_tokens = 500
)

print(response.choices[0].message.content)


subName = input("Hello, enter the name of the subreddit you'd like to post in :\n")
title = input("Now, name your post :\n")
body = input("Enter your body of text: ")



subreddit = reddit.subreddit(subName)
post = subreddit.submit(title=title,selftext=body)

print("Post submitted! Here is the URL: " , post.url)