from typing import Dict, List
import datetime

from .usuario import UsuarioBasico, Usuario

# Funcion para obtener un objeto usuario basico
def obtenerObjetoUsuarioBasico(valores:Dict)->UsuarioBasico:

	return UsuarioBasico(**valores)

# Funcion para obtener varios objetos usuario basico
def obtenerObjetosUsuarioBasico(lista_valores:List[Dict])->List[UsuarioBasico]:

	return [obtenerObjetoUsuarioBasico(valor) for valor in lista_valores]

# Funcion para obtener un objeto usuario
def obtenerObjetoUsuario(valores:Dict)->Usuario:

	return Usuario(usuario=valores["usuario"],
					nombre=valores["nombre"],
					apellido1=valores["apellido1"],
					apellido2=valores["apellido2"],
					fecha_nacimiento=valores["fecha_nacimiento"].strftime("%Y-%m-%d"),
					ciudad=valores["ciudad"],
					pais=valores["pais"],
					genero=valores["genero"],
					telefono=valores["telefono"],
					correo=valores["correo"])