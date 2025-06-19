import requests
import os
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

load_dotenv()

auth = HTTPBasicAuth(os.getenv("CLIENT_ID"), os.getenv("CLIENT_SECRET"))

data = {
    'grant_type': 'password',
    'username': os.getenv("USERNAME"),
    'password': os.getenv("PASSWORD")
}

headers = {'User-Agent': os.getenv("USER_AGENT")}

res = requests.post("https://www.reddit.com/api/v1/access_token",
                    auth=auth, data=data, headers=headers)

print(res.status_code)
print(res.text)
