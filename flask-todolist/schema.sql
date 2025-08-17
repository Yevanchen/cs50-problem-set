create table users (
    id integer primary key autoincrement,
    username text not null unique,
    password text not null
);

create table todos (
    id integer primary key autoincrement,
    user_id integer not null,
    task_content text not null,
    status text not null,
    foreign key (user_id) references users(id)
);

