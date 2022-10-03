from scraper import Scraper


def main():
    scraper = Scraper(
        property_type='mieszkanie',  # dom
        deal_type='sprzedaz',  # wynajem
        max_search=155393,
    )
    scraper.scrap_pages()


if __name__ == "__main__":
    main()
