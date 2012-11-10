-- passwords are the same as usernames, in hebrew
insert into users (name, password_hash) values ('אלי', '0b8c6b5219b0759f75ea34e0292ae2e0904e2924');
insert into users (name, password_hash) values ('גברי', '0a3c5c5ce69f4f0b47b12517eb929aeaa99d739f');

insert into conversations (talker_name, listener_name, title, status)
values ('גברי', null, 'שיתוף שקר כלשהו', 'pending');

insert into messages (conversation_id, author, text)
values (last_insert_rowid(), 'גברי', 'סיפור כזה או אחר על החיים הקשים במדינת ישראל.');

insert into conversations (talker_name, listener_name, title, status)
values ('אלי', 'גברי', 'שיתוף לדוגמא', 'active');

insert into messages (conversation_id, author, text)
values (last_insert_rowid(), 'אלי', 'עוד סיפור על חיים קשים.');

.quit