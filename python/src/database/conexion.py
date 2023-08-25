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