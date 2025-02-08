from requests import post
from flask import session
from config import client_id,client_secret

def refresh_access_token():
    if 'refresh_token' not in session:
        return None

    data = {
        "refresh_token": session['refresh_token'],
        "grant_type": "refresh_token",
        "client_id": client_id,
        "client_secret": client_secret
    }
    response = post("https://accounts.spotify.com/api/token", data=data)
    new_token = response.json()

    session['access_token'] = new_token['access_token']
    session['expires_at'] = new_token['expires_in']

    return new_token['access_token']