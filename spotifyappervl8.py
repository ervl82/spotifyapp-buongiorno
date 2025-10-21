#THIS SCRIPT RUNS CORRECTLY LOCALLY AND WILL PROMPT A SPOTIFY BROWSER WINDOW TO AUTHENTICATE THE USER THE FIRST TIME IT'S RUN LOCALLY. FROM THEN ON IT WILL WORK REFRESHING THE ACCESS TOKEN
#THIS SCRIPT DOES NOT RUN CORRECTLY ON GITHUB ACTIONS WITH THE REST OF THE WORKFLOW IN THE REPO AS IT DOES NOT HAVE THE CAPABILITY TO OPEN THE BROWSER WINDOW TO AUTHENTICATE

#!/usr/bin/env python
# coding: utf-8


oauth_source ='https://www.section.io/engineering-education/spotify-python-part-1/'
docs = 'https://spotipy.readthedocs.io/en/2.19.0/?highlight=get_access_token#spotipy.oauth2.SpotifyOAuth.get_access_token'

import random  # To select random tracks
import requests  # For making HTTP requests
import json  # For handling JSON responses
import time  # For adding delays between retries
from secrets import *  # Assuming clientId, clientSecret, redirect_url2
import spotipy  # For interacting with the Spotify API
from spotipy.oauth2 import SpotifyOAuth  # For OAuth2 authenticatio


# Define the scope and authenticate
scope = "playlist-modify-private playlist-read-collaborative playlist-read-private playlist-modify-public user-library-read user-library-modify user-top-read user-read-recently-played"
sp_oauth = SpotifyOAuth(clientId, clientSecret, redirect_url2, scope=scope)

spotify_token = ""
token_info = sp_oauth.get_cached_token()

if token_info:
    print('Found cached token!')
    spotify_token = token_info['access_token']
    print('Access Token: ' + spotify_token)
else:
    print('Cached token not found. Getting Access Token')
    try:
        token_info = sp_oauth.get_access_token(as_dict=False)
        spotify_token = token_info['access_token']
        print('Access Token: ' + spotify_token)
    except Exception as e:
        print(f"Error getting access token: {e}")
        exit(1)

if spotify_token:
    print('Access token available! Trying to get user information...')
    try:
        sp = spotipy.Spotify(spotify_token)
        results = sp.current_user()
        print('User: ' + results['id'])
    except Exception as e:
        print(f"Error getting user information: {e}")
        exit(1)
else:
    print('No user information available')
    exit(1)

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
                "Authorization": f"Bearer {spotify_token}"
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
                    "Authorization": f"Bearer {spotify_token}"
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
                "Authorization": f"Bearer {spotify_token}"
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
                "Authorization": f"Bearer {spotify_token}"
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
            "Authorization": f"Bearer {spotify_token}"
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
                "Authorization": f"Bearer {spotify_token}"
            },
            json={'uris': [track_uri]}
        )
        playlist_add_response.raise_for_status()
        print(f"Added random track {track_uri}")
    except requests.exceptions.RequestException as e:
        print(f"Error adding random track {track_uri}: {e}")
        time.sleep(2)  # Retry after a delay

print('Automation script has finished')




