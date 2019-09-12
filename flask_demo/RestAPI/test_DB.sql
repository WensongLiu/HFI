use user_table_HFI;

CREATE TABLE `users` (
	user_ID int primary key  auto_increment unique Not null,
    public_user_ID varchar(256) unique not null,
    user_name varchar(100) unique not null,
    user_password varchar(256) not null,
    client_ID varchar(100) not null,
    public_client_ID varchar(256) not null,
    admin boolean DEFAULT false
);

select * from users;
