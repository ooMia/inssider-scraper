class CompanyDB:

    def __del__(self):
        self.conn.close()

    def __init__(self, conn=None):
        import mysql.connector
        from db import MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE, MYSQL_PORT, MYSQL_HOST

        if conn:
            self.conn = conn
        else:
            self.conn = mysql.connector.connect(
                host=MYSQL_HOST,
                port=MYSQL_PORT,
                user=MYSQL_USER,
                password=MYSQL_PASSWORD,
                database=MYSQL_DATABASE
            )

        cursor = self.conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS company (
                id VARCHAR(255) PRIMARY KEY,
                name VARCHAR(255)
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS keyword (
                company_id VARCHAR(255),
                keyword VARCHAR(255),
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (company_id, keyword)
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS recruit (
                company_id VARCHAR(255),
                href VARCHAR(255),
                name VARCHAR(255),
                incentive VARCHAR(255),
                type VARCHAR(255),
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS investment (
                company_id VARCHAR(255),
                `update` VARCHAR(255),
                stage VARCHAR(255),
                amount VARCHAR(255),
                count VARCHAR(255),
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        self.conn.commit()

    from scrape.model import Company
    def store_company(self, comp: Company):
        # current timestamp

        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT INTO company (id, name) VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE name = VALUES(name)
            """,
            (comp.id, comp.name)
        )
        for keyword in comp.keyword:
            cursor.execute(
                """
                INSERT INTO keyword (company_id, keyword) VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE keyword = VALUES(keyword)
                """,
                (comp.id, keyword)
            )
        for detail in comp.recruit.detail:
            cursor.execute(
                """
                INSERT INTO recruit (company_id, href, name, incentive, type) VALUES (%s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE href = VALUES(href), name = VALUES(name),
                incentive = VALUES(incentive), type = VALUES(type)
                """,
                (comp.id, detail.href, detail.name, detail.incentive, detail.type)
            )
        cursor.execute(
            """
            INSERT INTO investment (company_id, `update`, stage, amount, count) VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE `update` = VALUES(`update`), stage = VALUES(stage),
            amount = VALUES(amount), count = VALUES(count)
            """,
            (comp.id, comp.investment.update, comp.investment.stage, comp.investment.amount, comp.investment.count)
        )
        self.conn.commit()

    def load_company_by_name(self, name: str) -> Company or None:
        from scrape.model import Company, CompanyRecruitDetail, CompanyRecruit, CompanyInvestment
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT * FROM company WHERE name = %s",
            (name,)
        )
        __comp = cursor.fetchone()
        comp_id = __comp[0]
        comp_name = __comp[1]
        cursor.execute(
            "SELECT keyword FROM keyword WHERE company_id = %s",
            (comp_id,)
        )
        keywords = cursor.fetchall()
        cursor.execute(
            "SELECT * FROM recruit WHERE company_id = %s",
            (comp_id,)
        )
        recruits = cursor.fetchall()
        cursor.execute(
            "SELECT * FROM investment WHERE company_id = %s",
            (comp_id,)
        )
        investment = cursor.fetchone()
        return Company(
            comp_id,
            comp_name,
            [keyword[0] for keyword in keywords],
            CompanyInvestment(investment[1], investment[2], investment[3], investment[4]),
            CompanyRecruit(
                [CompanyRecruitDetail(recruit[1], recruit[2], recruit[3], recruit[4]) for recruit in recruits]
            )
        )


if __name__ == "__main__":
    from scrape import SCRAPE_DETAIL_SAMPLE_URL
    from scrape.model import Company

    db = CompanyDB()
    db.store_company(
        Company.get_instance_by_href(SCRAPE_DETAIL_SAMPLE_URL)
    )
    comp = db.load_company_by_name("쿠팡")
    print(comp.id)
    print(comp.name)
    print(comp.investment)
    print(comp.recruit)
    print(len(comp.recruit.detail))
    print(len(comp.keyword))
