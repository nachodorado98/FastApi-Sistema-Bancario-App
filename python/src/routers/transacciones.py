from fastapi import APIRouter, status, Depends, HTTPException
from typing import List, Dict

from src.database.sesion import crearSesion
from src.database.conexion import Conexion

from src.modelos.token import Payload

from src.autenticacion.auth_utils import decodificarToken


router_transacciones=APIRouter(prefix="/transacciones", tags=["Transacciones"])


@router_transacciones.get("", status_code=status.HTTP_200_OK, summary="Devuelve las transacciones del usuario")
async def obtenerTransacciones(payload:Payload=Depends(decodificarToken), con:Conexion=Depends(crearSesion))->List[Dict]:

	"""
	Devuelve los diccionarios asociados a las transacciones del usuario.

	## Respuesta

	200 (OK): Si se obtienen las transacciones correctamente

	- **Transaccion**: El id de la transaccion (str).
	- **Concepto**: El concepto de la transaccion (str).
	- **Cantidad**: La cantidad de la transaccion (float).
	- **Fecha**: La fecha de la transaccion en formato yyyy-mm-dd (str)
	- **Historico**: El historico de la transaccion (float).

	401 (UNAUTHORIZED): Si los datos no son correctos

	- **Mensaje**: El mensaje de la excepcion (str).

	404 (NOT FOUND): Si no se obtienen las transacciones correctamente

	- **Mensaje**: El mensaje de la excepcion (str).
	"""

	transacciones=con.obtenerTransacciones(payload.sub)

	con.cerrarConexion()

	if transacciones is None:

		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transacciones no existentes")

	return transacciones