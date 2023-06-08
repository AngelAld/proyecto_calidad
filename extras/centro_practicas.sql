CREATE TABLE
    CENTRO_PRACTICAS (
        id_centro_practicas serial NOT NULL,
        ruc varchar(255) NOT NULL,
        razon_social varchar(255) NOT NULL,
        rubro varchar(255) NOT NULL,
        telefono varchar(12) NOT NULL,
        correo varchar(255) NOT NULL,
        DIRECCIONid_direccion int4 NOT NULL,
        PRIMARY KEY (id_centro_practicas)
    );

CREATE TABLE
    DIRECCION (
        id_direccion serial NOT NULL,
        num varchar(255) NOT NULL,
        tipo_via varchar(255) NOT NULL,
        via varchar(255) NOT NULL,
        lon varchar(255) NOT NULL,
        lat varchar(255) NOT NULL,
        ciudad varchar(255) NOT NULL,
        pais varchar(255) NOT NULL,
        PRIMARY KEY (id_direccion)
    );

ALTER TABLE CENTRO_PRACTICAS ADD CONSTRAINT FKCENTRO_PRA163921 FOREIGN KEY (DIRECCIONid_direccion) REFERENCES DIRECCION (id_direccion);


