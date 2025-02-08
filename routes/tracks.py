from flask import Blueprint ,session ,redirect 
from requests import get
from datetime import datetime
import pandas as pd

tracks_bp=Blueprint('tracks',__name__)

@tracks_bp.route('/tracks')  
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
    
@tracks_bp.route('/playlists')
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
            track_id=j['track']['id']
            track_name = j["track"]["album"]["artists"][0]["name"]
            track_artist = j['track']['name']
            
            #data.append({'track_id': track_id, 'track_name': track_name, 'track_artist': track_artist})    
        tracks_url=tracks_data.get('next')
    session['data']=data     
    return redirect('/liked_songs')

@tracks_bp.route('/liked_songs')
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
        
        #data.append({'track_id':track_id,'track_name':track_name,'track_artist':track_artist})   
        
    df=pd.DataFrame(data)
    df.to_csv('songs.csv',index=False)
    return (data) 