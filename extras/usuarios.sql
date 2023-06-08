
CREATE OR REPLACE FUNCTION fn_login
(p_usuario VARCHAR(20)
)
RETURNS TABLE(
	id integer, 
    idrol integer, 
    nombre VARCHAR(100), 
    usuario VARCHAR(100),
	clave text, 
    correo VARCHAR(100), 
    estado CHAR(1), 
    rol VARCHAR(50))
LANGUAGE 'plpgsql'
AS $BODY$
BEGIN
	RETURN QUERY
		SELECT 
			u.*, r.nombre as rol
		FROM usuario u
			INNER JOIN rol r on r.id=u.idrol
		WHERE u.usuario=p_usuario;
END
$BODY$;