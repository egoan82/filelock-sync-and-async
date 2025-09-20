#!/usr/bin/env python3
"""
Ejemplo avanzado: Uso mixto de FileLock y AsyncFileLock

Este ejemplo demuestra cómo procesos síncronos y asíncronos pueden
coordinar el acceso a recursos compartidos usando el mismo lockfile.
"""

import sys
import os
import time
import asyncio
import threading
import json
from datetime import datetime

# Agregar la carpeta src al path para importar
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from simple_filelock import FileLock
from simple_filelock_async import AsyncFileLock


def proceso_sincronizado(worker_id, archivo_compartido, total_iteraciones=5):
    """
    Proceso síncrono que actualiza un archivo compartido
    """
    lockfile_path = f"{archivo_compartido}.lock"
    
    print(f"[Sync-Worker-{worker_id}] Iniciado")
    
    for i in range(total_iteraciones):
        try:
            with FileLock(lockfile_path, timeout=10, debug=True):
                print(f"[Sync-Worker-{worker_id}] 🔒 Lock obtenido - iteración {i+1}")
                
                # Leer archivo actual
                if os.path.exists(archivo_compartido):
                    with open(archivo_compartido, 'r') as f:
                        datos = json.load(f)
                else:
                    datos = {"operaciones": [], "contadores": {"sync": 0, "async": 0}}
                
                # Simular procesamiento
                time.sleep(1)
                
                # Actualizar datos
                datos["contadores"]["sync"] += 1
                datos["operaciones"].append({
                    "tipo": "sync",
                    "worker_id": worker_id,
                    "iteracion": i + 1,
                    "timestamp": datetime.now().isoformat()
                })
                
                # Escribir archivo
                with open(archivo_compartido, 'w') as f:
                    json.dump(datos, f, indent=2)
                
                print(f"[Sync-Worker-{worker_id}] ✅ Operación {i+1} completada")
                
        except TimeoutError:
            print(f"[Sync-Worker-{worker_id}] ⏰ Timeout en iteración {i+1}")
        except Exception as e:
            print(f"[Sync-Worker-{worker_id}] ❌ Error: {e}")
        
        # Pausa entre iteraciones
        time.sleep(0.5)
    
    print(f"[Sync-Worker-{worker_id}] 🏁 Finalizado")


async def proceso_asincronizado(worker_id, archivo_compartido, total_iteraciones=5):
    """
    Proceso asíncrono que actualiza el mismo archivo compartido
    """
    lockfile_path = f"{archivo_compartido}.lock"
    
    print(f"[Async-Worker-{worker_id}] Iniciado")
    
    for i in range(total_iteraciones):
        try:
            async with AsyncFileLock(lockfile_path, timeout=10, debug=True):
                print(f"[Async-Worker-{worker_id}] 🔒 Lock obtenido - iteración {i+1}")
                
                # Leer archivo actual (en executor para no bloquear event loop)
                loop = asyncio.get_event_loop()
                
                def leer_archivo():
                    if os.path.exists(archivo_compartido):
                        with open(archivo_compartido, 'r') as f:
                            return json.load(f)
                    return {"operaciones": [], "contadores": {"sync": 0, "async": 0}}
                
                datos = await loop.run_in_executor(None, leer_archivo)
                
                # Simular procesamiento asíncrono
                await asyncio.sleep(1)
                
                # Actualizar datos
                datos["contadores"]["async"] += 1
                datos["operaciones"].append({
                    "tipo": "async",
                    "worker_id": worker_id,
                    "iteracion": i + 1,
                    "timestamp": datetime.now().isoformat()
                })
                
                # Escribir archivo (en executor)
                def escribir_archivo():
                    with open(archivo_compartido, 'w') as f:
                        json.dump(datos, f, indent=2)
                
                await loop.run_in_executor(None, escribir_archivo)
                
                print(f"[Async-Worker-{worker_id}] ✅ Operación {i+1} completada")
                
        except TimeoutError:
            print(f"[Async-Worker-{worker_id}] ⏰ Timeout en iteración {i+1}")
        except Exception as e:
            print(f"[Async-Worker-{worker_id}] ❌ Error: {e}")
        
        # Pausa entre iteraciones
        await asyncio.sleep(0.5)
    
    print(f"[Async-Worker-{worker_id}] 🏁 Finalizado")


async def main():
    print("=== Ejemplo: Coordinación Sync/Async con FileLock ===")
    
    archivo_compartido = "/tmp/datos_mixtos.json"
    
    # Limpiar archivo anterior
    if os.path.exists(archivo_compartido):
        os.remove(archivo_compartido)
    
    print(f"Archivo compartido: {archivo_compartido}")
    print("Iniciando workers síncronos y asíncronos concurrentemente...\n")
    
    # Crear workers síncronos en hilos
    hilos_sync = []
    for i in range(1, 3):  # 2 workers síncronos
        hilo = threading.Thread(
            target=proceso_sincronizado, 
            args=(i, archivo_compartido, 3)
        )
        hilos_sync.append(hilo)
        hilo.start()
    
    # Crear workers asíncronos
    tareas_async = []
    for i in range(1, 3):  # 2 workers asíncronos
        tarea = asyncio.create_task(
            proceso_asincronizado(i, archivo_compartido, 3)
        )
        tareas_async.append(tarea)
    
    # Esperar a que terminen los workers asíncronos
    await asyncio.gather(*tareas_async)
    
    # Esperar a que terminen los workers síncronos
    for hilo in hilos_sync:
        hilo.join()
    
    print("\n=== Resultados Finales ===")
    
    # Mostrar resultados
    if os.path.exists(archivo_compartido):
        with open(archivo_compartido, 'r') as f:
            datos_finales = json.load(f)
        
        print(f"Total de operaciones sync: {datos_finales['contadores']['sync']}")
        print(f"Total de operaciones async: {datos_finales['contadores']['async']}")
        print(f"Total de operaciones: {len(datos_finales['operaciones'])}")
        
        print("\nÚltimas 5 operaciones:")
        for op in datos_finales['operaciones'][-5:]:
            print(f"  - {op['tipo'].upper()} Worker-{op['worker_id']} "
                  f"(iter {op['iteracion']}) - {op['timestamp']}")


if __name__ == "__main__":
    asyncio.run(main())