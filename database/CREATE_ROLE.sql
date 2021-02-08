/* Drop and create the new user */
DROP USER MUSIC_ADM CASCADE
/

CREATE USER MUSIC_ADM IDENTIFIED BY MUSIC
/

/* Drop and create the roles for the new tables/views
     MUSIC_COLL_RO - Read only, can only select
     MUSIC_COLL_RW - Read/write - can select, insert, update
     MUSIC_COLL_RW - System administrator - can select, insert, update, delete
 */
DROP ROLE MUSIC_COLL_RO;
DROP ROLE MUSIC_COLL_RW;
DROP ROLE MUSIC_COLL_SA;

CREATE ROLE MUSIC_COLL_RO;

CREATE ROLE MUSIC_COLL_RW;

CREATE ROLE MUSIC_COLL_SA;

/* Grant low-end roles to each upper role in the hierarchy */
GRANT MUSIC_COLL_RO TO MUSIC_COLL_RW,MUSIC_COLL_SA;
GRANT MUSIC_COLL_RW TO MUSIC_COLL_SA;
