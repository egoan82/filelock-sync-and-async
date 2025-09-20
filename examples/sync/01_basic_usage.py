#!/usr/bin/env python3
"""
Ejemplo básico de uso de FileLock

Este ejemplo muestra el uso más simple de la clase FileLock
usando el contexto 'with' para garantizar la liberación automática del lock.
"""

import sys
import os
import time

# Agregar la carpeta src al path para importar
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from simple_filelock import FileLock


def main():
    print("=== Ejemplo Básico de FileLock ===")
    
    lockfile_path = "/tmp/ejemplo_basico.lock"
    
    print(f"Usando lockfile: {lockfile_path}")
    
    try:
        # Uso básico con context manager
        with FileLock(lockfile_path, debug=True):
            print("🔒 Lock adquirido - ejecutando sección crítica...")
            print("Simulando trabajo que requiere exclusividad mutua...")
            time.sleep(3)
            print("✅ Trabajo completado")
        
        print("🔓 Lock liberado automáticamente al salir del contexto")
        
    except TimeoutError as e:
        print(f"❌ Error de timeout: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")


if __name__ == "__main__":
    main()