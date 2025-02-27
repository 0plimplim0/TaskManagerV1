import sqlite3
import os
import time

DB_NAME = "beta1-database.db"

def initialize_db():
    if not os.path.exists(DB_NAME):
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                title TEXT PRIMARY KEY,
                description TEXT
            )
        ''')
        connection.commit()
        connection.close()
        print("Base de datos creada exitosamente.")

initialize_db()

connection = sqlite3.connect(DB_NAME)

cursor = connection.cursor()

def menu():
    print("============================")
    print("TASK MANAGER | version: BETA")
    print("============================")
    print("1. Agregar una tarea")
    print("2. Eliminar una tarea")
    print("3. Editar una tarea")
    print("4. Mostrar todas las tareas")
    print("5. Salir del programa")
    print("============================")

def view_tasks():
    rows = cursor.execute("select * from tasks;").fetchall()

    if rows:
        print("\n=== Lista de tareas ===\n")
        for title, desc in rows:
            print(f"- {title}: {desc}")
        print("=======================")
    else: print("No se ha agregado ninguna tarea.")

    input("\nPresiona ENTER para volver al menú.")

def add_task():
    title = input("Titulo: ")
    description = input("Descripción: ")

    try: 
        cursor.execute("insert into tasks (title, description) values (?, ?)", (title, description))
        connection.commit()
        print("La tarea se ha agregado correctamente.")
    except Exception as error:
        print("Error al agregar la tarea: ", error)

    time.sleep(2)

def delete_task():
    task = input("Qué tarea quieres eliminar: ").strip()

    try:
        cursor.execute("delete from tasks where title is ?;", (task,))
        connection.commit()
        print("La tarea se ha eliminado correctamente.")
    except Exception as error:
        print("Error al eliminar la tarea: ", error)

    time.sleep(2)

def update_task():
    task = input("Qué tarea quieres actualizar?: ")
    task_exist = cursor.execute("select * from tasks where title is ?;", (task,)).fetchall()

    try:
        if task_exist:
            option = input("Qué quieres actualizar? (titulo, descripcion): ").lower()
            if option == "titulo":
                new_title = input("Nuevo titulo: ").strip()
                cursor.execute("update tasks set title = ? where title = ?;", (new_title, task))
                connection.commit()
                print("La tarea se ha actualizado correctamente.")
            elif option == "descripcion":
                new_description = input("Nueva descripcion: ").strip()
                cursor.execute("update tasks set description = ? where title = ?;", (new_description, task))
                connection.commit()
                print("La tarea se ha actualizado correctamente.")
            else: 
                print("Opcion invalida.")
        else:
            print("No existe ninguna tarea con ese titulo.")
    except Exception as error:
        print("Error al actualizar la tarea:", error)
    
    time.sleep(2)



while True:
    os.system("clear")
    menu()
    
    try:
        usr_input = int(input("Selecciona una opción: "))
    except ValueError:
        print("Entrada invalida. Debes ingresar un número.")
        time.sleep(2)
        continue

    if usr_input == 1:
        add_task()
    elif usr_input == 2:
        delete_task()
    elif usr_input == 3:
        update_task()
    elif usr_input == 4:
        view_tasks()
    elif usr_input == 5:
        connection.close()
        print("Saliendo...")
        break
    else:
        print("Selecciona una opción valida.")
