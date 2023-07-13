CREATE TABLE ANEXOS (
  id_anexo            SERIAL NOT NULL, 
  id_informe_final_es int4 NOT NULL, 
  descripcion         varchar(255) NOT NULL, 
  anexo               varchar(255) NOT NULL, 
  PRIMARY KEY (id_anexo));
CREATE TABLE BIBLIOGRAFIA (
  id_bibliografia     SERIAL NOT NULL, 
  id_informe_final_es int4 NOT NULL, 
  descripcion         text NOT NULL, 
  PRIMARY KEY (id_bibliografia));
CREATE TABLE CENTRO_PRACTICAS (
  id_centro_practicas SERIAL NOT NULL, 
  ruc                 varchar(255) NOT NULL, 
  razon_social        varchar(255) NOT NULL, 
  alias               varchar(50) NOT NULL UNIQUE, 
  rubro               varchar(255) NOT NULL, 
  telefono            varchar(12) NOT NULL, 
  correo              varchar(255) NOT NULL, 
  id_ubicacion        int4, 
  PRIMARY KEY (id_centro_practicas));
CREATE TABLE CONCLUSIONES (
  id_conclusiones     SERIAL NOT NULL, 
  id_informe_final_es int4 NOT NULL, 
  descripcion         text NOT NULL, 
  PRIMARY KEY (id_conclusiones));
CREATE TABLE DETALLE_PRACTICA (
  id_detalle_practica   SERIAL NOT NULL, 
  fecha_inicio          date, 
  fecha_fin             date, 
  informacion_adicional text, 
  estado                char(1) NOT NULL, 
  horas                 int4, 
  id_practica           int4 NOT NULL, 
  id_jefe_inmediato     int4 NOT NULL, 
  id_semestre_academico int4 NOT NULL, 
  id_linea_desarrollo   int4 NOT NULL, 
  tipo_practica         text NOT NULL, 
  PRIMARY KEY (id_detalle_practica));
CREATE TABLE DIRECTOR_ESCUELA (
  id_director_escuela    SERIAL NOT NULL, 
  nombre                 varchar(255) NOT NULL UNIQUE, 
  correo                 varchar(255) NOT NULL UNIQUE, 
  estado                 char(1) NOT NULL, 
  id_escuela_profesional int4 NOT NULL, 
  id_usuario             int4, 
  PRIMARY KEY (id_director_escuela));
CREATE TABLE DOCENTE_APOYO (
  id_docente_apoyo       SERIAL NOT NULL, 
  nombre                 varchar(255) NOT NULL UNIQUE, 
  correo                 varchar(255) NOT NULL UNIQUE, 
  estado                 char(1) NOT NULL, 
  id_titulo              int4 NOT NULL, 
  id_escuela_profesional int4 NOT NULL, 
  id_usuario             int4, 
  PRIMARY KEY (id_docente_apoyo));
CREATE TABLE Escala (
  id_escala   SERIAL NOT NULL, 
  descripcion varchar(255) NOT NULL UNIQUE, 
  valor       int4 NOT NULL UNIQUE, 
  PRIMARY KEY (id_escala));
CREATE TABLE ESCUELA_PROFESIONAL (
  id_escuela_profesional SERIAL NOT NULL, 
  nombre                 varchar(50) NOT NULL UNIQUE, 
  descripcion            text, 
  estado                 char(1) NOT NULL, 
  id_facultad            int4 NOT NULL, 
  PRIMARY KEY (id_escuela_profesional));
CREATE TABLE ESTUDIANTE (
  id_estudiante                 SERIAL NOT NULL, 
  cod_universitario             char(10) NOT NULL UNIQUE, 
  dni                           char(8) NOT NULL UNIQUE, 
  nombre                        varchar(255) NOT NULL UNIQUE, 
  correo_usat                   varchar(255) NOT NULL UNIQUE, 
  correo_personal               varchar(255), 
  telefono                      varchar(20) NOT NULL UNIQUE, 
  telefono2                     varchar(20), 
  estado                        char(1) NOT NULL, 
  id_usuario                    int4, 
  id_semestre_academico_ingreso int4, 
  id_plan_estudio               int4, 
  PRIMARY KEY (id_estudiante));
CREATE TABLE FACULTAD (
  id_facultad SERIAL NOT NULL, 
  nombre      varchar(255) NOT NULL UNIQUE, 
  descripcion text, 
  estado      char(1) NOT NULL, 
  PRIMARY KEY (id_facultad));
