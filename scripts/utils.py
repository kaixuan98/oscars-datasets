import duckdb


def create_master_list():
    outputPath = "data/raw/master_list.csv"
    oscars_df = duckdb.sql(
        "SELECT film, year_film, year_ceremony from 'data/raw/the_oscar_award.csv' where canon_category='BEST PICTURE' AND year_ceremony > 2000 AND year_ceremony < 2026"
    ).df()
    oscars_df.to_csv(outputPath)
    return outputPath
