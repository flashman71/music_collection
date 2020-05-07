# music_collection
Builds tables of artists,releases,and tracks as well as similar artists

<BR>
This is for my personal use.  It's so I can learn some Python coding as well as Neo4j graph database.  
<BR>
Dependencies:<BR>
    
    Oracle database (actually any database, but the current database services are setup for Oracle)<BR>
    
    last.fm - Need an apikey to access web services<BR><BR>
    
Local requirements:
    artists.txt - This is a list of bands/musicians that will be queried against the last.fm database
                  to collect the information.

File system layout:<BR>
    
    music_collection---root directory, contains the .py files<BR>

                      --music_client.py - Main driver program<BR>

                      --music_database.py - Functions for accessing the database (inserts/updates)<BR>

                      --music_services.py - Web services used by the client program<BR>

                    |<BR>
                    <BR>
                    ->db<BR>
                    
                       --music_collection.rc - Configuration file with directory locations output, log, etc<BR>
                       
                       --artists.txt - List of bands/musicians, 1 per line<BR>
                       
                    |<BR>
                    
                    ->output  --Contains the exception list of bands/musicians that could not be found on last.fm<BR>
                    
                    |<BR>
                    
                    ->log  --Contains the exceptions when processing albums and tracks for bands/musicians<BR>
                    
