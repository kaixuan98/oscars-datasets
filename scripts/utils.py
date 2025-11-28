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


def create_master_list_from_rt():
    outputPath = "data/raw/master_list_rt.csv"
    sql_template = """
        SELECT film, year_film, year_ceremony, rt_url
        FROM 'data/scraped/rotten-tomato.csv'
    """
    template = Template(sql_template)
    query = template.render()
    master_df = duckdb.sql(query).df()
    master_df.to_csv(outputPath, index=False)
