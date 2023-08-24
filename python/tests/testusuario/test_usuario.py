def test_pagina_obtener_usuarios_vacia(cliente):

	respuesta=cliente.get("/usuarios")

	contenido=respuesta.json()

	assert respuesta.status_code==200
	assert contenido==[]
