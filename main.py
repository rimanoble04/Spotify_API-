from dotenv import load_dotenv
import os
import base64
from requests import post
import json

load_dotenv()

client_ID=os.getenv("CLIENT_ID")
client_secret=os.getenv("CLIENT_SECRET")

#Getting authorization
def get_token(): 
    #Setting up authorization string and encoding it
    auth_str= client_ID +":"+ client_secret
    auth_bytes=auth_str.encode("utf-8")
    auth_base64= str(base64.b64encode(auth_bytes),"utf-8")
    
    #Setting up owner url
    url="https://accounts.spotify.com/api/token"
    
    #Access token request headers
    headers={
        "Authorization":"Basic "+auth_base64,
        "Content-Type":"application/x-www-form-urlencoded"
    }
    data={"grant_type":"client_credentials"}
    
    #post request, convert to json and parse access token
    result=post(url, headers=headers, data=data)
    json_result= json.loads(result.content)
    token= json_result["access_token"]
    return token

token=get_token()