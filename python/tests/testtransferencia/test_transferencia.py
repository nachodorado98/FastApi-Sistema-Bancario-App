import pytest

@pytest.mark.parametrize(["token"],
	[("token",), ("dgfdkjg89e5yujgfkjgdf",), ("nacho98",), ("amanditaa",), ("1234",)]
)
def test_pagina_realizar_transferencia_no_autenticado(cliente, token):

	header={"Authorization": f"Bearer {token}"}

	respuesta=cliente.post("/transferencias", json={"usuario_destino":"amanda99", "concepto":"concepto", "cantidad":1.0}, headers=header)

	contenido=respuesta.json()

	assert respuesta.status_code==401
	assert "detail" in contenido

@pytest.mark.parametrize(["cantidad"],
	[("uno",), ("cantidad",), ("100euros",)]
)
def test_pagina_realizar_transferencia_autenticado_incorrecto(cliente, header_autorizado, cantidad):

	respuesta=cliente.post("/transferencias", json={"usuario_destino":"amanda99", "concepto":"concepto", "cantidad":cantidad}, headers=header_autorizado)

	contenido=respuesta.json()

	assert respuesta.status_code==422
	assert not "mensaje" in contenido
	assert not "saldo" in contenido

@pytest.mark.parametrize(["cantidad"],
	[(0.0,),(-100,),(-1,),(-0.1,)]
)
def test_pagina_realizar_transferencia_autenticado_cantidad_incorrecta(cliente, header_autorizado, cantidad):

	respuesta=cliente.post("/transferencias", json={"usuario_destino":"amanda99", "concepto":"concepto", "cantidad":cantidad}, headers=header_autorizado)

	contenido=respuesta.json()

	assert respuesta.status_code==400
	assert "detail" in contenido

@pytest.mark.parametrize(["cantidad", "cantidad_transferir"],
	[(10,100), (100,101), (1,1.1), (0.1,0.11), (20.5,22)]
)
def test_pagina_realizar_transferencia_autenticado_cantidad_superior(cliente, header_autorizado, cantidad, cantidad_transferir):

	cliente.post("/transacciones/ingresar", json={"concepto":"concepto", "cantidad":cantidad}, headers=header_autorizado)

	respuesta=cliente.post("/transferencias", json={"usuario_destino":"amanda99", "concepto":"concepto", "cantidad":cantidad_transferir}, headers=header_autorizado)

	contenido=respuesta.json()

	assert respuesta.status_code==400
	assert "detail" in contenido

@pytest.mark.parametrize(["usuario"],
	[("nacho99",), ("nacho",), ("amanda99",)]
)
def test_pagina_realizar_transferencia_autenticado_usuario_no_existente(cliente, header_autorizado, usuario):

	cliente.post("/transacciones/ingresar", json={"concepto":"concepto", "cantidad":100}, headers=header_autorizado)

	respuesta=cliente.post("/transferencias", json={"usuario_destino":usuario, "concepto":"concepto", "cantidad":50}, headers=header_autorizado)

	contenido=respuesta.json()

	assert respuesta.status_code==400
	assert "detail" in contenido

def test_pagina_realizar_transferencia_autenticado_usuario_mismo_usuario(cliente, header_autorizado):

	cliente.post("/transacciones/ingresar", json={"concepto":"concepto", "cantidad":100}, headers=header_autorizado)

	respuesta=cliente.post("/transferencias", json={"usuario_destino":"nacho98", "concepto":"concepto", "cantidad":50}, headers=header_autorizado)

	contenido=respuesta.json()

	assert respuesta.status_code==400
	assert "detail" in contenido

@pytest.mark.parametrize(["usuario"],
	[("nacho99",), ("nacho",), ("amanda99",)]
)
def test_pagina_realizar_transferencia_autenticado(conexion, cliente, header_autorizado, usuario):

	cliente.post("/usuarios", json={"usuario":usuario,"nombre":"Nacho","apellido1":"Dorado","apellido2":"Ruiz","fecha_nacimiento":"1998-02-16","ciudad":"Madrid","pais":"España","genero":"masculino","telefono":"611111111","correo":"natxo98@gmail.com", "contrasena":"12345678"})

	cliente.post("/transacciones/ingresar", json={"concepto":"concepto", "cantidad":100}, headers=header_autorizado)

	respuesta=cliente.post("/transferencias", json={"usuario_destino":usuario, "concepto":"concepto", "cantidad":50}, headers=header_autorizado)

	contenido=respuesta.json()

	assert respuesta.status_code==201
	assert "mensaje" in contenido
	assert "saldo" in contenido

	conexion.c.execute("SELECT * FROM transferencias")

	assert len(conexion.c.fetchall())==1

