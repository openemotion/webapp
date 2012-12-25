create table visits (
  conversation_id integer references conversations(id),
  user string,
  visit_date datetime,
  unique(conversation_id, user) on conflict replace
);

create index visits_unique on visits(conversation_id, user);
