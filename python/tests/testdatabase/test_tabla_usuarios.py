def test_insertar_usuario(conexion):

	conexion.insertarUsuario("nacho98", "nacho", "dorado", "ruiz",
							"1998-02-16", "madrid", "españa", "masculino",
							"123456789", "natxo98@gmail.com", "1234")

	conexion.c.execute("SELECT * FROM usuarios")

	usuarios=conexion.c.fetchall()

	assert len(usuarios)==1
	assert usuarios[0]["saldo"]==0.0

def test_insertar_usuarios(conexion):

	conexion.insertarUsuario("nacho98", "nacho", "dorado", "ruiz",
							"1998-02-16", "madrid", "españa", "masculino",
							"123456789", "natxo98@gmail.com", "1234")
	conexion.insertarUsuario("nacho99", "nacho", "dorado", "ruiz",
							"1998-02-16", "madrid", "españa", "masculino",
							"123456789", "natxo98@gmail.com", "1234")
	conexion.insertarUsuario("nacho989", "nacho", "dorado", "ruiz",
							"1998-02-16", "madrid", "españa", "masculino",
							"123456789", "natxo98@gmail.com", "1234")

	conexion.c.execute("SELECT * FROM usuarios")

	assert len(conexion.c.fetchall())==3

def test_usuario_no_existe(conexion):

	assert not conexion.existe_usuario("nacho98")

def test_usuario_existe(conexion):

	assert not conexion.existe_usuario("nacho98")

	conexion.insertarUsuario("nacho98", "nacho", "dorado", "ruiz",
							"1998-02-16", "madrid", "españa", "masculino",
							"123456789", "natxo98@gmail.com", "1234")

	assert conexion.existe_usuario("nacho98")

def test_obtener_usuarios_no_existen(conexion):

	assert conexion.obtenerUsuarios() is None

def test_obtener_usuarios_existen(conexion):

	conexion.insertarUsuario("nacho98", "nacho", "dorado", "ruiz",
							"1998-02-16", "madrid", "españa", "masculino",
							"123456789", "natxo98@gmail.com", "1234")
	conexion.insertarUsuario("nacho99", "nacho", "dorado", "ruiz",
							"1998-02-16", "madrid", "españa", "masculino",
							"123456789", "natxo98@gmail.com", "1234")
	conexion.insertarUsuario("nacho989", "nacho", "dorado", "ruiz",
							"1998-02-16", "madrid", "españa", "masculino",
							"123456789", "natxo98@gmail.com", "1234")

	usuarios=conexion.obtenerUsuarios()

	assert len(usuarios)==3

	for usuario in usuarios:

		assert "usuario" in usuario
