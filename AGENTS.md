# AGENTS.md

## Resumen

Scraper Python que extrae precios de plantas de APIs JSON de tiendas (Home Depot MX) y los carga en Postgres. Pipeline ETL: Extract → Transform → Load.

## Comandos

```bash
uv sync              # instalar dependencias
uv run main.py       # ejecutar pipeline completo
uv run pytest        # ejecutar tests
uv run python -m load.connection  # crear tablas de BD (solo primera vez)
docker compose up -d # levantar Postgres 16
```

## Requisitos

- Python 3.14+ (`.python-version`)
- `uv` como package manager
- `.env` con credenciales de BD — copiar de `.env.example`

## Arquitectura

```
extractors/  →  models.py  →  load/  →  Postgres
  (fetch+parse)   (Pydantic)   (SQLAlchemy)
```

- **Extractor** (`extractors/base.py`): clase abstracta que define el contrato `fetch()` + `parse()`. Cada tienda hereda de acá.
- **Product** (`models.py`): modelo Pydantic que valida y transporta datos entre capas. Es el "objeto de transferencia".
- **DB models** (`load/db_models.py`): modelos SQLAlchemy con relación uno-a-muchos (`ProductModel` → `PriceHistoryModel`).
- **Load** (`load/load.py`): upsert por SKU + agrega historial de precios.

## Convenciones

- Comentarios en español, código en inglés
- No hay linter/formatter/typechecker — seguir el estilo existente
- No confundir `models.py` (Pydantic) con `load/db_models.py` (SQLAlchemy)

## Gotchas

- `load/connection.py` solo crea tablas como `__main__`, no al importar
- `tienda_falsa.py` es mock, devuelve dicts en vez de `Product`
- SKU es unique en la BD — duplicados fallan
- Home Depot API requiere `User-Agent` tipo navegador
