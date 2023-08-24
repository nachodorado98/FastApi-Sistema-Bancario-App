from fastapi import APIRouter, status, Depends
from typing import List, Dict

from src.database.sesion import crearSesion
from src.database.conexion import Conexion

router_usuarios=APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router_usuarios.get("", status_code=status.HTTP_200_OK, summary="Devuelve los usuarios existentes")
async def obtenerUsuarios(con:Conexion=Depends(crearSesion))->List[Dict]:

	con.c.execute("SELECT * FROM usuarios")

	usuarios=con.c.fetchall()

	return usuarios