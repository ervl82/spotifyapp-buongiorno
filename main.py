#!/usr/bin/env python
# coding: utf-8

# In[1]:


oauth_source ='https://www.section.io/engineering-education/spotify-python-part-1/'
docs = 'https://spotipy.readthedocs.io/en/2.19.0/?highlight=get_access_token#spotipy.oauth2.SpotifyOAuth.get_access_token'


# In[2]:


# import relevant libraries
import json # to handle API requests outputs
import requests # to make requests to API
from secrets import * # secrets.py file contains clientId, clientSecret, redirect_url, redirect_url2
import spotipy # to use spotipy library functions
from spotipy.oauth2 import SpotifyOAuth # to get Access Token


# In[3]:


# define script access scope
scope = "playlist-modify-private playlist-read-collaborative playlist-read-private playlist-modify-public user-library-read user-library-modify user-top-read user-read-recently-played"


# In[4]:


# Code to get token to use spotipy functions
# sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=clientId, client_secret= clientSecret, redirect_uri=redirect_url, scope=scope))


# In[5]:


# define oauth object and get access token
sp_oauth = SpotifyOAuth( clientId, clientSecret,redirect_url2,scope=scope)

spotify_token = ""

token_info = sp_oauth.get_cached_token()

if token_info:
    print('Found cached token!')
    spotify_token = token_info['access_token']
    print('Access Token: '+ spotify_token )
else:
    print('Cached token not found. Getting Access Token')
    token_info = sp_oauth.get_access_token()
    spotify_token = token_info['access_token']
    print('Access Token: '+ spotify_token)

if spotify_token:
    print('Access token available! Trying to get user information...')
    sp = spotipy.Spotify(spotify_token)
    results = sp.current_user()
    print('User: '+ results['id'])

else:
    print('No user information available')


# In[6]:


# set Playlists ids from Spotify
buongiorno = "6gp8NsLGHOpldIqBUukJQV"


# In[7]:


# get playlist current episodes and store in a delete list to delete them later
playlist_url = f"https://api.spotify.com/v1/playlists/{buongiorno}/tracks"
playlist_response = requests.get(
        playlist_url,
        headers ={
            "Content_Type": "application/json", 
            "Authorization" : f"Bearer {spotify_token}"
        }
    )
playlist_json = playlist_response.json()

playlist_json_items = playlist_json['items']
delete_episode_uri_list = []
for item in playlist_json_items:
    delete_episode_uri = item['track']['uri']
    delete_episode_uri_list.append(delete_episode_uri)
print(delete_episode_uri_list)


# In[8]:


#remove episodes in the delete list from playlist and print delete confirmations as snapshot_ids
for delete_episode in delete_episode_uri_list:
    playlist_remove_url = f"https://api.spotify.com/v1/playlists/{buongiorno}/tracks"
    playlist_remove_response = requests.delete(
        playlist_remove_url,
        headers ={
            "Accept": "application/json",
            "Content_Type": "application/json", 
            "Authorization" : f"Bearer {spotify_token}"
        },
        json = {
            'tracks': [
                {'uri': delete_episode_uri_list[0]},
                {'uri': delete_episode_uri_list[1]},
                {'uri': delete_episode_uri_list[2]}
            ]
        }
    )
    playlist_remove_json = playlist_remove_response.json()
    playlist_remove_json


# In[9]:


# set shows ids from Spotify and print list
in4minuti = "33YWzJrR8RkFFdocLDSc3c"
the_essential = "43A9fUmUbLYaHKSi1lAtn5"
start ="0tbtlfiFG6pK91TiARb9vQ"
shows_list = []
shows_list.append(in4minuti)
shows_list.append(the_essential)
shows_list.append(start)
shows_list


# In[10]:


#get shows episodes and store latest episode uri for each show into a list, print episodes uri list
episodes_uri_list = []
for show in shows_list:
    episode_url = f"https://api.spotify.com/v1/shows/{show}/episodes"
    episode_response = requests.get(
        episode_url,
        headers ={
            "Content_Type": "application/json", 
            "Authorization" : f"Bearer {spotify_token}"
        }
    )
    episodes_json = episode_response.json()
    
    episode_uri = episodes_json['items'][0]['uri']
    episodes_uri_list.append(episode_uri)
    
print(episodes_uri_list)


# In[11]:


#add episodes to playlist based on uri value stored in episodes uri list, and print add confirmations as snapshot_ids
for episode_uri in episodes_uri_list:
    playlist_add_url = f"https://api.spotify.com/v1/playlists/{buongiorno}/tracks?uris={episode_uri}"
    playlist_add_response = requests.post(
        playlist_add_url,
        headers ={
            "Content_Type": "application/json", 
            "Authorization" : f"Bearer {spotify_token}"
        }
    )
    playlist_add_json = playlist_add_response.json()
    playlist_add_json


# In[12]:


print('Automation script has finished')


# In[ ]:




