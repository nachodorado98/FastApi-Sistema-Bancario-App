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

CREATE TABLE transacciones(transaccion VARCHAR(32) PRIMARY KEY,
							usuario VARCHAR(20),
							concepto VARCHAR(50),
							cantidad DOUBLE PRECISION,
							fecha DATE,
							historico DOUBLE PRECISION,
							FOREIGN KEY (usuario) REFERENCES usuarios(usuario) ON DELETE CASCADE);

CREATE TABLE transferencias(transferencia VARCHAR(32) PRIMARY KEY,
							transaccion_origen VARCHAR(32),
							transaccion_destino VARCHAR(32),
							cantidad_neta DOUBLE PRECISION,
							FOREIGN KEY (transaccion_origen) REFERENCES transacciones(transaccion) ON DELETE CASCADE,
							FOREIGN KEY (transaccion_destino) REFERENCES transacciones(transaccion) ON DELETE CASCADE)