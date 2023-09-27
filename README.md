Monitor de Cambios en Archivos de SSH.

Este script de Python permite monitorear los archivos en el directorio ~/.ssh en busca de cambios utilizando la función hash SHA-256. Si alguno de los archivos se modifica o se reemplaza, el script imprimirá un mensaje de advertencia.

Uso

1.-Asegúrate de tener Python 3 instalado en tu sistema.

2.-Guarda este script en un archivo con extensión .py, por ejemplo, ssh_monitor.py.

3.-Ejecuta el script utilizando el siguiente comando:

python ChangesSSH.py

El script calculará inicialmente los hashes de los archivos id_rsa, id_rsa.pub y authorized_keys en el directorio ~/.ssh.

Luego, entrará en un bucle infinito que verificará periódicamente si estos archivos han cambiado. El intervalo de verificación predeterminado es de 24 horas (86400 segundos), pero puedes ajustarlo según tus necesidades.

Si se detecta un cambio en cualquiera de los archivos, el script imprimirá un mensaje indicando cuál archivo ha sido modificado o reemplazado.

El script seguirá ejecutándose indefinidamente hasta que lo detengas manualmente (puedes hacerlo presionando Ctrl+C en la terminal).

Notas

·Este script utiliza la biblioteca hashlib de Python para calcular los hashes SHA-256 de los archivos.

·Asegúrate de tener los permisos adecuados para acceder al directorio ~/.ssh y a los archivos que deseas monitorear.

·Puedes personalizar la lista de archivos que deseas monitorear agregando o eliminando nombres de archivo en la lista file_name en el script.

·Ten en cuenta que este script se ejecutará en segundo plano y consumirá recursos de CPU mientras se ejecuta. Ajusta el intervalo de verificación según tus necesidades para equilibrar la detección de cambios y el uso de recursos.


+Advertencia
Este script se proporciona "tal cual" y se recomienda utilizarlo con precaución en entornos de producción. La monitorización de archivos es una práctica común para detectar cambios no autorizados, pero asegúrate de comprender los riesgos y las implicaciones de seguridad antes de implementarlo en un entorno de producción.




