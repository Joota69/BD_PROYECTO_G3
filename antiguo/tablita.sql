-- Crear la tabla de usuarios
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    contraseña VARCHAR(255) NOT NULL
);

-- Insertar 4 usuarios
INSERT INTO usuarios (nombre, contraseña) VALUES 
('usuario1', 'contraseña1'),
('usuario2', 'contraseña2'),
('usuario3', 'contraseña3'),
('usuario4', 'contraseña4');

-- Crear la tabla de acciones
CREATE TABLE acciones (
	 id_accion INT,
    id_usuario INT,
    accion CHAR(1),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id)
);
ALTER TABLE acciones MODIFY COLUMN id_accion INT AUTO_INCREMENT PRIMARY KEY;
-- Insertar acciones para los usuarios

SELECT * FROM usuarios;
SELECT * FROM acciones;

SELECT * FROM acciones WHERE id_accion = 0;


SELECT accion, COUNT(*) AS veces_repetidas 
FROM acciones 
GROUP BY accion 
ORDER BY veces_repetidas DESC 
LIMIT 1;

