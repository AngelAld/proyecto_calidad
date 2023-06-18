INSERT INTO ROL(nombre, estado) VALUES ('Director de escuela', 'A');
INSERT INTO ROL(nombre, estado) VALUES ('Docente de Apoyo', 'A');
INSERT INTO ROL(nombre, estado) VALUES ('Estudiante', 'A');

INSERT INTO USUARIO(id_rol, nombre, usuario, clave, estado) VALUES(
    1,
    'Usuario de pruebas',
    'Admin123',
    'pbkdf2:sha256:600000$M09Hs8m0HnOgjHEN$9e09f13c3f67a284b1457535ec98155af7591427150c9cc069ef1e25bd728398',
    'A'
);

INSERT INTO USUARIO(id_rol, nombre, usuario, clave, estado) VALUES(
    2,
    'Docente de pruebas',
    'Docente123',
    'pbkdf2:sha256:600000$M09Hs8m0HnOgjHEN$9e09f13c3f67a284b1457535ec98155af7591427150c9cc069ef1e25bd728398',
    'A'
);

--FUNCIONES DE FACULTAD PROBADAS -----------------------------------------------------------------------------------------
select * from fn_agregar_facultad('Ingenieria', 'AAA', 'A');

select * from fn_agregar_facultad('Medicina', 'AAA', 'A');

select * from  fn_listar_facultad();

select * from fn_consultar_facultad_id(1);

select * from fn_editar_facultad(1, 'Ingenieria Editada', 'AAA', 'A'); 

select * from fn_actualizar_estado_facultad(2, 'I');


--FUNCIONES DE LINEA DESARROLLO PROBADAS ----------------------------------------------------------------------------------
insert into escuela_profesional(nombre, descripcion, estado, id_facultad) values('Escuela prueba', 'aaaaa', 'A', 2);

select * from fn_agregar_linea_desarrollo('Linea prueba', 'aaaa', 'A', 1);

select * from fn_editar_linea_desarrollo(1, 'Linea Prueba editada', 'aaa', 'A', 2);

select * from fn_actualizar_estado_linea_desarrollo (1, 'I');

select * from fn_listar_linea_desarrollo();

select * from fn_consultar_linea_desarrollo_id (1);



--FUNCIONES DE DOCENTE DE APOYO PROBADAS ----------------------------------------------------------------------------------


-- SEMESTRES

