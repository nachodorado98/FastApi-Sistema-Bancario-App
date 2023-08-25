import pytest

@pytest.mark.parametrize(["usuario"],
	[
		({"usuario":"nacho98","nombre":"Nacho","apellido1":"Dorado","apellido2":"Ruiz","fecha_nacimiento":"199802-16","ciudad":"Madrid","pais":"España","genero":"masculino","telefono":"612345789","correo":"natxo98@gmail.com", "contrasena":"12345678"},),
		({"usuario":"nacho98","nombre":"Nacho","apellido1":"Dorado","apellido2":"Ruiz","fecha_nacimiento":"16/02/1998","ciudad":"Madrid","pais":"España","genero":"masculino","telefono":"612345789","correo":"natxo98@gmail.com", "contrasena":"12345fdfdg"},),
		({"usuario":"nacho98","nombre":"Nacho","apellido1":"Dorado","apellido2":"Ruiz","fecha_nacimiento":"1998-02-16","ciudad":"Madrid","pais":"España","genero":"hombre","telefono":"612345789","correo":"natxo98@gmail.com", "contrasena":"12345fdfdhfg"},),
		({"usuario":"nacho98","nombre":"Nacho","apellido1":"Dorado","apellido2":"Ruiz","fecha_nacimiento":"1998-02-16","ciudad":"Madrid","pais":"España","genero":"mujer","telefono":"612345789","correo":"natxo98@gmail.com", "contrasena":"1234567gfdhfdh8"},),
		({"usuario":"nacho98","nombre":"Nacho","apellido1":"Dorado","apellido2":"Ruiz","fecha_nacimiento":"1998-02-16","ciudad":"Madrid","pais":"España","genero":"masculino","telefono":"811111111","correo":"natxo98@gmail.com", "contrasena":"contrasena1234"},),
		({"usuario":"nacho98","nombre":"Nacho","apellido1":"Dorado","apellido2":"Ruiz","fecha_nacimiento":"1998-02-16","ciudad":"Madrid","pais":"España","genero":"masculino","telefono":"61234","correo":"natxo98@gmail.com", "contrasena":"12345678"},),
		({"usuario":"nacho98","nombre":"Nacho","apellido1":"Dorado","apellido2":"Ruiz","fecha_nacimiento":"2000-02-16","ciudad":"Madrid","pais":"España","genero":"masculino","telefono":"612aaa789","correo":"natxo98@gmail.com", "contrasena":"12345fdfdg"},),
		({"usuario":"nacho98","nombre":"Nacho","apellido1":"Dorado","apellido2":"Ruiz","fecha_nacimiento":"1998-02-16","ciudad":"Madrid","pais":"España","genero":"MASCULINO","telefono":"612345789","correo":"@gmail.com", "contrasena":"12345fdfdhfg"},),
		({"usuario":"nacho98","nombre":"Nacho","apellido1":"Dorado","apellido2":"Ruiz","fecha_nacimiento":"1998-02-16","ciudad":"Madrid","pais":"España","genero":"FEMENINO","telefono":"612345789","correo":"natxo98gmail.com", "contrasena":"1234567gfdhfdh8"},),
		({"usuario":"nacho98","nombre":"Nacho","apellido1":"Dorado","apellido2":"Ruiz","fecha_nacimiento":"1998-02-16","ciudad":"Madrid","pais":"España","genero":"masculino","telefono":"611111111","correo":"natxo98@gmail", "contrasena":"contrasena1234"},),
		({"usuario":"nacho98","nombre":"Nacho","apellido1":"Dorado","apellido2":"Ruiz","fecha_nacimiento":"1998-02-16","ciudad":"Madrid","pais":"España","genero":"masculino","telefono":"612345789","correo":"natxo98@.com", "contrasena":"12345678"},),
		({"usuario":"nacho98","nombre":"Nacho","apellido1":"Dorado","apellido2":"Ruiz","fecha_nacimiento":"2000-02-16","ciudad":"Madrid","pais":"España","genero":"masculino","telefono":"612345789","correo":"natxo98@gmail.ese", "contrasena":"12345fdfdg"},),
		({"usuario":"nacho98","nombre":"Nacho","apellido1":"Dorado","apellido2":"Ruiz","fecha_nacimiento":"1998-02-16","ciudad":"Madrid","pais":"España","genero":"MASCULINO","telefono":"612345789","correo":"natxo98@gmail.com", "contrasena":"123456789"},),
		({"usuario":"nacho98","nombre":"Nacho","apellido1":"Dorado","apellido2":"Ruiz","fecha_nacimiento":"1998-02-16","ciudad":"Madrid","pais":"España","genero":"FEMENINO","telefono":"612345789","correo":"natxo98@gmail.com", "contrasena":"12345"},),
		({"usuario":"nacho98","nombre":"Nacho","apellido1":"Dorado","apellido2":"Ruiz","fecha_nacimiento":"1998-02-16","ciudad":"Madrid","pais":"España","genero":"masculino","telefono":"611111111","correo":"natxo98@gmail.com", "contrasena":"contrase na1234"},)
	]
)
def test_pagina_agregar_usuario_incorrecto(cliente, conexion, usuario):

	respuesta=cliente.post("/usuarios", json=usuario)

	contenido=respuesta.json()

	assert respuesta.status_code==422
	assert not "mensaje" in contenido
	assert not "usuario" in contenido

	conexion.c.execute("SELECT * FROM usuarios")

	assert len(conexion.c.fetchall())==0

