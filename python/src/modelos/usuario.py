from pydantic import BaseModel, validator
import datetime
import re

class UsuarioBasico(BaseModel):

	usuario:str

class Usuario(UsuarioBasico):

	nombre:str
	apellido1:str
	apellido2:str
	fecha_nacimiento:str
	ciudad:str
	pais:str
	genero:str
	telefono:str
	correo:str

	# Metodo para validar la fecha de nacimiento
	@validator("fecha_nacimiento")
	def comprobarFecha(cls, fecha_nacimiento:str)->str:

		try:

			fecha_datetime=datetime.datetime.strptime(fecha_nacimiento, "%Y-%m-%d")

		except:

			raise ValueError("el formato de edad no es correcto")

		diferencia=(datetime.datetime.today()-fecha_datetime).days

		diferencia_anos=diferencia//365

		if diferencia_anos<18 or diferencia_anos>99:

			raise ValueError("la edad no esta dentro del rango")

		return fecha_nacimiento

	# Metodo para validar el genero
	@validator("genero")
	def comprobarGenero(cls, genero:str)->str:

		if genero.title()!="Masculino" and genero.title()!="Femenino":

			raise ValueError("el genero no esta entre los posibles")

		return genero

	# Metodo para validar el telefono
	@validator("telefono")
	def comprobarTelefono(cls, telefono:str)->str:

		patron=r"[69][0-9]{8}"

		if not re.search(patron, telefono):

			raise ValueError("el telefono no es correcto")

		return telefono

	# Metodo para validar el correo
	@validator("correo")
	def comprobarCorreo(cls, correo:str)->str:

		patron=r"[a-zA-Z0-9_\.]+@[a-zA-Z0-9]+(\.com|\.es)$"

		if not re.search(patron, correo):

			raise ValueError("el correo no es correcto")

		return correo

class UsuarioBBDD(Usuario):

	contrasena:str

	# Metodo para validar la contraseña
	@validator("contrasena")
	def comprobarContrasena(cls, contrasena:str)->str:

		if len(contrasena)<8 or " " in contrasena or "123456789" in contrasena:

			raise ValueError("la contraseña no cumple los requisitos")

		return contrasena

	class Config:

		json_schema_extra={"example":{"usuario":"nacho98",
										"nombre":"Nacho",
										"apellido1":"Dorado",
										"apellido2":"Ruiz",
										"fecha_nacimiento":"1998-02-16",
										"ciudad":"Madrid",
										"pais":"España",
										"genero":"Masculino",
										"telefono":"612345789",
										"correo":"natxo98@gmail.com",
										"contrasena":"123456789"}}

	