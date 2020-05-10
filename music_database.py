import cx_Oracle
import sys

# ************************************************************************************************
#   This file contains functions to access Oracle stored procedures
#   which are used to insert/update records in the database.
#   Connection can be made with username/password, or OS username can be used (eg, sqlplus /)
#   
# ************************************************************************************************

# Open a connection to the database
def connectDb(creds):
    if creds == '':
       creds = '/'

    con = cx_Oracle.connect(creds)
    print("Connected")
    return con

# Closed the database connection
def closeDb(con):
    print("Disconnecting")
    con.close()

# Insert/update artist
#   Dependency:
#              Oracle stored procedure
#               music_app.music_coll_ops.ins_upd_artist
#   Input(s):
#            db connection
#            artist_id --Artist ID if this is an existing record
#            artist_name --Band/musician name
#            artist_mbid --MBID from last.fm if an existing record
#            app_name --Calling application name, for logging
#   Return(s):
#             Artist Id
#             Status of database call -->0 for success, any other value is failure
#             Status Message -->Success or reason for failure
def upsert_artist(conn,artist_id,artist_name,artist_mbid,app_name):
     with conn.cursor() as cursor:
                           new_artist_id = cursor.var(int)
                           artist_status = cursor.var(int)
                           artist_message = cursor.var(str)
                           cursor.callproc('music_app.music_coll_ops.ins_upd_artist',[artist_id,artist_name,artist_mbid,app_name,new_artist_id,artist_status,artist_message])
                           conn.commit()
                           return new_artist_id.getvalue(),artist_status.getvalue(),artist_message.getvalue()

# Insert/update album
#   Dependency:
#              Oracle stored procedure
#               music_app.music_coll_ops.ins_upd_album
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
def upsert_album(conn,album_id,artist_id,album_name,app_name):
     with conn.cursor() as cursor:
                           new_album_id = cursor.var(int)
                           album_status = cursor.var(int)
                           album_message = cursor.var(str)
                           cursor.callproc('music_app.music_coll_ops.ins_upd_album',[album_id,artist_id,album_name,app_name,new_album_id,album_status,album_message])
                           conn.commit()
                           return new_album_id.getvalue(),album_status.getvalue(),album_message.getvalue()

# Insert/update track
#   Dependency:
#              Oracle stored procedure
#               music_app.music_coll_ops.ins_upd_track
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
def upsert_track(conn,track_id,artist_id,album_id,track_name,app_name):
     with conn.cursor() as cursor:
                           new_track_id = cursor.var(int)
                           track_status = cursor.var(int)
                           track_message = cursor.var(str)
                           cursor.callproc('music_app.music_coll_ops.ins_upd_track',[track_id,artist_id,album_id,track_name,app_name,new_track_id,track_status,track_message])
                           conn.commit()
                           return new_track_id.getvalue(),track_status.getvalue(),track_message.getvalue()
