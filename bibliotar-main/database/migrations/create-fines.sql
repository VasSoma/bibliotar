create table fines (
	fine_id	 integer generated always as identity primary key,
	user_id integer not null,
	amount integer,
	is_paid boolean default false,
	date date,
	foreign key (user_id) references users(user_id)
)