create table roles (
	role_id integer generated always as identity primary key,
	role_name varchar(100) not null
);