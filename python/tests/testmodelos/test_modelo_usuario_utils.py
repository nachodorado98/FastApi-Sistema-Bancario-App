import datetime

from src.modelos.usuario import UsuarioBasico, Usuario
from src.modelos.usuario_utils import obtenerObjetoUsuarioBasico, obtenerObjetosUsuarioBasico, obtenerObjetoUsuario

def test_obtener_usuario_basico():

	usuario={"usuario":"nacho98"}

	objeto=obtenerObjetoUsuarioBasico(usuario)

	assert isinstance(objeto, UsuarioBasico)
	assert objeto.usuario=="nacho98"


def test_obtener_varios_usuarios_basicos():

	usuarios=[{"usuario":"nacho98"},{"usuario":"nacho98"},{"usuario":"nacho98"}]

	objetos=obtenerObjetosUsuarioBasico(usuarios)

	assert len(objetos)==3

	for objeto in objetos:

		assert isinstance(objeto, UsuarioBasico)
		assert objeto.usuario=="nacho98"


def test_obtener_usuario():

	usuario={"usuario":"nacho98","nombre":"Nacho","apellido1":"Dorado","apellido2":"Ruiz",
			"fecha_nacimiento":datetime.datetime(1998,2,16),"ciudad":"Madrid","pais":"España",
			"genero":"masculino","telefono":"611111111","correo":"natxo98@gmail.com"}

	objeto=obtenerObjetoUsuario(usuario)

	assert isinstance(objeto, Usuario)
	assert objeto.usuario=="nacho98"
	assert objeto.fecha_nacimiento=="1998-02-16"