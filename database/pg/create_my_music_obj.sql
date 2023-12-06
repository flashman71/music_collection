
DROP VIEW IF EXISTS MUS_OWNER.MY_MUSIC;

DROP TABLE IF EXISTS MUS_OWNER.ALBUM CASCADE;
DROP TABLE IF EXISTS MUS_OWNER.ARTIST CASCADE;

DROP TYPE IF EXISTS COMMON.GENRE CASCADE;
DROP TYPE IF EXISTS COMMON.RECORD_TYPE CASCADE;


CREATE TYPE COMMON.GENRE AS ENUM('Punk','Hardcore','Metal','Post-Punk','New Wave','Electronic','Pub Rock','Rap','Reggae','Rock','Country','Funk','Blues','Pop','Jazz/Torch','Motown','Ska','Ska/Punk');

CREATE TYPE COMMON.RECORD_TYPE AS ENUM('EP','Album','Double Album','Multi-Album Set','Single','Compilation');

CREATE TABLE IF NOT EXISTS MUS_OWNER.ARTIST(ID           SERIAL  PRIMARY KEY,
                                            ARTIST_NAME  VARCHAR NOT NULL
                                            );

CREATE TABLE IF NOT EXISTS MUS_OWNER.ALBUM(ID                 SERIAL PRIMARY KEY,
                                           ARTIST_ID          INTEGER              NOT NULL,
                                           FULL_ALBUM_NAME    VARCHAR              NOT NULL,
                                           PART_ALBUM_NAME    VARCHAR              NOT NULL,
                                           TYPE               COMMON.RECORD_TYPE   NOT NULL,
                                           GENRE              COMMON.GENRE         NOT NULL,
                                           RELEASE_DATE       DATE                 NOT NULL,
                                           RECORD_OWNER       VARCHAR              NOT NULL,
                                           CONSTRAINT         FK_ARTIST_ID FOREIGN KEY (ARTIST_ID) REFERENCES MUS_OWNER.ARTIST(ID));
