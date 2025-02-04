from dotenv import load_dotenv
import os
import base64

load_dotenv()

client_ID=os.getenv("CLIENT_ID")
client_secret=os.getenv("CLIENT_SECRET")

#Getting authorization
def get_token(): 
    print("hi")