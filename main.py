from extractors.home_depot import HomeDepot

if __name__ == "__main__":
    home_depot = HomeDepot(
        "https://www.homedepot.com.mx/search/resources/api/v2/products?storeId=10351&searchTerm=kwPlantasComestibles&limit=28&offset=0&contractId=4000000000000000003&currency=MXN&langId=-5&marketId=21&stLocId=12605&extendedCatalog=false&marketOnly=true&physicalStoreId=8702&profileName=HCL_V2_findProductsBySearchTermWithPrice&selectedFacets=%5Bobject+Object%5D&minPrice=-1&maxPrice=-1&selectedPageOffset=0&orderBy=0"
    )

    products = home_depot.run()
    print(products)
