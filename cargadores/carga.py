import subprocess
import os

file_names = ["carga_00_tablas.py",
              "carga_01_clientes.py", 
              "carga_02_comunas.py", 
              "carga_03_direcciones.py",
              "carga_04_direcciones_clientes.py",
              "carga_05_restaurantes.py",
              "carga_06_platos.py",
              "carga_07_platos_restaurantes.py",
              "carga_08_sucursales.py",
              "carga_09_deliverys.py",
              "carga_10_suscripciones.py",
              "carga_11_despachadores.py",
              "carga_12_pedidos.py",
              "carga_13_calificaciones.py",
              "carga_14_pedidos_platos.py"
              ]

for file_name in file_names:
    print(f"Running {file_name}...")
    subprocess.run(["python3", os.path.join('cargadores', file_name)])
    print(f"{file_name} finished running.")

os.system("python3 manage.py migrate") #cargamos la migracion de django