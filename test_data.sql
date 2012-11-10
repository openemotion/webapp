-- passwords are the same as usernames, in hebrew
insert into users (name, password_hash) values ('אלי', '0b8c6b5219b0759f75ea34e0292ae2e0904e2924');
insert into users (name, password_hash) values ('אלון', 'a57868288d69faa25dec2185c470d22e45838e6e');

insert into conversations (talker_name, listener_name, title, first_message, status)
values ('אלי', null, 'שיתוף שקר כלשהו', 'סיפור כזה או אחר על החיים הקשים במדינת ישראל.', 'pending');

insert into conversations (talker_name, listener_name, title, first_message, status)
values ('אלי', 'אלון', 'שיתוף לדוגמא', 'עוד סיפור על חיים קשים.', 'active');

.quit