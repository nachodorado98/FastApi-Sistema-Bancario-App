import pytest

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