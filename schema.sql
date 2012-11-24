drop table if exists users;
drop table if exists conversations;
drop table if exists messages;

create table users (
  id integer primary key autoincrement,
  create_time datetime default current_timestamp,
  name string,
  password_hash string
);

create index users_id on users(id);
create index users_name on users(name);

create table conversations (
  id integer primary key autoincrement,
  start_time datetime default current_timestamp,
  talker_name string,
  listener_name string,
  title string,
  status string -- pending / active / closed
);

create index conversations_id on conversations(id);
create index conversations_sharer on conversations(talker_name);
create index conversations_facilitator on conversations(listener_name);

create table messages (
  id integer primary key autoincrement,
  conversation_id integer references conversations(id),
  timestamp datetime default current_timestamp,
  author string,
  type string,
  text string
);

create index messages_id on messages(id);
create index messages_conversation on messages(conversation_id);
