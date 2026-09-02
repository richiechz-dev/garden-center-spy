# Garden Center Spy

[![Python 3.14+](https://img.shields.io/badge/python-3.14+-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/downloads/)
[![PostgreSQL](https://img.shields.io/badge/postgreSQL-16-4169E1.svg?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
![Run Status](https://github.com/richiechz-dev/vivero_spy/actions/workflows/scrape.yml/badge.svg)

Scraper en Python para extraer precios de plantas consumiendo APIs JSON públicas de tiendas (no scraping HTML). Pipeline ETL con persistencia en PostgreSQL.

## Tech Stack

- **Python 3.14+** — lenguaje principal
- **Pydantic** — validación y modelado de datos
- **SQLAlchemy** — ORM para persistencia en PostgreSQL
- **Requests** — consumo de APIs JSON
- **Docker Compose** — infraestructura de base de datos (desarrollo local)
- **Neon (PostgreSQL)** — base de datos persistente en producción
- **pytest** — tests unitarios

## Cómo funciona

```
Home Depot API  →  Extractor  →  Pydantic Model  →  SQLAlchemy  →  Postgres
   (JSON)         (fetch+parse)    (Product)        (ORM)        (persistencia)
```

1. **Extract**: consume el endpoint JSON y extrae productos con precio Offer
2. **Transform**: valida y modela cada producto con Pydantic
3. **Load**: upsert por SKU en PostgreSQL con historial de precios

## Automated Pipeline

El pipeline corre automáticamente todos los días vía GitHub Actions 
(`.github/workflows/scrape.yml`), conectado a una instancia persistente 
de PostgreSQL en [Neon](https://neon.com).

- **Schedule**: diario a las 8:00 AM (hora CDMX / 14:00 UTC)
- **Trigger manual**: disponible en la pestaña Actions del repo
- **Persistencia**: el historial de precios se acumula entre corridas en 
  `price_history`, habilitando análisis de tendencias a lo largo del tiempo

```
GitHub Actions (cron) → Extract/Transform/Load → Neon Postgres (persistente)
```
## Project Structure

```
vivero_spy/
├── extractors/
│   ├── base.py          # Clase abstracta Extractor
│   └── home_depot.py    # Extractor para Home Depot MX
├── load/
│   ├── connection.py    # Configuración de BD
│   ├── db_models.py     # Modelos SQLAlchemy
│   └── load.py          # Lógica de upsert
├── models.py            # Modelo Pydantic Product
├── main.py              # Punto de entrada
├── tests/               # Tests unitarios
├── docker-compose.yaml  # Postgres 16
└── .env.example         # Variables de entorno
```

## Objetivo

Obtener datos de precios de plantas para usarlos como base de un pipeline (extracción y posterior carga a base de datos).

## Alcance actual

Los precios se extraen únicamente de la sucursal de Hidalgo (`physicalStoreId=8774`). Los precios pueden variar entre sucursales de Home Depot MX; esto es una limitación conocida del MVP, no soporta multi-sucursal aún.

## Requisitos

- Python 3.14+
- [uv](https://docs.astral.sh/uv/)
  - Docker (para Postgres en local)

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

## Roadmap

- [x] Separar capas extract/transform/load
- [x] Modelo de datos (Product) con validación
- [x] Normalizar estructura de salida entre extractores
- [x] Persistencia en Postgres
- [x] Automatización con GitHub Actions (cron diario)
- [ ] Soporte para más tiendas (ikea, etc.)
- [ ] API con FastAPI

## Nota sobre la fuente de datos

Este proyecto usa el endpoint JSON interno que la web de Home Depot MX consume (descubierto vía DevTools), no una API pública oficial. Puede dejar de funcionar si Home Depot cambia su estructura interna.
