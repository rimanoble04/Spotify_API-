#OAuth Authorization Code Flow
from dotenv import load_dotenv
import os
import urllib.parse
import base64
from requests import request
import random as r
import json
from flask import Flask, sessions, redirect, url_for

load_dotenv()

client_ID=os.getenv("CLIENT_ID")
client_secret=os.getenv("CLIENT_SECRET")

redirect_uri="https://localhost:5000/callback"
auth_url = "https://accounts.spotify.com/authorize"
token_url = "https://accounts.spotify.com/api/token"   

app = Flask(__name__)
app.secret_key="random_secret_key"


@app.route('/')
def index():
    return "Welcome<a href='/login'>Login here</a>"
    
@app.route('/login')    
def login():
    scope="user-top-read user-library-read "
    params={
        'client_id':client_ID,
        'response_type':'code',
        'redirect_uri':redirect_uri,
        'scope':scope,
        'show_dialog':True
    }
    
    auth_req_url=f"{auth_url}?{urllib.parse.urlencode(params)}"
    return redirect(auth_req_url)
    
@app.route('/callback')    
def callback():
    if request.args=='error':
        print('error')
    if 'code' in request.args:
        
        req_body={
            'code':request.args['code'],
            'redirect_uri':redirect_uri,
            'grant_type':'authorization_code',
            'client_id':client_ID,
            'client_secret':client_secret
        }
    response= request.post(token_url,data=req_body)    
    token_info=response.json()
    
    print(token_info)
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
