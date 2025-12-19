import wikipediaapi


def get_wikipedia_client(
    language="en", user_agent="OscarsAnalysis/1.0 (averychin7@gmail.com)"
):
    """
    Create and return a Wikipedia API client with specified language and user agent.
    """
    wiki = wikipediaapi.Wikipedia(
        user_agent=user_agent,
        language=language,
        extract_format=wikipediaapi.ExtractFormat.HTML,
    )
    return wiki
