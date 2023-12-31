import pytest

@pytest.mark.parametrize(["token"],
	[("token",), ("dgfdkjg89e5yujgfkjgdf",), ("nacho98",), ("amanditaa",), ("1234",)]
)
def test_pagina_realizar_ingreso_no_autenticado(cliente, token):

	header={"Authorization": f"Bearer {token}"}

	respuesta=cliente.post("/transacciones/ingresar", json={"concepto":"concepto", "cantidad":1.0}, headers=header)

	contenido=respuesta.json()

	assert respuesta.status_code==401
	assert "detail" in contenido

@pytest.mark.parametrize(["cantidad"],
	[("uno",), ("cantidad",), ("100euros",)]
)
def test_pagina_realizar_ingreso_autenticado_incorrecto(cliente, header_autorizado, cantidad):

	respuesta=cliente.post("/transacciones/ingresar", json={"concepto":"concepto", "cantidad":cantidad}, headers=header_autorizado)

	contenido=respuesta.json()

	assert respuesta.status_code==422
	assert not "mensaje" in contenido
	assert not "saldo" in contenido

@pytest.mark.parametrize(["cantidad"],
	[(0.0,), (-100,), (-1,),(-0.1,)]
)
def test_pagina_realizar_ingreso_autenticado_cantidad_incorrecta(cliente, header_autorizado, cantidad):

	respuesta=cliente.post("/transacciones/ingresar", json={"concepto":"concepto", "cantidad":cantidad}, headers=header_autorizado)

	contenido=respuesta.json()

	assert respuesta.status_code==400
	assert "detail" in contenido

@pytest.mark.parametrize(["cantidad"],
	[(0.1,), (100,), (1,),(30.5,)]
)
def test_pagina_realizar_ingreso_autenticado(cliente, header_autorizado, cantidad):

	respuesta=cliente.post("/transacciones/ingresar", json={"concepto":"concepto", "cantidad":cantidad}, headers=header_autorizado)

	contenido=respuesta.json()

	assert respuesta.status_code==201
	assert "mensaje" in contenido
	assert "saldo" in contenido
	assert contenido["saldo"]==cantidad

@pytest.mark.parametrize(["token"],
	[("token",), ("dgfdkjg89e5yujgfkjgdf",), ("nacho98",), ("amanditaa",), ("1234",)]
)
def test_pagina_obtener_transacciones_no_autenticado(cliente, token):

	header={"Authorization": f"Bearer {token}"}

	respuesta=cliente.get("/transacciones", headers=header)

	contenido=respuesta.json()

	assert respuesta.status_code==401
	assert "detail" in contenido

def test_pagina_obtener_transacciones_autenticado_no_existen(cliente, header_autorizado):

	respuesta=cliente.get("/transacciones", headers=header_autorizado)

	contenido=respuesta.json()

	assert respuesta.status_code==404
	assert "detail" in contenido

def test_pagina_obtener_transacciones_autenticado(cliente, header_autorizado):

	cliente.post("/transacciones/ingresar", json={"concepto":"concepto", "cantidad":10}, headers=header_autorizado)
	cliente.post("/transacciones/ingresar", json={"concepto":"concepto", "cantidad":50}, headers=header_autorizado)
	cliente.post("/transacciones/ingresar", json={"concepto":"concepto", "cantidad":70.5}, headers=header_autorizado)

	respuesta=cliente.get("/transacciones", headers=header_autorizado)

	contenido=respuesta.json()

	assert respuesta.status_code==200
	assert len(contenido)==3

	for transaccion in contenido:

		assert "transaccion" in transaccion
		assert "concepto" in transaccion
		assert "cantidad" in transaccion
		assert "fecha" in transaccion
		assert "historico" in transaccion

@pytest.mark.parametrize(["token"],
	[("token",), ("dgfdkjg89e5yujgfkjgdf",), ("nacho98",), ("amanditaa",), ("1234",)]
)
def test_pagina_realizar_retirada_no_autenticado(cliente, token):

	header={"Authorization": f"Bearer {token}"}

	respuesta=cliente.post("/transacciones/retirar", json={"concepto":"concepto", "cantidad":1.0}, headers=header)

	contenido=respuesta.json()

	assert respuesta.status_code==401
	assert "detail" in contenido

@pytest.mark.parametrize(["cantidad"],
	[("uno",), ("cantidad",), ("100euros",)]
)
def test_pagina_realizar_retirada_autenticado_incorrecto(cliente, header_autorizado, cantidad):

	cliente.post("/transacciones/ingresar", json={"concepto":"concepto", "cantidad":10}, headers=header_autorizado)

	respuesta=cliente.post("/transacciones/retirar", json={"concepto":"concepto", "cantidad":cantidad}, headers=header_autorizado)

	contenido=respuesta.json()

	assert respuesta.status_code==422
	assert not "mensaje" in contenido
	assert not "saldo" in contenido

@pytest.mark.parametrize(["cantidad"],
	[(0.0,), (-100,), (-1,),(-0.1,)]
)
def test_pagina_realizar_retirada_autenticado_cantidad_incorrecta(cliente, header_autorizado, cantidad):

	cliente.post("/transacciones/ingresar", json={"concepto":"concepto", "cantidad":10}, headers=header_autorizado)

	respuesta=cliente.post("/transacciones/retirar", json={"concepto":"concepto", "cantidad":cantidad}, headers=header_autorizado)

	contenido=respuesta.json()

	assert respuesta.status_code==400
	assert "detail" in contenido

@pytest.mark.parametrize(["cantidad", "cantidad_retirar"],
	[(10,100), (100,101), (1,1.1),(0.1,0.11),(20.5,22)]
)
def test_pagina_realizar_retirada_autenticado_cantidad_superior(cliente, header_autorizado, cantidad, cantidad_retirar):

	cliente.post("/transacciones/ingresar", json={"concepto":"concepto", "cantidad":cantidad}, headers=header_autorizado)

	respuesta=cliente.post("/transacciones/retirar", json={"concepto":"concepto", "cantidad":cantidad_retirar}, headers=header_autorizado)

	contenido=respuesta.json()

	assert respuesta.status_code==400
	assert "detail" in contenido

@pytest.mark.parametrize(["cantidad", "cantidad_retirar"],
	[(100,100), (100,90), (1.11,1.1),(25,12.5),(30.5,22)]
)
def test_pagina_realizar_retirada_autenticado(cliente, header_autorizado, cantidad, cantidad_retirar):

	cliente.post("/transacciones/ingresar", json={"concepto":"concepto", "cantidad":cantidad}, headers=header_autorizado)

	respuesta=cliente.post("/transacciones/retirar", json={"concepto":"concepto", "cantidad":cantidad_retirar}, headers=header_autorizado)

	contenido=respuesta.json()

	assert respuesta.status_code==201
	assert "mensaje" in contenido
	assert "saldo" in contenido
	assert contenido["saldo"]==cantidad-cantidad_retirar
