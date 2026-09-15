# AGENTS.md

## Resumen

Scraper Python que extrae precios de plantas de APIs JSON de tiendas (Home Depot MX) y los carga en Postgres. Pipeline ETL: Extract → Transform → Load.

## Comandos

```bash
uv sync              # instalar dependencias
uv run main.py       # ejecutar pipeline completo
uv run pytest        # ejecutar tests (todos)
uv run pytest tests/test_models.py::test_create_product_with_required_fields  # test individual
uv run python -m load.connection  # crear tablas de BD (solo primera vez)
docker compose up -d # levantar Postgres 16
```

## Requisitos

- Python 3.14+ (`pyproject.toml` requiere `>=3.14`)
- `uv` como package manager
- `.env` con credenciales de BD — copiar de `.env.example`

## Arquitectura

```
extractors/  →  models.py  →  load/  →  Postgres
  (fetch+parse)   (Pydantic)   (SQLAlchemy)
```

- **Extractor** (`extractors/base.py`): clase abstracta con contrato `fetch()` + `parse()`. Cada tienda hereda de acá.
- **Product** (`models.py`): modelo Pydantic que valida y transporta datos entre capas.
- **DB models** (`load/db_models.py`): relación uno-a-muchos (`ProductModel` → `PriceHistoryModel`). El precio solo vive en `price_history`, no en `products`.
- **Load** (`load/load.py`): upsert por SKU + agrega historial de precios.

## CI

- GitHub Actions (`.github/workflows/scrape.yml`): cron diario 14:00 UTC (8AM CDMX) + manual dispatch.
- **No ejecuta tests** en CI — solo `uv run main.py`.
- Env vars `DATABASE_URL` y `HOME_DEPOT_API_URL` vienen de GitHub Secrets (Neon en prod).

## Convenciones

- Comentarios en español, código en inglés
- No hay linter/formatter/typechecker — seguir el estilo existente
- No confundir `models.py` (Pydantic) con `load/db_models.py` (SQLAlchemy)

## Gotchas

- `load/connection.py` levanta el engine y valida `DATABASE_URL` **al importar**, no solo en `__main__`. Si falta la var, `import load.load` falla con `ValueError`.
- `load/` no tiene `__init__.py` — funciona por `python -m` que agrega CWD a `sys.path`.
- `tienda_falsa.py` es mock, devuelve dicts en vez de `Product`, y tiene código ejecutable a nivel módulo.
- Home Depot API requiere `User-Agent` tipo navegador (hardcoded en `home_depot.py`).
