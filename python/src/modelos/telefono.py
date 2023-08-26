from pydantic import BaseModel, validator
import re

class Telefono(BaseModel):

	telefono:str

	# Metodo para validar el telefono
	@validator("telefono")
	def comprobarTelefono(cls, telefono:str)->str:

		patron=r"[69][0-9]{8}"

		if not re.search(patron, telefono):

			raise ValueError("el telefono no es correcto")

		return telefono

	class Config:

		json_schema_extra={"example":{"telefono":"612345789"}}