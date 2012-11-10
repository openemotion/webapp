-- passwords are the same as usernames, in hebrew
insert into users (name, password_hash) values ('אלי', '0b8c6b5219b0759f75ea34e0292ae2e0904e2924');
insert into users (name, password_hash) values ('אלון', 'a57868288d69faa25dec2185c470d22e45838e6e');

insert into conversations (talker_name, listener_name, title, status)
values ('אלי', null, 'שיתוף שקר כלשהו', 'pending');

insert into messages (conversation_id, author, text)
values (last_insert_rowid(), 'אלי', 'סיפור כזה או אחר על החיים הקשים במדינת ישראל.');

insert into conversations (talker_name, listener_name, title, status)
values ('אלי', 'אלון', 'שיתוף לדוגמא', 'active');

insert into messages (conversation_id, author, text)
values (last_insert_rowid(), 'אלי', 'עוד סיפור על חיים קשים.');

.quit