#!/usr/bin/env python3
"""
Ejemplo de Tipado y Valores por Defecto

Este ejemplo demuestra el tipado completo agregado a las clases FileLock
y AsyncFileLock, así como el uso de valores por defecto explícitos.
"""

import sys
import os
import asyncio
from typing import Optional, Union

# Agregar la carpeta src al path para importar
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from simple_filelock import FileLock
from simple_filelock_async import AsyncFileLock


def ejemplo_tipado_sincronizado() -> None:
    """
    Ejemplo que muestra el tipado para FileLock
    """
    print("=== Ejemplo de Tipado para FileLock ===")
    
    # Ejemplo 1: Usando valores por defecto
    lockfile_path: str = "/tmp/ejemplo_tipado.lock"
    
    # Con valores por defecto (timeout=None, debug=False)
    lock1: FileLock = FileLock(lockfile_path)
    
    print(f"Lock creado con valores por defecto:")
    print(f"  - Ruta: {lock1.lockfile_path}")
    print(f"  - Timeout: {lock1.timeout}")
    print(f"  - Debug: {lock1.debug}")
    
    # Ejemplo 2: Especificando parámetros
    timeout_segundos: Optional[float] = 5.0
    modo_debug: bool = True
    
    lock2: FileLock = FileLock(lockfile_path, timeout=timeout_segundos, debug=modo_debug)
    
    print(f"\nLock creado con parámetros específicos:")
    print(f"  - Ruta: {lock2.lockfile_path}")
    print(f"  - Timeout: {lock2.timeout}")
    print(f"  - Debug: {lock2.debug}")
    
    # Ejemplo 3: Uso con context manager (tipado implícito)
    try:
        with FileLock(lockfile_path, timeout=3.0, debug=True) as lock:
            print(f"\n✅ Context manager - tipo inferido: {type(lock)}")
            print("Ejecutando sección crítica...")
            
            # El método is_locked() retorna bool
            esta_bloqueado: bool = lock.is_locked()
            print(f"¿Está bloqueado? {esta_bloqueado}")
            
    except TimeoutError as e:
        print(f"⏰ Timeout: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")


async def ejemplo_tipado_asincronizado() -> None:
    """
    Ejemplo que muestra el tipado para AsyncFileLock
    """
    print("\n=== Ejemplo de Tipado para AsyncFileLock ===")
    
    # Ejemplo 1: Usando valores por defecto
    lockfile_path: str = "/tmp/ejemplo_async_tipado.lock"
    
    # Con valores por defecto (timeout=None, debug=False)
    lock1: AsyncFileLock = AsyncFileLock(lockfile_path)
    
    print(f"AsyncLock creado con valores por defecto:")
    print(f"  - Ruta: {lock1.lockfile_path}")
    print(f"  - Timeout: {lock1.timeout}")
    print(f"  - Debug: {lock1.debug}")
    
    # Ejemplo 2: Especificando parámetros con diferentes tipos
    timeout_opcional: Optional[float] = None  # Sin timeout
    modo_debug: bool = False
    
    lock2: AsyncFileLock = AsyncFileLock(
        lockfile_path=lockfile_path,
        timeout=timeout_opcional,
        debug=modo_debug
    )
    
    print(f"\nAsyncLock con timeout None:")
    print(f"  - Ruta: {lock2.lockfile_path}")
    print(f"  - Timeout: {lock2.timeout}")
    print(f"  - Debug: {lock2.debug}")
    
    # Ejemplo 3: Uso con async context manager
    try:
        async with AsyncFileLock(lockfile_path, timeout=2.5, debug=True) as lock:
            print(f"\n✅ Async context manager - tipo inferido: {type(lock)}")
            print("Ejecutando sección crítica asíncrona...")
            
            # El método is_locked() es asíncrono y retorna bool
            esta_bloqueado: bool = await lock.is_locked()
            print(f"¿Está bloqueado? {esta_bloqueado}")
            
            # Simular trabajo asíncrono
            await asyncio.sleep(0.5)
            
    except TimeoutError as e:
        print(f"⏰ Timeout: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")


def ejemplo_parametros_flexibles() -> None:
    """
    Ejemplo mostrando la flexibilidad de los parámetros tipados
    """
    print("\n=== Ejemplo de Flexibilidad de Parámetros ===")
    
    # Diferentes formas de especificar timeout
    timeouts_validos: list[Optional[float]] = [
        None,      # Sin timeout (esperar indefinidamente)
        0.0,       # Timeout inmediato (no bloquear)
        1.5,       # 1.5 segundos
        10,        # 10 segundos (int se convierte automáticamente)
    ]
    
    lockfile_base: str = "/tmp/ejemplo_flexible"
    
    for i, timeout in enumerate(timeouts_validos):
        try:
            lockfile: str = f"{lockfile_base}_{i}.lock"
            
            # Crear lock con diferentes configuraciones
            with FileLock(lockfile, timeout=timeout, debug=True) as lock:
                print(f"✅ Lock {i+1} - timeout={timeout} funcionando")
                
                # Mostrar tipos inferidos
                tipo_timeout: type = type(lock.timeout)
                tipo_debug: type = type(lock.debug)
                tipo_path: type = type(lock.lockfile_path)
                
                print(f"  - Tipos: timeout={tipo_timeout.__name__}, "
                      f"debug={tipo_debug.__name__}, path={tipo_path.__name__}")
                
        except TimeoutError:
            print(f"⏰ Lock {i+1} - timeout={timeout} - no disponible inmediatamente")
        except Exception as e:
            print(f"❌ Lock {i+1} - timeout={timeout} - error: {e}")


def main() -> None:
    """
    Función principal que ejecuta todos los ejemplos
    """
    print("🔍 Ejemplo de Tipado y Valores por Defecto para FileLock")
    print("=" * 60)
    
    # Ejemplos síncronos
    ejemplo_tipado_sincronizado()
    ejemplo_parametros_flexibles()
    
    # Ejemplos asíncronos
    print("\n" + "=" * 60)
    asyncio.run(ejemplo_tipado_asincronizado())
    
    print("\n" + "=" * 60)
    print("✅ Todos los ejemplos de tipado completados exitosamente!")
    print("\nBeneficios del tipado agregado:")
    print("  🎯 Mejor soporte de IDEs (autocompletado, detección de errores)")
    print("  📝 Documentación automática de tipos esperados")
    print("  🔍 Detección temprana de errores con herramientas como mypy")
    print("  📚 Código más legible y mantenible")


if __name__ == "__main__":
    main()