import duckdb
from jinja2 import Template
import pandas as pd


def create_master_list():
    outputPath = "data/raw/master_list.csv"
    oscars_df = duckdb.sql(
        "SELECT film, year_film, year_ceremony from 'data/raw/the_oscar_award.csv' where canon_category='BEST PICTURE' AND year_ceremony > 2000 AND year_ceremony < 2026"
    ).df()
    oscars_df.to_csv(outputPath)
    return outputPath


def create_master_list_with_imdb():
    outputPath = "data/raw/master_list_imdb.csv"
    master_df = pd.DataFrame()
    for year in range(2001, 2026):
        release_start_date = f"{year-1}-01-01"
        release_end_date = f"{year}-03-01"
        sql_template = """
            SELECT film, year_film, year_ceremony, tmdb.imdb_id
            FROM 'data/raw/the_oscar_award.csv' AS oscars
            JOIN 'data/raw/TMDB_all_movies.csv' AS tmdb 
                ON oscars.film = tmdb.title
            WHERE canon_category = 'BEST PICTURE'
              AND year_ceremony = {{ year }}
              AND tmdb.release_date > DATE '{{ release_start_date }}'
              AND tmdb.release_date < DATE '{{ release_end_date }}'
              AND tmdb.imdb_id IS NOT NULL;
        """
        template = Template(sql_template)
        query = template.render(
            year=year,
            release_start_date=release_start_date,
            release_end_date=release_end_date,
        )
        bp_per_year = duckdb.sql(query).df()
        master_df = pd.concat([master_df, bp_per_year], ignore_index=True)
    master_df.to_csv(outputPath, index=False)
