from scrape.DetailScraper import DetailScraper

scraper = DetailScraper()


def test_investment():
    assert scraper.investment.get('update') is not None
    assert scraper.investment.get('stage') is not None
    assert scraper.investment.get('amount') is not None
    assert scraper.investment.get('count') is not None


def test_keywords():
    assert len(scraper.keywords) > 0


def test_recruit():
    # assume default url contains recruit data
    assert len(scraper.recruit) > 0
    assert scraper.recruit[0].get('href') is not None
    assert scraper.recruit[0].get('name') is not None
    assert scraper.recruit[0].get('incentive') is not None
    assert scraper.recruit[0].get('type') is not None
