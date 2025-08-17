select distinct people2.name
from movies
join stars as stars1 on movies.id = stars1.movie_id
join people as people1 on stars1.person_id = people1.id

join stars as stars2 on movies.id = stars2.movie_id
join people as people2 on stars2.person_id = people2.id
where people1.name = 'Kevin Bacon' and people1.birth = '1958'