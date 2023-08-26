from pydantic import BaseModel, validator
import re

class Contrasena(BaseModel):

	contrasena_antigua:str
	contrasena_nueva:str

	# Metodo para validar la contraseña nueva
	@validator("contrasena_nueva")
	def comprobarContrasenaNueva(cls, contrasena_nueva:str)->str:

		if len(contrasena_nueva)<8 or " " in contrasena_nueva or "123456789" in contrasena_nueva or "987654321" in contrasena_nueva:

			raise ValueError("la contraseña no cumple los requisitos")

		return contrasena_nueva

	class Config:

		json_schema_extra={"example":{"contrasena_antigua":"123456789",
										"contrasena_nueva":"987654321"}}