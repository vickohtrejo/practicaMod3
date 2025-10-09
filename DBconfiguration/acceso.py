import psycopg2
import getpass #vuelve invisible en pantalla un input

# Configuración de conexión a la base de datos en Docker
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "credenciales"
DB_USER = 'Admin'
DB_PASSWORD = "p4ssw0rdDB"

def conectar_db():
    """Conecta a la base de datos PostgreSQL y retorna la conexión."""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return conn
    except Exception as e:
        print("Error de conexión:", e)
        return None


def obtener_datos_usuario(username, password):
    #Consulta la base de datos para obtener los datos de un usuario a partir de sus credenciales.
    conn = conectar_db()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        # Verificar si el usuario y contraseña existen en la tabla credenciales
        query = """
        SELECT u.id_usuario, u.nombre, u.correo, u.telefono, u.fecha_nacimiento
        FROM credenciales c
        JOIN usuarios u ON c.id_usuario = u.id_usuario
        WHERE c.username = %s AND c.password_hash = %s;
        """
        cursor.execute(query, (username, password))
        usuario = cursor.fetchone()

        if usuario:
            print("\nDatos del usuario encontrado:")
            print(f"ID: {usuario[0]}")
            print(f"Nombre: {usuario[1]}")
            print(f"Correo: {usuario[2]}")
            print(f"Teléfono: {usuario[3]}")
            print(f"Fecha de Nacimiento: {usuario[4]}")
            cursor.close()
            conn.close()
        else:
            print("\nUsuario o contraseña incorrectos.")
            cursor.close()
            conn.close()
    except Exception as e:
        print("Error al consultar la base de datos:", e)

def insertar_usuario(nombre, correo, telefono, fecha_nacimiento, username, password):
    conn = conectar_db()
    #Si no logra conectarse, no sigue
    if not conn:
        return
    
    try:
        cursor = conn.cursor() #Crear el cursor
        #Insertar usuario en la tabla
        cursor.execute(
            """
            INSERT INTO usuarios(nombre, correo, telefono, fecha_nacimiento)
            VALUES (%s,%s,%s,%s) RETURNING id_usuario;
            """,(nombre,correo,telefono,fecha_nacimiento))
        # Guardar id del nuevo usuario
        id_usuario = cursor.fetchone()[0]

        #Almacenamos las credenciales
        cursor.execute(
            """
            INSERT INTO credenciales(id_usuario, username, password_hash)
            VALUES (%s,%s,%s);
            """,(id_usuario, username, password))
        
        #Confirmar los cambios en la base de datos
        conn.commit()
        print("Usuario y la credencial han sido insertados correctamente")
    #Si ocurre un error..
    except Exception as e:
        print("Error al insertar: ",e)
        #Revierte cualquier cambio
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def actualizar_correo(id_usuario, nuevo_correo):
    conn = conectar_db()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        #Actualización
        cursor.execute(("UPDATE usuarios SET correo = %s WHERE id_usuario = %s;"),(nuevo_correo, id_usuario))

        #Ejecutar cambios
        conn.commit()
        print("Correo actualizado correctamente")
    except Exception as e:
        print("Error al actualizar: ",e)
        #Revierte cualquier cambio
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def eliminar_usuario(id_usuario):
    conn = conectar_db()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        #Eliminar credencial primero por la restricción de llave foranea
        cursor.execute(("DELETE FROM credenciales WHERE id_usuario = %s;"),(id_usuario))
        #Eliminar usuario
        cursor.execute(("DELETE FROM usuarios WHERE id_usuario = %s;"),(id_usuario))

        conn.commit()
        print("Usuario correctamente eliminado")

    except Exception as e:
        print("Error al eliminar: ",e)
        #Revierte cualquier cambio
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def menu():
    while True:
        print("-------SELECCIÓN DE EJECUCIÓN----------")
        print("1.- Consulta de usuario")
        print("2.- Insertar nuevo usuario")
        print("3.- Actualizar correo de usuario")
        print("4.- Eliminar usuario")
        print("0.- Salir")

        opcion = input("\nSelecciona una opción (0 - 4): ")
        if opcion == "1":
            print("Inicio de sesión en la base de datos")
            #Solicitar credenciales al usuario
            user = input("Ingrese su usuario: ")
            pwd = getpass.getpass("Ingrese su contraseña: ")#No muestra la contraseña a escribir
            #Consultar base de datos
            obtener_datos_usuario(user, pwd)

        elif opcion == "2":
            print("Insertar datos")
            nombreNuevo = input("Ingresa el nombre del nuevo usuario: ")
            correo = input("Ingresa el correo: ")
            telefono = input("Ingresa el telefono: ")
            fecha_nacimiento = input("Ingresa la fecha de nacimiento: ")
            usuario = input("Ingresa nombre de usuario nuevo: ")
            contra = input("Ingresa contraseña nueva: ")
            insertar_usuario(nombreNuevo, correo, telefono, fecha_nacimiento, usuario,contra)
        
        elif opcion == "3":
            print("Actualizar correo")
            id_usuario = input("Comparte el id del usuario al que deseas modificar: ")
            correoNuevo = input("Comparte el correo nuevo: ")
            actualizar_correo(id_usuario, correoNuevo)

        elif opcion == "4":
            print("Eliminación de Usuario")
            id_usuario = input("Comparte el id del usuario que deseas eliminar: ")
            eliminar_usuario(id_usuario)

        elif opcion == "0":
            print("Programa Terminado")
            break
        
        else:
            print("Prueba de nuevo")

if __name__ == "__main__":
    menu()

    #print("Inicio de sesión en la base de datos")
    # Solicitar credenciales al usuario
    #user = input("Ingrese su usuario: ")
    #pwd = getpass.getpass("Ingrese su contraseña: ")#No muestra la contraseña a escribir
    #Consultar base de datos
    #obtener_datos_usuario(user, pwd)

    #print("Insertar datos")
    #nombreNuevo = input("Ingresa el nombre del nuevo usuario")
    #correo = input("Ingresa el correo")
    #telefono = input("Ingresa el telefono")
    #fecha_nacimiento = input("Ingresa la fecha de nacimiento")
    #usuario = input("Ingresa nombre de usuario nuevo")
    #contra = input("Ingresa contraseña nueva")
    #insertar_usuario(nombreNuevo, correo, telefono, fecha_nacimiento, usuario,contra)

    #print("Actualizar correo")
    #id_usuario = input("Comparte el id del usuario al que deseas modificar")
    #correoNuevo = input("Comparte el correo nuevo")
    #actualizar_correo(id_usuario, correoNuevo)

    #print("Eliminación de Usuario")
    #id_usuario = input("Comparte el id del usuario que deseas eliminar")
    #eliminar_usuario()