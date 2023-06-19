# import pymysql
import psycopg2


def obtener_conexion():
    return psycopg2.connect(host='127.0.0.1',
                            port=5432,
                            user='postgres',
                            password='123456789',
                            database='bd_calidad')

# si no tienen postgres instalado pueden usar esta bd online

# def obtener_conexion():
#       return psycopg2.connect(host='jelani.db.elephantsql.com',
#                               port=5432,
#                               user='nzsbwaov',
#                               password='KGMLF1yVbv70Y7GqkfPRPVNL0C0GWQ2O',
#                               database='nzsbwaov')