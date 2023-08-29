import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List, Dict, Optional

from .confconexion import *

# Clase para la conexion a la BBDD
class Conexion:

	def __init__(self)->None:

		try:
			
			self.bbdd=psycopg2.connect(host=HOST, user=USUARIO, password=CONTRASENA, port=PUERTO, database=BBDD)
			self.c=self.bbdd.cursor(cursor_factory=RealDictCursor)

		except psycopg2.OperationalError as e:

			print("Error en la conexion a la BBDD")
			print(e)

	# Metodo para cerrar la conexion a la BBDD
	def cerrarConexion(self)->None:

		self.c.close()
		self.bbdd.close()

	# Metodo para insertar un usuario
	def insertarUsuario(self,
						usuario:str,
						nombre:str,
						apellido1:str,
						apellido2:str,
						fecha_nacimiento:str,
						ciudad:str,
						pais:str,
						genero:str,
						telefono:str,
						correo:str,
						contrasena:str)->None:

		self.c.execute("""INSERT INTO usuarios
						VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
						(usuario, nombre, apellido1, apellido2, fecha_nacimiento, ciudad, pais, genero, telefono, correo, contrasena))

		self.bbdd.commit()

	# Metodo para comprobar que un usuario existe
	def existe_usuario(self, usuario:str)->bool:

		self.c.execute("""SELECT *
						FROM usuarios
						WHERE usuario=%s""",
						(usuario,))

		return False if self.c.fetchone() is None else True

	# Metodo para obtener los usuarios
	def obtenerUsuarios(self)->Optional[List[Dict]]:

		self.c.execute("""SELECT usuario
						FROM usuarios""")

		usuarios=self.c.fetchall()

		return None if usuarios==[] else usuarios

	# Metodo para obtener la contraseña (hash) del usuario
	def obtenerContrasena(self, usuario:str)->Optional[str]:

		self.c.execute("""SELECT contrasena
						FROM usuarios
						WHERE usuario=%s""",
						(usuario,))

		contrasena=self.c.fetchone()

		return contrasena["contrasena"] if contrasena is not None else contrasena

	# Metodo para obtener los datos de un usuario
	def obtenerDatosUsuario(self, usuario:str)->Optional[Dict]:

		self.c.execute("""SELECT usuario, nombre, apellido1, apellido2, fecha_nacimiento, ciudad, pais, genero, telefono, correo
						FROM usuarios
						WHERE usuario=%s""",
						(usuario,))

		return self.c.fetchone()

	# Metodo para actualizar el numero de telefono de un usuario
	def actualizarTelefono(self, usuario:str, telefono:str)->None:

		self.c.execute("""UPDATE usuarios
						SET telefono=%s
						WHERE usuario=%s""",
						(telefono, usuario))

		self.bbdd.commit()

	# Metodo para cambiar la contraseña de un usuario
	def cambiarContrasena(self, usuario:str, contrasena:str)->None:

		self.c.execute("""UPDATE usuarios
						SET contrasena=%s
						WHERE usuario=%s""",
						(contrasena, usuario))

		self.bbdd.commit()

	# Metodo para obtener las transacciones de un usuario
	def obtenerTransacciones(self, usuario:str)->Optional[List[Dict]]:

		self.c.execute("""SELECT transaccion, concepto, cantidad, fecha, historico
					FROM transacciones
					WHERE usuario=%s""",
					(usuario,))

		transacciones=self.c.fetchall()

		return None if transacciones==[] else transacciones

	# Metodo para obtener el saldo del usuario
	def obtenerSaldo(self, usuario:str)->Optional[float]:

		self.c.execute("""SELECT saldo
						FROM usuarios
						WHERE usuario=%s""",
						(usuario,))

		saldo=self.c.fetchone()

		return saldo["saldo"] if saldo is not None else saldo

	# Metodo para actualizar el saldo de un usuario
	def actualizarSaldo(self, usuario:str, saldo:float)->None:

		self.c.execute("""UPDATE usuarios
						SET saldo=%s
						WHERE usuario=%s""",
						(saldo, usuario))

		self.bbdd.commit()

	# Metodo para insertar una transaccion
	def insertarTransaccion(self, transaccion:str, usuario:str, concepto:str, cantidad:float, fecha:str, historico:float)->None:

		self.c.execute("""INSERT INTO transacciones
						VALUES(%s, %s, %s, %s, %s, %s)""",
						(transaccion, usuario, concepto, cantidad, fecha, historico))

		self.bbdd.commit()