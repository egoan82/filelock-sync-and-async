#!/usr/bin/env python3
"""
Script para ejecutar todos los ejemplos de FileLock y AsyncFileLock

Este script ejecuta todos los ejemplos disponibles en el repositorio
para verificar su funcionamiento.
"""

import os
import sys
import subprocess
import time
from pathlib import Path


def run_example(example_path, timeout=60):
    """Ejecuta un ejemplo específico"""
    print(f"\n{'='*60}")
    print(f"Ejecutando: {example_path}")
    print('='*60)
    
    try:
        # Ejecutar el ejemplo
        result = subprocess.run(
            [sys.executable, example_path],
            timeout=timeout,
            capture_output=False,  # Mostrar output en tiempo real
            text=True
        )
        
        if result.returncode == 0:
            print(f"\n✅ {example_path} completado exitosamente")
            return True
        else:
            print(f"\n❌ {example_path} falló con código {result.returncode}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"\n⏰ {example_path} excedió el timeout de {timeout} segundos")
        return False
    except Exception as e:
        print(f"\n❌ Error ejecutando {example_path}: {e}")
        return False


def main():
    print("=== Ejecutor de Ejemplos FileLock ===")
    
    # Obtener directorio base
    base_dir = Path(__file__).parent
    
    # Definir ejemplos a ejecutar (en orden)
    ejemplos = [
        # Ejemplo de tipado
        "typing_example.py",
        
        # Ejemplos síncronos
        "sync/01_basic_usage.py",
        "sync/02_timeout_example.py", 
        "sync/03_file_processing.py",
        
        # Ejemplos asíncronos
        "async/01_basic_async.py",
        "async/02_concurrent_tasks.py",
        "async/03_web_scraping_simulation.py",
        
        # Ejemplos avanzados
        "advanced/01_mixed_sync_async.py",
        "advanced/02_distributed_counter.py",
        "advanced/03_job_queue.py"
    ]
    
    print(f"Se ejecutarán {len(ejemplos)} ejemplos:")
    for i, ejemplo in enumerate(ejemplos, 1):
        print(f"  {i:2d}. {ejemplo}")
    
    # Confirmación del usuario
    print("\n¿Continuar? (y/N): ", end="")
    respuesta = input().strip().lower()
    
    if respuesta not in ['y', 'yes', 's', 'sí']:
        print("Ejecución cancelada")
        return
    
    # Ejecutar ejemplos
    resultados = {}
    tiempo_inicio = time.time()
    
    for ejemplo in ejemplos:
        ejemplo_path = base_dir / ejemplo
        
        if not ejemplo_path.exists():
            print(f"\n❌ No se encontró: {ejemplo}")
            resultados[ejemplo] = False
            continue
        
        # Pausa entre ejemplos para limpiar output
        if ejemplo != ejemplos[0]:
            print(f"\nPresiona Enter para continuar con el siguiente ejemplo...")
            input()
        
        # Ejecutar ejemplo
        exito = run_example(ejemplo_path)
        resultados[ejemplo] = exito
    
    # Resumen final
    tiempo_total = time.time() - tiempo_inicio
    
    print(f"\n{'='*80}")
    print("RESUMEN DE EJECUCIÓN")
    print('='*80)
    
    exitosos = sum(1 for r in resultados.values() if r)
    fallidos = len(resultados) - exitosos
    
    print(f"Tiempo total: {tiempo_total:.1f} segundos")
    print(f"Ejemplos ejecutados: {len(resultados)}")
    print(f"Exitosos: {exitosos}")
    print(f"Fallidos: {fallidos}")
    
    print("\nDetalle por ejemplo:")
    for ejemplo, exito in resultados.items():
        status = "✅ ÉXITO" if exito else "❌ FALLÓ"
        print(f"  {status:10s} {ejemplo}")
    
    if fallidos > 0:
        print(f"\n⚠️  {fallidos} ejemplo(s) presentaron errores")
        sys.exit(1)
    else:
        print(f"\n🎉 ¡Todos los ejemplos se ejecutaron exitosamente!")


if __name__ == "__main__":
    main()