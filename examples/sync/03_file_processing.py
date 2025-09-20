#!/usr/bin/env python3
"""
Ejemplo práctico: Procesamiento de archivos con FileLock

Este ejemplo muestra un caso de uso real donde múltiples procesos
necesitan procesar un archivo compartido de forma exclusiva.
"""

import sys
import os
import time
import json
import threading
from datetime import datetime

# Agregar la carpeta src al path para importar
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from simple_filelock import FileLock


def procesar_archivo_json(worker_id, archivo_datos, archivo_log):
    """
    Simula el procesamiento de un archivo JSON compartido
    """
    lockfile_path = f"/tmp/{os.path.basename(archivo_datos)}.lock"
    
    try:
        print(f"[Worker-{worker_id}] Intentando procesar {archivo_datos}")
        
        with FileLock(lockfile_path, timeout=10, debug=True):
            print(f"[Worker-{worker_id}] 🔒 Acceso exclusivo obtenido")
            
            # Leer el archivo actual
            if os.path.exists(archivo_datos):
                with open(archivo_datos, 'r') as f:
                    datos = json.load(f)
            else:
                datos = {"contadores": {}, "historial": []}
            
            # Simular procesamiento
            print(f"[Worker-{worker_id}] Procesando datos...")
            time.sleep(2)  # Simula trabajo
            
            # Actualizar datos
            worker_key = f"worker_{worker_id}"
            if worker_key not in datos["contadores"]:
                datos["contadores"][worker_key] = 0
            datos["contadores"][worker_key] += 1
            
            datos["historial"].append({
                "worker": worker_id,
                "timestamp": datetime.now().isoformat(),
                "accion": "procesamiento_completado"
            })
            
            # Escribir archivo actualizado
            with open(archivo_datos, 'w') as f:
                json.dump(datos, f, indent=2)
            
            # Log de la operación
            with open(archivo_log, 'a') as f:
                f.write(f"[{datetime.now()}] Worker-{worker_id} completó el procesamiento\n")
            
            print(f"[Worker-{worker_id}] ✅ Procesamiento completado")
            
    except TimeoutError:
        print(f"[Worker-{worker_id}] ⏰ No se pudo obtener acceso exclusivo")
    except Exception as e:
        print(f"[Worker-{worker_id}] ❌ Error: {e}")


def main():
    print("=== Ejemplo: Procesamiento de archivos con FileLock ===")
    
    archivo_datos = "/tmp/datos_compartidos.json"
    archivo_log = "/tmp/procesamiento.log"
    
    # Limpiar archivos anteriores
    for archivo in [archivo_datos, archivo_log]:
        if os.path.exists(archivo):
            os.remove(archivo)
    
    print(f"Archivo de datos: {archivo_datos}")
    print(f"Archivo de log: {archivo_log}")
    print()
    
    # Crear múltiples workers que procesarán el archivo concurrentemente
    workers = []
    for i in range(1, 5):  # 4 workers
        worker = threading.Thread(
            target=procesar_archivo_json, 
            args=(i, archivo_datos, archivo_log)
        )
        workers.append(worker)
        worker.start()
        time.sleep(0.5)  # Pequeña pausa entre inicios
    
    # Esperar a que todos terminen
    for worker in workers:
        worker.join()
    
    print("\n=== Resultados finales ===")
    
    # Mostrar el archivo de datos final
    if os.path.exists(archivo_datos):
        with open(archivo_datos, 'r') as f:
            datos_finales = json.load(f)
        print("Datos finales:", json.dumps(datos_finales, indent=2))
    
    # Mostrar el log
    if os.path.exists(archivo_log):
        print("\nLog de operaciones:")
        with open(archivo_log, 'r') as f:
            print(f.read())


if __name__ == "__main__":
    main()