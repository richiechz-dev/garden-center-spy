from extractors.home_depot import HomeDepot


def test_parse_descarta_producto_without_offer_price():
    # Verifica que los productos sin precio Offer son descartados
    extractor = HomeDepot("url_false")

    raw_data = {
        "contents": [
            {
                "name": "Planta sin oferta",
                "partNumber": "123",
                "price": [
                    {"usage": "Display", "value": "100.0"}
                    # a propósito, NO hay ningún {"usage": "Offer", ...}
                ],
            }
        ]
    }

    resultado = extractor.parse(raw_data)

    assert len(resultado) == 0


def test_parse_producto_con_offer_price_valido():
    # Verifica que un producto con Offer price se parsea correctamente
    extractor = HomeDepot("url_false")
    raw_data = {
        "contents": [
            {
                "name": "Rosa Mini",
                "partNumber": "HD-456",
                "price": [{"usage": "Offer", "value": "150.0"}],
            }
        ]
    }
    resultado = extractor.parse(raw_data)

    assert len(resultado) == 1
    assert resultado[0].name == "Rosa Mini"
    assert resultado[0].price == 150.0
    assert resultado[0].sku == "HD-456"


def test_parse_contents_vacio():
    # Verifica que un contents vacío devuelve lista vacía
    extractor = HomeDepot("url_false")
    resultado = extractor.parse({"contents": []})
    assert resultado == []


def test_parse_sin_seo_href_ni_part_number():
    # Verifica que sin seo.href o partNumber, las URLs quedan en None
    extractor = HomeDepot("url_false")
    raw_data = {
        "contents": [
            {
                "name": "Planta",
                "price": [{"usage": "Offer", "value": "50.0"}],
            }
        ]
    }
    resultado = extractor.parse(raw_data)

    assert resultado[0].product_url is None
    assert resultado[0].image_url is None


def test_parse_multiples_productos_mixtos():
    # Verifica que solo pasan productos con Offer price, los demás se ignoran
    extractor = HomeDepot("url_false")
    raw_data = {
        "contents": [
            {
                "name": "Valida",
                "partNumber": "1",
                "price": [{"usage": "Offer", "value": "10"}],
            },
            {
                "name": "Sin Offer",
                "partNumber": "2",
                "price": [{"usage": "Display", "value": "20"}],
            },
            {
                "name": "Sin price",
                "partNumber": "3",
            },
        ]
    }
    resultado = extractor.parse(raw_data)

    assert len(resultado) == 1
    assert resultado[0].name == "Valida"


def test_parse_oferta_tipo_string():
    # Verifica que el precio Offer en formato string se convierte a float
    extractor = HomeDepot("url_false")
    raw_data = {
        "contents": [
            {
                "name": "Cactus",
                "partNumber": "C-789",
                "price": [{"usage": "Offer", "value": "200.00"}],
            }
        ]
    }
    resultado = extractor.parse(raw_data)

    assert resultado[0].price == 200.0
