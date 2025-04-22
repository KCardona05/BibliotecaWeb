import mysql.connector
from config.database import db_config

def conectar_db():
    try:
        conexion = mysql.connector.connect(**db_config)
        print("Conexión existosa a la base de datos")
        return conexion
    except mysql.connector.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None