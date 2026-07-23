import requests

class SpyPlant:
    """
    Class for scraping dynamic pages for obtain prices of a page with multiple items 
    """
    def __init__(self, url) -> None:
        self.url = url
        self.data = {}

    def spy_on(self):

        """
        Method that create a request and save data raw
        """

        headers = {
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'es-419,es;q=0.9',
        }
        
        response = requests.get(self.url, headers=headers)

        response.raise_for_status()
        print(f"Se espio correctamente \n'status': {response.status_code}\n")

        self.data = response.json()

    def get_prices_data(self) -> list[dict]:
        """
        Method for obtain a prices dictionary

        return: list[dict]
        """
        prices_raw = self.data.get('contents', [])

        clean_list = []
        for product in prices_raw:

            plant_info = {
                'name': product.get('name'),
                'price_per_unit': float (product.get('x_prices.8702.mxn', 0))
            }
            clean_list.append(plant_info)

        return clean_list

class SinglePlantSpy(SpyPlant):
    """
    Class for scraping dynamic pages for obtain a price of one page
    """
    def get_prices_data(self) -> list[dict]:

        # import json
        # print(json.dumps(self.data, indent=2))
        product_raw = self.data.get('contents', [])

        clean_list = []
        for product in product_raw: 
            plant_info = {
                'name': product.get('name', 'No encontrado'),
                'price': float(product.get('x_prices.1165.mxn', 0))
            }
            clean_list.append(plant_info)

        return clean_list
        

                        