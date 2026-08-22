from extractors.home_depot import HomeDepot
from load.load import load_products

if __name__ == "__main__":
    home_depot = HomeDepot(
        "https://www.homedepot.com.mx/search/resources/api/v2/products?offset=0&limit=28&marketId=290&stLocId=12526&physicalStoreId=8774&orderBy=5&storeId=10351&catalogId=10101&profileName=HCL_V2_findProductsByCategoryWithPriceRangeSequenceTest&langId=-5&contractId=4000000000000000003&currency=MXN&categoryId=11156"
    )

    products = home_depot.run()
    load_products(products)
    print(f"Se han cargado {len(products)} productos")
