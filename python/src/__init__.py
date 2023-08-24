from fastapi import FastAPI

from .metadata.confmetadata import *
from .routers.inicio import router_inicio

# Funcion para crear la app
def crearApp():

	app=FastAPI(title=TITULO,
				description=DESCRIPCION,
				version=VERSION,
				contact=CONTACTO,
				license_info=LICENCIA)

	app.include_router(router_inicio)

	return app