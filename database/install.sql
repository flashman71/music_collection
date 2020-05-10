/*
   Executes database scripts
    MUSIC_COLL_TEST.pkg and run_tests.sql can be removed if utplsql package is not installed
*/
@CREATE_ROLE.sql
@CREATE_TABLES.tab
@CREATE_VIEWS.vw
@MUSIC_COLL_UTIL.pkg
@MUSIC_COLL_OPS.pkg
@MUSIC_COLL_TEST.pkg
@run_tests.sql