select * from fn_create_semestre('A1',CURRENT_DATE,CURRENT_DATE+30,'A');
select * from fn_create_semestre('A2',CURRENT_DATE+30,CURRENT_DATE+60,'A');
select * from fn_create_semestre('A3',CURRENT_DATE+60,CURRENT_DATE+90,'A');
select * from fn_create_semestre('A4',CURRENT_DATE+90,CURRENT_DATE+120,'A');
select * from fn_create_semestre('A5',CURRENT_DATE+120,CURRENT_DATE+150,'A');
select * from fn_create_semestre('A6',CURRENT_DATE+150,CURRENT_DATE+180,'A');
select * from fn_create_semestre('A7',CURRENT_DATE+180,CURRENT_DATE+210,'A');
select * from fn_create_semestre('A8',CURRENT_DATE+210,CURRENT_DATE+240,'A');
select * from fn_create_semestre('A9',CURRENT_DATE+240,CURRENT_DATE+270,'A');
select * from fn_create_semestre('A10',CURRENT_DATE+270,CURRENT_DATE+300,'A');
select * from fn_create_semestre('A11',CURRENT_DATE+300,CURRENT_DATE+330,'A');
select * from fn_create_semestre('A12',CURRENT_DATE+330,CURRENT_DATE+360,'A');
select * from fn_create_semestre('A13',CURRENT_DATE+360,CURRENT_DATE+390,'A');
select * from fn_create_semestre('A14',CURRENT_DATE+390,CURRENT_DATE+420,'A');
select * from fn_create_semestre('A15',CURRENT_DATE+420,CURRENT_DATE+450,'A');
select * from fn_create_semestre('A16',CURRENT_DATE+450,CURRENT_DATE+480,'A');
select * from fn_create_semestre('A17',CURRENT_DATE+480,CURRENT_DATE+510,'A');
select * from fn_create_semestre('A18',CURRENT_DATE+510,CURRENT_DATE+540,'A');
select * from fn_create_semestre('A19',CURRENT_DATE+540,CURRENT_DATE+570,'A');
select * from fn_create_semestre('A20',CURRENT_DATE+570,CURRENT_DATE+600,'A');
select * from fn_create_semestre('A21',CURRENT_DATE+600,CURRENT_DATE+630,'A');
select * from fn_create_semestre('A22',CURRENT_DATE+630,CURRENT_DATE+660,'A');
select * from fn_create_semestre('A23',CURRENT_DATE+660,CURRENT_DATE+690,'A');
select * from fn_create_semestre('A24',CURRENT_DATE+690,CURRENT_DATE+720,'A');
select * from fn_create_semestre('A25',CURRENT_DATE+720,CURRENT_DATE+750,'A');
select * from fn_create_semestre('A26',CURRENT_DATE+750,CURRENT_DATE+780,'A');
select * from fn_create_semestre('A27',CURRENT_DATE+780,CURRENT_DATE+810,'A');
select * from fn_create_semestre('A28',CURRENT_DATE+810,CURRENT_DATE+840,'A');
select * from fn_create_semestre('A29',CURRENT_DATE+840,CURRENT_DATE+870,'A');
select * from fn_create_semestre('A30',CURRENT_DATE+870,CURRENT_DATE+900,'A');
select * from fn_create_semestre('A31',CURRENT_DATE+900,CURRENT_DATE+930,'A');
select * from fn_create_semestre('A32',CURRENT_DATE+930,CURRENT_DATE+960,'A');
select * from fn_create_semestre('A33',CURRENT_DATE+960,CURRENT_DATE+990,'A');
select * from fn_create_semestre('A34',CURRENT_DATE+990,CURRENT_DATE+1020,'A');
select * from fn_create_semestre('A35',CURRENT_DATE+1020,CURRENT_DATE+1050,'A');
select * from fn_create_semestre('A36',CURRENT_DATE+1050,CURRENT_DATE+1080,'A');
select * from fn_create_semestre('A37',CURRENT_DATE+1080,CURRENT_DATE+1110,'A');
select * from fn_create_semestre('A38',CURRENT_DATE+1110,CURRENT_DATE+1140,'A');
select * from fn_create_semestre('A39',CURRENT_DATE+1140,CURRENT_DATE+1170,'A');
select * from fn_create_semestre('A40',CURRENT_DATE+1170,CURRENT_DATE+1200,'A');
select * from fn_create_semestre('A41',CURRENT_DATE+1200,CURRENT_DATE+1230,'A');
select * from fn_create_semestre('A42',CURRENT_DATE+1230,CURRENT_DATE+1260,'A');
select * from fn_create_semestre('A43',CURRENT_DATE+1260,CURRENT_DATE+1290,'A');
select * from fn_create_semestre('A44',CURRENT_DATE+1290,CURRENT_DATE+1320,'A');
select * from fn_create_semestre('A45',CURRENT_DATE+1320,CURRENT_DATE+1350,'A');
select * from fn_create_semestre('A46',CURRENT_DATE+1350,CURRENT_DATE+1380,'A');
select * from fn_create_semestre('A47',CURRENT_DATE+1380,CURRENT_DATE+1410,'A');
select * from fn_create_semestre('A48',CURRENT_DATE+1410,CURRENT_DATE+1440,'A');
select * from fn_create_semestre('A49',CURRENT_DATE+1440,CURRENT_DATE+1470,'A');
select * from fn_create_semestre('A50',CURRENT_DATE+1470,CURRENT_DATE+1500,'A');