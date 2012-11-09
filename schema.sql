drop table if exists users;
drop table if exists conversations;
drop table if exists messages;

create table users (
  id integer primary key autoincrement,
  name string,
  password_hash string,
  is_facilitator boolean
);

create table conversations (
  id integer primary key autoincrement,
  start_time datetime default current_timestamp,
  author integer references users(id),
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