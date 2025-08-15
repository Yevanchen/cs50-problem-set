select * from flights
join airports on flights.origin_airport_id = airports.id

where year = 2023 and month = 7 and day >= 28
and airports.city = 'Fiftyville'



