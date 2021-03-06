/*
   Additonal views to simplify front end activity
*/

SET SERVEROUTPUT ON SIZE 100000

/* Collect all artists and associated albums */
CREATE OR REPLACE VIEW MUSIC_ADM.ARTISTS_ALBUMS_V
AS
SELECT MART.ID ARTIST_ID,
       MART.NAME,
       MART.MBID,
       MALB.ID  ALBUM_ID,
       MALB.ALBUM_NAME       
FROM   MUSIC_ADM.ARTISTS MART,
       MUSIC_ADM.ALBUMS  MALB
WHERE  MART.ID = MALB.ARTIST_ID
/

/* Collect all albums and associated tracks */
CREATE OR REPLACE VIEW MUSIC_ADM.ALBUMS_TRACKS_V
AS
SELECT MALB.ID ALBUM_ID,
       MALB.ALBUM_NAME,
       MATR.ID TRACK_ID,
       MATR.TRACK_NAME
FROM   MUSIC_ADM.ALBUMS MALB,
       MUSIC_ADM.TRACKS MATR
WHERE  MALB.ID = MATR.ALBUM_ID
/

/* Grant access to the roles */
GRANT SELECT ON MUSIC_ADM.ARTISTS_ALBUMS_V TO MUSIC_COLL_RO
/
GRANT SELECT ON MUSIC_ADM.ALBUMS_TRACKS_V TO MUSIC_COLL_RO
/

