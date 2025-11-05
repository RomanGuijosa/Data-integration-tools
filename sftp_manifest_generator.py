"""
sftp_manifest_generator.py
--------------------------
Script para conectarse a un servidor SFTP, listar archivos (por ejemplo .sas)
y generar un archivo manifest.csv con ruta, tamaño, fecha y nombre.

Autor: Roman Guijosa
Versión: 1.0
Fecha: 2025-11-04

Requisitos:
    - Python 3.8+
    - Paramiko (pip install paramiko)
"""

import paramiko
import csv
import os

# Datos de conexión
HOST = "servidor"
PORT = 22               
USERNAME = "roman"
PASSWORD = "password"  
REMOTE_PATH = "/user/datos" 
OUTPUT_CSV = "manifest.csv"  

# Conexión SFTP
client = paramiko.Transport((HOST, PORT))
client.connect(username=USERNAME, password=PASSWORD)
sftp = paramiko.SFTPClient.from_transport(client)

def listar_archivos(remotepath):
    """Recorre los archivos SAS del directorio remoto"""
    archivos = []
    for entry in sftp.listdir_attr(remotepath):
        nombre = entry.filename
        ruta = os.path.join(remotepath, nombre)
        if nombre.endswith(".sas"):
            archivos.append({
                "ruta_completa": ruta,
                "fecha_modificacion": entry.st_mtime,
                "tamano_bytes": entry.st_size,
                "nombre_archivo": nombre
            })
    return archivos

# Obtener la lista de archivos
archivos = listar_archivos(REMOTE_PATH)

# Guardar en CSV local
with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["ruta_completa", "fecha_modificacion", "tamano_bytes", "nombre_archivo"])
    writer.writeheader()
    writer.writerows(archivos)

sftp.close()
client.close()

print(f"✅ Archivo CSV generado: {OUTPUT_CSV} con {len(archivos)} archivos.")