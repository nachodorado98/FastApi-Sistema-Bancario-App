from passlib.context import CryptContext
import smtplib

from .confutils import CORREO, CONTRASENA

# Funcion para generar el hash de una contraseña
def generarHash(contrasena:str)->str:

	objeto_hash=CryptContext(schemes=["bcrypt"], deprecated="auto")

	return objeto_hash.hash(contrasena)

# Funcion para comprobar el hash y la contraseña
def comprobarHash(contrasena:str, contrasena_hash:str)->bool:

	objeto_hash=CryptContext(schemes=["bcrypt"], deprecated="auto")

	return objeto_hash.verify(contrasena, contrasena_hash)

# Funcion para enviar el correo al usuario
def enviarCorreo(correo_usuario:str, usuario_usuario:str, nombre_usuario:str)->bool:

	mensaje=f"""From:{CORREO}
	To:{correo_usuario}
	Subject:SUBSCRIPCION SISTEMA BANCARIO\n
	Bienvenido {nombre_usuario}!
	Te has subscrito a la API del Sistema Bancario con el nombre de usuario: {usuario_usuario}
	"""

	try:

		server=smtplib.SMTP("smtp.gmail.com",587)
		server.starttls()
		server.login(CORREO, CONTRASENA)
		server.sendmail(CORREO, correo_usuario, mensaje)

		return True

	except smtplib.SMTPRecipientsRefused as e:

		print(e)

		return False