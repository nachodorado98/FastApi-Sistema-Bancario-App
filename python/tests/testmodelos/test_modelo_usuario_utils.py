from src.modelos.usuario import UsuarioBasico
from src.modelos.usuario_utils import obtenerObjetoUsuarioBasico, obtenerObjetosUsuarioBasico

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