@pytest.mark.parametrize(["token"],
	[("token",), ("dgfdkjg89e5yujgfkjgdf",), ("nacho98",), ("amanditaa",), ("1234",)]
)
def test_pagina_obtener_transferencias_no_autenticado(cliente, token):

	header={"Authorization": f"Bearer {token}"}

	respuesta=cliente.get("/transferencias", headers=header)

	contenido=respuesta.json()

	assert respuesta.status_code==401
	assert "detail" in contenido

def test_pagina_obtener_transferencias_autenticado_no_existen(cliente, header_autorizado):

	respuesta=cliente.get("/transferencias", headers=header_autorizado)

	contenido=respuesta.json()

	assert respuesta.status_code==404
	assert "detail" in contenido

@pytest.mark.parametrize(["usuario"],
	[("nacho99",), ("nacho",), ("amanda99",)]
)
def test_pagina_obtener_transferencias_autenticado(cliente, header_autorizado, usuario):

	cliente.post("/usuarios", json={"usuario":usuario,"nombre":"Nacho","apellido1":"Dorado","apellido2":"Ruiz","fecha_nacimiento":"1998-02-16","ciudad":"Madrid","pais":"España","genero":"masculino","telefono":"611111111","correo":"natxo98@gmail.com", "contrasena":"12345678"})

	cliente.post("/transacciones/ingresar", json={"concepto":"concepto", "cantidad":100}, headers=header_autorizado)

	cliente.post("/transferencias", json={"usuario_destino":usuario, "concepto":"concepto", "cantidad":10}, headers=header_autorizado)
	cliente.post("/transferencias", json={"usuario_destino":usuario, "concepto":"concepto", "cantidad":10}, headers=header_autorizado)
	cliente.post("/transferencias", json={"usuario_destino":usuario, "concepto":"concepto", "cantidad":10}, headers=header_autorizado)

	respuesta=cliente.get("/transferencias", headers=header_autorizado)

	contenido=respuesta.json()

	assert respuesta.status_code==200
	assert len(contenido)==3

	for transferencia in contenido:

		assert "transferencia" in transferencia
		assert "usuario_origen" in transferencia
		assert "usuario_destino" in transferencia
		assert "concepto" in transferencia
		assert "cantidad" in transferencia
		assert "fecha" in transferencia

@pytest.mark.parametrize(["token"],
	[("token",), ("dgfdkjg89e5yujgfkjgdf",), ("nacho98",), ("amanditaa",), ("1234",)]
)
def test_pagina_obtener_transferencias_realizadas_no_autenticado(cliente, token):

	header={"Authorization": f"Bearer {token}"}

	respuesta=cliente.get("/transferencias/realizadas", headers=header)

	contenido=respuesta.json()

	assert respuesta.status_code==401
	assert "detail" in contenido

def test_pagina_obtener_transferencias_realizadas_autenticado_no_existen(cliente, header_autorizado):

	respuesta=cliente.get("/transferencias/realizadas", headers=header_autorizado)

	contenido=respuesta.json()

	assert respuesta.status_code==404
	assert "detail" in contenido

