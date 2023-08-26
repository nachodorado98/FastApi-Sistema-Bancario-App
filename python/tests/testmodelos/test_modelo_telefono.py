import pytest

from src.modelos.telefono import Telefono

@pytest.mark.parametrize(["telefono"],
	[({"telefono":"112345789"},),({"telefono":"512345789"},),({"telefono":"91123457"},),({"telefono":"61234578a"},),({"telefono":"61234aa78"},)]
)
def test_modelo_telefono_incorrecto(telefono):

	with pytest.raises(ValueError):

		Telefono(**telefono)

@pytest.mark.parametrize(["telefono"],
	[({"telefono":"612345789"},),({"telefono":"911111111"},),({"telefono":"911223457"},),({"telefono":"6666666666"},)]
)
def test_modelo_telefono_correcto(telefono):

	Telefono(**telefono)