CREATE TABLE FICHA_DESEMPENO (
  id_ficha_desempeno  SERIAL NOT NULL, 
  responsabilidad     int4, 
  proactividad        int4, 
  comunicacion        int4, 
  trabajo_equipo      int4, 
  compromiso_calidad  int4, 
  organizacion        int4, 
  puntualidad         int4, 
  estado              char(1) NOT NULL, 
  fecha               date, 
  conclusiones        text, 
  firma_em            text, 
  area_desemp         varchar(255), 
  comentario_docente  text, 
  id_detalle_practica int4 NOT NULL, 
  PRIMARY KEY (id_ficha_desempeno));
CREATE TABLE INFORME_FINAL_EM (
  id_informe_final_em SERIAL NOT NULL, 
  cum_objetivos       text, 
  cum_horas           text, 
  responsabilidad     text, 
  extra               text, 
  firma               text, 
  fecha               date, 
  estado              char(1) NOT NULL, 
  comentario_docente  text, 
  id_detalle_practica int4 NOT NULL, 
  PRIMARY KEY (id_informe_final_em));
CREATE TABLE INFORME_FINAL_ES (
  id_informe_final_es SERIAL NOT NULL, 
  introduccion        text, 
  cant_trabajadores   int4, 
  representante_legal text, 
  vision              text, 
  mision              text, 
  infra_fisica        text, 
  infra_tecnologica   text, 
  organigrama         text, 
  desc_area_trabajo   text, 
  desc_labores_r      text, 
  estado              char(1) NOT NULL, 
  fecha               date, 
  comentario_docente  text, 
  id_detalle_practica int4 NOT NULL, 
  PRIMARY KEY (id_informe_final_es));
CREATE TABLE INFORME_INICIAL_EM (
  id_informe_inicial_em SERIAL NOT NULL, 
  compromiso            text, 
  labores               text, 
  firma_em              text, 
  firma_es              text, 
  fecha                 date, 
  estado                char(1) NOT NULL, 
  comentario_docente    text, 
  id_detalle_practica   int4 NOT NULL, 
  PRIMARY KEY (id_informe_inicial_em));
CREATE TABLE INFORME_INICIAL_ES (
  id_informe_inicial_es SERIAL NOT NULL, 
  id_detalle_practica   int4 NOT NULL, 
  fecha                 date, 
  firma_es              text, 
  firma_jefe            text, 
  estado                char(1) NOT NULL, 
  comentario_docente    text, 
  PRIMARY KEY (id_informe_inicial_es));
CREATE TABLE JEFE_INMEDIATO (
  id_jefe_inmediato   SERIAL NOT NULL, 
  nombre              varchar(255) NOT NULL, 
  correo              varchar(255) NOT NULL, 
  telefono            varchar(12) NOT NULL, 
  cargo               varchar(255) NOT NULL, 
  estado              char(1) NOT NULL, 
  id_centro_practicas int4 NOT NULL, 
  id_usuario          int4 NOT NULL, 
  PRIMARY KEY (id_jefe_inmediato));
CREATE TABLE LINEA_DESARROLLO (
  id_linea_desarrollo    SERIAL NOT NULL, 
  nombre                 varchar(255) NOT NULL UNIQUE, 
  descripcion            varchar(255), 
  estado                 char(1) NOT NULL, 
  id_escuela_profesional int4 NOT NULL, 
  PRIMARY KEY (id_linea_desarrollo));
CREATE TABLE OBJETIVO (
  id_objetivo           SERIAL NOT NULL, 
  id_informe_inicial_es int4 NOT NULL, 
  descripcion           varchar(255) NOT NULL, 
  PRIMARY KEY (id_objetivo));
CREATE TABLE PLAN_ESTUDIO (
  id_plan_estudio        SERIAL NOT NULL, 
  nombre                 varchar(50) NOT NULL UNIQUE, 
  estado                 char(1) NOT NULL, 
  id_escuela_profesional int4 NOT NULL, 
  PRIMARY KEY (id_plan_estudio));
CREATE TABLE PLAN_TRABAJO (
  id_plan_trabajo       SERIAL NOT NULL, 
  id_informe_inicial_es int4 NOT NULL, 
  n_semana              int4 NOT NULL, 
  fecha_inicio          date NOT NULL, 
  fecha_fin             date NOT NULL, 
  actividad             varchar(255) NOT NULL, 
  num_horas             int4 NOT NULL, 
  PRIMARY KEY (id_plan_trabajo));
CREATE TABLE PRACTICA (
  id_practica   SERIAL NOT NULL, 
  estado        char(1) NOT NULL, 
  id_estudiante int4 NOT NULL, 
  PRIMARY KEY (id_practica));
CREATE TABLE RECOMENDACIONES (
  id_recomendaciones  SERIAL NOT NULL, 
  id_informe_final_es int4 NOT NULL, 
  descripcion         text NOT NULL, 
  PRIMARY KEY (id_recomendaciones));
