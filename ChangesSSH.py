# -*- coding: utf-8 -*-
'''
   ________                                __________ __  __
  / ____/ /_  ____ _____  ____ ____  _____/ ___/ ___// / / /
 / /   / __ \/ __ `/ __ \/ __ `/ _ \/ ___/\__ \\__ \/ /_/ / 
/ /___/ / / / /_/ / / / / /_/ /  __(__  )___/ /__/ / __  /  
\____/_/ /_/\__,_/_/ /_/\__, /\___/____//____/____/_/ /_/   
                       /____/                               
'''
#######################################################
#    ChangesSSH.py
#
# ChangesSSH is a simple program for monitoring and 
# logging changes in the system SSH directory. It can
# detect modifications and deletions of important 
# files, such as SSH keys and configuration files.
#
#
# 10/18/23 - Changed to Python3 (finally)
#
# Author: Facundo Fernandez 
#
#
#######################################################

import time
import os
import hashlib
import logging
import sqlite3
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import schedule
import threading

# Setting up the log in a file / Configurar el registro (log) en un archivo
log_file = 'ssh_changes.log'
logging.basicConfig(filename=log_file, level=logging.INFO,
                    format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# SSH Directory / Directorio SSH
ssh_dir = os.path.expanduser("~/.ssh")

# Dictionary for storing file hashes / Diccionario para almacenar los hash de los archivos
file_hashes = {}

# Function to create a connection and cursor / Función para crear una conexión y cursor
def create_connection_and_cursor():
    connection = sqlite3.connect('ssh_changes.db')
    cursor = connection.cursor()
    return connection, cursor

# Function to close the connection / Función para cerrar la conexión
def close_connection(connection):
    connection.commit()
    connection.close()

# Create or connect to the SQLite database / Crear o conectar a la base de datos SQLite
db = sqlite3.connect('ssh_changes.db')
cursor = db.cursor()

def create_table():
    cursor.execute('''CREATE TABLE IF NOT EXISTS changes
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       event_type TEXT,
                       file_name TEXT,
                       timestamp DATETIME)''')
    db.commit()

def calculate_hash(file_path):
    # Calculate SHA-256 hash of the file / Calcular el hash SHA-256 del archivo
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while True:
            data = f.read(65536)
            if not data:
                break
            hasher.update(data)
    return hasher.hexdigest()

def verify_integrity():
    for file_name in file_hashes:
        file_path = os.path.join(ssh_dir, file_name)
        if os.path.exists(file_path):
            current_hash = calculate_hash(file_path)
            if current_hash != file_hashes[file_name]:
                logging.info(f"Integridad comprometida: El archivo {file_name} ha sido modificado.")
                connection, cursor = create_connection_and_cursor()
                cursor.execute("INSERT INTO changes (event_type, file_name, timestamp) VALUES (?, ?, ?)",
                               ("MODIFIED", file_name, time.strftime('%Y-%m-%d %H:%M:%S')))
                close_connection(connection)

class SSHDirectoryHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            logging.info(f"El archivo {event.src_path} ha sido modificado.")
            connection, cursor = create_connection_and_cursor()
            cursor.execute("INSERT INTO changes (event_type, file_name, timestamp) VALUES (?, ?, ?)",
                           ("MODIFIED", os.path.basename(event.src_path), time.strftime('%Y-%m-%d %H:%M:%S')))
            close_connection(connection)
            verify_integrity()

    def on_deleted(self, event):
        if not event.is_directory:
            logging.info(f"El archivo {event.src_path} ha sido eliminado.")
            connection, cursor = create_connection_and_cursor()
            cursor.execute("INSERT INTO changes (event_type, file_name, timestamp) VALUES (?, ?, ?)",
                           ("DELETED", os.path.basename(event.src_path), time.strftime('%Y-%m-%d %H:%M:%S')))
            close_connection(connection)
            verify_integrity()


if __name__ == "__main__":
    create_table()  # Create the table in the database if it does not exist / Crear la tabla en la base de datos si no existe

    # Obtain the initial hashes of the files / Obtener los hashes iniciales de los archivos
    for file_name in ["id_rsa", "id_rsa.pub", "authorized_keys"]:
        file_path = os.path.join(ssh_dir, file_name)
        if os.path.exists(file_path):
            file_hashes[file_name] = calculate_hash(file_path)

    event_handler = SSHDirectoryHandler()
    observer = Observer()
    observer.schedule(event_handler, path=ssh_dir, recursive=False)
    observer.start()

    # Schedule tasks for file integrity verification and file protection / Programar tareas para verificación de integridad y protección de archivos
    schedule.every(1).days.do(verify_integrity)
    schedule.every(1).days.do(protect_critical_files)

    while True:
        schedule.run_pending()
        time.sleep(1)
