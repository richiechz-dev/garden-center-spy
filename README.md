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
Home Depot / IKEA API  →  Extractor  →  Pydantic Model  →  SQLAlchemy  →  Postgres
      (JSON)              (fetch+parse)    (Product)        (ORM)        (persistencia)
```

1. **Extract**: consume endpoints JSON y extrae productos con precio válido
   (Home Depot: precio `Offer`; IKEA: `salesPrice.numeral`)
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
│   ├── home_depot.py    # Extractor para Home Depot MX
│   └── ikea.py          # Extractor para IKEA MX
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

Los precios se extraen únicamente de la sucursal de Hidalgo (`physicalStoreId=8774`) de Home Depot MX y de la categoría de IKEA configurada en `IKEA_CATEGORY`. Los precios pueden variar entre sucursales de Home Depot MX; esto es una limitación conocida del MVP, no soporta multi-sucursal aún.

### Categorías de IKEA

`IKEA_CATEGORY` es el código de categoría que se manda en el body del POST a la API de IKEA (campo `searchParameters.input`). Ejemplo para plantas naturales:

```bash
IKEA_CATEGORY=10779   # Plantas naturales
```

Otros ejemplos útiles:

```bash
IKEA_CATEGORY=31787   # Plantas naturales y macetas de exterior
IKEA_CATEGORY=700523  # Plantas de escritorio
IKEA_CATEGORY=700527  # Plantas con flores
```

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
- [x] Soporte para más tiendas (IKEA)
- [ ] API con FastAPI

## Nota sobre la fuente de datos

Este proyecto usa los endpoints JSON internos que las webs de Home Depot MX e IKEA MX consumen (descubiertos vía DevTools), no APIs públicas oficiales. Las URLs reales no se incluyen en el repo a propósito; se configuran en `.env`:

1. Abre la web de la tienda en tu navegador y abre DevTools (F12).
2. Ve a la pestaña **Network** y filtra por `Fetch/XHR`.
3. Navega a un listado de plantas (ej. categoría de plantas).
4. Copia la URL de la request que devuelve el JSON a `HOME_DEPOT_API_URL` / `IKEA_API_URL`.

Pueden dejar de funcionar si la tienda cambia su estructura interna.