CREATE TABLE RESULTADO_APRENDIZAJE (
  id_resultado_aprendizaje SERIAL NOT NULL, 
  descripcion              varchar(255) NOT NULL, 
  escala                   int4 NOT NULL, 
  id_ficha_desempeno       int4 NOT NULL, 
  PRIMARY KEY (id_resultado_aprendizaje));
CREATE TABLE ROL (
  id_rol SERIAL NOT NULL, 
  nombre varchar(255) NOT NULL UNIQUE, 
  estado char(1) NOT NULL, 
  PRIMARY KEY (id_rol));
CREATE TABLE SEMESTRE_ACADEMICO (
  id_semestre  SERIAL NOT NULL, 
  nombre       varchar(255) NOT NULL UNIQUE, 
  fecha_inicio date NOT NULL, 
  fecha_fin    date NOT NULL, 
  estado       char(1) NOT NULL, 
  PRIMARY KEY (id_semestre));
CREATE TABLE TITULO_PROFESIONAL (
  id_titulo   SERIAL NOT NULL, 
  nombre      varchar(255) NOT NULL UNIQUE, 
  descripcion varchar(255), 
  estado      char(1) NOT NULL, 
  PRIMARY KEY (id_titulo));
CREATE TABLE UBICACION (
  id_ubicacion SERIAL NOT NULL, 
  num          varchar(255) NOT NULL, 
  via          varchar(255) NOT NULL, 
  lon          varchar(255) NOT NULL, 
  lat          varchar(255) NOT NULL, 
  pais         varchar(255) NOT NULL, 
  ciudad       varchar(255) NOT NULL, 
  estado       char(1) NOT NULL, 
  PRIMARY KEY (id_ubicacion));
CREATE TABLE USUARIO (
  id_usuario SERIAL NOT NULL, 
  usuario    varchar(50) NOT NULL UNIQUE, 
  nombre     varchar(255) NOT NULL UNIQUE, 
  clave      text NOT NULL, 
  estado     char(1) NOT NULL, 
  id_rol     int4 NOT NULL, 
  PRIMARY KEY (id_usuario));
