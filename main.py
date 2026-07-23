from package_scraping.spy_dynamic_pages import SinglePlantSpy, SpyPlant

def multiple_plants():
    
    url = "https://www.homedepot.com.mx/search/resources/api/v2/products?storeId=10351&searchTerm=kwPlantasComestibles&limit=28&offset=0&contractId=4000000000000000003&currency=MXN&langId=-5&marketId=21&stLocId=12605&extendedCatalog=false&marketOnly=true&physicalStoreId=8702&profileName=HCL_V2_findProductsBySearchTermWithPrice&selectedFacets=%5Bobject+Object%5D&minPrice=-1&maxPrice=-1&selectedPageOffset=0&orderBy=0"
    
    my_spy = SpyPlant(url)
    my_spy.spy_on()
    data = my_spy.get_prices_data()

    for plant in data:
        print(f"Nombre de la planta: {plant['name']}")
        print(f"Precio: ${plant['price_per_unit']} \n")

def one_plant():

    url = 'https://www.homedepot.com.mx/search/resources/api/v2/products?storeId=10351&id=20947&catalogId=10101&langId=-5&physicalStoreId=1165&profileName=HDM_V2_findProductByIds_IncludeZeroPrices&contractId=4000000000000000003&currency=MXN'

    spy_potus = SinglePlantSpy(url)
    spy_potus.spy_on()
    data = spy_potus.get_prices_data()

    for plant in data:
        print(f"Nombre: {plant['name']}")
        print(f"Precio: ${plant['price']} \n")

    

def main():

    multiple_plants()
    print("\n")
    one_plant()
    

if __name__ == "__main__":
    main()
