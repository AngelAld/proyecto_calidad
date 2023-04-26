#import pymysql
import psycopg2


#def obtener_conexion():
#    return pymysql.connect(host='127.0.0.1',
#                                port=3306,
#                                user='testuser',
#                                password='123456',
 #                               db='proyecto_calidad')
def obtener_conexion():
    return psycopg2.connect(host='127.0.0.1',
                                port=5432,
                                user='postgres',
                                password='USAT2023',
                                database='proyecto_calidad')
