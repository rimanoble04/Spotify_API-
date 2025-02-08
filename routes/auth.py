from config import client_id,client_secret,redirect_uri
from flask import Blueprint,session ,redirect ,request 
import urllib.parse
import base64
from requests import post
from datetime import datetime

auth_bp= Blueprint('auth', __name__)

auth_url="https://accounts.spotify.com/authorize"
token_url="https://accounts.spotify.com/api/token"

@auth_bp.route('/')
def home():
    return "Welcome to home page<a href='/login'>Login</a>"

@auth_bp.route('/login')
def login():
    scope="user-top-read user-library-read playlist-read-private"
    params={
        'client_id':client_id,
        'redirect_uri':redirect_uri,
        'response_type':'code',
        'scope':scope,
        'show_dialog':True
    }
    auth_req_url=f"{auth_url}?{urllib.parse.urlencode(params)}"
    return redirect(auth_req_url)
    
@auth_bp.route('/callback')    
def callback():
    
    if 'error' in request.args:
        print('Error occured')
        
    if 'code' in request.args:
        code=request.args['code']
                    
        acc_url=client_id+':'+client_secret
        acc_bytes=acc_url.encode('utf-8')
        acc_base64=str(base64.b64encode(acc_bytes),'utf-8')
        
        form= {
            'code': code,
            'redirect_uri': redirect_uri,
            'grant_type': 'authorization_code'
        }
        
        headers= {
            'content-type': 'application/x-www-form-urlencoded',
            'Authorization': 'Basic '+ acc_base64     
        }
        
        response=post(token_url,headers=headers,data=form)
        token=response.json()
        print(token) 
        
        session['access_token'] = token['access_token']
        session['refresh_token'] = token['refresh_token']
        session['expires_at'] = datetime.now().timestamp()+token['expires_in']
        
        return redirect('/tracks')