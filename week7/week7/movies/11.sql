select title
from movies
join ratings on movies.id = ratings.movie_id
join stars on movies.id = stars.movie_id
join people on stars.person_id = people.id
where people.name = 'Chadwick Boseman'
order by ratings.rating desc, movies.title
limit 5;