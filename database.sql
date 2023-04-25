CREATE TABLE SEMESTRE_ACADEMICO (
  id_semestre  int(11) NOT NULL AUTO_INCREMENT, 
  nombre       varchar(50) NOT NULL, 
  fecha_inicio date NOT NULL, 
  fecha_fin    date NOT NULL, 
  estado       char(1) NOT NULL, 
  PRIMARY KEY (id_semestre));

DELIMITER //
CREATE OR REPLACE  FUNCTION fn_create_semestre(
  p_nombre VARCHAR(50),
  p_fecha_inicio DATE,
  p_fecha_fin DATE,
  p_estado CHAR(1)
) RETURNS VARCHAR(255)
BEGIN
  DECLARE semestre_existe INT;
  DECLARE fecha_actual DATE;
  

  SELECT COUNT(*) INTO semestre_existe FROM SEMESTRE_ACADEMICO WHERE nombre = p_nombre;
  IF semestre_existe > 0 THEN
    RETURN 'Semestre ya existe';
  END IF;

  IF p_fecha_fin <= p_fecha_inicio THEN
    RETURN 'La fecha de fin debe ser posterior a la fecha de inicio';
  END IF;

  SET fecha_actual = CURDATE();
  IF fecha_actual BETWEEN p_fecha_inicio AND p_fecha_fin THEN
    SET p_estado = 'A';
  END IF;
  
  INSERT INTO SEMESTRE_ACADEMICO (nombre, fecha_inicio, fecha_fin, estado) VALUES (p_nombre, p_fecha_inicio, p_fecha_fin, p_estado);
  
  RETURN 'Operación realizada con éxito';
END;//

DELIMITER ;

DELIMITER //
CREATE OR REPLACE FUNCTION fn_update_semestre(
  p_id_semestre INT,
  p_nombre VARCHAR(50),
  p_fecha_inicio DATE,
  p_fecha_fin DATE,
  p_estado CHAR(1)
) RETURNS VARCHAR(255)
BEGIN
  DECLARE semestre_existe INT;
  
  SELECT COUNT(*) INTO semestre_existe FROM SEMESTRE_ACADEMICO WHERE nombre = p_nombre AND id_semestre != p_id_semestre;
  IF semestre_existe > 0 THEN
    RETURN 'Semestre ya existe';
  END IF;
  IF p_fecha_fin <= p_fecha_inicio THEN
    RETURN 'La fecha de fin debe ser posterior a la fecha de inicio';
  END IF;
  UPDATE SEMESTRE_ACADEMICO SET nombre = p_nombre, fecha_inicio = p_fecha_inicio, fecha_fin = p_fecha_fin, estado = p_estado WHERE id_semestre = p_id_semestre;
  RETURN 'Operación realizada con éxito';
END;//

DELIMITER ;

DELIMITER //
CREATE OR REPLACE FUNCTION fn_delete_semestre(p_id INT)
RETURNS VARCHAR(100)
BEGIN
    DECLARE mensaje VARCHAR(100);
    DECLARE error_msg VARCHAR(100);

    SET error_msg = 'No se pudo eliminar el registro.';

    DELETE FROM SEMESTRE_ACADEMICO WHERE id_semestre  = p_id;
    
    -- Verificar si se eliminó el registro correctamente
    IF ROW_COUNT() > 0 THEN
        SET mensaje = 'Operación realizada con éxito';
    ELSE
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = error_msg;
    END IF;

    RETURN mensaje;
END;//

DELIMITER ;