def test_pagina_agregar_usuario_existente(cliente, conexion):

	conexion.insertarUsuario("nacho98", "Nacho", "Dorado", "Ruiz", "1998-02-16", "Madrid", "España", "Masculino", "612345789", "natxo98@gmail.com", "1234")

	conexion.c.execute("SELECT * FROM usuarios")

	assert len(conexion.c.fetchall())==1

	respuesta=cliente.post("/usuarios", json={"usuario":"nacho98","nombre":"Nacho","apellido1":"Dorado","apellido2":"Ruiz","fecha_nacimiento":"1998-02-16","ciudad":"Madrid","pais":"España","genero":"masculino","telefono":"611111111","correo":"natxo98@gmail.com", "contrasena":"contrasena1234"})

	contenido=respuesta.json()

	assert respuesta.status_code==400
	assert "detail" in contenido

	conexion.c.execute("SELECT * FROM usuarios")

	assert len(conexion.c.fetchall())==1

def test_pagina_agregar_usuario(cliente, conexion):

	respuesta=cliente.post("/usuarios", json={"usuario":"nacho98","nombre":"Nacho","apellido1":"Dorado","apellido2":"Ruiz","fecha_nacimiento":"1998-02-16","ciudad":"Madrid","pais":"España","genero":"masculino","telefono":"611111111","correo":"natxo98@gmail.com", "contrasena":"contrasena1234"})

	contenido=respuesta.json()

	assert respuesta.status_code==201
	assert "mensaje" in contenido
	assert "usuario" in contenido
	assert "usuario" in contenido["usuario"]
	assert "nombre" in contenido["usuario"]
	assert "saldo" in contenido["usuario"]

	conexion.c.execute("SELECT * FROM usuarios")

	assert len(conexion.c.fetchall())==1

def test_pagina_agregar_varios_usuarios(cliente, conexion):

	cliente.post("/usuarios", json={"usuario":"nacho98","nombre":"Nacho","apellido1":"Dorado","apellido2":"Ruiz","fecha_nacimiento":"1998-02-16","ciudad":"Madrid","pais":"España","genero":"masculino","telefono":"611111111","correo":"natxo98@gmail.com", "contrasena":"contrasena1234"})
	cliente.post("/usuarios", json={"usuario":"nacho99","nombre":"Nacho","apellido1":"Dorado","apellido2":"Ruiz","fecha_nacimiento":"1998-02-16","ciudad":"Madrid","pais":"España","genero":"masculino","telefono":"611111111","correo":"natxo98@gmail.com", "contrasena":"contrasena1234"})
	cliente.post("/usuarios", json={"usuario":"nacho989","nombre":"Nacho","apellido1":"Dorado","apellido2":"Ruiz","fecha_nacimiento":"1998-02-16","ciudad":"Madrid","pais":"España","genero":"masculino","telefono":"611111111","correo":"natxo98@gmail.com", "contrasena":"contrasena1234"})
	cliente.post("/usuarios", json={"usuario":"nacho998","nombre":"Nacho","apellido1":"Dorado","apellido2":"Ruiz","fecha_nacimiento":"1998-02-16","ciudad":"Madrid","pais":"España","genero":"masculino","telefono":"611111111","correo":"natxo98@gmail.com", "contrasena":"contrasena1234"})

	conexion.c.execute("SELECT * FROM usuarios")

	assert len(conexion.c.fetchall())==4

