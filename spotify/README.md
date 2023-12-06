=====================================================================
           Spotify Top Tracks Collector
=====================================================================

Purpose
     Collects data from Spotify API using Spotipy.  This will get the
     top tracks for short, medium, and long term, as defined by Spotify.

Requires
     Spotipy
     Spotify developer account
       --must create and get a client id and client secret
         these are needed to access your data
       --first time this is executed it will open a web page, defined by redirect url
         on the Spotify development account page, and will ask for the url to be pasted on the command line.
         It will only ask for this on the initial run

Output
     The data is collected into csv files, then converted to html pages.  There is a function available
     to transfer the data to a remote server.

