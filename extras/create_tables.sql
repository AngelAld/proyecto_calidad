CREATE TABLE ANEXOS (
  id_anexo               int4 NOT NULL, 
  id_informe_final_es    int4 NOT NULL, 
  descripcion            varchar(255) NOT NULL, 
  anexo                  varchar(255) NOT NULL, 
  INFORME_FINAL_ESestado char(1) NOT NULL, 
  PRIMARY KEY (id_anexo, 
  id_informe_final_es, 
  INFORME_FINAL_ESestado));
CREATE TABLE BIBLIOGRAFIA (
  id_bibliografia        int4 NOT NULL, 
  id_informe_final_es    int4 NOT NULL, 
  descripcion            text NOT NULL, 
  INFORME_FINAL_ESestado char(1) NOT NULL, 
  PRIMARY KEY (id_bibliografia, 
  id_informe_final_es, 
  INFORME_FINAL_ESestado));
CREATE TABLE CENTRO_PRACTICAS (
  id_centro_practicas SERIAL NOT NULL, 
  ruc                 varchar(255) NOT NULL, 
  razon_social        varchar(255) NOT NULL, 
  alias               varchar(50) NOT NULL, 
  rubro               varchar(255) NOT NULL, 
  telefono            varchar(12) NOT NULL, 
  correo              varchar(255) NOT NULL, 
  id_ubicacion        int4 NOT NULL, 
  PRIMARY KEY (id_centro_practicas));
CREATE TABLE CONCLUSIONES (
  id_conclusiones        int4 NOT NULL, 
  id_informe_final_es    int4 NOT NULL, 
  descripcion            text NOT NULL, 
  INFORME_FINAL_ESestado char(1) NOT NULL, 
  PRIMARY KEY (id_conclusiones, 
  id_informe_final_es, 
  INFORME_FINAL_ESestado));
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
  PRIMARY KEY (id_detalle_practica));
CREATE TABLE DIRECTOR_ESCUELA (
  id_director_escuela    SERIAL NOT NULL, 
  nombre                 varchar(255) NOT NULL, 
  correo                 varchar(255) NOT NULL, 
  estado                 char(1) NOT NULL, 
  id_escuela_profesional int4 NOT NULL, 
  id_usuario             int4, 
  PRIMARY KEY (id_director_escuela));
CREATE TABLE DOCENTE_APOYO (
  id_docente_apoyo       SERIAL NOT NULL, 
  nombre                 varchar(255) NOT NULL, 
  correo                 varchar(255) NOT NULL, 
  estado                 char(1) NOT NULL, 
  id_titulo              int4 NOT NULL, 
  id_escuela_profesional int4 NOT NULL, 
  id_usuario             int4, 
  PRIMARY KEY (id_docente_apoyo));
CREATE TABLE ESCUELA_PROFESIONAL (
  id_escuela_profesional SERIAL NOT NULL, 
  nombre                 varchar(50) NOT NULL UNIQUE, 
  descripcion            text, 
  estado                 char(1) NOT NULL, 
  id_facultad            int4 NOT NULL, 
  PRIMARY KEY (id_escuela_profesional));
CREATE TABLE ESTUDIANTE (
  id_estudiante                 SERIAL NOT NULL, 
  cod_universitario             char(10) NOT NULL, 
  dni                           char(8) NOT NULL, 
  nombre                        varchar(255) NOT NULL, 
  correo_usat                   varchar(255) NOT NULL, 
  correo_personal               varchar(255), 
  telefono                      varchar(15) NOT NULL, 
  telefono2                     varchar(15), 
  estado                        char(1) NOT NULL, 
  id_usuario                    int4, 
  id_semestre_academico_ingreso int4, 
  id_plan_estudio               int4 NOT NULL, 
  PRIMARY KEY (id_estudiante));
CREATE TABLE FACULTAD (
  id_facultad SERIAL NOT NULL, 
  nombre      varchar(255) NOT NULL UNIQUE, 
  descripcion text, 
  estado      char(1) NOT NULL, 
  PRIMARY KEY (id_facultad));
CREATE TABLE FICHA_DESEMPEÑO (
  id_ficha_desempeño  SERIAL NOT NULL, 
  responsabilidad     int4 NOT NULL, 
  proactividad        int4 NOT NULL, 
  comunicacion        int4 NOT NULL, 
  trabajo_equipo      int4 NOT NULL, 
  compromiso_calidad  int4 NOT NULL, 
  organizacion        int4 NOT NULL, 
  puntualidad         int4 NOT NULL, 
  estado              char(1) NOT NULL, 
  id_detalle_practica int4 NOT NULL, 
  PRIMARY KEY (id_ficha_desempeño));
CREATE TABLE INFORME_FINAL_EM (
  id_informe_final_em SERIAL NOT NULL, 
  cum_objetivos       text, 
  cum_horas           text, 
  responsabilidad     text, 
  extra               text, 
  firma               bytea, 
  estado              char(1) NOT NULL, 
  id_detalle_practica int4 NOT NULL, 
  PRIMARY KEY (id_informe_final_em));
