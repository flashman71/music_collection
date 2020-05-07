# music_collection
Builds tables of artists,releases,and tracks as well as similar artists


This is for my personal use.  It's so I can learn some Python coding as well as Neo4j graph database.  

Dependencies:
    
    Oracle database (actually any database, but the current database services are setup for Oracle)
    
    last.fm - Need an apikey to access web services
    
Local requirements:
    artists.txt - This is a list of bands/musicians that will be queried against the last.fm database
                  to collect the information.

File system layout:
    
    music_collection---root directory, contains the .py files

                      --music_client.py - Main driver program

                      --music_database.py - Functions for accessing the database (inserts/updates)

                      --music_services.py - Web services used by the client program

                    |
                    
                    ->db
                    
                       --music_collection.rc - Configuration file with directory locations output, log, etc
                       
                       --artists.txt - List of bands/musicians, 1 per line
                       
                    |
                    
                    ->output  --Contains the exception list of bands/musicians that could not be found on last.fm
                    
                    |
                    
                    ->log  --Contains the exceptions when processing albums and tracks for bands/musicians
                    
