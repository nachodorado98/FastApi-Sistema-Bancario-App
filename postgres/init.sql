CREATE DATABASE bbdd_sistema_bancario;

\c bbdd_sistema_bancario;

CREATE TABLE usuarios (usuario VARCHAR(20) PRIMARY KEY,
						nombre VARCHAR(20),
						apellido1 VARCHAR(20),
						apellido2 VARCHAR(20),
						fecha_nacimiento DATE,
						ciudad VARCHAR(20),
						pais VARCHAR(20),
						genero VARCHAR(20),
						telefono VARCHAR(9),
						correo VARCHAR(50),
						contrasena VARCHAR(70),
						saldo DOUBLE PRECISION DEFAULT 0.0);
