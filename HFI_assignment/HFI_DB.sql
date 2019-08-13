use dataset_hfi;
SET SQL_SAFE_UPDATES = 0;

create table records(
	recordID int(16)  auto_increment unique Not null,
	memberID int(16) unsigned, 
	fullName varchar(50),  
    gender varchar(10), 
    referralDate varchar(20), 
    referralSource varchar(50), 
    clientReferredAs varchar(20),
    memberStatus varchar(200),
    programSought varchar(20)
);

create table admin(
	memberID int(16) primary key Not null,
	fullName varchar(50),  
    gender varchar(10), 
    referralDate varchar(20), 
    referralSource varchar(50), 
    clientReferredAs varchar(20),
    memberStatus varchar(200),
    programSought varchar(20)
);

insert into admin(memberID, fullName, gender, referralDate, referralSource, clientReferredAs, memberStatus, programSought)
values(1898693,"Wensong Liu","male","18/07/2019","admin","admin","admin","admin");

UPDATE `records`
SET `referralDate` = str_to_date( `referralDate`, '%m/%d/%Y' );


select * from admin;
select * from records;

select referralSource,count(1) from records group by referralSource;