ALTER TABLE ESCUELA_PROFESIONAL ADD CONSTRAINT FKESCUELA_PR974682 FOREIGN KEY (id_facultad) REFERENCES FACULTAD (id_facultad);
ALTER TABLE DOCENTE_APOYO ADD CONSTRAINT FKDOCENTE_AP446613 FOREIGN KEY (id_titulo) REFERENCES TITULO_PROFESIONAL (id_titulo);
ALTER TABLE DOCENTE_APOYO ADD CONSTRAINT FKDOCENTE_AP718622 FOREIGN KEY (id_escuela_profesional) REFERENCES ESCUELA_PROFESIONAL (id_escuela_profesional);
ALTER TABLE DIRECTOR_ESCUELA ADD CONSTRAINT FKDIRECTOR_E206053 FOREIGN KEY (id_escuela_profesional) REFERENCES ESCUELA_PROFESIONAL (id_escuela_profesional);
ALTER TABLE PLAN_ESTUDIO ADD CONSTRAINT FKPLAN_ESTUD59740 FOREIGN KEY (id_escuela_profesional) REFERENCES ESCUELA_PROFESIONAL (id_escuela_profesional);
ALTER TABLE JEFE_INMEDIATO ADD CONSTRAINT FKJEFE_INMED524949 FOREIGN KEY (id_centro_practicas) REFERENCES CENTRO_PRACTICAS (id_centro_practicas);
ALTER TABLE DETALLE_PRACTICA ADD CONSTRAINT FKDETALLE_PR215336 FOREIGN KEY (id_practica) REFERENCES PRACTICA (id_practica);
ALTER TABLE DETALLE_PRACTICA ADD CONSTRAINT FKDETALLE_PR602371 FOREIGN KEY (id_jefe_inmediato) REFERENCES JEFE_INMEDIATO (id_jefe_inmediato);
ALTER TABLE USUARIO ADD CONSTRAINT FKUSUARIO4727 FOREIGN KEY (id_rol) REFERENCES ROL (id_rol);
ALTER TABLE ESTUDIANTE ADD CONSTRAINT FKESTUDIANTE529263 FOREIGN KEY (id_usuario) REFERENCES USUARIO (id_usuario);
ALTER TABLE DIRECTOR_ESCUELA ADD CONSTRAINT FKDIRECTOR_E761047 FOREIGN KEY (id_usuario) REFERENCES USUARIO (id_usuario);
ALTER TABLE DOCENTE_APOYO ADD CONSTRAINT FKDOCENTE_AP163628 FOREIGN KEY (id_usuario) REFERENCES USUARIO (id_usuario);
ALTER TABLE PRACTICA ADD CONSTRAINT FKPRACTICA599798 FOREIGN KEY (id_estudiante) REFERENCES ESTUDIANTE (id_estudiante);
ALTER TABLE DETALLE_PRACTICA ADD CONSTRAINT FKDETALLE_PR642416 FOREIGN KEY (id_semestre_academico) REFERENCES SEMESTRE_ACADEMICO (id_semestre);
ALTER TABLE ESTUDIANTE ADD CONSTRAINT FKESTUDIANTE613214 FOREIGN KEY (id_semestre_academico_ingreso) REFERENCES SEMESTRE_ACADEMICO (id_semestre);
ALTER TABLE PLAN_TRABAJO ADD CONSTRAINT FKPLAN_TRABA223183 FOREIGN KEY (id_informe_inicial_es) REFERENCES INFORME_INICIAL_ES (id_informe_inicial_es) ON DELETE Cascade;
ALTER TABLE OBJETIVO ADD CONSTRAINT FKOBJETIVO739515 FOREIGN KEY (id_informe_inicial_es) REFERENCES INFORME_INICIAL_ES (id_informe_inicial_es) ON DELETE Cascade;
ALTER TABLE INFORME_INICIAL_ES ADD CONSTRAINT FKINFORME_IN64603 FOREIGN KEY (id_detalle_practica) REFERENCES DETALLE_PRACTICA (id_detalle_practica) ON DELETE Cascade;
ALTER TABLE INFORME_INICIAL_EM ADD CONSTRAINT FKINFORME_IN64597 FOREIGN KEY (id_detalle_practica) REFERENCES DETALLE_PRACTICA (id_detalle_practica) ON DELETE Cascade;
ALTER TABLE RECOMENDACIONES ADD CONSTRAINT FKRECOMENDAC626388 FOREIGN KEY (id_informe_final_es) REFERENCES INFORME_FINAL_ES (id_informe_final_es) ON DELETE Cascade;
ALTER TABLE CONCLUSIONES ADD CONSTRAINT FKCONCLUSION136439 FOREIGN KEY (id_informe_final_es) REFERENCES INFORME_FINAL_ES (id_informe_final_es) ON DELETE Cascade;
ALTER TABLE INFORME_FINAL_ES ADD CONSTRAINT FKINFORME_FI1483 FOREIGN KEY (id_detalle_practica) REFERENCES DETALLE_PRACTICA (id_detalle_practica) ON DELETE Cascade;
ALTER TABLE BIBLIOGRAFIA ADD CONSTRAINT FKBIBLIOGRAF317237 FOREIGN KEY (id_informe_final_es) REFERENCES INFORME_FINAL_ES (id_informe_final_es) ON DELETE Cascade;
ALTER TABLE ANEXOS ADD CONSTRAINT FKANEXOS46774 FOREIGN KEY (id_informe_final_es) REFERENCES INFORME_FINAL_ES (id_informe_final_es) ON DELETE Cascade;
ALTER TABLE INFORME_FINAL_EM ADD CONSTRAINT FKINFORME_FI1477 FOREIGN KEY (id_detalle_practica) REFERENCES DETALLE_PRACTICA (id_detalle_practica) ON DELETE Cascade;
ALTER TABLE FICHA_DESEMPENO ADD CONSTRAINT FKFICHA_DESE742921 FOREIGN KEY (id_detalle_practica) REFERENCES DETALLE_PRACTICA (id_detalle_practica) ON DELETE Cascade;
ALTER TABLE LINEA_DESARROLLO ADD CONSTRAINT FKLINEA_DESA831180 FOREIGN KEY (id_escuela_profesional) REFERENCES ESCUELA_PROFESIONAL (id_escuela_profesional);
ALTER TABLE ESTUDIANTE ADD CONSTRAINT FKESTUDIANTE401223 FOREIGN KEY (id_plan_estudio) REFERENCES PLAN_ESTUDIO (id_plan_estudio);
ALTER TABLE DETALLE_PRACTICA ADD CONSTRAINT FKDETALLE_PR399145 FOREIGN KEY (id_linea_desarrollo) REFERENCES LINEA_DESARROLLO (id_linea_desarrollo);
ALTER TABLE JEFE_INMEDIATO ADD CONSTRAINT FKJEFE_INMED727574 FOREIGN KEY (id_usuario) REFERENCES USUARIO (id_usuario);
ALTER TABLE CENTRO_PRACTICAS ADD CONSTRAINT FKCENTRO_PRA585086 FOREIGN KEY (id_ubicacion) REFERENCES UBICACION (id_ubicacion);
ALTER TABLE RESULTADO_APRENDIZAJE ADD CONSTRAINT FKRESULTADO_304597 FOREIGN KEY (id_ficha_desempeno) REFERENCES FICHA_DESEMPENO (id_ficha_desempeno) ON DELETE Cascade;
