import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import spotipy.util as util
from pathlib import Path
import json
import requests # to make requests to API
import sys
import urllib.parse
import base64
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService

load_dotenv()

sp = None

SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
SPOTIFY_CLIENT_CALLBACK_URL = 'http://localhost:8888/callback'
SPOTIFY_USERNAME = os.getenv('SPOTIFY_USERNAME')
SPOTIFY_PASSWORD = os.getenv('SPOTIFY_PASSWORD')
SPOTIFY_CLIENT_REFRESH_TOKEN = os.getenv('SPOTIFY_CLIENT_REFRESH_TOKEN')

AUTH_SCOPE = "playlist-modify-private playlist-read-collaborative playlist-read-private playlist-modify-public user-library-read user-library-modify user-top-read user-read-recently-played"

print(SPOTIFY_CLIENT_REFRESH_TOKEN)

SPOTIFY_CLIENT_REFRESH_TOKEN

# # Define base url for authorization site and define response type
# auth_url_base = 'https://accounts.spotify.com/authorize?'
# response_type = 'code'

# # Create payload based on data from config file extracted during __init__
# payload = {
#   'client_id': SPOTIFY_CLIENT_ID,                   
#   'redirect_uri': SPOTIFY_CLIENT_CALLBACK_URL,                   
#   'response_type': response_type,                   
#   'scope': AUTH_SCOPE
# }

# # Encode the payload for a url and append to the base url
# url_params = urllib.parse.urlencode(payload)
# full_auth_url = auth_url_base + url_params
# print('Custom authorization url:', full_auth_url, '\n')

# print('Directing to Spotify Authorization page...')

# # Create selenium options
# options = FirefoxOptions()
# options.add_argument("--headless")

# # Create selenium driver
# driver = webdriver.Firefox(
#   service = FirefoxService(GeckoDriverManager().install()),
#   options = options
# )

# # Open browser
# driver.get(full_auth_url)

# # Find html form fields
# login_field = driver.find_element(By.ID, 'login-username')
# pass_field = driver.find_element(By.ID, 'login-password')
# sub_button = driver.find_element(By.ID, 'login-button')

# print('Submitting user login data...\n')

# print(f"Username ({SPOTIFY_USERNAME}) length of {len(SPOTIFY_USERNAME)}")
# print(f"Password (******) length of {len(SPOTIFY_PASSWORD)}")

# # Pass user data to form
# login_field.send_keys(SPOTIFY_USERNAME)
# pass_field.send_keys(SPOTIFY_PASSWORD)

# print('Sent keys...\n')

# # Selenium raises an error when you can't connect to a domain
# # Catch that error to handle it and extract the URL for the access token.
# try:
#   # Submit the form
#   sub_button.click()
#   print('sub_button click...\n')

#   # pause for redirect to acceptance page
#   time.sleep(3)

#   # Find agree button
#   # driver.find_element_by_id('auth-accept')
#   agree_button = driver.find_element('[data-testid="auth-accept"]')
#   print('Button Found')

#   # Click button and wait for error
#   agree_button.click()
#   print('Button Clicked')
#   time.sleep(30)
# except Exception as err:
#   # Catch error and do nothing to keep code going
#   print('Error caught')
#   print('Redirect successful...\n')
#   print('Extracting authorization code now...\n')

# time.sleep(5)

# # Get current url which now contains the access token 
# redirect = driver.current_url
# driver.close()

# print('Redirect-URI:', redirect)

# parsed = urllib.parse.urlparse(redirect)
# return_package = urllib.parse.parse_qs(parsed.query)

# # Return the query from the rediret url
# AUTH_CODE = return_package['code'][0]

# # Generate body for request to get access token
# grant_type = 'authorization_code'

# body = {
#   'grant_type': grant_type,
#   'code': AUTH_CODE,
#   'redirect_uri': SPOTIFY_CLIENT_CALLBACK_URL
# }

# # Format client id and secret for request header + encode them
# client_params = SPOTIFY_CLIENT_ID + ':' + SPOTIFY_CLIENT_SECRET
# encoded_client_params = base64.b64encode(client_params.encode('ascii'))

# print('\nLoading Client Secret, Client ID, and Authorization Pay Load...')

# # Create header with encoded client id and secret
# headers = {'Authorization': 'Basic ' + encoded_client_params.decode('ascii')}

# print('\nRequesting Access and Refresh Tokens...')

# # Submit post request to get the access tokens
# response = requests.post(
#   'https://accounts.spotify.com/api/token',
#   data = body,
#   headers = headers
# )

# tokens = response.text
# tokens_parsed = json.loads(tokens)

