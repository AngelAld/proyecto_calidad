# import pymysql
import psycopg2


<<<<<<< HEAD
#def obtener_conexion():
#    return psycopg2.connect(host='angelar-3301.postgres.pythonanywhere-services.com',
#                            port=13301,
#                            user='super',
#                            password='PROYECTOCALIDAD',
#                            database='db_calidad')
=======
# def obtener_conexion():
#     return psycopg2.connect(host='angelar-3301.postgres.pythonanywhere-services.com',
#                             port=13301,
#                             user='super',
#                             password='PROYECTOCALIDAD',
#                             database='db_calidad')
>>>>>>> fc82150efad09c297c572d19d54b3b3fe9a42105


def obtener_conexion():
      return psycopg2.connect(host='jelani.db.elephantsql.com',
                              port=5432,
                              user='nzsbwaov',
                              password='KGMLF1yVbv70Y7GqkfPRPVNL0C0GWQ2O',
                              database='nzsbwaov')