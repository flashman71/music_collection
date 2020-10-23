\connect musicdb svc_musicapp;

CREATE OR REPLACE PROCEDURE music.log_message(P_APP            VARCHAR,
                                              P_MESSAGE        VARCHAR,
                                              INOUT O_STATUS   INTEGER,
                                              INOUT O_MESSAGE  VARCHAR)
LANGUAGE plpgsql
AS $$
DECLARE
BEGIN
  O_STATUS  := 0;
  O_MESSAGE := 'SUCCESS';

  INSERT INTO music.app_messages_v(app_name,message)
  VALUES (P_APP, P_MESSAGE);
EXCEPTION
  WHEN OTHERS THEN
   O_STATUS  := -1;
   O_MESSAGE := 'EXCEPTION LOG_MESSAGE, Error ['||SQLSTATE||'], Message ['||SUBSTR(SQLERRM,1,100)||']';
END $$;;

CREATE OR REPLACE PROCEDURE music.process_artists(IN    P_ARTIST_NAME     VARCHAR, 
                                                  IN    P_MBID            VARCHAR, 
                                                  IN    P_APP             VARCHAR, 
                                                  INOUT O_ID              INTEGER, 
                                                  INOUT O_STATUS          INTEGER, 
                                                  INOUT O_MESSAGE         VARCHAR)
LANGUAGE plpgsql
AS $$
DECLARE
 V_RETURN_STATUS  INTEGER;
 V_RETURN_MESSAGE VARCHAR;
BEGIN
 O_ID      := -1;
 O_STATUS  := 0;
 O_MESSAGE := 'SUCCESS';

  INSERT INTO music.artists_$t(name,mbid,app_created)
  VALUES(P_ARTIST_NAME,P_MBID,P_APP) 
  ON CONFLICT ON CONSTRAINT artists_$t_name_mbid_key
  DO
   UPDATE SET    date_updated = current_timestamp, app_updated  = P_APP
   RETURNING ID INTO O_ID;
EXCEPTION
  WHEN OTHERS THEN
   O_STATUS  := -1;
   O_MESSAGE := 'EXCEPTION PROCESS_ARTISTS, Error ['||SQLSTATE||'], Message ['||SUBSTR(SQLERRM,1,100)||']';
   CALL music.log_message(P_APP,O_MESSAGE,V_RETURN_STATUS,V_RETURN_MESSAGE);
END $$;; 

CREATE OR REPLACE PROCEDURE music.process_albums(P_ARTIST_ID          INTEGER,
                                                 P_ALBUM_NAME         VARCHAR,
                                                 P_APP                VARCHAR,
                                                 INOUT O_ID           INTEGER,
                                                 INOUT O_STATUS       INTEGER,
                                                 INOUT O_MESSAGE      VARCHAR)
LANGUAGE plpgsql
AS $$
DECLARE
 V_RETURN_STATUS  INTEGER;
 V_RETURN_MESSAGE VARCHAR;
BEGIN
 O_ID      := -1;
 O_STATUS  := 0;
 O_MESSAGE := 'SUCCESS';

  INSERT INTO music.albums_$t(album_name,artist_id,app_created)
  VALUES (P_ALBUM_NAME,P_ARTIST_ID,P_APP)
  ON CONFLICT ON CONSTRAINT albums_$t_album_name_artist_id_key
  DO
   UPDATE SET album_name = P_ALBUM_NAME, artist_id = P_ARTIST_ID, app_updated = P_APP
   RETURNING ID INTO O_ID;
EXCEPTION
  WHEN OTHERS THEN
   O_STATUS  := -1;
   O_MESSAGE := 'EXCEPTION PROCESS_ALBUMS, Album Name ['||P_ALBUM_NAME||'], Error ['||SQLSTATE||'], Message ['||SUBSTR(SQLERRM,1,100)||']';
   CALL music.log_message(P_APP,O_MESSAGE,V_RETURN_STATUS,V_RETURN_MESSAGE);
END $$;;

CREATE OR REPLACE PROCEDURE music.process_tracks(P_ALBUM_ID           INTEGER,
                                                 P_TRACK_NAME         VARCHAR,
                                                 P_APP                VARCHAR,
                                                 INOUT O_ID           INTEGER,
                                                 INOUT O_STATUS       INTEGER,
                                                 INOUT O_MESSAGE      VARCHAR)
LANGUAGE plpgsql
AS $$
DECLARE
 V_RETURN_STATUS  INTEGER;
 V_RETURN_MESSAGE VARCHAR;
BEGIN
 O_ID      := -1;
 O_STATUS  := 0;
 O_MESSAGE := 'SUCCESS';

  INSERT INTO music.tracks_$t(track_name,album_id,app_created)
  VALUES (P_TRACK_NAME,P_ALBUM_ID,P_APP)
  ON CONFLICT ON CONSTRAINT tracks_$t_track_name_album_id_key
  DO
   UPDATE SET track_name = P_TRACK_NAME, album_id = P_ALBUM_ID, app_updated = P_APP
   RETURNING ID INTO O_ID;
EXCEPTION
  WHEN OTHERS THEN
   O_STATUS  := -1;
   O_MESSAGE := 'EXCEPTION PROCESS_TRACKS, Track ['||P_TRACK_NAME||'], Error ['||SQLSTATE||'], Message ['||SUBSTR(SQLERRM,1,100)||']';
   CALL music.log_message(P_APP,O_MESSAGE,V_RETURN_STATUS,V_RETURN_MESSAGE);
END $$;;

