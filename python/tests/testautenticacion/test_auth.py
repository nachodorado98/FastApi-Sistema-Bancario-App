import pytest

def test_pagina_obtener_token_no_existe(cliente, conexion):

	form=datos_form={"grant_type": "password", "username": "nacho98", "password": "1235", "scope": "", "client_id": "", "client_secret": ""}

	respuesta=cliente.post("/tokens", data=form)

	contenido=respuesta.json()

	assert respuesta.status_code==401
	assert "detail" in contenido
	assert contenido["detail"]=="No existe el usuario"


@pytest.mark.parametrize(["contrasena"],
	[("1234567892",),("123456789",),("1234",),("12345678910",),("contrasena",)]
)
def test_pagina_obtener_token_contrasena_error(cliente, conexion, contrasena):

	cliente.post("/usuarios", json={"usuario":"nacho98","nombre":"Nacho","apellido1":"Dorado","apellido2":"Ruiz","fecha_nacimiento":"1998-02-16","ciudad":"Madrid","pais":"España","genero":"masculino","telefono":"611111111","correo":"natxo98@gmail.com", "contrasena":"contrasena1234"})
	
	form=datos_form={"grant_type": "password", "username": "nacho98", "password": contrasena, "scope": "", "client_id": "", "client_secret": ""}

	respuesta=cliente.post("/tokens", data=form)

	contenido=respuesta.json()

	assert respuesta.status_code==401
	assert "detail" in contenido
	assert contenido["detail"]=="La contraseña es erronea"


def test_pagina_obtener_token_autorizado(cliente, conexion):

	cliente.post("/usuarios", json={"usuario":"nacho98","nombre":"Nacho","apellido1":"Dorado","apellido2":"Ruiz","fecha_nacimiento":"1998-02-16","ciudad":"Madrid","pais":"España","genero":"masculino","telefono":"611111111","correo":"natxo98@gmail.com", "contrasena":"contrasena1234"})

	datos_form={"grant_type": "password", "username": "nacho98", "password": "contrasena1234", "scope": "", "client_id": "", "client_secret": ""}

	respuesta=cliente.post("/tokens", data=datos_form)

	contenido=respuesta.json()

	assert respuesta.status_code==200
	assert "access_token" in contenido
	assert "token_type" in contenido