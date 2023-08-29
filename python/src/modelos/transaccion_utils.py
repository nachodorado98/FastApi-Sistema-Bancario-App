from typing import Dict, List
import datetime

from .transaccion import Transaccion

# Funcion para obtener un objeto transaccion
def obtenerObjetoTransaccion(valores:Dict)->Transaccion:

	return Transaccion(transaccion=valores["transaccion"],
						concepto=valores["concepto"],
						cantidad=valores["cantidad"],
						fecha=valores["fecha"].strftime("%Y-%m-%d"),
						historico=valores["historico"])

# Funcion para obtener varios objetos transaccion
def obtenerObjetosTransaccion(lista_valores:List[Dict])->List[Transaccion]:

	return [obtenerObjetoTransaccion(valor) for valor in lista_valores]