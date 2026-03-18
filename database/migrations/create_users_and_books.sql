create table user (
	user_id integer generated always as identity primary key,
	name varchar(100) not null,
	address varchar(100) not null,
	phone_number  varchar(15) not null,
	password_hashed varchar(255) not null,
	role varchar(20) default 'user'
);

create table book (
	book_id integer generated always as identity primary key,
	title varchar(200) not null,
	isbn varchar(20) not null,
	quantity integer default 1,
	is_available boolean default true

)

