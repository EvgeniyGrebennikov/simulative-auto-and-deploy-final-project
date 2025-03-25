drop table if exists orders;
drop table if exists products;
drop table if exists categories;
drop table if exists receipts;
drop table if exists discounts;


create table if not exists categories (
	id serial primary key not null,
	name varchar (100) not null unique
);

create table if not exists products (
	id serial primary key not null,
	item varchar(250) not null unique,
	price numeric(10, 2) not null,
	category_id int not null,
	foreign key (category_id)
	references categories(id)
		on delete set null
	on update cascade
);


create table if not exists receipts (
	id serial primary key not null,
	doc varchar(16) not null unique
);


create table  if not exists discounts (
	id serial primary key not null,
	discount smallint unique
);


create table  if not exists orders (
	id serial primary key not null,
	date date not null,
	product_id int default null,
	amount smallint default null,
	discount_id smallint default null,
	doc_id bigint not null,
	foreign key (product_id) references products(id),
	foreign key (discount_id) references discounts(id),
	foreign key (doc_id) references receipts(id)
	on delete set null
	on update cascade
);
