import os

# Obtiene la lista de archivos en el directorio actual
files_in_directory = os.listdir()

# Imprime la lista de archivos
print("Archivos en el directorio actual:")
for file_name in files_in_directory:
    print(file_name)
