drop schema if exists library;
create schema library;
use library;

create table users(
	id int(5) not null primary key auto_increment,
	user_name varchar(20),
    user_password varchar(20),
    user_email varchar(40)
	);

create table day_to_day(
	id int(5) primary key not null auto_increment,
	book_name varchar(40),
    op_type int(10),
    days int(10)
	);

create table books(
	id int(5) primary key not null auto_increment,
	book_name varchar(40),
    book_code varchar(10),
    book_description varchar(40),
    book_price decimal(5, 2),
    book_author int(11),
    book_publisher int(11),
    book_category int(11)
	);


create table category(
	id int(11) primary key not null auto_increment,
    category_name varchar(50)
    );
    
create table publisher(
	id int(4) primary key not null auto_increment,
    publisher_name varchar(50)
    );
    
create table author(
	id int primary key not null auto_increment,
    author_name varchar(50)
    );