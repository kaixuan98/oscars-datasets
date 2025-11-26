from scripts.extract import download_kaggle_dataset
from scripts.load import upload_to_s3
from scripts.scraper_source.douban.scraper import DoubanScraper
from scripts.scraper_source.letterbox.scraper import LetterboxScraper
from scripts.scraper_source.metacritic.scraper import MetacriticScraper
from scripts.scraper_source.rotten_tomato.scraper import RottenTomatoScraper
from scripts.utils import create_master_list

# all dataset sources url
sources = ["alanvourch/tmdb-movies-daily-updates"]
# sources = ["unanimad/the-oscar-award"]

if __name__ == "__main__":
    # file_paths = download_kaggle_dataset(sources)
    # upload_to_s3(file_paths)
    # master_list_path = create_master_list()

    # letterbox
    lb_scraper = LetterboxScraper()
    lb_scraper.run()

    # rotten tomato
    # rt_scraper = RottenTomatoScraper()
    # rt_scraper.run()

    # douban_scraper = DoubanScraper()
    # douban_scraper.run()
    # metacritics
    # mc_scraper = MetacriticScraper()
    # mc_scraper.run()
