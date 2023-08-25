import pytest

from src.utilidades.utils import generarHash, comprobarHash, enviarCorreo

@pytest.mark.parametrize(["contrasena"],
	[("contrasena1234",),("123456789",),("contrasena_secreta",)]
)
def test_generar_hash_contrasena(contrasena):

	contrasena_hash=generarHash(contrasena)

	assert len(contrasena_hash)==60
	assert contrasena not in contrasena_hash


@pytest.mark.parametrize(["contrasena", "contrasena_mal"],
	[
		("contrasena1234","contrasena123"),
		("123456789","1234567899"),
		("contrasena_secreta","contrasenasecreta")

	]
)
def test_comprobar_hash_contrasena_incorrecta(contrasena, contrasena_mal):

	contrasena_hash=generarHash(contrasena)

	assert not comprobarHash(contrasena_mal, contrasena_hash)


@pytest.mark.parametrize(["contrasena"],
	[("contrasena1234",),("123456789",),("contrasena_secreta",)]
)
def test_comprobar_hash_contrasena_correcta(contrasena):

	contrasena_hash=generarHash(contrasena)

	assert comprobarHash(contrasena, contrasena_hash)

@pytest.mark.parametrize(["correo"],
	[("natxo98gail.com",),("@gmail.com",),("correo@.yyy",)]
)
def test_enviar_correo_incorrecto(correo):

	assert not enviarCorreo(correo, "nacho98", "nacho")

def test_enviar_correo_correcto():

	assert enviarCorreo("natxo98@gmail.com", "nacho98", "nacho")
