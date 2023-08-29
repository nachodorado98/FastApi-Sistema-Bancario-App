from fastapi import APIRouter, status, Depends, HTTPException
from typing import List, Dict
import uuid
import datetime

from src.database.sesion import crearSesion
from src.database.conexion import Conexion

from src.modelos.token import Payload
from src.modelos.transaccion import Transaccion, TransaccionBasica
from src.modelos.transaccion_utils import obtenerObjetosTransaccion

from src.autenticacion.auth_utils import decodificarToken


router_transacciones=APIRouter(prefix="/transacciones", tags=["Transacciones"])


@router_transacciones.get("", status_code=status.HTTP_200_OK, summary="Devuelve las transacciones del usuario")
async def obtenerTransacciones(payload:Payload=Depends(decodificarToken), con:Conexion=Depends(crearSesion))->List[Transaccion]:

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

	return obtenerObjetosTransaccion(transacciones)


@router_transacciones.post("/ingresar", status_code=status.HTTP_201_CREATED, summary="Realiza un ingreso del usuario")
async def realizarIngreso(transaccion:TransaccionBasica, payload:Payload=Depends(decodificarToken), con:Conexion=Depends(crearSesion))->Dict:

	"""
	Realiza una transaccion de ingreso y lo inserta en la BBDD.

	Devuelve un mensaje de confirmacion del ingreso.

	## Respuesta

	201 (CREATED): Si se realiza el ingreso correctamente

	- **Mensaje**: El mensaje de ingreso correcto del usuario (str).

	400 (BAD REQUEST): Si no se realiza el ingreso correctamente

	- **Mensaje**: El mensaje de la excepcion (str).

	401 (UNAUTHORIZED): Si los datos no son correctos

	- **Mensaje**: El mensaje de la excepcion (str).
	"""

	if transaccion.cantidad<=0.0:

		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cantidad erronea")

	saldo_actual=con.obtenerSaldo(payload.sub)

	saldo_actualizado=saldo_actual+transaccion.cantidad

	con.actualizarSaldo("nacho98", saldo_actualizado)

	transaccion_id=uuid.uuid4().hex

	fecha=datetime.datetime.now().strftime("%Y-%m-%d")

	con.insertarTransaccion(transaccion_id, payload.sub, transaccion.concepto, transaccion.cantidad, fecha, saldo_actualizado)

	con.cerrarConexion()

	return {"mensaje":"Ingreso realizado correctamente"}