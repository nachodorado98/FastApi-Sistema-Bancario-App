import pytest

from src.modelos.usuario import Usuario, UsuarioBBDD


@pytest.mark.parametrize(["usuario"],
	[
		({"usuario":"nacho98","nombre":"Nacho","apellido1":"Dorado","apellido2":"Ruiz","fecha_nacimiento":"1998-0216","ciudad":"Madrid","pais":"España","genero":"Masculino","telefono":"612345789","correo":"natxo98@gmail.com"},),
		({"usuario":"nacho98","nombre":"Nacho","apellido1":"Dorado","apellido2":"Ruiz","fecha_nacimiento":"16-02-1998","ciudad":"Madrid","pais":"España","genero":"Masculino","telefono":"612345789","correo":"natxo98@gmail.com"},),
		({"usuario":"nacho98","nombre":"Nacho","apellido1":"Dorado","apellido2":"Ruiz","fecha_nacimiento":"16/02/1998","ciudad":"Madrid","pais":"España","genero":"Masculino","telefono":"612345789","correo":"natxo98@gmail.com"},),
		({"usuario":"nacho98","nombre":"Nacho","apellido1":"Dorado","apellido2":"Ruiz","fecha_nacimiento":"1900-01-01","ciudad":"Madrid","pais":"España","genero":"Masculino","telefono":"612345789","correo":"natxo98@gmail.com"},),
		({"usuario":"nacho98","nombre":"Nacho","apellido1":"Dorado","apellido2":"Ruiz","fecha_nacimiento":"2023-01-01","ciudad":"Madrid","pais":"España","genero":"Masculino","telefono":"612345789","correo":"natxo98@gmail.com"},)
	]
)
def test_modelo_usuario_fecha_nacimiento_incorrecta(usuario):

	with pytest.raises(ValueError):

		Usuario(**usuario)

@pytest.mark.parametrize(["usuario"],
	[
		({"usuario":"nacho98","nombre":"Nacho","apellido1":"Dorado","apellido2":"Ruiz","fecha_nacimiento":"1998-02-16","ciudad":"Madrid","pais":"España","genero":"hombre","telefono":"612345789","correo":"natxo98@gmail.com"},),
		({"usuario":"nacho98","nombre":"Nacho","apellido1":"Dorado","apellido2":"Ruiz","fecha_nacimiento":"1998-02-16","ciudad":"Madrid","pais":"España","genero":"mujer","telefono":"612345789","correo":"natxo98@gmail.com"},)
	]
)
def test_modelo_usuario_genero_incorrecto(usuario):

	with pytest.raises(ValueError):

		Usuario(**usuario)

@pytest.mark.parametrize(["usuario"],
	[
		({"usuario":"nacho98","nombre":"Nacho","apellido1":"Dorado","apellido2":"Ruiz","fecha_nacimiento":"1998-02-16","ciudad":"Madrid","pais":"España","genero":"Masculino","telefono":"112345789","correo":"natxo98@gmail.com"},),
		({"usuario":"nacho98","nombre":"Nacho","apellido1":"Dorado","apellido2":"Ruiz","fecha_nacimiento":"1998-02-16","ciudad":"Madrid","pais":"España","genero":"Masculino","telefono":"512345789","correo":"natxo98@gmail.com"},),
		({"usuario":"nacho98","nombre":"Nacho","apellido1":"Dorado","apellido2":"Ruiz","fecha_nacimiento":"1998-02-16","ciudad":"Madrid","pais":"España","genero":"Masculino","telefono":"91123457","correo":"natxo98@gmail.com"},),
		({"usuario":"nacho98","nombre":"Nacho","apellido1":"Dorado","apellido2":"Ruiz","fecha_nacimiento":"1998-02-16","ciudad":"Madrid","pais":"España","genero":"Masculino","telefono":"61234578a","correo":"natxo98@gmail.com"},),
		({"usuario":"nacho98","nombre":"Nacho","apellido1":"Dorado","apellido2":"Ruiz","fecha_nacimiento":"1998-02-16","ciudad":"Madrid","pais":"España","genero":"Masculino","telefono":"61234aa78","correo":"natxo98@gmail.com"},)	
	]
)
def test_modelo_usuario_telefono_incorrecto(usuario):

	with pytest.raises(ValueError):

		Usuario(**usuario)

