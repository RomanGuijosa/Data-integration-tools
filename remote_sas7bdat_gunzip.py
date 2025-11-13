import paramiko

# DATOS PARA CONEXION Y RUTA

HOST = "tu_servidor.com"
PORT = 22
USERNAME = "tu_usuario"
PASSWORD = "tu_contraseña"
REMOTE_PATH = "/datos"

# CONEXIÓN SSH

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOST, port=PORT, username=USERNAME, password=PASSWORD)

# DESCOMPRIMIR ARCHIVOS MEDIANTE COMANDOS

comando = f"""
cd {REMOTE_PATH}
for f in *.sas7bdat.gz; do
    base="${{f%.gz}}"        
    if [ ! -f "$base" ]; then
        echo "Descomprimiendo $f -> $base"
        gzip -cd "$f" > "$base"
    else
        echo "Archivo existente, omitido: $base"
    fi
done
"""

print("Ejecutando descompresión en servidor remoto...\n")
stdin, stdout, stderr = ssh.exec_command(comando)

# Mostrar salida del proceso
print(stdout.read().decode())
print(stderr.read().decode())

ssh.close()
print(" Proceso completado!")

