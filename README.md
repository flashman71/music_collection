# music_collection
Builds tables of artists,releases,and tracks as well as similar artists


This is for my personal use.  It's so I can learn some Python coding as well as Neo4j graph database.  

Dependencies:
    
    Requires a database, currently setup for Oracle and Postgres.  
    My testing was done on a local install of Postgres, and a Docker version of Oracle.
    
    last.fm - Need an apikey to access web services
    
Python dependencies:
    neo4j
    pyscopg2
    cx_Oracle   

Local requirements:
    artists.txt - This is a list of bands/musicians that will be queried against the last.fm database
                  to collect the information. I use a minimal file for testing.

Install:
    last.fm -- Sign up for an API key, this should be stored in a local file.  Edit the configuration 
               file -- db/music_collection.rc --and add the location for the KEYFILE variable.
    Database --Oracle and Postgres are currently available.  In db/music_collection.rc, set the TYPE to ORACLE or POSTGRES.

               Oracle:
                 Note - utPlsql is used to run unit tests.  If this is not installed then run_tests.sql will fail.
                 Create a user, must have permission to create roles, views, tables, packages/procedures/functions.
                 As the user that was created, run database/install.sql
                 Oracle can use either a password or OS authentication, see music_database.py for connection.  
                 For Oracle authentication setup, consult the Oracle manuals.

               Postgres:
                 Change directory to database/pg
                 (Linux only) Run the following:
                   sudo -u postgres psql -f create_music_app.sql
                   sudo -u postgres psql -f music_app_procs.sql
                 (Windows) - You will need to run the 2 .sql scripts using pgadmin or psql manually.
                 
File system layout:
    
    music_collection---root directory, contains the .py files

                      --music_client.py - Main driver program

                      --music_database.py - Functions for accessing the database (inserts/updates)

                      --music_services.py - Web services used by the client program
                     
                      --music_similar.py - Uses Neo4j database, creates graphs of similar artists

                    |
                    
                    ->db
                    
                       --music_collection.rc - Configuration file with directory locations output, log, etc
                       
                       --artists.txt - List of bands/musicians, 1 per line
                       
                    |
                    
                    ->output  --Contains the exception list of bands/musicians that could not be found on last.fm
                    
                    |
                    
                    ->log  --Contains the exceptions when processing albums and tracks for bands/musicians
                    |
                    ->database --Contains database setup for Oracle and Postgres
