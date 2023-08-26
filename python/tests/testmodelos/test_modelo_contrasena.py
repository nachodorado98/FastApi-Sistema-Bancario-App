import pytest

from src.modelos.contrasena import Contrasena

@pytest.mark.parametrize(["contrasena_nueva"],
	[("123456789",),("1234567",),("987654321",),("1234 56789",),("fdfd",),("hjgjh 6686",),("gfgg123456789fgg",)]
)
def test_modelo_contrasena_incorrecto(contrasena_nueva):

	with pytest.raises(ValueError):

		Contrasena(contrasena_antigua="123456789", contrasena_nueva=contrasena_nueva)

@pytest.mark.parametrize(["contrasena_nueva"],
	[("12345678",),("1234567aa",),("98765asd4321",),("1234856789",),("fdfdfdfdg",),("hjgjh776686",),("gfgg12345p6789fgg",)]
)
def test_modelo_contrasena_correcto(contrasena_nueva):

	Contrasena(contrasena_antigua="123456789", contrasena_nueva=contrasena_nueva)