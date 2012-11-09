drop table if exists users;
drop table if exists conversations;
drop table if exists messages;

create table users (
  name string,
  password_hash string
);

create index users_name on users(name);

create table conversations (
  id integer primary key autoincrement,
  start_time datetime default current_timestamp,
  talker_name string,
  listener_name string,
  title string,
  first_message string
);

create index conversations_id on conversations(id);
create index conversations_sharer on conversations(talker_name);
create index conversations_facilitator on conversations(listener_name);

-- create table messages (
--   id integer primary key autoincrement,
--   conversation_id integer foreign key conversations(id),
--   author string not null,
--   text string not null
-- );

.quit