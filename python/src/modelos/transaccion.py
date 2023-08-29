from pydantic import BaseModel

class TransaccionBasica(BaseModel):

	concepto:str
	cantidad:float

class Transaccion(TransaccionBasica):

	transaccion:str
	fecha:str
	historico:float
