from extractors.ikea import Ikea


def _item(product: dict) -> dict:
    return {"type": "PRODUCT", "product": product}


def test_parse_producto_valido():
    # Verifica que un producto válido se parsea correctamente
    extractor = Ikea("url_false", "10779")
    raw_data = {
        "items": [
            _item(
                {
                    "name": "EPIPREMNUM",
                    "typeName": "Planta en maceta",
                    "itemMeasureReferenceText": "15 cm",
                    "mainImageUrl": "https://www.ikea.com/mx/es/img.jpg",
                    "pipUrl": "https://www.ikea.com/mx/es/p/epipremnum-20488330/",
                    "itemNo": "20488330",
                    "salesPrice": {"currencyCode": "MXN", "numeral": 49.0},
                }
            )
        ]
    }
    resultado = extractor.parse(raw_data)

    assert len(resultado) == 1
    assert resultado[0].name == "EPIPREMNUM"
    assert resultado[0].sku == "20488330"
    assert resultado[0].price == 49.0
    assert resultado[0].currency == "MXN"
    assert resultado[0].store == "IKEA"


def test_parse_descarta_producto_sin_precio():
    # Verifica que los productos sin salesPrice/numeral son descartados
    extractor = Ikea("url_false", "10779")
    raw_data = {
        "items": [
            _item({"name": "Planta sin precio", "itemNo": "123", "typeName": "Planta"}),
            _item(
                {
                    "name": "Planta sin numeral",
                    "itemNo": "124",
                    "salesPrice": {"currencyCode": "MXN"},
                }
            ),
        ]
    }
    resultado = extractor.parse(raw_data)

    assert len(resultado) == 0


def test_parse_items_vacio():
    # Verifica que un items vacío devuelve lista vacía
    extractor = Ikea("url_false", "10779")
    resultado = extractor.parse({"items": []})

    assert resultado == []


def test_parse_ignora_item_sin_type_product():
    # Verifica que items que no son PRODUCT se ignoran
    extractor = Ikea("url_false", "10779")
    raw_data = {
        "items": [
            {
                "type": "PLANNER",
                "product": {
                    "name": "Planificador",
                    "itemNo": "999",
                    "salesPrice": {"numeral": 10.0},
                },
            },
            _item(
                {
                    "name": "Planta real",
                    "itemNo": "100",
                    "salesPrice": {"numeral": 20.0},
                }
            ),
        ]
    }
    resultado = extractor.parse(raw_data)

    assert len(resultado) == 1
    assert resultado[0].name == "Planta real"


def test_parse_sin_pip_url_ni_imagen():
    # Verifica que sin pipUrl o mainImageUrl, las URLs quedan en None
    extractor = Ikea("url_false", "10779")
    raw_data = {
        "items": [_item({"name": "Planta", "itemNo": "200", "salesPrice": {"numeral": 50.0}})]
    }
    resultado = extractor.parse(raw_data)

    assert resultado[0].product_url is None
    assert resultado[0].image_url is None


def test_parse_mapea_campos_normalizados():
    # Verifica el mapeo de scientific_name, category y measurement
    extractor = Ikea("url_false", "10779")
    raw_data = {
        "items": [
            _item(
                {
                    "name": "MONSTERA DELICIOSA",
                    "typeName": "Planta en maceta",
                    "itemMeasureReferenceText": "25 cm",
                    "itemNo": "50547130",
                    "salesPrice": {"currencyCode": "MXN", "numeral": 299.0},
                }
            )
        ]
    }
    resultado = extractor.parse(raw_data)

    assert resultado[0].scientific_name == "MONSTERA DELICIOSA"
    assert resultado[0].category == "Planta en maceta"
    assert resultado[0].measurement == "25 cm"
    assert resultado[0].description is None