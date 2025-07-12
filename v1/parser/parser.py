from typing import Any

import requests
import json
from bs4 import BeautifulSoup

if __name__ == '__main__': from iparser import IParser
else: from .iparser import IParser


class ProductParser(IParser):
    def __init__(self, url: str):
        self.productUrl = url

    def parse(self, url: str) -> list[dict[str, str]]:
        # getting main page html
        mainPage: requests.Response = requests.get(url)
        if mainPage.status_code != 200: return None

        pd: dict[str, Any] = json.loads(mainPage.text)

        try:
            return [{
                'url': url,
                'name': pd['items']['item'][0]['item_marketing_name'],
                'description': pd['items']['item'][0]['description'],
                'calories': pd['items']['collective_nutrition']['nutrient_facts']['nutrient'][2]['value'],
                'fats': pd['items']['collective_nutrition']['nutrient_facts']['nutrient'][3]['value'],
                'carbs': pd['items']['collective_nutrition']['nutrient_facts']['nutrient'][4]['value'],
                'proteins': pd['items']['collective_nutrition']['nutrient_facts']['nutrient'][5]['value'],
                'unsaturated_fats': pd['items']['collective_nutrition']['nutrient_facts']['nutrient'][8]['value'],
                'sugar': pd['items']['collective_nutrition']['nutrient_facts']['nutrient'][7]['value'],
                'salt': pd['items']['collective_nutrition']['nutrient_facts']['nutrient'][6]['value'],
                'portion': pd['items']['collective_nutrition']['nutrient_facts']['nutrient'][0]['value'],
            }]
        except: return []


class MainMenuParser(IParser):
    def __init__(self, productLink: str, url: str):
        self.productLink = productLink
        self.mainMenuUrl: str = url

    def adaptLink(self, productId: str):
        return self.productLink.format(productId)

    def parse(self) -> list[dict[str, str]]:
        '''
            Parse all product links from mail menu and then parse
            all products using Product parser for every item
        '''

        # getting page data
        mainMenuResponse: requests.Response = requests.get(self.mainMenuUrl)
        if mainMenuResponse.status_code != 200: return None

        mainMenuPage: BeautifulSoup = BeautifulSoup(mainMenuResponse.text, 'lxml')

        # getting all elem from menu
        itemClass: str = 'cmp-category__item'
        linkObjName: str = 'cmp-category__item-link'

        items: list = mainMenuPage.find_all('li', class_=itemClass)

        result: list[dict[str, str]] = []

        # getting links for every product and parse each
        for item in items:
            data = item.find('a', class_=linkObjName)
            if not data: continue

            try:
                ''' FOR EXAMPLE
                    {
                        'product-category-e073fc1adf-626fa0f4e5': {
                            'linkPosition': 'fullmenu:ВОДА ГАЗОВАНА велика:200356:82', 
                            'xdm:linkURL': '/ua/uk-ua/product/7316.html', 
                            'dc:title': 'ВОДА ГАЗОВАНА велика'
                        }
                    }
                '''

                jsonData: dict[str, Any] = json.loads(
                    data.get('data-cmp-data-layer')
                )
                productJsonData: dict[str, Any] = jsonData.get(next(iter(jsonData))) # clear data
            except json.decoder.JSONDecodeError: continue

            # getting base product info and creating obj for every product
            linkPosition: str = productJsonData.get('linkPosition')

            if not linkPosition: continue

            # transform product url (adding main part)
            productId = linkPosition.split(':')[-2]
            productUrl = self.adaptLink(productId)

            # parse all product data
            productParser = ProductParser(productUrl)
            productParseResult: list[dict[str, str]] = productParser.parse(productUrl)
            if len(productParseResult) == 0: continue

            result.append(productParseResult[0])

        return result



if __name__ == '__main__':
    p = MainMenuParser(
        # 'https://www.mcdonalds.com/dnaapp/itemList?country=UA&language=uk&item={}()&nutrient_req=Y',
        'https://www.mcdonalds.com/dnaapp/itemList?country=UA&language=uk&showLiveData=true&item={}()&nutrient_req=Y',
        'https://www.mcdonalds.com/ua/uk-ua/eat/fullmenu.html'
    )
    for v in p.parse():
        print(v)