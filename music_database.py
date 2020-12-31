import cx_Oracle
import psycopg2
import sys

# ************************************************************************************************
#   This file contains functions to access database objects
#   which are used to insert/update records in the database.
#   It is built for Oracle and Postgresql databases.
#   Connection can be made with username/password, or OS username can be used (eg, sqlplus /)
#   All return types are set as strings.
#   
# ************************************************************************************************

# Open a connection to the database
def connectDb(dbtype,dbhost,dbname,dbuser,dbpass,dbport):
  # Default return value to null
    con = ""

    if dbtype == 'ORACLE':
       if dbuser == '':
          creds = '/'
       else:
          creds = dbuser + "/" + dbpass + "@" + dbhost + ":" + dbport + "/" + dbname

       con = cx_Oracle.connect(creds)
    else:
       if dbtype == 'POSTGRES':
          con = psycopg2.connect(host=dbhost,dbname=dbname,user=dbuser,password=dbpass)

    return con

# Closed the database connection
def closeDb(con):
    print("Disconnecting")
    con.close()

# Insert/update artist
#   Dependency:
#              Oracle stored procedure
#               music_adm.music_coll_ops.ins_upd_artist
#              Postgres procedure
#               music.process_artists   
#   Input(s):
#            db type
#            db connection
#            artist_id --Artist ID if this is an existing record
#            artist_name --Band/musician name
#            artist_mbid --MBID from last.fm if an existing record
#            app_name --Calling application name, for logging
#   Return(s):
#             Artist Id
#             Status of database call -->0 for success, any other value is failure
#             Status Message -->Success or reason for failure
def process_artist(dbtype,conn,artist_id,artist_name,artist_mbid,app_name):
     with conn.cursor() as cursor:
                           if dbtype == 'ORACLE':
                               new_artist_id = cursor.var(str)
                               artist_status = cursor.var(str)
                               artist_message = cursor.var(str)
                               cursor.callproc('music_adm.music_coll_ops.ins_upd_artist',[artist_id,artist_name,artist_mbid,app_name,new_artist_id,artist_status,artist_message])
                           elif dbtype == 'POSTGRES':
                               cursor.execute("CALL music.process_artists(%s,%s,%s,null,null,null);",(artist_name,artist_mbid,app_name))
                               proc_results = cursor.fetchall()
                               new_artist_id = proc_results[0][0]
                               artist_status = proc_results[0][1]
                               artist_message = proc_results[0][2]
                               cursor.close()
 
                           conn.commit()

                           if dbtype == 'ORACLE':
                               return new_artist_id.getvalue(),artist_status.getvalue(),artist_message.getvalue()
                           elif dbtype == 'POSTGRES':
                               return str(new_artist_id),str(artist_status),str(artist_message)
                               

# Insert/update album
#   Dependency:
#              Oracle stored procedure
#               music_adm.music_coll_ops.ins_upd_album
#              Postgres procedure
#               music.process_albums   
#   Input(s):
#            db connection
#            album_id --Album ID if this is an existing record
#            artist_id --Artist ID if this is an existing record
#            album_name --Name of the album
#            app_name --Calling application name, for logging
#   Return(s):
#             Album Id
#             Status of database call -->0 for success, any other value is failure
#             Status Message -->Success or reason for failure
def process_album(dbtype,conn,album_id,artist_id,album_name,app_name):
     with conn.cursor() as cursor:
                           if dbtype == 'ORACLE':
                               new_album_id = cursor.var(str)
                               album_status = cursor.var(str)
                               album_message = cursor.var(str)
                               cursor.callproc('music_adm.music_coll_ops.ins_upd_album',[album_id,artist_id,album_name,app_name,new_album_id,album_status,album_message])
                           elif dbtype == 'POSTGRES':
                               cursor.execute("CALL music.process_albums(%s,%s,%s,null,null,null);",(artist_id,album_name,app_name))
                               proc_results = cursor.fetchall()
                               new_album_id = proc_results[0][0]
                               album_status = proc_results[0][1]
                               album_message = proc_results[0][2]
                               cursor.close()
 
                           conn.commit()
                              
                           if dbtype == 'ORACLE':
                               return new_album_id.getvalue(),album_status.getvalue(),album_message.getvalue()
                           elif dbtype == 'POSTGRES':
                               return str(new_album_id),str(album_status),str(album_message)

# Insert/update track
#   Dependency:
#              Oracle stored procedure
#               music_adm.music_coll_ops.ins_upd_track
#              Postgres procedure
#               music.process_tracks   
#   Input(s):
#            db connection
#            track_id --Track ID if this is an existing track
#            artist_id --Artist ID if this is an existing record
#            album_id --Album ID if this is an existing record
#            track_name --Name of the track
#            app_name --Calling application name, for logging
#   Return(s):
#             Track Id
#             Status of database call -->0 for success, any other value is failure
#             Status Message -->Success or reason for failure
def process_track(dbtype,conn,track_id,artist_id,album_id,track_name,app_name):
     with conn.cursor() as cursor:
                           if dbtype == 'ORACLE':
                               new_track_id = cursor.var(str)
                               track_status = cursor.var(str)
                               track_message = cursor.var(str)
                               cursor.callproc('music_adm.music_coll_ops.ins_upd_track',[track_id,artist_id,album_id,track_name,app_name,new_track_id,track_status,track_message])
                           elif dbtype == 'POSTGRES':
                               cursor.execute("CALL music.process_tracks(%s,%s,%s,null,null,null);",(album_id,track_name,app_name))
                               proc_results = cursor.fetchall()
                               new_track_id = proc_results[0][0]
                               track_status = proc_results[0][1]
                               track_message = proc_results[0][2]
                               cursor.close()
 
                           conn.commit()

                           if dbtype == 'ORACLE':
                               return new_track_id.getvalue(),track_status.getvalue(),track_message.getvalue()
                           elif dbtype == 'POSTGRES':
                               return str(new_track_id),str(track_status),str(track_message)

