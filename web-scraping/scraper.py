from urllib.error import HTTPError
import unicodedata
import pandas as pd
import math
from bs4 import BeautifulSoup
from datetime import datetime
import logging
import datetime
from tqdm import trange, tqdm
from selenium import webdriver


logging.basicConfig(level=logging.INFO)
LISTINGS_ON_PAGE_LIMIT = 10
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36',
    'Cookie': 'some cookie data'
}


class Scraper:
    def __init__(self, deal_type: str, property_type: str, max_search: int = 1):
        assert max_search > 0, "max_search should be positive"
        assert property_type in ['mieszkanie', 'dom'], "property_type should be 'mieszkanie' or 'dom'"
        assert deal_type in ['sprzedaz', 'wynajem'], "deal_type should be 'sprzedaz' or 'wynajem'"
        self.deal_type = deal_type
        self.property_type = property_type
        self.max_search = max_search
        self.pages_to_scrap = math.ceil(self.max_search / LISTINGS_ON_PAGE_LIMIT)
        self.current_time = datetime.datetime.now().strftime("%m_%d_%Y__%H_%M_%S")


    def scrap_listing(self, listing_element):
        listing_url = f"https://www.otodom.pl{listing_element.find_all('a', href=True)[0]['href']}"
        listing_property_dict = {}

        try:
            driver = webdriver.Chrome(r'C:\Users\Klaudia\.wdm\drivers\chromedriver\win32\105.0.5195\chromedriver.exe')
            driver.get(listing_url)
            requested_html = driver.page_source
            driver.quit()
        except HTTPError as e:
            print('Error code: ', e.code)
            print('Error reason: ', e.reason)
            print('Error headers: ', e.headers)
            return {}
        soup = BeautifulSoup(requested_html, features='html.parser')
        property_list = soup.find_all('div', {'class': 'css-1ccovha estckra9'})
        additional_features_list = soup.find_all('div', {'class': 'css-f45csg estckra9'})
        for property_element in property_list:
            property_elem_list = property_element.find_all('div', {'class': 'css-1qzszy5 estckra8'})
            key = property_elem_list[0].text
            value = property_elem_list[1].text
            listing_property_dict[key] = value
        for additional_element in additional_features_list:
            additional_elem_list = additional_element.find_all('div', {'class': ['css-1qzszy5 estckra8', 'css-1sqc82x estckra8']})
            key = additional_elem_list[0].text
            value = additional_elem_list[1].text
            listing_property_dict[key] = value

        return listing_property_dict

    def scrap_pages(self):
        result_list = []
        for current_page in range(1, self.pages_to_scrap + 1):
            logging.info(f'Page {current_page}/{self.pages_to_scrap}')
            url = f'https://otodom.pl/pl/oferty/{self.deal_type}/{self.property_type}/cala-polska?limit={LISTINGS_ON_PAGE_LIMIT}&page={current_page}'

            try:
                driver = webdriver.Chrome(r'C:\Users\Klaudia\.wdm\drivers\chromedriver\win32\105.0.5195\chromedriver.exe')
                driver.get(url)
                requested_html = driver.page_source
                driver.quit()
            except HTTPError as e:
                print('Error code: ', e.code)
                print('Error reason: ', e.reason)
                print('Error headers: ', e.headers)
                continue

            soup = BeautifulSoup(requested_html, features='html.parser')

            listings_div = soup.find_all('div', {'data-cy': "search.listing"})[1]

            listings_list = listings_div.find_all('li', {"class": "css-p74l73 es62z2j19"})

            print(len(listings_list))
            for listing_element in tqdm(listings_list):
                listing_property_dict = {}
                header_basic_info = [
                    unicodedata.normalize("NFKD", e.text) for e in
                    listing_element.find_all('span', {'class': 'css-s8wpzb eclomwz2'})]
                listing_property_dict['Cena'] = header_basic_info[0]
                listing_property_dict['Cena za metr kwadratowy'] = header_basic_info[1]
                listing_property_dict['Ilość pokoi'] = header_basic_info[2]
                listing_property_dict['Powierzchnia'] = header_basic_info[3]
                listing_property_dict['Lokalizacja'] = \
                    listing_element.find_all('p', {'class': 'css-80g06k es62z2j12'})[0].text
                listing_property_dict = {**listing_property_dict, **self.scrap_listing(listing_element)}
                result_list.append(listing_property_dict)
            df = pd.DataFrame(result_list).drop_duplicates()
            df.to_csv(f'../data/scrapped_raw_data_{self.current_time}_{current_page}.csv')