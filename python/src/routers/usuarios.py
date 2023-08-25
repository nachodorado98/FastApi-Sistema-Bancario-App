from fastapi import APIRouter, status, Depends, HTTPException, BackgroundTasks
from typing import List, Dict

from src.database.sesion import crearSesion
from src.database.conexion import Conexion

from src.modelos.usuario import UsuarioBBDD, UsuarioBasico
from src.modelos.usuario_utils import obtenerObjetosUsuarioBasico

from src.utilidades.utils import generarHash, enviarCorreo

router_usuarios=APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router_usuarios.post("", status_code=status.HTTP_201_CREATED, summary="Crea un usuario")
async def crearUsuario(usuario:UsuarioBBDD,
						tarea:BackgroundTasks,
						con:Conexion=Depends(crearSesion))->Dict:

	"""
	Crea un usuario y lo inserta en la BBDD.

	Devuelve un mensaje y el diccionario que representa el usuario creado.

	## Respuesta

	201 (CREATED): Si se crea el usuario correctamente

	- **Mensaje**: El mensaje de creacion correcto del usuario (str).
	- **Usuario**: El usuario con el usuario, nombre y saldo (Dict).

	400 (BAD REQUEST): Si no se crea el usuario correctamente

	- **Mensaje**: El mensaje de la excepcion (str).
	"""

	if con.existe_usuario(usuario.usuario):

		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario existente")

	con.insertarUsuario(usuario.usuario,
						usuario.nombre.title(),
						usuario.apellido1.title(),
						usuario.apellido2.title(),
						usuario.fecha_nacimiento,
						usuario.ciudad.title(),
						usuario.pais.title(),
						usuario.genero.title(),
						usuario.telefono,
						usuario.correo,
						generarHash(usuario.contrasena))

	con.cerrarConexion()

	tarea.add_task(enviarCorreo, usuario.correo, usuario.usuario, usuario.nombre)

	return {"mensaje":"Usuario creado correctamente",
			"usuario":{"usuario":usuario.usuario,
						"nombre":usuario.nombre.title(),
						"saldo":0.0}}

@router_usuarios.get("", status_code=status.HTTP_200_OK, summary="Devuelve los usuarios existentes")
async def obtenerUsuarios(con:Conexion=Depends(crearSesion))->List[UsuarioBasico]:

	"""
	Devuelve los diccionarios asociados a los usuarios disponibles en la BBDD.

	## Respuesta

	200 (OK): Si se obtienen los usuarios correctamente

	- **Usuario**: El usuario del usuario (str).

	404 (NOT FOUND): Si no se obtienen los usuarios correctamente

	- **Mensaje**: El mensaje de la excepcion (str).
	"""

	usuarios=con.obtenerUsuarios()

	con.cerrarConexion()

	if usuarios is None:

		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuarios no existentes")

	return obtenerObjetosUsuarioBasico(usuarios)