# print('\nParsing and extracting tokens...')
# SPOTIFY_CLIENT_TOKEN = tokens_parsed['access_token']
# SPOTIFY_CLIENT_REFRESH_TOKEN = tokens_parsed['refresh_token']

# print(SPOTIFY_CLIENT_TOKEN)
# print(SPOTIFY_CLIENT_REFRESH_TOKEN)


# grant_type2 = 'refresh_token'
# body2 = {
#   'grant_type':grant_type2,
#   'refresh_token': SPOTIFY_CLIENT_REFRESH_TOKEN
# }

# client_params2 = SPOTIFY_CLIENT_ID + ':' + SPOTIFY_CLIENT_SECRET
# encoded_client_params2 = base64.b64encode(client_params2.encode('ascii'))
# headers2 = {'Authorization': 'Basic ' + encoded_client_params2.decode('ascii')}

# response2 = requests.post(
#   'https://accounts.spotify.com/api/token',
#   data = body2,
#   headers = headers2
# )

# print(response2)

# tokens2 = response2.text
# tokens_parsed2 = json.loads(tokens2)

# print('\nParsing and extracting tokens...')
# print(tokens2)
# print(token_parsed2)
# SPOTIFY_CLIENT_TOKEN = tokens_parsed2['access_token']
# # SPOTIFY_CLIENT_REFRESH_TOKEN = tokens_parsed2['refresh_token']

# print(SPOTIFY_CLIENT_TOKEN)
# # print(SPOTIFY_CLIENT_REFRESH_TOKEN)

# # set Playlists ids from Spotify
# buongiorno = "6gp8NsLGHOpldIqBUukJQV"


# # get playlist current episodes and store in a delete list to delete them later
# playlist_url = f"https://api.spotify.com/v1/playlists/{buongiorno}/tracks"
# playlist_response = requests.get(
#         playlist_url,
#         headers ={
#             "Content_Type": "application/json", 
#             "Authorization" : f"Bearer {SPOTIFY_CLIENT_TOKEN}"
#         }
#     )
# playlist_json = playlist_response.json()

# playlist_json_items = playlist_json['items']
# delete_episode_uri_list = []
# for item in playlist_json_items:
#     delete_episode_uri = item['track']['uri']
#     delete_episode_uri_list.append(delete_episode_uri)
# print(delete_episode_uri_list)


# #remove episodes in the delete list from playlist and print delete confirmations as snapshot_ids
# for delete_episode in delete_episode_uri_list:
#     playlist_remove_url = f"https://api.spotify.com/v1/playlists/{buongiorno}/tracks"
#     playlist_remove_response = requests.delete(
#         playlist_remove_url,
#         headers ={
#             "Accept": "application/json",
#             "Content_Type": "application/json", 
#             "Authorization" : f"Bearer {SPOTIFY_CLIENT_TOKEN}"
#         },
#         json = {
#             'tracks': [
#                 {'uri': delete_episode_uri_list[0]},
#                 {'uri': delete_episode_uri_list[1]},
#                 {'uri': delete_episode_uri_list[2]}
#             ]
#         }
#     )
#     playlist_remove_json = playlist_remove_response.json()
#     playlist_remove_json


# # set shows ids from Spotify and print list
# in4minuti = "33YWzJrR8RkFFdocLDSc3c"
# the_essential = "43A9fUmUbLYaHKSi1lAtn5"
# start ="0tbtlfiFG6pK91TiARb9vQ"
# shows_list = []
# shows_list.append(in4minuti)
# shows_list.append(the_essential)
# shows_list.append(start)
# shows_list


# #get shows episodes and store latest episode uri for each show into a list, print episodes uri list
# episodes_uri_list = []
# for show in shows_list:
#     episode_url = f"https://api.spotify.com/v1/shows/{show}/episodes"
#     episode_response = requests.get(
#         episode_url,
#         headers ={
#             "Content_Type": "application/json", 
#             "Authorization" : f"Bearer {SPOTIFY_CLIENT_TOKEN}"
#         }
#     )
#     episodes_json = episode_response.json()
    
#     episode_uri = episodes_json['items'][0]['uri']
#     episodes_uri_list.append(episode_uri)
    
# print(episodes_uri_list)

# #add episodes to playlist based on uri value stored in episodes uri list, and print add confirmations as snapshot_ids
# for episode_uri in episodes_uri_list:
#     playlist_add_url = f"https://api.spotify.com/v1/playlists/{buongiorno}/tracks?uris={episode_uri}"
#     playlist_add_response = requests.post(
#         playlist_add_url,
#         headers ={
#             "Content_Type": "application/json", 
#             "Authorization" : f"Bearer {SPOTIFY_CLIENT_TOKEN}"
#         }
#     )
#     playlist_add_json = playlist_add_response.json()
#     playlist_add_json


# print('Automation script has finished')
