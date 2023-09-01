from typing import Dict, List
import datetime

from .transferencia import Transferencia

# Funcion para obtener un objeto transferencia
def obtenerObjetoTransferencia(valores:Dict)->Transferencia:

	return Transferencia(transferencia=valores["transferencia"],
						usuario_origen=valores["usuario_origen"],
						usuario_destino=valores["usuario_destino"],
						concepto=valores["concepto"],
						cantidad=valores["cantidad"],
						fecha=valores["fecha"].strftime("%Y-%m-%d"))

# Funcion para obtener varios objetos transferencia
def obtenerObjetosTransferencia(lista_valores:List[Dict])->List[Transferencia]:

	return [obtenerObjetoTransferencia(valor) for valor in lista_valores]