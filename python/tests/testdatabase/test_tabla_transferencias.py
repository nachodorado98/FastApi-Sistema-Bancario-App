import pytest

@pytest.mark.parametrize(["usuario1", "usuario2"],
	[
		("nacho98", "nacho"),
		("nacho", "nacho98"),
		("amanda99", "nacho"),
		("nacho98", "amanda")
	]
)
def test_insertar_transferencia(conexion, usuario1, usuario2):

	conexion.insertarUsuario(usuario1, "nacho", "dorado", "ruiz",
							"1998-02-16", "madrid", "españa", "masculino",
							"123456789", "natxo98@gmail.com", "1234")

	conexion.insertarUsuario(usuario2, "nacho", "dorado", "ruiz",
							"1998-02-16", "madrid", "españa", "masculino",
							"123456789", "natxo98@gmail.com", "1234")

	conexion.insertarTransaccion("1", usuario1, "Ingreso Inicial", 100, "2023-09-01", 100)

	conexion.insertarTransaccion("2", usuario1, "Retirada", 50, "2023-09-01", 50)

	conexion.insertarTransaccion("3", usuario2, "Ingreso", 50, "2023-09-01", 50)

	conexion.insertarTransferencia("1", "2", "3", 50)

	conexion.c.execute("SELECT * FROM transferencias")

	transferencias=conexion.c.fetchall()

	assert len(transferencias)==1
	assert "transferencia" in transferencias[0]
	assert "transaccion_origen" in transferencias[0]
	assert "transaccion_destino" in transferencias[0]
	assert "cantidad_neta" in transferencias[0]
