create database login;
use login;
create table slogin(
	username varchar(10),
    passw varchar(15));
    
insert into slogin VALUES('1BM20IS001','1BM20IS016');
insert into slogin VALUES('1BM20IS002','1BM20IS016');
insert into slogin VALUES('1BM20IS003','1BM20IS016');
insert into slogin VALUES('1BM20IS004','1BM20IS016');
insert into slogin VALUES('1BM20IS005','1BM20IS016');

select * from slogin;