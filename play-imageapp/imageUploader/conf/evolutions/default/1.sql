# --- !Ups

create table images (
    id int primary key not null auto_increment,
    image BLOB not null
  ) ENGINE=InnoDB DEFAULT CHARSET=utf8;


# --- !Downs

drop table images;