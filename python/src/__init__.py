from fastapi import FastAPI

from .metadata.confmetadata import *
from .routers.inicio import router_inicio
from .routers.usuarios import router_usuarios

# Funcion para crear la app
def crearApp():

	app=FastAPI(title=TITULO,
				description=DESCRIPCION,
				version=VERSION,
				contact=CONTACTO,
				license_info=LICENCIA)

	app.include_router(router_inicio)
	app.include_router(router_usuarios)

	return app