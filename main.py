from dotenv import load_dotenv
import os
import base64
from requests import post,get
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
    
    #post request, convert to json and extracts access token
    result=post(url, headers=headers, data=data)
    json_result= json.loads(result.content)
    token= json_result["access_token"]
    return token

#Authorization headers are used in api calls by client to inform spotify that an authorized user is trying to access resource.
def get_auth_header(token):
    return {"Authorization":"Bearer "+ token}


def search_artist(token,artist_name):
    url="https://api.spotify.com/v1/search"
    headers=get_auth_header(token)
    query=f"?q={artist_name}&type=artist&limit=1"
    query_url=url + query
    
    result=get(query_url, headers=headers)
    json_result=json.loads(result.content)["artists"]["items"][0]
    return json_result["id"]

def top_songs(token):
    artist=input('Enter artist name: ')
    art_id=search_artist(token,artist)

    url=f"https://api.spotify.com/v1/artists/{art_id}/top-tracks"
    headers=get_auth_header(token)
    result=get(url, headers=headers)
    json_result= json.loads(result.content)["tracks"][0]
    print(json_result["name"])
    
token=get_token()
result=top_songs(token)
#result=search_artist(token,"bts")
