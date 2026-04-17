create table users_roles (
	user_id integer references users(user_id),
	role_id integer references roles(role_id),
	
	primary key (user_id, role_id)
)