import os
import sys
sys.path.append(os.path.abspath(".."))

import pytest
from fastapi.testclient import TestClient 

from src import crearApp
from src.database.conexion import Conexion

@pytest.fixture()
def app():

	app=crearApp()

	return app

@pytest.fixture()
def cliente(app):

	return TestClient(app)

@pytest.fixture()
def conexion(app):

	con=Conexion()

	con.c.execute("DELETE FROM usuarios")

	con.bbdd.commit()

	return con

@pytest.fixture()
def header_autorizado(cliente, conexion):

	cliente.post("/usuarios", json={"usuario":"nacho98","nombre":"Nacho","apellido1":"Dorado","apellido2":"Ruiz","fecha_nacimiento":"1998-02-16","ciudad":"Madrid","pais":"España","genero":"masculino","telefono":"611111111","correo":"natxo98@gmail.com", "contrasena":"987654321"})

	datos_form={"grant_type": "password", "username": "nacho98", "password": "987654321", "scope": "", "client_id": "", "client_secret": ""}

	contenido_token=cliente.post("/tokens", data=datos_form).json()

	token=contenido_token["access_token"]

	return {"Authorization": f"Bearer {token}"}

	