@pytest.mark.parametrize(["usuario"],
	[("nacho99",), ("nacho",), ("amanda99",)]
)
def test_pagina_obtener_transferencias_realizadas_autenticado(cliente, header_autorizado, header_autorizado_auxiliar, usuario):

	cliente.post("/usuarios", json={"usuario":usuario,"nombre":"Nacho","apellido1":"Dorado","apellido2":"Ruiz","fecha_nacimiento":"1998-02-16","ciudad":"Madrid","pais":"España","genero":"masculino","telefono":"611111111","correo":"natxo98@gmail.com", "contrasena":"12345678"})
	
	cliente.post("/transacciones/ingresar", json={"concepto":"concepto", "cantidad":100}, headers=header_autorizado)
	cliente.post("/transacciones/ingresar", json={"concepto":"concepto", "cantidad":100}, headers=header_autorizado_auxiliar)

	cliente.post("/transferencias", json={"usuario_destino":usuario, "concepto":"concepto", "cantidad":10}, headers=header_autorizado)
	cliente.post("/transferencias", json={"usuario_destino":usuario, "concepto":"concepto", "cantidad":10}, headers=header_autorizado)
	cliente.post("/transferencias", json={"usuario_destino":usuario, "concepto":"concepto", "cantidad":10}, headers=header_autorizado)

	cliente.post("/transferencias", json={"usuario_destino":"nacho98", "concepto":"concepto", "cantidad":10}, headers=header_autorizado_auxiliar)
	cliente.post("/transferencias", json={"usuario_destino":"nacho98", "concepto":"concepto", "cantidad":10}, headers=header_autorizado_auxiliar)

	assert len(cliente.get("/transferencias", headers=header_autorizado).json())==5

	respuesta=cliente.get("/transferencias/realizadas", headers=header_autorizado)

	contenido=respuesta.json()

	assert respuesta.status_code==200
	assert len(contenido)==3

	for transferencia in contenido:

		assert "transferencia" in transferencia
		assert "usuario_origen" in transferencia
		assert "usuario_destino" in transferencia
		assert "concepto" in transferencia
		assert "cantidad" in transferencia
		assert "fecha" in transferencia

@pytest.mark.parametrize(["token"],
	[("token",), ("dgfdkjg89e5yujgfkjgdf",), ("nacho98",), ("amanditaa",), ("1234",)]
)
def test_pagina_obtener_transferencias_recibidas_no_autenticado(cliente, token):

	header={"Authorization": f"Bearer {token}"}

	respuesta=cliente.get("/transferencias/recibidas", headers=header)

	contenido=respuesta.json()

	assert respuesta.status_code==401
	assert "detail" in contenido

def test_pagina_obtener_transferencias_recibidas_autenticado_no_existen(cliente, header_autorizado):

	respuesta=cliente.get("/transferencias/recibidas", headers=header_autorizado)

	contenido=respuesta.json()

	assert respuesta.status_code==404
	assert "detail" in contenido

@pytest.mark.parametrize(["usuario"],
	[("nacho99",), ("nacho",), ("amanda99",)]
)
def test_pagina_obtener_transferencias_recibidas_autenticado(cliente, header_autorizado, header_autorizado_auxiliar, usuario):

	cliente.post("/usuarios", json={"usuario":usuario,"nombre":"Nacho","apellido1":"Dorado","apellido2":"Ruiz","fecha_nacimiento":"1998-02-16","ciudad":"Madrid","pais":"España","genero":"masculino","telefono":"611111111","correo":"natxo98@gmail.com", "contrasena":"12345678"})
	
	cliente.post("/transacciones/ingresar", json={"concepto":"concepto", "cantidad":100}, headers=header_autorizado)
	cliente.post("/transacciones/ingresar", json={"concepto":"concepto", "cantidad":100}, headers=header_autorizado_auxiliar)

	cliente.post("/transferencias", json={"usuario_destino":usuario, "concepto":"concepto", "cantidad":10}, headers=header_autorizado)
	cliente.post("/transferencias", json={"usuario_destino":usuario, "concepto":"concepto", "cantidad":10}, headers=header_autorizado)
	cliente.post("/transferencias", json={"usuario_destino":usuario, "concepto":"concepto", "cantidad":10}, headers=header_autorizado)

	cliente.post("/transferencias", json={"usuario_destino":"nacho98", "concepto":"concepto", "cantidad":10}, headers=header_autorizado_auxiliar)
	cliente.post("/transferencias", json={"usuario_destino":"nacho98", "concepto":"concepto", "cantidad":10}, headers=header_autorizado_auxiliar)

	assert len(cliente.get("/transferencias", headers=header_autorizado).json())==5
	
	respuesta=cliente.get("/transferencias/recibidas", headers=header_autorizado)

	contenido=respuesta.json()

	assert respuesta.status_code==200
	assert len(contenido)==2

	for transferencia in contenido:

		assert "transferencia" in transferencia
		assert "usuario_origen" in transferencia
		assert "usuario_destino" in transferencia
		assert "concepto" in transferencia
		assert "cantidad" in transferencia
		assert "fecha" in transferencia