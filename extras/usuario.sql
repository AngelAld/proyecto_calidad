
CREATE OR REPLACE FUNCTION fn_login
(p_usuario VARCHAR(20)
)
RETURNS TABLE(
	id_usuario integer, 
    usuario VARCHAR(50),
	nombre VARCHAR,
	clave text,
    estado CHAR(1),
	idrol integer,  
    rol VARCHAR(50))
LANGUAGE 'plpgsql'
AS $BODY$
BEGIN
	RETURN QUERY
		SELECT 
			u.*, r.nombre as rol
		FROM usuario u
			INNER JOIN rol r on r.id_rol=u.id_rol
		WHERE u.usuario=p_usuario;
END
$BODY$;