@pytest.mark.parametrize(["usuario"],
	[
		({"usuario":"nacho98","nombre":"Nacho","apellido1":"Dorado","apellido2":"Ruiz","fecha_nacimiento":"1998-02-16","ciudad":"Madrid","pais":"España","genero":"Masculino","telefono":"612345789","correo":"natxo98gmail.com"},),
		({"usuario":"nacho98","nombre":"Nacho","apellido1":"Dorado","apellido2":"Ruiz","fecha_nacimiento":"1998-02-16","ciudad":"Madrid","pais":"España","genero":"Masculino","telefono":"612345789","correo":"natxo98@gmail.om"},),
		({"usuario":"nacho98","nombre":"Nacho","apellido1":"Dorado","apellido2":"Ruiz","fecha_nacimiento":"1998-02-16","ciudad":"Madrid","pais":"España","genero":"Masculino","telefono":"612345789","correo":"natxo98@gmailcom"},),
		({"usuario":"nacho98","nombre":"Nacho","apellido1":"Dorado","apellido2":"Ruiz","fecha_nacimiento":"1998-02-16","ciudad":"Madrid","pais":"España","genero":"Femenino","telefono":"612345789","correo":"natxo98@gmail."},),
		({"usuario":"nacho98","nombre":"Nacho","apellido1":"Dorado","apellido2":"Ruiz","fecha_nacimiento":"1998-02-16","ciudad":"Madrid","pais":"España","genero":"Femenino","telefono":"612345789","correo":"natxo98@gmail.ese"},),
		({"usuario":"nacho98","nombre":"Nacho","apellido1":"Dorado","apellido2":"Ruiz","fecha_nacimiento":"1998-02-16","ciudad":"Madrid","pais":"España","genero":"Femenino","telefono":"612345789","correo":"@gmail.com"},),
		({"usuario":"nacho98","nombre":"Nacho","apellido1":"Dorado","apellido2":"Ruiz","fecha_nacimiento":"1998-02-16","ciudad":"Madrid","pais":"España","genero":"Femenino","telefono":"612345789","correo":"natxo98@.com"},)
	]
)
def test_modelo_usuario_correo_incorrecto(usuario):

	with pytest.raises(ValueError):

		Usuario(**usuario)

@pytest.mark.parametrize(["usuario"],
	[
		({"usuario":"nacho98","nombre":"Nacho","apellido1":"Dorado","apellido2":"Ruiz","fecha_nacimiento":"1998-02-16","ciudad":"Madrid","pais":"España","genero":"masculino","telefono":"612345789","correo":"natxo98@gmail.com"},),
		({"usuario":"nacho98","nombre":"Nacho","apellido1":"Dorado","apellido2":"Ruiz","fecha_nacimiento":"2000-02-16","ciudad":"Madrid","pais":"España","genero":"masculino","telefono":"612345789","correo":"natxo98@gmail.com"},),
		({"usuario":"nacho98","nombre":"Nacho","apellido1":"Dorado","apellido2":"Ruiz","fecha_nacimiento":"1998-02-16","ciudad":"Madrid","pais":"España","genero":"MASCULINO","telefono":"612345789","correo":"natxo98@gmail.com"},),
		({"usuario":"nacho98","nombre":"Nacho","apellido1":"Dorado","apellido2":"Ruiz","fecha_nacimiento":"1998-02-16","ciudad":"Madrid","pais":"España","genero":"FEMENINO","telefono":"612345789","correo":"natxo98@gmail.com"},),
		({"usuario":"nacho98","nombre":"Nacho","apellido1":"Dorado","apellido2":"Ruiz","fecha_nacimiento":"1998-02-16","ciudad":"Madrid","pais":"España","genero":"masculino","telefono":"611111111","correo":"natxo98@gmail.com"},),
		({"usuario":"nacho98","nombre":"Nacho","apellido1":"Dorado","apellido2":"Ruiz","fecha_nacimiento":"1998-02-16","ciudad":"Madrid","pais":"España","genero":"masculino","telefono":"900000000","correo":"natxo98@gmail.com"},),
		({"usuario":"nacho98","nombre":"Nacho","apellido1":"Dorado","apellido2":"Ruiz","fecha_nacimiento":"1998-02-16","ciudad":"Madrid","pais":"España","genero":"masculino","telefono":"612345789","correo":"na98@gmail.com"},),
		({"usuario":"nacho98","nombre":"Nacho","apellido1":"Dorado","apellido2":"Ruiz","fecha_nacimiento":"1998-02-16","ciudad":"Madrid","pais":"España","genero":"masculino","telefono":"612345789","correo":"natxo98@gmail.es"},),
		({"usuario":"nacho98","nombre":"Nacho","apellido1":"Dorado","apellido2":"Ruiz","fecha_nacimiento":"1998-02-16","ciudad":"Madrid","pais":"España","genero":"masculino","telefono":"612345789","correo":"nacho.golden@hotmail.com"},),
		({"usuario":"nacho98","nombre":"Nacho","apellido1":"Dorado","apellido2":"Ruiz","fecha_nacimiento":"1998-02-16","ciudad":"Madrid","pais":"España","genero":"masculino","telefono":"612345789","correo":"natxo98@ucm.com"},)	
	]
)
def test_modelo_usuario_correcto(usuario):

	Usuario(**usuario)

