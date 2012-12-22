alter table conversations rename to conversations_old;

create table conversations (
  id integer primary key autoincrement,
  start_time datetime default current_timestamp,
  update_time datetime default current_timestamp,
  talker_name string,
  title string,
  status string -- pending / active
);

insert into conversations (id, start_time, talker_name, title, status)
select id, start_time, talker_name, title, status from conversations_old;

drop table conversations_old;

create index conversations_id on conversations(id);
create index conversations_talker on conversations(talker_name);

update conversations set update_time = (
    select timestamp from messages where messages.conversation_id = conversations.id
    order by timestamp desc
    limit 1
);
