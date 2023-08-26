from fastapi import APIRouter, status, Depends, HTTPException, BackgroundTasks
from typing import List, Dict

from src.database.sesion import crearSesion
from src.database.conexion import Conexion

from src.modelos.usuario import UsuarioBBDD, UsuarioBasico, Usuario
from src.modelos.usuario_utils import obtenerObjetosUsuarioBasico, obtenerObjetoUsuario
from src.modelos.token import Payload
from src.modelos.telefono import Telefono
from src.modelos.contrasena import Contrasena

from src.utilidades.utils import generarHash, enviarCorreo, comprobarHash

from src.autenticacion.auth_utils import decodificarToken

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

@router_usuarios.get("/me", status_code=status.HTTP_200_OK, summary="Devuelve los datos del usuario")
async def obtenerPerfil(payload:Payload=Depends(decodificarToken), con:Conexion=Depends(crearSesion))->Usuario:

	"""
	Devuelve el diccionario de los datos del usuario.

	## Respuesta

	200 (OK): Si se obtienen los datos del usuario correctamente

	- **Usuario**: El nombre de usuario del usuario (str).
	- **Nombre**: El nombre del usuario (str).
	- **Apellido1**: El primer apellido del usuario (str).
	- **Apellido2**: El segundo apellido del usuario (str).
	- **Fecha_nacimiento**: La fecha de nacimiento del usuario en formato yyyy-mm-dd (str).
	- **Ciudad**: La ciudad del usuario (str).
	- **Pais**: El pais del usuario (str).
	- **Genero**: El genero del usuario (str).
	- **Telefono**: El telefono del usuario (str).
	- **Correo**: El correo del usuario (str).

	401 (UNAUTHORIZED): Si los datos no son correctos

	- **Mensaje**: El mensaje de la excepcion (str).
	"""

	datos_usuario=con.obtenerDatosUsuario(payload.sub)

	con.cerrarConexion()

	return obtenerObjetoUsuario(datos_usuario)

@router_usuarios.patch("/me/actualizar_telefono", status_code=status.HTTP_200_OK, summary="Actualiza el telefono del usuario")
async def actualizarTelefono(telefono:Telefono, payload:Payload=Depends(decodificarToken), con:Conexion=Depends(crearSesion))->Dict:

	"""
	Actualiza el telefono del usuario a uno nuevo.

	Devuelve un mensaje y el diccionario que representa el telefono actualizado.

	## Respuesta

	200 (OK): Si se actualiza el telefono correctamente

	- **Mensaje**: El mensaje de actualizacion del telefono (str).
	- **Telefono**: El telefono con el telefono antiguo y el telefono actualizado (Dict).

	400 (BAD REQUEST): Si no se actualiza el telefono correctamente

	- **Mensaje**: El mensaje de la excepcion (str).

	401 (UNAUTHORIZED): Si los datos no son correctos

	- **Mensaje**: El mensaje de la excepcion (str).
	"""

	telefono_usuario=con.obtenerDatosUsuario(payload.sub)["telefono"]

	if telefono.telefono==telefono_usuario:

		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El telefono es el mismo")

	con.actualizarTelefono(payload.sub, telefono.telefono)

	con.cerrarConexion()

	return {"mensaje":"Telefono actualizado correctamente",
			"telefono":{"telefono antiguo":telefono_usuario,
						"telefono nuevo":telefono.telefono}}


@router_usuarios.patch("/me/cambiar_contrasena", status_code=status.HTTP_200_OK, summary="Cambia la contraseña del usuario")
async def cambiarContrasena(contrasena:Contrasena, payload:Payload=Depends(decodificarToken), con:Conexion=Depends(crearSesion))->Dict:

	"""
	Cambia/Actualiza la contraseña antigua del usuario a la nueva contraseña.

	Devuelve un mensaje de confirmacion.

	## Respuesta

	200 (OK): Si se cambia la contraseña correctamente

	- **Mensaje**: El mensaje del cambio/actualizacion de la contraseña (str).

	400 (BAD REQUEST): Si no se cambia la contraseña correctamente

	- **Mensaje**: El mensaje de la excepcion (str).

	401 (UNAUTHORIZED): Si los datos no son correctos

	- **Mensaje**: El mensaje de la excepcion (str).
	"""

	if contrasena.contrasena_antigua==contrasena.contrasena_nueva:

		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Las contraseñas son iguales", headers={"WWW-Authentication":"Bearer"})		

	hash_contrasena=con.obtenerContrasena(payload.sub)

	if not comprobarHash(contrasena.contrasena_antigua, hash_contrasena):

		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña antigua no es correcta", headers={"WWW-Authentication":"Bearer"})		

	con.cambiarContrasena(payload.sub, generarHash(contrasena.contrasena_nueva))

	con.cerrarConexion()

	return {"mensaje":"Contrasena cambiada correctamente"}