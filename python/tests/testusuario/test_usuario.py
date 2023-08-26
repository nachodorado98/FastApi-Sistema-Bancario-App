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

@pytest.mark.parametrize(["token"],
	[("token",), ("dgfdkjg89e5yujgfkjgdf",), ("nacho98",), ("amanditaa",), ("1234",)]
)
def test_pagina_actualizar_telefono_usuario_no_autenticado(cliente, token):

	header={"Authorization": f"Bearer {token}"}

	respuesta=cliente.patch("/usuarios/me/actualizar_telefono", json={"telefono":"612345789"}, headers=header)

	contenido=respuesta.json()

	assert respuesta.status_code==401
	assert "detail" in contenido

@pytest.mark.parametrize(["telefono"],
	[({"telefono":"112345789"},),({"telefono":"512345789"},),({"telefono":"91123457"},),({"telefono":"61234578a"},),({"telefono":"61234aa78"},)]
)
def test_pagina_actualizar_telefono_usuario_autenticado_incorrecto(cliente, header_autorizado, telefono):

	respuesta=cliente.patch("/usuarios/me/actualizar_telefono", json=telefono, headers=header_autorizado)

	contenido=respuesta.json()

	assert respuesta.status_code==422
	assert not "mensaje" in contenido
	assert not "telefono" in contenido

def test_pagina_actualizar_telefono_usuario_autenticado_mismo_numero(cliente, header_autorizado):

	respuesta=cliente.patch("/usuarios/me/actualizar_telefono", json={"telefono":"611111111"}, headers=header_autorizado)

	contenido=respuesta.json()

	assert respuesta.status_code==400
	assert "detail" in contenido

@pytest.mark.parametrize(["telefono"],
	[({"telefono":"912345678"},),({"telefono":"612345789"},),({"telefono":"666666666"},),({"telefono":"611111116"},)]
)
def test_pagina_actualizar_telefono_usuario_autenticado(cliente, header_autorizado, telefono):

	respuesta=cliente.patch("/usuarios/me/actualizar_telefono", json=telefono, headers=header_autorizado)

	contenido=respuesta.json()

	assert respuesta.status_code==200
	assert "mensaje" in contenido
	assert "telefono" in contenido

@pytest.mark.parametrize(["token"],
	[("token",), ("dgfdkjg89e5yujgfkjgdf",), ("nacho98",), ("amanditaa",), ("1234",)]
)
def test_pagina_cambiar_contrasena_usuario_no_autenticado(cliente, token):

	header={"Authorization": f"Bearer {token}"}

	respuesta=cliente.patch("/usuarios/me/cambiar_contrasena", json={"contrasena_antigua":"123456789","contrasena_nueva":"contrasena1234"}, headers=header)

	contenido=respuesta.json()

	assert respuesta.status_code==401
	assert "detail" in contenido

@pytest.mark.parametrize(["contrasena_nueva"],
	[("123456789",),("1234567",),("987654321",),("1234 56789",),("ddd",),("fgf123456789gfgf",),("fdf666b gh7",)]
)
def test_pagina_cambiar_contrasena_usuario_autenticado_incorrecto(cliente, header_autorizado, contrasena_nueva):

	respuesta=cliente.patch("/usuarios/me/cambiar_contrasena", json={"contrasena_antigua":"123456789","contrasena_nueva":contrasena_nueva}, headers=header_autorizado)

	contenido=respuesta.json()

	assert respuesta.status_code==422
	assert not "mensaje" in contenido

@pytest.mark.parametrize(["contrasena"],
	[("123456781",),("12345678",),("98765432",),("1234a56789",),("ddddgf6667",),("fgf12345aa89gfgf",),("fdf666b78gh7",)]
)
def test_pagina_cambiar_contrasena_usuario_autenticado_contrasenas_iguales(cliente, header_autorizado, contrasena):

	respuesta=cliente.patch("/usuarios/me/cambiar_contrasena", json={"contrasena_antigua":contrasena,"contrasena_nueva":contrasena}, headers=header_autorizado)

	contenido=respuesta.json()

	assert respuesta.status_code==400
	assert "detail" in contenido

@pytest.mark.parametrize(["contrasena_antigua"],
	[("123456781",),("12345678",),("98765432",),("1234a56789",),("ddddgf6667",),("fgf12345aa89gfgf",),("fdf666b78gh7",)]
)
def test_pagina_cambiar_contrasena_usuario_autenticado_contrasena_antigua_incorrecta(cliente, header_autorizado, contrasena_antigua):

	respuesta=cliente.patch("/usuarios/me/cambiar_contrasena", json={"contrasena_antigua":contrasena_antigua,"contrasena_nueva":"contrasena1234"}, headers=header_autorizado)

	contenido=respuesta.json()

	assert respuesta.status_code==400
	assert "detail" in contenido

@pytest.mark.parametrize(["contrasena_nueva"],
	[("123456781",),("12345678",),("98765432",),("1234a56789",),("ddddgf6667",),("fgf12345aa89gfgf",),("fdf666b78gh7",)]
)
def test_pagina_cambiar_contrasena_usuario_autenticado(cliente, header_autorizado, contrasena_nueva):

	respuesta=cliente.patch("/usuarios/me/cambiar_contrasena", json={"contrasena_antigua":"987654321","contrasena_nueva":contrasena_nueva}, headers=header_autorizado)

	contenido=respuesta.json()

	assert respuesta.status_code==200
	assert "mensaje" in contenido