@pytest.mark.parametrize(["usuario"],
	[
		({"usuario":"nacho98","nombre":"Nacho","apellido1":"Dorado","apellido2":"Ruiz","fecha_nacimiento":"1998-02-16","ciudad":"Madrid","pais":"España","genero":"masculino","telefono":"612345789","correo":"natxo98@gmail.com", "contrasena":"1234567"},),
		({"usuario":"nacho98","nombre":"Nacho","apellido1":"Dorado","apellido2":"Ruiz","fecha_nacimiento":"2000-02-16","ciudad":"Madrid","pais":"España","genero":"masculino","telefono":"612345789","correo":"natxo98@gmail.com", "contrasena":"123456789"},),
		({"usuario":"nacho98","nombre":"Nacho","apellido1":"Dorado","apellido2":"Ruiz","fecha_nacimiento":"1998-02-16","ciudad":"Madrid","pais":"España","genero":"MASCULINO","telefono":"612345789","correo":"natxo98@gmail.com", "contrasena":"12345"},),
		({"usuario":"nacho98","nombre":"Nacho","apellido1":"Dorado","apellido2":"Ruiz","fecha_nacimiento":"1998-02-16","ciudad":"Madrid","pais":"España","genero":"FEMENINO","telefono":"612345789","correo":"natxo98@gmail.com", "contrasena":"1234567 8"},),
		({"usuario":"nacho98","nombre":"Nacho","apellido1":"Dorado","apellido2":"Ruiz","fecha_nacimiento":"1998-02-16","ciudad":"Madrid","pais":"España","genero":"masculino","telefono":"611111111","correo":"natxo98@gmail.com", "contrasena":"dsgfdgfdhfdhf d"},),
		({"usuario":"nacho98","nombre":"Nacho","apellido1":"Dorado","apellido2":"Ruiz","fecha_nacimiento":"1998-02-16","ciudad":"Madrid","pais":"España","genero":"masculino","telefono":"900000000","correo":"natxo98@gmail.com", "contrasena":"fbfdg123456789vds"},)
	]
)
def test_modelo_usuario_bbdd_contrasena_incorrecta(usuario):

	with pytest.raises(ValueError):

		UsuarioBBDD(**usuario)

@pytest.mark.parametrize(["usuario"],
	[
		({"usuario":"nacho98","nombre":"Nacho","apellido1":"Dorado","apellido2":"Ruiz","fecha_nacimiento":"1998-02-16","ciudad":"Madrid","pais":"España","genero":"masculino","telefono":"612345789","correo":"natxo98@gmail.com", "contrasena":"12345678"},),
		({"usuario":"nacho98","nombre":"Nacho","apellido1":"Dorado","apellido2":"Ruiz","fecha_nacimiento":"2000-02-16","ciudad":"Madrid","pais":"España","genero":"masculino","telefono":"612345789","correo":"natxo98@gmail.com", "contrasena":"12345fdfdg"},),
		({"usuario":"nacho98","nombre":"Nacho","apellido1":"Dorado","apellido2":"Ruiz","fecha_nacimiento":"1998-02-16","ciudad":"Madrid","pais":"España","genero":"MASCULINO","telefono":"612345789","correo":"natxo98@gmail.com", "contrasena":"12345fdfdhfg"},),
		({"usuario":"nacho98","nombre":"Nacho","apellido1":"Dorado","apellido2":"Ruiz","fecha_nacimiento":"1998-02-16","ciudad":"Madrid","pais":"España","genero":"FEMENINO","telefono":"612345789","correo":"natxo98@gmail.com", "contrasena":"1234567gfdhfdh8"},),
		({"usuario":"nacho98","nombre":"Nacho","apellido1":"Dorado","apellido2":"Ruiz","fecha_nacimiento":"1998-02-16","ciudad":"Madrid","pais":"España","genero":"masculino","telefono":"611111111","correo":"natxo98@gmail.com", "contrasena":"contrasena1234"},)
	]
)
def test_modelo_usuario_bbdd_correcto(usuario):

	UsuarioBBDD(**usuario)