CREATE TABLE INFORME_FINAL_ES (
  id_informe_final_es SERIAL NOT NULL, 
  cant_trabajadores   int4 NOT NULL, 
  vision              text NOT NULL, 
  mision              text NOT NULL, 
  infra_fisica        text NOT NULL, 
  infra_tecnologica   text NOT NULL, 
  organigrama         bytea NOT NULL, 
  desc_area_trabajo   text NOT NULL, 
  desc_labores_r      text NOT NULL, 
  estado              char(1) NOT NULL, 
  id_detalle_practica int4 NOT NULL, 
  PRIMARY KEY (id_informe_final_es));
CREATE TABLE INFORME_INICIAL_EM (
  id_informe_inicial_em               SERIAL NOT NULL, 
  compromiso                          text NOT NULL, 
  labores                             text NOT NULL, 
  firma                               varchar(255) NOT NULL, 
  estado                              char(1) NOT NULL, 
  DETALLE_PRACTICAid_detalle_practica int4 NOT NULL, 
  PRIMARY KEY (id_informe_inicial_em));
CREATE TABLE INFORME_INICIAL_ES (
  id_informe_inicial_es SERIAL NOT NULL, 
  estado                char(1) NOT NULL, 
  id_detalle_practica   int4 NOT NULL, 
  PRIMARY KEY (id_informe_inicial_es));
CREATE TABLE JEFE_INMEDIATO (
  id_jefe_inmediato   SERIAL NOT NULL, 
  nombre              varchar(255) NOT NULL, 
  correo              varchar(255) NOT NULL, 
  telefono            varchar(12) NOT NULL, 
  cargo               varchar(255) NOT NULL, 
  estado              char(1) NOT NULL, 
  id_centro_practicas int4 NOT NULL, 
  PRIMARY KEY (id_jefe_inmediato));
CREATE TABLE LINEA_DESARROLLO (
  id_linea_desarrollo    SERIAL NOT NULL, 
  nombre                 varchar(255) NOT NULL, 
  descripcion            varchar(255), 
  estado                 char(1) NOT NULL, 
  id_escuela_profesional int4 NOT NULL, 
  PRIMARY KEY (id_linea_desarrollo));
CREATE TABLE OBJETIVO (
  id_objetivo           int4 NOT NULL, 
  id_informe_inicial_es int4 NOT NULL, 
  descripcion           varchar(255) NOT NULL, 
  PRIMARY KEY (id_objetivo, 
  id_informe_inicial_es));
CREATE TABLE PLAN_ESTUDIO (
  id_plan_estudio        SERIAL NOT NULL, 
  nombre                 varchar(50) NOT NULL, 
  estado                 char(1) NOT NULL, 
  id_escuela_profesional int4 NOT NULL, 
  PRIMARY KEY (id_plan_estudio));
CREATE TABLE PLAN_TRABAJO (
  id_plan_trabajo       int4 NOT NULL, 
  id_informe_inicial_es int4 NOT NULL, 
  n_semana              int4 NOT NULL, 
  fecha_inicio          date NOT NULL, 
  fecha_fin             date NOT NULL, 
  actividad             varchar(255) NOT NULL, 
  num_horas             int4 NOT NULL, 
  PRIMARY KEY (id_plan_trabajo, 
  id_informe_inicial_es));
CREATE TABLE PRACTICA (
  id_practica   SERIAL NOT NULL, 
  descripcion   varchar(255) NOT NULL, 
  estado        char(1), 
  id_estudiante int4 NOT NULL, 
  PRIMARY KEY (id_practica));
CREATE TABLE RECOMENDACIONES (
  id_recomendaciones     int4 NOT NULL, 
  id_informe_final_es    int4 NOT NULL, 
  descripcion            text NOT NULL, 
  INFORME_FINAL_ESestado char(1) NOT NULL, 
  PRIMARY KEY (id_recomendaciones, 
  id_informe_final_es, 
  INFORME_FINAL_ESestado));
CREATE TABLE RESULTADO_APRENDIZAJE (
  id_resultado_aprendizaje int4 NOT NULL, 
  id_ficha_desempeño       int4 NOT NULL, 
  descripcion              varchar(255) NOT NULL, 
  escala                   int4 NOT NULL, 
  PRIMARY KEY (id_resultado_aprendizaje, 
  id_ficha_desempeño));
CREATE TABLE ROL (
  id_rol SERIAL NOT NULL, 
  nombre varchar(255) NOT NULL, 
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
  nombre      varchar(255) NOT NULL, 
  descripcion int4, 
  estado      char(1) NOT NULL, 
  PRIMARY KEY (id_titulo));
CREATE TABLE UBICACION (
  id_ubicacion SERIAL NOT NULL, 
  num          varchar(255) NOT NULL, 
  tipo_via     varchar(255) NOT NULL, 
  via          varchar(255) NOT NULL, 
  lon          varchar(255) NOT NULL, 
  lat          varchar(255) NOT NULL, 
  pais         varchar(255) NOT NULL, 
  ciudad       varchar(255) NOT NULL, 
  PRIMARY KEY (id_ubicacion));
