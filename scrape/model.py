from dataclasses import dataclass

from scrape.DetailScraper import DetailScraper


@dataclass
class CompanyInvestment:
    update: str
    stage: str
    amount: str
    count: str

    @staticmethod
    def get_instance_by_scraper(ds: DetailScraper):
        __update = ds.investment['update']
        __stage = ds.investment['stage']
        __amount = ds.investment['amount']
        __count = ds.investment['count']
        return CompanyInvestment(__update, __stage, __amount, __count)


@dataclass
class CompanyRecruitDetail:
    href: str
    name: str
    incentive: str
    type: str


@dataclass
class CompanyRecruit:
    detail: list[CompanyRecruitDetail]

    @staticmethod
    def get_instance_by_scraper(ds: DetailScraper) -> 'CompanyRecruit':
        if ds.recruit is None:
            return CompanyRecruit([])
        __detail = [CompanyRecruitDetail(**d) for d in ds.recruit]
        return CompanyRecruit(__detail)


@dataclass
class Company:
    id: str
    name: str
    keyword: list[str]
    investment: CompanyInvestment
    recruit: CompanyRecruit

    @staticmethod
    def get_instance_by_href(href, ds: DetailScraper = None) -> 'Company':
        import urllib.parse
        __id = href.split('/')[-2]
        __name = urllib.parse.unquote(href.split('/')[-1])

        from scrape.DetailScraper import DetailScraper
        if ds is None:
            ds = DetailScraper(href)
        __keyword = ds.keywords
        __investment = CompanyInvestment.get_instance_by_scraper(ds)
        __recruit = CompanyRecruit.get_instance_by_scraper(ds)

        return Company(__id, __name, __keyword, __investment, __recruit)

    def href(self):
        import urllib.parse
        return str.join(self.id, urllib.parse.quote(self.name))


if __name__ == '__main__':
    from pprint import pprint
    from scrape import SCRAPE_DETAIL_SAMPLE_URL

    company = Company.get_instance_by_href(SCRAPE_DETAIL_SAMPLE_URL)
    pprint(company)
