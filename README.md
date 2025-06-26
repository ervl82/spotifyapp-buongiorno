# buongiorno app

The end goal is to create an automation to add everyday to a given playlist the new episodes of selected daily new podcasts and delete the old ones. The playlist, called Buongiorno, will then everyday only have 3 podcasts episodes which are the current day ones. A trigger has been added to the Google Home Mini device via the Google Home app so that whn hearing the command "Hey Google, buongiorno", it will automatically play the playlist and in the morning I can listen to 15 mins of my favorite news podcasts. 

The spotifyappervl8.py script works well locally and achieves exactly this objective. The first time it was run it prompted a Spotify browser window requesting user authentication. From then on it worked well using a cached or refreshed access token. It used to work while deployed in Heroku too, but since Heroku is no longer free it needs to be run on another platform. Github Actions was selected as the best as it's free and easy to use. The Actions workflow is set up with a yaml file that makes the main.py script run on a schedule via a cron job. However, an error always occurs while running the main.py script. After researching the error I found out that it's caused by the fact that Github Actions cannot prompt the Spotify user authentication window to get authorization to generate the first access token that will then be cached or refreshed and used for each successive run on the virtual machine. 

[UPDATE] 
Using Iphone automations it's been possible to link the morning alarm clock to the playing of the Buongiorno automated playlist. Works like a charm, waking up everyday with the latest podcast news and a few randomly picked songs from other playlists instead of the annoying Iphone alarm sound

  
- SOLUTION TO FIRST TIME AUTHENTICATION FOR GITHUB ACTIONS VIRTUAL MACHINE: 
  Create a headless selenium bot clicking through login and authenticating as if browser prompt was opening. It works with GitHub actions. After first run a regresh token is generated and from then on that can be used indefintely to generate new access tokens on behalf of the user
  
  Verdict: IT WORKS! BEING USED RIGHT NOW
  
  Source: https://github.com/lukethacoder/spotify-playlist-backup
