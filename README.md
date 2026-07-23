# Garden_Center_Spy

Scraper en Python para extraer precios de plantas desde endpoints JSON de Home Depot MX unicamente usando la libreria requests. Siendo un proyecto mvp.

## Objetivo

Obtener datos de precios de plantas para usarlos como base de un pipeline (extracción y posterior carga a base de datos).

## Requisitos

- Python 3.14+
- [uv](https://docs.astral.sh/uv/)
- Dependencias del `pyproject.toml` (`requests`)

## Instalación

```bash
uv sync
```

## Uso

Ejecuta el script principal:

```bash
uv run main.py
```

Actualmente incluye:
- Extracción de múltiples productos (`SpyPlant`)
- Extracción de producto individual (`SinglePlantSpy`)

## Estado del proyecto - Roadmap

MVP funcional. Próximos pasos:
   - [ ] Separar capas extract/transform/load 
   - [ ] Modelo de datos (Product) con validación
   - [ ] Normalizar estructura de salida entre extractores
   - [ ] Persistencia en Postgres
   - [ ] Soporte para más tiendas (Walmart, etc.)
   - [ ] API con FastAPI

## Arquitectura Planeada

Extract --> Transform --> Load --> Postgres --> API