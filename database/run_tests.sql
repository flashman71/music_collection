/* 
   Execute unit test suite
*/

SET FEEDBACK ON
SET SERVEROUTPUT ON SIZE 100000
 begin ut.run('music_adm.music_coll_test'); end;
/
