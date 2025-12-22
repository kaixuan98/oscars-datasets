from scripts.extract import download_kaggle_dataset
from scripts.load import upload_to_s3
from scripts.scraper_source.awards.bafta import BaftaStrategy
from scripts.scraper_source.awards.critics_choice import CriticsChoiceStrategy
from scripts.scraper_source.awards.screen_actor_guild import ScreenActorGuildStrategy
from scripts.scraper_source.awards.venice_golden_lion import VeniceGoldenLionStrategy
from scripts.scraper_source.douban.scraper import DoubanScraper
from scripts.scraper_source.awards.award_scraper_context import (
    AwardScraperContext,
)
from scripts.scraper_source.awards.golden_globe import GoldenGlobeStrategy
from scripts.scraper_source.rotten_tomato.distribution_scraper import (
    run_distribution_scraper,
)
from scripts.scraper_source.letterbox.scraper import LetterboxScraper
from scripts.scraper_source.metacritic.scraper import MetacriticScraper
from scripts.scraper_source.rotten_tomato.scraper import RottenTomatoScraper
from scripts.utils import create_master_list, create_master_list_from_rt

# all dataset sources url
sources = ["alanvourch/tmdb-movies-daily-updates"]
# sources = ["unanimad/the-oscar-award"]

if __name__ == "__main__":
    # file_paths = download_kaggle_dataset(sources)
    # upload_to_s3(file_paths)
    # master_list_path = create_master_list()

    # letterbox
    # lb_scraper = LetterboxScraper()
    # lb_scraper.run()

    # rotten tomato
    # rt_scraper = RottenTomatoScraper()
    # rt_scraper.run()

    # metacritics
    # mc_scraper = MetacriticScraper()
    # mc_scraper.run()

    # douban
    # douban_scraper = DoubanScraper()
    # douban_scraper.run()

    # awards
    # golden_globe_context = AwardScraperContext(GoldenGlobeStrategy())
    # golden_globe_context.process_extraction()

    # critics_choice_context = AwardScraperContext(CriticsChoiceStrategy())
    # critics_choice_context.process_extraction()

    # sag_context = AwardScraperContext(ScreenActorGuildStrategy())
    # sag_context.process_extraction()

    # bafta_context = AwardScraperContext(BaftaStrategy())
    # bafta_context.process_extraction()

    venice_context = AwardScraperContext(VeniceGoldenLionStrategy())
    venice_context.process_extraction()

    # rotten tomato - distributors
    # create_master_list_from_rt()
    # run_distribution_scraper()
