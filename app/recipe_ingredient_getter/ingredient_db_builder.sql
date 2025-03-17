
create table if not exists recipes (
    id integer primary key autoincrement,
    name text not null,
    full_text text not null,
    recipe_source text not null
);

create table if not exists ingredients (
  id integer primary key autoincrement,
  name text not null,
  recipe_id integer not null,
  unit_of_measurement text not null,
  amount float not null,
  category text not null,
  foreign key (recipe_id) references recipes(id)
);


  