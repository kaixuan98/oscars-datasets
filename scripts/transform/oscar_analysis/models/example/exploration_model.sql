SELECT * from "data/raw/the_oscar_award.csv";
describe table "data/raw/TMDB_all_movies.csv";
describe table "data/raw/the_oscar_award.csv";

SELECT title from "data/raw/TMDB_all_movies.csv" where release_date > '2024-01-01' and release_date < '2025-01-01' ;

SELECT distinct * from "data/raw/the_oscar_award.csv" where year_ceremony = 2025 AND canon_category= 'BEST PICTURE' ; 

select * from 'data/raw/the_oscar_award.csv' where canon_category='BEST PICTURE' AND year_ceremony > 2000 AND year_ceremony < 2025;


SELECT title, budget, imdb_rating, imdb_votes from "data/raw/TMDB_all_movies.csv" where title in (SELECT distinct film from "data/raw/the_oscar_award.csv" where year_ceremony = 2025 AND canon_category= 'BEST PICTURE') AND release_date > '2024-01-01' AND release_date < '2025-03-01' AND vote_average > 0 ORDER BY vote_average DESC;