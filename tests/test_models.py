from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from models import Product


def test_create_product_with_required_fields():
    # Verifica que un producto se crea correctamente con todos los campos requeridos
    product = Product(
        name="Rosa",
        sku="HD-123",
        price=99.9,
        store="Home Depot MX",
        scraped_at=datetime.now(UTC),
    )
    assert product.name == "Rosa"
    assert product.price == 99.9


def test_optional_fields_default_to_none():
    # Verifica que los campos opcionales tienen valores por defecto correctos
    product = Product(
        name="Rosa",
        sku="HD-123",
        price=99.9,
        store="Home Depot MX",
        scraped_at=datetime.now(UTC),
    )
    assert product.currency == "MXN"
    assert product.description is None
    assert product.image_url is None
    assert product.product_url is None


def test_missing_required_fields_raises_validation_error():
    # Verifica que faltar campos requeridos lanza error de validación de Pydantic
    with pytest.raises(ValidationError):
        Product(price=99.9)


def test_invalid_price_type_raises_validation_error():
    # Verifica que un tipo incorrecto en price lanza error de validación
    with pytest.raises(ValidationError):
        Product(
            name="Rosa",
            sku="HD-123",
            price="no-numero",
            store="Home Depot MX",
            scraped_at=datetime.now(UTC),
        )
