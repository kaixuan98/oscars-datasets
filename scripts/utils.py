import duckdb
from jinja2 import Template
import pandas as pd


def create_master_list():
    outputPath = "data/raw/master_list.csv"
    oscars_df = duckdb.sql(
        "SELECT film, year_film, year_ceremony from 'data/raw/the_oscar_award.csv' where canon_category='BEST PICTURE' AND year_ceremony > 1990 AND year_ceremony < 2026"
    ).df()
    oscars_df.to_csv(outputPath)
    return outputPath


def create_master_list_from_rt(file):
    outputPath = "data/raw/master_list_rt.csv"
    sql_template = """
        SELECT film, year_film, year_ceremony, rt_url
        FROM {{filename}}
    """
    template = Template(sql_template)
    query = template.render(filename=file)
    master_df = duckdb.sql(query).df()
    master_df.to_csv(outputPath, index=False)


def extract_all_years():
    all_years = [
        row[0]
        for row in duckdb.sql("""
            SELECT DISTINCT CAST(year_ceremony AS VARCHAR) AS year
            FROM 'data/raw/master_list.csv'
            WHERE year_ceremony IS NOT NULL
            ORDER BY CAST(year_ceremony AS INTEGER)
        """).fetchall()
    ]
    return all_years
