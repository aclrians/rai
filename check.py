from dotenv import load_dotenv
import os

load_dotenv()

print("CLIENT_ID =", os.getenv("CLIENT_ID"))
print("CLIENT_SECRET =", os.getenv("CLIENT_SECRET"))
print("USERNAME =", os.getenv("USERNAME"))
print("PASSWORD =", os.getenv("PASSWORD"))
print("USER_AGENT =", os.getenv("USER_AGENT"))