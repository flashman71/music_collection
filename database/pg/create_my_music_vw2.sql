CREATE VIEW MUS_OWNER.MY_MUSIC2
AS
SELECT MAR.ARTIST_NAME,
       MAL.FULL_ALBUM_NAME,
       MAL.TYPE,
       MAL.GENRE,
       MAL.RELEASE_DATE
FROM   MUS_OWNER.ARTIST MAR,
       MUS_OWNER.ALBUM MAL
WHERE  MAR.ID = MAL.ARTIST_ID;
