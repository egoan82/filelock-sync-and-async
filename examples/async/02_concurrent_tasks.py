#!/usr/bin/env python3
"""
Ejemplo de múltiples tareas concurrentes con AsyncFileLock

Este ejemplo demuestra cómo múltiples tareas asíncronas pueden
competir por el mismo recurso usando AsyncFileLock.
"""

import sys
import os
import asyncio
import random

# Agregar la carpeta src al path para importar
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from simple_filelock_async import AsyncFileLock


async def tarea_worker(worker_id, duracion_trabajo):
    """
    Simula una tarea worker que necesita acceso exclusivo a un recurso
    """
    lockfile_path = "/tmp/ejemplo_async_concurrent.lock"
    
    print(f"[Worker-{worker_id}] Iniciando, necesita trabajar por {duracion_trabajo:.1f}s")
    
    try:
        async with AsyncFileLock(lockfile_path, timeout=10, debug=True):
            print(f"[Worker-{worker_id}] ✅ Lock adquirido - comenzando trabajo exclusivo")
            
            # Simular trabajo que requiere acceso exclusivo
            pasos = int(duracion_trabajo * 2)  # Simular pasos de trabajo
            for i in range(pasos):
                print(f"[Worker-{worker_id}] Ejecutando paso {i+1}/{pasos}")
                await asyncio.sleep(0.5)
            
            print(f"[Worker-{worker_id}] 🏁 Trabajo completado")
            
    except TimeoutError:
        print(f"[Worker-{worker_id}] ⏰ Timeout - no se pudo obtener el lock")
    except Exception as e:
        print(f"[Worker-{worker_id}] ❌ Error: {e}")


async def main():
    print("=== Ejemplo de Tareas Concurrentes con AsyncFileLock ===")
    print("Iniciando múltiples workers asíncronos...")
    
    # Crear múltiples tareas con diferentes duraciones de trabajo
    tareas = []
    for i in range(1, 5):  # 4 workers
        duracion = random.uniform(2, 5)  # Entre 2 y 5 segundos
        tarea = asyncio.create_task(tarea_worker(i, duracion))
        tareas.append(tarea)
    
    print(f"Se iniciaron {len(tareas)} workers concurrentes")
    print("Cada worker intentará adquirir el mismo lock...\n")
    
    # Esperar a que todas las tareas terminen
    await asyncio.gather(*tareas)
    
    print("\nTodos los workers han terminado.")


if __name__ == "__main__":
    asyncio.run(main())