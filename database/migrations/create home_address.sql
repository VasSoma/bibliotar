Create table home_address(
	address_id int PRIMARY KEY,
	user_id integer not null UNIQUE,
	county varchar(255),
	postal_code varchar(10),
	city varchar(255),
	street varchar(255),
	house_number varchar(10),
	foreign key (user_id) references users(user_id) ON DELETE CASCADE
);