# actions-test

The end goal is to create an automation to add everyday to a given playlist the new episodes of selected daily new podcasts and delete the old ones. The playlist, called Buongiorno, will then everyday only have 3 podcasts episodes which are the current day ones. A trigger has been added to the Google Home Mini device via the Google Home app so that whn hearing the command "Hey Google, buongiorno", it will automatically play the playlist and in the morning I can listen to 15 mins of my favorite news podcasts. 

The spotifyappervl8.py script works well locally and achieves exactly this objective. The first time it was run it prompted a Spotify browser window requesting user authentication. From then on it worked well using a cached or refreshed access token. It used to work while deployed in Heroku too, but since Heroku is no longer free it needs to be run on another platform. Github Actions was selected as the best as it's free and easy to use. The Actions workflow is set up with a yaml file that makes the main.py script run on a schedule via a cron job. However, an error always occurs while running the main.py script. After researching the error I found out that it's caused by the fact that Github Actions cannot prompt the Spotify user authentication window to get authorization to generate the first access token that will then be cached or refreshed and used for each successive run on the virtual machine. 

Currently the following are the potential solutions: 

- SOLUTION 1: 
  Run the spotifyappervl8.py script locally as it always works. 
  Verdict: NOT SUITABLE AS CRON JOB IS NEEDED
  
- SOLUTION 2: 
  Use sp_doc and sp_key cookies to generate an access token. The cookies last for 1 year and the token for 1 hour but it's re-generated after 1 hour by running the code if it expired. 
  
  Verdict: ONLY WORKS WITH WEB PLAYER SCOPE AND NOT FOR PRIVATE PLAYLIST EDITING (ERROR 403)
  
  Source: https://github.com/enriquegh/spotify-webplayer-token
  
- SOLUTION 3: 
  Use a cache handler in the code to generate first token locally and then store it as an environment variable to be called in the code
  
  Verdict: TO BE TESTED
  
  Source: https://github.com/spotipy-dev/spotipy/issues/632; https://github.com/spotipy-dev/spotipy/issues/852
  
- SOLUTION 4: 
  Create a selenium bot clicking through login and authenticating as if browser prompt was opening. Should work with GitHub actions 
  
  Verdict: TO BE TESTED
  
  Source: https://github.com/lukethacoder/spotify-playlist-backup
