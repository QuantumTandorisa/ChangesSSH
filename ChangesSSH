import os
import hashlib
import time

# Ruta al directorio .ssh // Path to .ssh directory
ssh_dir = os.path.expanduser("~/.ssh")

# Crear un diccionario para almacenar los hash de los archivos // Create a dictionary for storing file hashes
file_hashes = {}

def calculate_hash(file_path):
    # Calcular el hash SHA-256 del archivo // Calculate SHA-256 hash of the file
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while True:
            data = f.read(65536)  # Leer el archivo en fragmentos para manejar archivos grandes // Read the file in fragments to handle large files
            if not data:
                break
            hasher.update(data)
    return hasher.hexdigest()

# Obtener los hashes iniciales de los archivos // Obtain the initial hashes of the files
for file_name in ["id_rsa", "id_rsa.pub", "authorized_keys"]:
    file_path = os.path.join(ssh_dir, file_name)
    if os.path.exists(file_path):
        file_hashes[file_name] = calculate_hash(file_path)

# Definir el intervalo de verificación (en segundos) // Define check interval (in seconds)
interval = 86400

while True:
    # Verificar los archivos en busca de cambios // Check files for changes
    for file_name in file_hashes:
        file_path = os.path.join(ssh_dir, file_name)
        if os.path.exists(file_path):
            current_hash = calculate_hash(file_path)
            if current_hash != file_hashes[file_name]:
                print(f"El archivo {file_name} ha sido modificado o reemplazado.")
                file_hashes[file_name] = current_hash

    # Esperar antes de la próxima verificación // Wait before the next verification
    time.sleep(interval)
