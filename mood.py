from dotenv import load_dotenv
import os 
from flask import Flask ,session ,redirect ,request ,jsonify
import urllib.parse
import base64
from requests import post,get
from datetime import datetime
import pandas as pd

load_dotenv()

client_id=os.getenv("CLIENT_ID")
client_secret=os.getenv("CLIENT_SECRET")
redirect_uri="http://localhost:5000/callback"


app=Flask(__name__)
app.secret_key="random_secret_key"

auth_url="https://accounts.spotify.com/authorize"
token_url="https://accounts.spotify.com/api/token"

@app.route('/')
def home():
    return "Welcome to home page<a href='/login'>Login</a>"

@app.route('/login')
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
    
@app.route('/callback')    
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
 
@app.route('/tracks')  
def get_top_tracks():
    
    if 'access_token' not in session:
        return redirect('/login')
    if datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh')
    
    type="tracks"
    url=f"https://api.spotify.com/v1/me/top/{type}"
    
    header={"Authorization":"Bearer "+ session['access_token']}
    response=get(url,headers=header)
    result=response.json()
    
    #result=jsonify(result_first['items'][0]['artists'][0]['name'])
    data=[]
    for i in result['items']:
        track_id=i['id']
        track_name=i['name']
        track_artist=i['artists'][0]['name']
        
        data.append({'track_id':track_id,'track_name':track_name,'track_artist':track_artist})    
        
    session['data']=data    
    return redirect('/playlists')
    
@app.route('/playlists')
def get_current_user_playlists():
    
    if 'access_token' not in session:
        return redirect('/login')
    if datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh')
    
    
    url=f"https://api.spotify.com/v1/me/playlists"
    
    header={"Authorization":"Bearer "+ session['access_token']}
    response=get(url,headers=header)
    result=response.json()
    
    for i in result['items']:
        playlist_id=i['id']
        
    tracks_url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"    
    
    data= session['data']
    
    #idk why i get an error in line 129 its a key error pls check the json to extract correctly
    while tracks_url:
        tracks_response=get(tracks_url,headers=header)
        tracks_data=tracks_response.json()
    
        for j in tracks_data['items']:
            track_id=j['id']
            track_name = j['name']
            track_artist = j['artists'][0]['name']
            
            data.append({'track_id': track_id, 'track_name': track_name, 'track_artist': track_artist})    
        tracks_url=tracks_data.get('next')
    session['data']=data     
    return redirect('/liked_songs')

@app.route('/liked_songs')
def get_liked_songs():
    
    if 'access_token' not in session:
        return redirect('/login')
    if datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh')
    
    url=f"https://api.spotify.com/v1/me/tracks"
    
    header={"Authorization":"Bearer "+ session['access_token']}
    response=get(url,headers=header)
    result=response.json()
    
    #result=jsonify(result_first['items'][0]['artists'][0]['name'])
    data=session['data']
    for i in result['items']:
        track=i['track']
        track_id=track['id']
        track_name=track['name']
        track_artist=track['artists'][0]['name']
        
        data.append({'track_id':track_id,'track_name':track_name,'track_artist':track_artist})   
        
    df=pd.DataFrame(data)
    df.to_csv('songs.csv',index=False)
    return redirect('/')    
    
@app.route('/refresh')
def refresh_token():
    if 'refresh_token' not in session:
        return redirect('/login')
    
    if datetime.now().timestamp() > session['expires_at']:
        
        req_body={
            "refresh_token": session['refresh_token'],
            "grant_type": "refresh_token",
            "client_id":client_id,
            "client_secret":client_secret,
        }    
        response=post(token_url,data=req_body)
        new_token=response.json()
        
        session['access_token'] = new_token['access_token']
        session['refresh_token'] = new_token['refresh_token']
        session['expires_at'] = datetime.now().timestamp() + new_token['expires_in']
        
        return redirect('/tracks') 
        
if __name__=='__main__':
    app.run(host='0.0.0.0',debug=True)   