def test_pagina_obtener_usuarios_no_existentes(cliente, conexion):

	respuesta=cliente.get("/usuarios")

	contenido=respuesta.json()

	assert respuesta.status_code==404
	assert "detail" in contenido

def test_pagina_obtener_usuarios_existentes(cliente, conexion):

	cliente.post("/usuarios", json={"usuario":"nacho98","nombre":"Nacho","apellido1":"Dorado","apellido2":"Ruiz","fecha_nacimiento":"1998-02-16","ciudad":"Madrid","pais":"España","genero":"masculino","telefono":"611111111","correo":"natxo98@gmail.com", "contrasena":"contrasena1234"})
	cliente.post("/usuarios", json={"usuario":"nacho99","nombre":"Nacho","apellido1":"Dorado","apellido2":"Ruiz","fecha_nacimiento":"1998-02-16","ciudad":"Madrid","pais":"España","genero":"masculino","telefono":"611111111","correo":"natxo98@gmail.com", "contrasena":"contrasena1234"})
	cliente.post("/usuarios", json={"usuario":"nacho989","nombre":"Nacho","apellido1":"Dorado","apellido2":"Ruiz","fecha_nacimiento":"1998-02-16","ciudad":"Madrid","pais":"España","genero":"masculino","telefono":"611111111","correo":"natxo98@gmail.com", "contrasena":"contrasena1234"})
	cliente.post("/usuarios", json={"usuario":"nacho998","nombre":"Nacho","apellido1":"Dorado","apellido2":"Ruiz","fecha_nacimiento":"1998-02-16","ciudad":"Madrid","pais":"España","genero":"masculino","telefono":"611111111","correo":"natxo98@gmail.com", "contrasena":"contrasena1234"})

	respuesta=cliente.get("/usuarios")

	contenido=respuesta.json()

	assert respuesta.status_code==200
	assert len(contenido)==4

	for usuario in contenido:

		assert "usuario" in usuario


@pytest.mark.parametrize(["token"],
	[("token",), ("dgfdkjg89e5yujgfkjgdf",), ("nacho98",), ("amanditaa",), ("1234",)]
)
def test_pagina_obtener_datos_usuario_no_autenticado(cliente, token):

	header={"Authorization": f"Bearer {token}"}

	respuesta=cliente.get("/usuarios/me", headers=header)

	contenido=respuesta.json()

	assert respuesta.status_code==401
	assert "detail" in contenido

@pytest.mark.parametrize(["usuario", "contrasena"],
	[
		("nacho98", "123456aa7891"),
		("nacho98", "qwertyuiop"),
		("amanda99", "1q2w3e4r5t6y7u"),
	]
)
def test_pagina_obtener_datos_usuario_autenticado(cliente, conexion, usuario, contrasena):

	cliente.post("/usuarios", json={"usuario":usuario,"nombre":"Nacho","apellido1":"Dorado","apellido2":"Ruiz","fecha_nacimiento":"1998-02-16","ciudad":"Madrid","pais":"España","genero":"masculino","telefono":"611111111","correo":"natxo98@gmail.com", "contrasena":contrasena})

	datos_form={"grant_type": "password", "username": usuario, "password": contrasena, "scope": "", "client_id": "", "client_secret": ""}

	contenido_token=cliente.post("/tokens", data=datos_form).json()

	token=contenido_token["access_token"]

	header={"Authorization": f"Bearer {token}"}

	respuesta=cliente.get("/usuarios/me", headers=header)

	contenido=respuesta.json()

	assert respuesta.status_code==200
	assert "usuario" in contenido
	assert contenido["usuario"]==usuario
	assert "nombre" in contenido
	assert "apellido1" in contenido
	assert "apellido2" in contenido
	assert "fecha_nacimiento" in contenido
	assert "ciudad" in contenido
	assert "pais" in contenido
	assert "genero" in contenido
	assert "telefono" in contenido
	assert "correo" in contenido
	assert "contrasena" not in contenido