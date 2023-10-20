ChangesSSH es un programa escrito en Python que se utiliza para monitorear y registrar cambios en el directorio SSH del sistema. Puede detectar modificaciones y eliminaciones de archivos importantes, como claves SSH y archivos de configuración.

## Características

- Monitorea el directorio SSH en busca de cambios en tiempo real.
- Registra los eventos de modificación y eliminación de archivos en una base de datos SQLite.
- Calcula y compara los hashes SHA-256 de los archivos para verificar su integridad.

## Requisitos

- Python 3.x
- Bibliotecas requeridas, que puedes instalar ejecutando `pip install -r requirements.txt`.

## Uso

- Clona este repositorio en tu sistema.
- Ejecuta el programa con el comando `python3 ChangesSSH.py`.

El programa monitoreará el directorio SSH y registrará los cambios en la base de datos "ssh_changes.db".
Puedes consultar los registros almacenados en la base de datos con una herramienta SQLite o utilizando el script de ejemplo proporcionado.

## Configuración

Puedes personalizar las acciones adicionales que deseas tomar en caso de cambios detectados en la función verify_integrity y protect_critical_files.
