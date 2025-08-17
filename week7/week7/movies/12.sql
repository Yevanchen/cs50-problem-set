select title from movies
join stars on movies.id = stars.movie_id
join people on stars.person_id = people.id
where people.name = 'Bradley Cooper'
and title in (
    select title from movies
    join stars on movies.id = stars.movie_id
    join people on stars.person_id = people.id
    where people.name = 'Jennifer Lawrence'
);
