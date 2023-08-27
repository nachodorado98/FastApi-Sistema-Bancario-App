def test_obtener_transacciones_no_existen(conexion):

	conexion.insertarUsuario("nacho98", "nacho", "dorado", "ruiz",
							"1998-02-16", "madrid", "españa", "masculino",
							"123456789", "natxo98@gmail.com", "1234")

	assert conexion.obtenerTransacciones("nacho98") is None

def test_obtener_transacciones_existen(conexion):

	conexion.insertarUsuario("nacho98", "nacho", "dorado", "ruiz",
							"1998-02-16", "madrid", "españa", "masculino",
							"123456789", "natxo98@gmail.com", "1234")

	conexion.c.execute("INSERT INTO transacciones VALUES('1','nacho98','concepto', 1.0, '2023-08-27', 1.0)")
	conexion.c.execute("INSERT INTO transacciones VALUES('2','nacho98','concepto', 1.0, '2023-08-27', 1.0)")
	conexion.c.execute("INSERT INTO transacciones VALUES('3','nacho98','concepto', 1.0, '2023-08-27', 1.0)")

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