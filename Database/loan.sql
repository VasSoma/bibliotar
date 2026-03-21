create table loan (
    loan_id integer generated always as identity primary key,
    user_id integer not null,
    book_id integer not null,
    start_date date default current_date,
    due_date date not null,
    extension_count integer default 0 check (extension_count <= 2),
    foreign key (user_id) references users(user_id) on delete cascade,
    foreign key (book_id) references book(book_id) on delete restrict
);
