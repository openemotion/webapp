drop table if exists users;
drop table if exists conversations;
drop table if exists messages;

-- create table users (
--   id integer primary key autoincrement,
--   name string not null,
--   password string not null
-- )

create table conversations (
  id integer primary key autoincrement,
  start_time datetime default current_timestamp,
  author string,
  title string,
  first_message string
);

-- create table messages (
--   id integer primary key autoincrement,
--   conversation_id integer foreign key conversations(id),
--   author string not null,
--   text string not null
-- );

.quit