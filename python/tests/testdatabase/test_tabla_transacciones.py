import pytest

@pytest.mark.parametrize(["transaccion", "usuario", "concepto", "cantidad", "fecha", "historico"],
	[
		("1","nacho98", "concepto", 1.0, "2023-08-28", 10),
		("1gth","nacho99", "dgfdhgfd", 10.0, "2023-08-20", 1.5),
		("id","nachodorado", "concepto11", 1.05, "2023-07-28", 102),
		("12ff44","usuario", "transaccion", -1.0, "2023-08-28", -10)
	]
)
def test_insertar_transaccion(conexion, transaccion, usuario, concepto, cantidad, fecha, historico):

	conexion.insertarUsuario(usuario, "nacho", "dorado", "ruiz",
							"1998-02-16", "madrid", "españa", "masculino",
							"123456789", "natxo98@gmail.com", "1234")

	conexion.insertarTransaccion(transaccion, usuario, concepto, cantidad, fecha, historico)

	transacciones=conexion.obtenerTransacciones(usuario)

	assert len(transacciones)==1
	assert "transaccion" in transacciones[0]
	assert "concepto" in transacciones[0]
	assert "cantidad" in transacciones[0]
	assert "fecha" in transacciones[0]
	assert "historico" in transacciones[0]

def test_obtener_transacciones_no_existen(conexion):

	conexion.insertarUsuario("nacho98", "nacho", "dorado", "ruiz",
							"1998-02-16", "madrid", "españa", "masculino",
							"123456789", "natxo98@gmail.com", "1234")

	assert conexion.obtenerTransacciones("nacho98") is None

def test_obtener_transacciones_existen(conexion):

	conexion.insertarUsuario("nacho98", "nacho", "dorado", "ruiz",
							"1998-02-16", "madrid", "españa", "masculino",
							"123456789", "natxo98@gmail.com", "1234")

	conexion.insertarTransaccion("1","nacho98", "concepto", 1.0, "2023-08-28", 10)
	conexion.insertarTransaccion("2","nacho98", "concepto", 1.0, "2023-08-28", 10)
	conexion.insertarTransaccion("3","nacho98", "concepto", 1.0, "2023-08-28", 10)

	conexion.bbdd.commit()

	transacciones=conexion.obtenerTransacciones("nacho98")

	assert len(transacciones)==3
	
	for transaccion in transacciones:

		assert "transaccion" in transaccion
		assert "concepto" in transaccion
		assert "cantidad" in transaccion
		assert "fecha" in transaccion
		assert "historico" in transaccion
		assert not "usuario" in transaccion