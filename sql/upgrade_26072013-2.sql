alter table conversations add show_on_landing boolean;
update conversations set show_on_landing = true where id in (5,17,20,26);
