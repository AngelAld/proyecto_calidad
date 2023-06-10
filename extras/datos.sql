INSERT INTO ROL(nombre, estado) VALUES ('Director de escuela', 'A');
INSERT INTO ROL(nombre, estado) VALUES ('Docente de Apoyo', 'A');
INSERT INTO ROL(nombre, estado) VALUES ('Estudiante', 'A');

INSERT INTO USUARIO(idrol, nombre, usuario, clave, correo, estado) VALUES(
    1,
    'Usuario de pruebas',
    'Admin123',
    'pbkdf2:sha256:600000$M09Hs8m0HnOgjHEN$9e09f13c3f67a284b1457535ec98155af7591427150c9cc069ef1e25bd728398',
    'admin123@gmail.com',
    'A'
);

INSERT INTO USUARIO(idrol, nombre, usuario, clave, correo, estado) VALUES(
    2,
    'Docente de pruebas',
    'Docente123',
    'pbkdf2:sha256:600000$M09Hs8m0HnOgjHEN$9e09f13c3f67a284b1457535ec98155af7591427150c9cc069ef1e25bd728398',
    'docente12@gmail.com',
    'A'
);

--FUNCIONES DE FACULTAD PROBADAS -----------------------------------------------------------------------------------------
select * from fn_agregar_facultad('Ingenieria', 'AAA', 'A');

select * from fn_agregar_facultad('Medicina', 'AAA', 'A');

select * from  fn_listar_facultad();

select * from fn_consultar_facultad_id(1);

select * from fn_editar_facultad(1, 'Ingenieria Editada', 'AAA', 'A'); 

select * from fn_eliminar_facultad(1); 

select * from fn_actualizar_estado_facultad(2, 'I');


--FUNCIONES DE LINEA DESARROLLO PROBADAS ----------------------------------------------------------------------------------
insert into escuela_profesional(nombre, descripcion, estado, id_facultad) values('Escuela prueba', 'aaaaa', 'A', 2);

select * from fn_agregar_linea_desarrollo('Linea prueba', 'aaaa', 'A', 2);

select * from fn_editar_linea_desarrollo(1, 'Linea Prueba editada', 'aaa', 'A', 2);

select * from fn_actualizar_estado_linea_desarrollo (1, 'I');

select * from fn_listar_linea_desarrollo();

select * from fn_consultar_linea_desarrollo_id (1);

select * from fn_eliminar_linea_desarrollo (1);

select * from fn_eliminar_linea_desarrollo (1);

