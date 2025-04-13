
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

create table if not exists additional_items (
  id integer primary key autoincrement,
  name text not null,
  category text not null
);

create table if not exists shopping_list (
  id integer primary key autoincrement,
  name text not null,
  created_at timestamp default current_timestamp,
);

create table if not exists shopping_list_items (
  id integer primary key autoincrement,
  shopping_list_id integer not null,
  -- should be additional_item or recipe
  entry_type text not null,
  entry_id integer not null,
  removed integer not null default 0
)

create view if not exists combined_shopping_list_view as 
select 
  sl.id as shopping_list_id,
  sli.id as shopping_list_item_id,
  ig.category as category,
  ig.name as item_name,
  group_concat(re.name) as ingredient_recipes,
  ig.unit_of_measurement as unit_of_measurement,
  sum(ig.amount) as amount
from shopping_list sl
join shopping_list_items sli on sli.shopping_list_id = sl.id
join ingredients ig on sli.entry_id = ig.recipe_id
join recipe re on re.id = ig.recipe_id
where sli.entry_type = 'recipe' and sli.removed = 0
group by sl.id, ig.category, ig.name, ig.unit_of_measurement

union 

select
  sl.id as shopping_list_id,
  sli.id as shopping_list_item_id,
  it.category as category
  it.name as item_name
  'Non-Recipe Item' as ingredient_recipes, 
  'N/A' as unit_of_measurement,
  1 as amount
from shopping_list sl
join shopping_list_items sli on sli.shopping_list_id = sl.id
join additional_items it on sli.entry_id = it.id
where sli.entry_type = 'additional_item' and sli.removed = 0
;

