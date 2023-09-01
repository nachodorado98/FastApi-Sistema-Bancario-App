from .transaccion import TransaccionBasica

class TransferenciaBasica(TransaccionBasica):

	usuario_destino:str

class Transferencia(TransferenciaBasica):

	transferencia:str
	usuario_origen:str
	fecha:str