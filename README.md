# Garden_Center_Spy

Scraper en Python para extraer precios de plantas desde endpoints JSON de Home Depot MX. Proyecto MVP con pipeline ETL y persistencia en Postgres.

## Objetivo

Obtener datos de precios de plantas para usarlos como base de un pipeline (extracción y posterior carga a base de datos).

## Alcance actual
Los precios se extraen únicamente de la sucursal de Hidalgo (`physicalStoreId=8774`). Los precios pueden variar entre sucursales de Home Depot MX; esto es una limitación conocida del MVP, no soportar multi-sucursal aún.

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
- [ ] Soporte para más tiendas (ikea, etc.)
- [ ] API con FastAPI

## Arquitectura

```
extractors/  →  models.py  →  load/  →  Postgres
  (fetch+parse)   (Pydantic)   (SQLAlchemy)
```
## Nota sobre la fuente de datos
Este proyecto usa el endpoint JSON interno que la web de Home Depot MX consume (descubierto vía DevTools), no una API pública oficial. Puede dejar de funcionar si Home Depot cambia su estructura interna.