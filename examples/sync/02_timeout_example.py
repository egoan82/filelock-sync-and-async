#!/usr/bin/env python3
"""
Ejemplo de FileLock con timeout

Este ejemplo demuestra cómo usar FileLock con un timeout
para evitar esperas indefinidas cuando otro proceso mantiene el lock.
"""

import sys
import os
import time
import threading

# Agregar la carpeta src al path para importar
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from simple_filelock import FileLock


def proceso_largo(nombre, duracion):
    """Simula un proceso que mantiene el lock por un tiempo"""
    lockfile_path = "/tmp/ejemplo_timeout.lock"
    
    print(f"[{nombre}] Intentando adquirir el lock...")
    
    try:
        with FileLock(lockfile_path, timeout=5, debug=True):
            print(f"[{nombre}] ✅ Lock adquirido - trabajando por {duracion} segundos...")
            time.sleep(duracion)
            print(f"[{nombre}] 🏁 Trabajo completado")
            
    except TimeoutError as e:
        print(f"[{nombre}] ⏰ Timeout: {e}")
    except Exception as e:
        print(f"[{nombre}] ❌ Error: {e}")


def main():
    print("=== Ejemplo de FileLock con Timeout ===")
    print("Iniciando dos procesos concurrentes...")
    
    # Crear dos hilos que intentarán adquirir el mismo lock
    hilo1 = threading.Thread(target=proceso_largo, args=("Proceso-1", 8))
    hilo2 = threading.Thread(target=proceso_largo, args=("Proceso-2", 3))
    
    # Iniciar ambos hilos
    hilo1.start()
    time.sleep(0.1)  # Pequeña pausa para que el proceso 1 adquiera el lock primero
    hilo2.start()
    
    # Esperar a que ambos hilos terminen
    hilo1.join()
    hilo2.join()
    
    print("Todos los procesos han terminado.")


if __name__ == "__main__":
    main()