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

	return Conexion()