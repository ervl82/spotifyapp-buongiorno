import random  # To select random tracks

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

# # This commented out section below is needed for the first time the script is run on a virtual machine. It helps generate a refresh token that can then be used indefintely. It uses a headless selenium bot to give authorization on behalf of the user to the app

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


grant_type2 = 'refresh_token'
body2 = {
  'grant_type':grant_type2,
  'refresh_token': SPOTIFY_CLIENT_REFRESH_TOKEN
}

client_params2 = SPOTIFY_CLIENT_ID + ':' + SPOTIFY_CLIENT_SECRET
encoded_client_params2 = base64.b64encode(client_params2.encode('ascii'))
headers2 = {'Authorization': 'Basic ' + encoded_client_params2.decode('ascii')}

response2 = requests.post(
  'https://accounts.spotify.com/api/token',
  data = body2,
  headers = headers2
)

print(response2)

tokens2 = response2.text
tokens_parsed2 = json.loads(tokens2)

print('\nParsing and extracting tokens...')
SPOTIFY_CLIENT_TOKEN = tokens_parsed2['access_token']
# SPOTIFY_CLIENT_REFRESH_TOKEN = tokens_parsed2['refresh_token']

print(SPOTIFY_CLIENT_TOKEN)
# print(SPOTIFY_CLIENT_REFRESH_TOKEN)

# Define the playlists
buongiorno = "6gp8NsLGHOpldIqBUukJQV"  # Buongiorno playlist ID
dipinto_di_blu = "1INSZcL2niDMfaMwYHqVhV"  # Dipinto_di_blu playlist ID

# Get the current episodes from the Buongiorno playlist and store them for deletion
playlist_url = f"https://api.spotify.com/v1/playlists/{buongiorno}/tracks"
delete_episode_uri_list = []

# Fetch all pages of the playlist tracks
while playlist_url:
    try:
        playlist_response = requests.get(
            playlist_url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {SPOTIFY_CLIENT_TOKEN}"
            }
        )
        playlist_response.raise_for_status()  # Check for HTTP errors
        playlist_json = playlist_response.json()

        # Extract track URIs
        if 'items' in playlist_json:
            delete_episode_uri_list.extend(
                [item['track']['uri'] for item in playlist_json['items'] if item.get('track') and item['track'].get('uri')]
            )

        # Get the URL for the next page of results
        playlist_url = playlist_json.get('next')
    except requests.exceptions.RequestException as e:
        print(f"Error fetching playlist tracks: {e}")
        break
    except Exception as e:
        print(f"Unexpected error occurred: {e}")
        break

# Proceed with removing episodes only if we have valid tracks
if delete_episode_uri_list:
    print(f"Tracks to be removed: {delete_episode_uri_list}")  # Debugging output
    for i in range(0, len(delete_episode_uri_list), 100):  # API allows max 100 tracks per delete
        try:
            playlist_remove_url = f"https://api.spotify.com/v1/playlists/{buongiorno}/tracks"
            tracks_to_remove = [{'uri': uri} for uri in delete_episode_uri_list[i:i + 100]]
            print(f"Removing tracks: {tracks_to_remove}")  # Debugging output
            playlist_remove_response = requests.delete(
                playlist_remove_url,
                headers={
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {SPOTIFY_CLIENT_TOKEN}"
                },
                json={'tracks': tracks_to_remove}
            )
            playlist_remove_response.raise_for_status()
            print(f"Successfully removed tracks: {tracks_to_remove}")
        except requests.exceptions.RequestException as e:
            print(f"Error removing tracks: {e}")
            time.sleep(2)  # Retry after a delay
        except Exception as e:
            print(f"Unexpected error while removing tracks: {e}")
else:
    print("No tracks to remove from the playlist.")

# Get episodes from a list of shows
episodes_uri_list = []
shows_list = ["33YWzJrR8RkFFdocLDSc3c", "43A9fUmUbLYaHKSi1lAtn5", "0tbtlfiFG6pK91TiARb9vQ","1FaCiqGahURjjO42JOMiyd"]
for show in shows_list:
    try:
        episode_url = f"https://api.spotify.com/v1/shows/{show}/episodes"
        episode_response = requests.get(
            episode_url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {SPOTIFY_CLIENT_TOKEN}"
            }
        )
        episode_response.raise_for_status()

        episodes_json = episode_response.json()

        if episodes_json.get('items') and len(episodes_json['items']) > 0:
            episode_uri = episodes_json['items'][0]['uri']
            episodes_uri_list.append(episode_uri)
        else:
            print(f"No episodes found for show {show}. Skipping this show.")
            episodes_uri_list.append(None)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching episodes for show {show}: {e}")
        episodes_uri_list.append(None)
    except Exception as e:
        print(f"Unexpected error occurred while processing show {show}: {e}")
        episodes_uri_list.append(None)

print(episodes_uri_list)

# Add episodes to the Buongiorno playlist
for episode_uri in episodes_uri_list:
    if episode_uri is None:
        print("Skipping episode due to previous error.")
        continue
    try:
        playlist_add_url = f"https://api.spotify.com/v1/playlists/{buongiorno}/tracks"
        playlist_add_response = requests.post(
            playlist_add_url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {SPOTIFY_CLIENT_TOKEN}"
            },
            json={'uris': [episode_uri]}
        )
        playlist_add_response.raise_for_status()
        print(f"Added episode {episode_uri}")
    except requests.exceptions.RequestException as e:
        print(f"Error adding episode {episode_uri}: {e}")
        time.sleep(2)  # Retry after a delay

# Get 3 random tracks from the Dipinto_di_blu playlist
try:
    dipinto_url = f"https://api.spotify.com/v1/playlists/{dipinto_di_blu}/tracks"
    dipinto_response = requests.get(
        dipinto_url,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {SPOTIFY_CLIENT_TOKEN}"
        }
    )
    dipinto_response.raise_for_status()

    dipinto_json = dipinto_response.json()
    dipinto_tracks = [item['track']['uri'] for item in dipinto_json['items']]  # Get all track URIs

    # Select 3 random tracks
    random_tracks = random.sample(dipinto_tracks, 3)
    print(f"Selected random tracks: {random_tracks}")

except requests.exceptions.RequestException as e:
    print(f"Error fetching Dipinto_di_blu tracks: {e}")
    random_tracks = []  # If fetching fails, ensure the script continues

# Add the 3 random tracks to the Buongiorno playlist
for track_uri in random_tracks:
    try:
        playlist_add_url = f"https://api.spotify.com/v1/playlists/{buongiorno}/tracks"
        playlist_add_response = requests.post(
            playlist_add_url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {SPOTIFY_CLIENT_TOKEN}"
            },
            json={'uris': [track_uri]}
        )
        playlist_add_response.raise_for_status()
        print(f"Added random track {track_uri}")
    except requests.exceptions.RequestException as e:
        print(f"Error adding random track {track_uri}: {e}")
        time.sleep(2)  # Retry after a delay

print('Automation script has finished')