CREATE TABLE USUARIO (
  id_usuario SERIAL NOT NULL, 
  usuario    varchar(50) NOT NULL, 
  nombre     varchar(255) NOT NULL, 
  clave      text NOT NULL, 
  estado     char(1) NOT NULL, 
  id_rol     int4 NOT NULL, 
  PRIMARY KEY (id_usuario));
ALTER TABLE ESCUELA_PROFESIONAL ADD CONSTRAINT FKESCUELA_PR974682 FOREIGN KEY (id_facultad) REFERENCES FACULTAD (id_facultad);
ALTER TABLE DOCENTE_APOYO ADD CONSTRAINT FKDOCENTE_AP446613 FOREIGN KEY (id_titulo) REFERENCES TITULO_PROFESIONAL (id_titulo);
ALTER TABLE DOCENTE_APOYO ADD CONSTRAINT FKDOCENTE_AP718622 FOREIGN KEY (id_escuela_profesional) REFERENCES ESCUELA_PROFESIONAL (id_escuela_profesional);
ALTER TABLE DIRECTOR_ESCUELA ADD CONSTRAINT FKDIRECTOR_E206053 FOREIGN KEY (id_escuela_profesional) REFERENCES ESCUELA_PROFESIONAL (id_escuela_profesional);
ALTER TABLE PLAN_ESTUDIO ADD CONSTRAINT FKPLAN_ESTUD59740 FOREIGN KEY (id_escuela_profesional) REFERENCES ESCUELA_PROFESIONAL (id_escuela_profesional);
ALTER TABLE CENTRO_PRACTICAS ADD CONSTRAINT FKCENTRO_PRA585086 FOREIGN KEY (id_ubicacion) REFERENCES UBICACION (id_ubicacion);
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
ALTER TABLE PLAN_TRABAJO ADD CONSTRAINT FKPLAN_TRABA223183 FOREIGN KEY (id_informe_inicial_es) REFERENCES INFORME_INICIAL_ES (id_informe_inicial_es);
ALTER TABLE OBJETIVO ADD CONSTRAINT FKOBJETIVO739515 FOREIGN KEY (id_informe_inicial_es) REFERENCES INFORME_INICIAL_ES (id_informe_inicial_es);
ALTER TABLE INFORME_INICIAL_ES ADD CONSTRAINT FKINFORME_IN64603 FOREIGN KEY (id_detalle_practica) REFERENCES DETALLE_PRACTICA (id_detalle_practica);
ALTER TABLE INFORME_INICIAL_EM ADD CONSTRAINT FKINFORME_IN743698 FOREIGN KEY (DETALLE_PRACTICAid_detalle_practica) REFERENCES DETALLE_PRACTICA (id_detalle_practica);
ALTER TABLE RECOMENDACIONES ADD CONSTRAINT FKRECOMENDAC626388 FOREIGN KEY (id_informe_final_es) REFERENCES INFORME_FINAL_ES (id_informe_final_es);
ALTER TABLE CONCLUSIONES ADD CONSTRAINT FKCONCLUSION136439 FOREIGN KEY (id_informe_final_es) REFERENCES INFORME_FINAL_ES (id_informe_final_es);
ALTER TABLE INFORME_FINAL_ES ADD CONSTRAINT FKINFORME_FI1483 FOREIGN KEY (id_detalle_practica) REFERENCES DETALLE_PRACTICA (id_detalle_practica);
ALTER TABLE BIBLIOGRAFIA ADD CONSTRAINT FKBIBLIOGRAF317237 FOREIGN KEY (id_informe_final_es) REFERENCES INFORME_FINAL_ES (id_informe_final_es);
ALTER TABLE ANEXOS ADD CONSTRAINT FKANEXOS46774 FOREIGN KEY (id_informe_final_es) REFERENCES INFORME_FINAL_ES (id_informe_final_es);
ALTER TABLE INFORME_FINAL_EM ADD CONSTRAINT FKINFORME_FI1477 FOREIGN KEY (id_detalle_practica) REFERENCES DETALLE_PRACTICA (id_detalle_practica);
ALTER TABLE FICHA_DESEMPEÑO ADD CONSTRAINT FKFICHA_DESE746982 FOREIGN KEY (id_detalle_practica) REFERENCES DETALLE_PRACTICA (id_detalle_practica);
ALTER TABLE RESULTADO_APRENDIZAJE ADD CONSTRAINT FKRESULTADO_316780 FOREIGN KEY (id_ficha_desempeño) REFERENCES FICHA_DESEMPEÑO (id_ficha_desempeño);
ALTER TABLE LINEA_DESARROLLO ADD CONSTRAINT FKLINEA_DESA831180 FOREIGN KEY (id_escuela_profesional) REFERENCES ESCUELA_PROFESIONAL (id_escuela_profesional);
ALTER TABLE ESTUDIANTE ADD CONSTRAINT FKESTUDIANTE401223 FOREIGN KEY (id_plan_estudio) REFERENCES PLAN_ESTUDIO (id_plan_estudio);
ALTER TABLE DETALLE_PRACTICA ADD CONSTRAINT FKDETALLE_PR399145 FOREIGN KEY (id_linea_desarrollo) REFERENCES LINEA_DESARROLLO (id_linea_desarrollo);
