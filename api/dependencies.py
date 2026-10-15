from load.connection import SessionLocal


def get_db():
    """Generador que cede (yield) una sesión de BD al request.

    Analogía: es como un mesero que te trae los cubiertos (la sesión),
    los usa durante tu comida (el request) y AL FINAL los recoge
    (finally: db.close()), sin importar si terminaste o hubo error.

    El `yield` es la clave: FastAPI ejecuta el código ANTES del yield,
    pasa el valor al endpoint, espera a que termine el request,
    y DESPUÉS ejecuta lo que va después del yield (el finally).
    """
    db = SessionLocal()
    try:
        yield db          # cede la sesión al endpoint
    finally:
        db.close()        # se cierra SIEMPRE, aunque haya excepción
