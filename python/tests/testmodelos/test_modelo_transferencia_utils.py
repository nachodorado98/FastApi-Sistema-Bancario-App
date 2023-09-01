import datetime

from src.modelos.transferencia import Transferencia
from src.modelos.transferencia_utils import obtenerObjetoTransferencia, obtenerObjetosTransferencia

def test_obtener_transferencia():

	transferencia={"transferencia":"12345", "usuario_origen":"nacho", "usuario_destino":"amanda", 
					"concepto":"concepto","cantidad":1.0, "fecha":datetime.datetime(2023,9,1)}

	objeto=obtenerObjetoTransferencia(transferencia)

	assert isinstance(objeto, Transferencia)
	assert objeto.fecha=="2023-09-01"


def test_obtener_varias_transferencias():

	transferencias=[{"transferencia":"12345", "usuario_origen":"nacho", "usuario_destino":"amanda", 
					"concepto":"concepto","cantidad":1.0, "fecha":datetime.datetime(2023,9,1)},
					{"transferencia":"12345", "usuario_origen":"nacho", "usuario_destino":"amanda", 
					"concepto":"concepto","cantidad":1.0, "fecha":datetime.datetime(2023,9,1)},
					{"transferencia":"12345", "usuario_origen":"nacho", "usuario_destino":"amanda", 
					"concepto":"concepto","cantidad":1.0, "fecha":datetime.datetime(2023,9,1)}]

	objetos=obtenerObjetosTransferencia(transferencias)

	assert len(objetos)==3

	for objeto in objetos:

		assert isinstance(objeto, Transferencia)
		assert objeto.fecha=="2023-09-01"