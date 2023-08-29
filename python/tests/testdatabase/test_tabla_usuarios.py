import pytest
import datetime

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

def test_obtener_contrasena_usuario_no_existe(conexion):

	assert conexion.obtenerContrasena("nacho98") is None

@pytest.mark.parametrize(["usuario"],
	[("nacho98",),("nacho99",),("nacho989",)]
)
def test_obtener_contrasena_usuario_existe(conexion, usuario):

	conexion.insertarUsuario("nacho98", "nacho", "dorado", "ruiz",
							"1998-02-16", "madrid", "españa", "masculino",
							"123456789", "natxo98@gmail.com", "1234")
	conexion.insertarUsuario("nacho99", "nacho", "dorado", "ruiz",
							"1998-02-16", "madrid", "españa", "masculino",
							"123456789", "natxo98@gmail.com", "1234")
	conexion.insertarUsuario("nacho989", "nacho", "dorado", "ruiz",
							"1998-02-16", "madrid", "españa", "masculino",
							"123456789", "natxo98@gmail.com", "1234")

	contrasena=conexion.obtenerContrasena(usuario)

	assert contrasena=="1234"

def test_obtener_datos_usuario_no_existe(conexion):

	assert conexion.obtenerDatosUsuario("nacho98") is None

def test_obtener_datos_usuario_existe(conexion):

	conexion.insertarUsuario("nacho98", "nacho", "dorado", "ruiz",
							"1998-02-16", "madrid", "españa", "masculino",
							"123456789", "natxo98@gmail.com", "1234")

	datos=conexion.obtenerDatosUsuario("nacho98")

	assert datos["usuario"]=="nacho98"
	assert datos["nombre"]=="nacho"
	assert datos["apellido1"]=="dorado"
	assert datos["apellido2"]=="ruiz"
	assert datos["fecha_nacimiento"]==datetime.datetime(1998,2,16).date()
	assert datos["ciudad"]=="madrid"
	assert datos["pais"]=="españa"
	assert datos["genero"]=="masculino"
	assert datos["telefono"]=="123456789"
	assert datos["correo"]=="natxo98@gmail.com"
	assert "contrasena" not in datos

@pytest.mark.parametrize(["telefono", "telefono_nuevo"],
	[
		("123456789","61111111"),
		("123456789","98761234"),
		("123456789","45456897")
	]
)
def test_actualizar_telefono_usuario(conexion, telefono, telefono_nuevo):

	conexion.insertarUsuario("nacho98", "nacho", "dorado", "ruiz",
							"1998-02-16", "madrid", "españa", "masculino",
							telefono, "natxo98@gmail.com", "1234")

	conexion.actualizarTelefono("nacho98", telefono_nuevo)

	datos=conexion.obtenerDatosUsuario("nacho98")

	assert datos["telefono"]==telefono_nuevo

@pytest.mark.parametrize(["contrasena", "contrasena_nueva"],
	[
		("1234","2341"),
		("contrasena1234","1234contrasena"),
		("qwertyuiop","contrasenaaaaa")
	]
)
def test_cambiar_contrasena_usuario(conexion, contrasena, contrasena_nueva):

	conexion.insertarUsuario("nacho98", "nacho", "dorado", "ruiz",
							"1998-02-16", "madrid", "españa", "masculino",
							"612345789", "natxo98@gmail.com", contrasena)

	conexion.cambiarContrasena("nacho98", contrasena_nueva)

	assert conexion.obtenerContrasena("nacho98")==contrasena_nueva

def test_obtener_saldo_usuario_no_existe(conexion):

	assert conexion.obtenerSaldo("nacho98") is None

@pytest.mark.parametrize(["usuario"],
	[("nacho98",),("nacho99",),("nacho989",)]
)
def test_obtener_saldo_usuario_existe(conexion, usuario):

	conexion.insertarUsuario("nacho98", "nacho", "dorado", "ruiz",
							"1998-02-16", "madrid", "españa", "masculino",
							"123456789", "natxo98@gmail.com", "1234")
	conexion.insertarUsuario("nacho99", "nacho", "dorado", "ruiz",
							"1998-02-16", "madrid", "españa", "masculino",
							"123456789", "natxo98@gmail.com", "1234")
	conexion.insertarUsuario("nacho989", "nacho", "dorado", "ruiz",
							"1998-02-16", "madrid", "españa", "masculino",
							"123456789", "natxo98@gmail.com", "1234")

	saldo=conexion.obtenerSaldo(usuario)

	assert saldo==0.0

@pytest.mark.parametrize(["saldo"],
	[(10,),(1.5,),(-30.1,),(0.0,),(200.7,)]
)
def test_actualizar_saldo_usuario(conexion, saldo):

	conexion.insertarUsuario("nacho98", "nacho", "dorado", "ruiz",
							"1998-02-16", "madrid", "españa", "masculino",
							"612345789", "natxo98@gmail.com", "1234")

	conexion.actualizarSaldo("nacho98", saldo)

	saldo_nuevo=conexion.obtenerSaldo("nacho98")

	assert saldo_nuevo==saldo_nuevo