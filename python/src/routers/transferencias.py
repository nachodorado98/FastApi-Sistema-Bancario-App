from fastapi import APIRouter, status, Depends, HTTPException
from typing import Dict, List
import uuid
import datetime

from src.database.sesion import crearSesion
from src.database.conexion import Conexion

from src.modelos.token import Payload
from src.modelos.transferencia import TransferenciaBasica, Transferencia
from src.modelos.transferencia_utils import obtenerObjetosTransferencia

from src.autenticacion.auth_utils import decodificarToken


router_transferencias=APIRouter(prefix="/transferencias", tags=["Transferencias"])

@router_transferencias.get("", status_code=status.HTTP_200_OK, summary="Devuelve las transferencias del usuario")
async def obtenerTransferencias(payload:Payload=Depends(decodificarToken), con:Conexion=Depends(crearSesion))->List[Transferencia]:

	"""
	Devuelve los diccionarios asociados a las transferencias del usuario.

	## Respuesta

	200 (OK): Si se obtienen las transferencias correctamente

	- **Transferencia**: El id de la transferencia (str).
	- **Usuario_origen**: El usuario origen de la transferencia (str).
	- **Usuario_destino**: El usuario destino de la transferencia (str).
	- **Concepto**: El concepto de la transferencia (str).
	- **Cantidad**: La cantidad de la transferencia (float).
	- **Fecha**: La fecha de la transferencia en formato yyyy-mm-dd (str)

	401 (UNAUTHORIZED): Si los datos no son correctos

	- **Mensaje**: El mensaje de la excepcion (str).

	404 (NOT FOUND): Si no se obtienen las transferencias correctamente

	- **Mensaje**: El mensaje de la excepcion (str).
	"""

	transferencias=con.obtenerTransferencias(payload.sub)

	con.cerrarConexion()

	if transferencias is None:

		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transferencias no existentes")

	return obtenerObjetosTransferencia(transferencias)


@router_transferencias.post("", status_code=status.HTTP_201_CREATED, summary="Realiza una transferencia")
async def realizarTransferencia(transferencia:TransferenciaBasica, payload:Payload=Depends(decodificarToken), con:Conexion=Depends(crearSesion))->Dict:

	"""
	Realiza una transferencia al usuario indicado y lo inserta en la BBDD.

	Devuelve un mensaje de confirmacion de la transferencia y el saldo actual.

	## Respuesta

	201 (CREATED): Si se realiza la transferencia correctamente

	- **Mensaje**: El mensaje de transferencia correcto al usuario (str).
	- **Saldo**: El saldo del usuario (float).

	400 (BAD REQUEST): Si no se realiza la transferencia correctamente

	- **Mensaje**: El mensaje de la excepcion (str).

	401 (UNAUTHORIZED): Si los datos no son correctos

	- **Mensaje**: El mensaje de la excepcion (str).
	"""

	if transferencia.cantidad<=0.0:

		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cantidad a transferir erronea")

	saldo_actual_origen=con.obtenerSaldo(payload.sub)

	if transferencia.cantidad>saldo_actual_origen:

		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cantidad a transferir superior al saldo")

	if not con.existe_usuario(transferencia.usuario_destino):

		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario destino no existente")

	if transferencia.usuario_destino==payload.sub:

		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario destino igual que usuario origen")

	saldo_actualizado_origen=saldo_actual_origen-transferencia.cantidad

	con.actualizarSaldo(payload.sub, saldo_actualizado_origen)

	fecha=datetime.datetime.now().strftime("%Y-%m-%d")

	transaccion_id_origen=uuid.uuid4().hex

	con.insertarTransaccion(transaccion_id_origen, payload.sub, transferencia.concepto, -transferencia.cantidad, fecha, saldo_actualizado_origen)

	saldo_actual_destino=con.obtenerSaldo(transferencia.usuario_destino)

	saldo_actualizado_destino=saldo_actual_destino+transferencia.cantidad

	con.actualizarSaldo(transferencia.usuario_destino, saldo_actualizado_destino)

	transaccion_id_destino=uuid.uuid4().hex

	con.insertarTransaccion(transaccion_id_destino, transferencia.usuario_destino, transferencia.concepto, transferencia.cantidad, fecha, saldo_actualizado_destino)

	con.insertarTransferencia(uuid.uuid4().hex, transaccion_id_origen, transaccion_id_destino, transferencia.cantidad)

	con.cerrarConexion()

	return {"mensaje":"Transferencia realizada correctamente",
			"saldo":saldo_actualizado_origen}

@router_transferencias.get("/realizadas", status_code=status.HTTP_200_OK, summary="Devuelve las transferencias realizadas del usuario")
async def obtenerTransferenciasRealizadas(payload:Payload=Depends(decodificarToken), con:Conexion=Depends(crearSesion))->List[Transferencia]:

	"""
	Devuelve los diccionarios asociados a las transferencias realizadas por el usuario.

	## Respuesta

	200 (OK): Si se obtienen las transferencias realizadas correctamente

	- **Transferencia**: El id de la transferencia (str).
	- **Usuario_origen**: El usuario origen de la transferencia (str).
	- **Usuario_destino**: El usuario destino de la transferencia (str).
	- **Concepto**: El concepto de la transferencia (str).
	- **Cantidad**: La cantidad de la transferencia (float).
	- **Fecha**: La fecha de la transferencia en formato yyyy-mm-dd (str)

	401 (UNAUTHORIZED): Si los datos no son correctos

	- **Mensaje**: El mensaje de la excepcion (str).

	404 (NOT FOUND): Si no se obtienen las transferencias realizadas correctamente

	- **Mensaje**: El mensaje de la excepcion (str).
	"""

	transferencias=con.obtenerTransferenciasRealizadas(payload.sub)

	con.cerrarConexion()

	if transferencias is None:

		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transferencias realizadas no existentes")

	return obtenerObjetosTransferencia(transferencias)

@router_transferencias.get("/recibidas", status_code=status.HTTP_200_OK, summary="Devuelve las transferencias recibidas del usuario")
async def obtenerTransferenciasRecibidas(payload:Payload=Depends(decodificarToken), con:Conexion=Depends(crearSesion))->List[Transferencia]:

	"""
	Devuelve los diccionarios asociados a las transferencias recibidas del usuario.

	## Respuesta

	200 (OK): Si se obtienen las transferencias recibidas correctamente

	- **Transferencia**: El id de la transferencia (str).
	- **Usuario_origen**: El usuario origen de la transferencia (str).
	- **Usuario_destino**: El usuario destino de la transferencia (str).
	- **Concepto**: El concepto de la transferencia (str).
	- **Cantidad**: La cantidad de la transferencia (float).
	- **Fecha**: La fecha de la transferencia en formato yyyy-mm-dd (str)

	401 (UNAUTHORIZED): Si los datos no son correctos

	- **Mensaje**: El mensaje de la excepcion (str).

	404 (NOT FOUND): Si no se obtienen las transferencias recibidas correctamente

	- **Mensaje**: El mensaje de la excepcion (str).
	"""

	transferencias=con.obtenerTransferenciasRecibidas(payload.sub)

	con.cerrarConexion()

	if transferencias is None:

		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transferencias recibidas no existentes")

	return obtenerObjetosTransferencia(transferencias)