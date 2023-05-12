# import pymysql
import psycopg2


def obtener_conexion():
    return psycopg2.connect(host='127.0.0.1',
                            port=5432,
                            user='postgres',
                            password='USAT2023',
                            database='proyecto_calidad')
