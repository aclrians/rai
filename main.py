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

# process content through openAI
def aiRevision(content):
    response = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages = [
                {"role":"system", "content": "You are an experienced marketing director and you have helped customers transform their dull content into amazing sales pitches. Your job is to analyze the contents given to you by the user, the content should be transformed into well-written, unlike AI, and precise advertisments that are shown to those casually scrolling through reddit. Find a good mix between a sales pitch and casual conversation/storytelling, do NOT make it seem like you are trying to sell the product, just improve the pitch given by the user's prompt. Do NOT include hashtags as readers are less likely to read something with lame hashtags on it. "},
                {"role":"user","content": f"Improve the quality and virality of this user's product based on their description{content}"}
        ],
        temperature = 0.7,
        max_tokens = 500
    )   

    revisedWork = (response.choices[0].message.content)
    return revisedWork


# Checking with author
def publishing(revisedContent, sub,postTitle):
    print(f"\nHere is the revised content : {revisedContent}")
    subreddit = reddit.subreddit(sub)
    post = subreddit.submit(title=postTitle,selftext=revisedContent)
    print("Post submitted! Here is the URL: " , post.url)




subName = input("Hello, enter the name of the subreddit you'd like to post in :\n")
title = input("Now, name your post :\n")
body = input("Enter you the main idea of your post here:\n")

userDecision = input("\nWould you like to revise the content using ai?").lower()


if userDecision == "yes":
    aiRev = True
    while aiRev == True:
        userPick = input("\nWhat would you like to transform, the title or the body content?\n").lower()
        if userPick == "body":
            newContent= aiRevision(body)
            publishing(newContent, subName,title)
            aiRev = False

    # Sending our revised content to be published

    

