#!/usr/bin/env python3
"""
Ejemplo básico de uso de AsyncFileLock

Este ejemplo muestra el uso más simple de la clase AsyncFileLock
usando el contexto 'async with' para garantizar la liberación automática del lock.
"""

import sys
import os
import asyncio

# Agregar la carpeta src al path para importar
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from simple_filelock_async import AsyncFileLock


async def tarea_con_lock():
    """Tarea que requiere acceso exclusivo a un recurso"""
    lockfile_path = "/tmp/ejemplo_async_basico.lock"
    
    print(f"Usando lockfile: {lockfile_path}")
    
    try:
        # Uso básico con async context manager
        async with AsyncFileLock(lockfile_path, debug=True):
            print("🔒 Lock adquirido - ejecutando sección crítica asíncrona...")
            print("Simulando trabajo asíncrono que requiere exclusividad mutua...")
            
            # Simular trabajo asíncrono
            await asyncio.sleep(3)
            
            print("✅ Trabajo asíncrono completado")
        
        print("🔓 Lock liberado automáticamente al salir del contexto")
        
    except TimeoutError as e:
        print(f"❌ Error de timeout: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")


async def main():
    print("=== Ejemplo Básico de AsyncFileLock ===")
    await tarea_con_lock()


if __name__ == "__main__":
    asyncio.run(main())