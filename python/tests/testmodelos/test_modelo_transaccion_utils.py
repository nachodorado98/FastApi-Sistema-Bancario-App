import datetime

from src.modelos.transaccion import Transaccion
from src.modelos.transaccion_utils import obtenerObjetoTransaccion, obtenerObjetosTransaccion 

def test_obtener_transaccion():

	transaccion={"transaccion":"12345", "concepto":"concepto","cantidad":1.0,
				"fecha":datetime.datetime(2023,8,28), "historico":2.0}

	objeto=obtenerObjetoTransaccion(transaccion)

	assert isinstance(objeto, Transaccion)
	assert objeto.fecha=="2023-08-28"


def test_obtener_varias_transacciones():

	transacciones=[{"transaccion":"12345", "concepto":"concepto","cantidad":1.0,
				"fecha":datetime.datetime(2023,8,28), "historico":2.0},
				{"transaccion":"12345", "concepto":"concepto","cantidad":1.0,
				"fecha":datetime.datetime(2023,8,28), "historico":2.0},
				{"transaccion":"12345", "concepto":"concepto","cantidad":1.0,
				"fecha":datetime.datetime(2023,8,28), "historico":2.0}]

	objetos=obtenerObjetosTransaccion(transacciones)

	assert len(objetos)==3

	for objeto in objetos:

		assert isinstance(objeto, Transaccion)
		assert objeto.fecha=="2023-08-28"