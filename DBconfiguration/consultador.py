import psycopg2

#Conexión a la base de datos
conexion = psycopg2.connect(
    host = "localhost",
    port= "5432", #es el puerto que escucha postgres
    database = "credenciales",
    user = "Admin",
    password = "p4ssw0rdDB"
)

#crear cursor
cursor = conexion.cursor()

#ejecutar consulta
cursor.execute("SELECT * FROM usuarios")
#fetchone() =  una fila
#fetchmany(n) = hasta n filas
registros = cursor.fetchall() #Recuperar todas las filas devueltas
#registros almacena en tuplas

for fila in registros:
    print(fila)

#Cerrar la conexión
cursor.close()
conexion.close()