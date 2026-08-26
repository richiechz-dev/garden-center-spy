# Garden_Center_Spy

Scraper en Python para extraer precios de plantas desde endpoints JSON de Home Depot MX. Proyecto MVP con pipeline ETL y persistencia en Postgres.

## Objetivo

Obtener datos de precios de plantas para usarlos como base de un pipeline (extracción y posterior carga a base de datos).

## Requisitos

- Python 3.14+
- [uv](https://docs.astral.sh/uv/)
- Docker (para Postgres)

## Instalación

```bash
uv sync
```

Copia y configura las variables de entorno:

```bash
cp .env.example .env
```

Levanta Postgres:

```bash
docker compose up -d
```

Crea las tablas de la BD (solo primera vez):

```bash
uv run python -m load.connection
```

## Uso

```bash
uv run main.py
```

## Estado del proyecto - Roadmap

- [x] Separar capas extract/transform/load
- [x] Modelo de datos (Product) con validación
- [x] Normalizar estructura de salida entre extractores
- [x] Persistencia en Postgres
- [ ] Soporte para más tiendas (Walmart, etc.)
- [ ] API con FastAPI

## Arquitectura

```
extractors/  →  models.py  →  load/  →  Postgres
  (fetch+parse)   (Pydantic)   (SQLAlchemy)
```
