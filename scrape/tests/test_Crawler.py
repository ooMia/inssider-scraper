from scrape.Crawler import Crawler

crawler = Crawler()


def test_get_company_list():
    # assume first page ordered by its accumulated investment
    l = crawler.company_list_at(1)
    assert len(l) > 0
    assert l[0].get('href') is not None
    assert "쿠팡" == l[0].get('prod')
    assert "쿠팡" in l[0].get('corp')
