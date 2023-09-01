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

	conexion.insertarTransaccion("2", usuario1, "Retirada", -50, "2023-09-01", 50)

	conexion.insertarTransaccion("3", usuario2, "Ingreso", 50, "2023-09-01", 50)

	conexion.insertarTransferencia("1", "2", "3", 50)

	conexion.c.execute("SELECT * FROM transferencias")

	transferencias=conexion.c.fetchall()

	assert len(transferencias)==1
	assert "transferencia" in transferencias[0]
	assert "transaccion_origen" in transferencias[0]
	assert "transaccion_destino" in transferencias[0]
	assert "cantidad_neta" in transferencias[0]

def test_obtener_transferencias_no_existen(conexion):

	assert conexion.obtenerTransferencias("nacho98") is None

@pytest.mark.parametrize(["usuario1", "usuario2"],
	[
		("nacho98", "nacho"),
		("nacho", "nacho98"),
		("amanda99", "nacho"),
		("nacho98", "amanda")
	]
)
def test_obtener_transferencias_existe_realizada(conexion, usuario1, usuario2):

	conexion.insertarUsuario(usuario1, "nacho", "dorado", "ruiz",
							"1998-02-16", "madrid", "españa", "masculino",
							"123456789", "natxo98@gmail.com", "1234")

	conexion.insertarUsuario(usuario2, "nacho", "dorado", "ruiz",
							"1998-02-16", "madrid", "españa", "masculino",
							"123456789", "natxo98@gmail.com", "1234")

	conexion.insertarTransaccion("1", usuario1, "Ingreso Inicial", 100, "2023-09-01", 100)

	conexion.insertarTransaccion("2", usuario1, "Retirada TF", -50, "2023-09-01", 50)

	conexion.insertarTransaccion("3", usuario2, "Ingreso TF", 50, "2023-09-01", 50)

	conexion.insertarTransferencia("1", "2", "3", 50)

	transferencias=conexion.obtenerTransferencias(usuario1)

	assert len(transferencias)==1
	assert "transferencia" in transferencias[0]
	assert "usuario_origen" in transferencias[0]
	assert "usuario_destino" in transferencias[0]
	assert "concepto" in transferencias[0]
	assert "cantidad" in transferencias[0]
	assert "fecha" in transferencias[0]

@pytest.mark.parametrize(["usuario1", "usuario2"],
	[
		("nacho98", "nacho"),
		("nacho", "nacho98"),
		("amanda99", "nacho"),
		("nacho98", "amanda")
	]
)
def test_obtener_transferencias_existen_realizadas(conexion, usuario1, usuario2):

	conexion.insertarUsuario(usuario1, "nacho", "dorado", "ruiz",
							"1998-02-16", "madrid", "españa", "masculino",
							"123456789", "natxo98@gmail.com", "1234")

	conexion.insertarUsuario(usuario2, "nacho", "dorado", "ruiz",
							"1998-02-16", "madrid", "españa", "masculino",
							"123456789", "natxo98@gmail.com", "1234")

	conexion.insertarTransaccion("1", usuario1, "Ingreso Inicial", 100, "2023-09-01", 100)

	conexion.insertarTransaccion("2", usuario1, "Retirada TF1", -50, "2023-09-01", 50)

	conexion.insertarTransaccion("3", usuario2, "Ingreso TF1", 50, "2023-09-01", 50)

	conexion.insertarTransferencia("1", "2", "3", 50)

	conexion.insertarTransaccion("4", usuario1, "Retirada TF2", -10, "2023-09-01", 40)

	conexion.insertarTransaccion("5", usuario2, "Ingreso TF2", 10, "2023-09-01", 60)

	conexion.insertarTransferencia("2", "4", "5", 10)

	transferencias=conexion.obtenerTransferencias(usuario1)

	assert len(transferencias)==2

@pytest.mark.parametrize(["usuario1", "usuario2"],
	[
		("nacho98", "nacho"),
		("nacho", "nacho98"),
		("amanda99", "nacho"),
		("nacho98", "amanda")
	]
)
def test_obtener_transferencias_existen_realizadas_recibidas(conexion, usuario1, usuario2):

	conexion.insertarUsuario(usuario1, "nacho", "dorado", "ruiz",
							"1998-02-16", "madrid", "españa", "masculino",
							"123456789", "natxo98@gmail.com", "1234")

	conexion.insertarUsuario(usuario2, "nacho", "dorado", "ruiz",
							"1998-02-16", "madrid", "españa", "masculino",
							"123456789", "natxo98@gmail.com", "1234")

	conexion.insertarTransaccion("1", usuario1, "Ingreso Inicial", 100, "2023-09-01", 100)

	conexion.insertarTransaccion("2", usuario1, "Retirada TF1", -50, "2023-09-01", 50)

	conexion.insertarTransaccion("3", usuario2, "Ingreso TF1", 50, "2023-09-01", 50)

	conexion.insertarTransferencia("1", "2", "3", 50)

	conexion.insertarTransaccion("4", usuario1, "Retirada TF2", -10, "2023-09-01", 40)

	conexion.insertarTransaccion("5", usuario2, "Ingreso TF2", 10, "2023-09-01", 60)

	conexion.insertarTransferencia("2", "4", "5", 10)

	conexion.insertarTransaccion("6", usuario2, "Retirada TF3", -50, "2023-09-01", 10)

	conexion.insertarTransaccion("7", usuario1, "Ingreso TF3", 50, "2023-09-01", 90)

	conexion.insertarTransferencia("3", "6", "7", 50)

	transferencias=conexion.obtenerTransferencias(usuario1)

	assert len(transferencias)==3