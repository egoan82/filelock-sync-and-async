#!/usr/bin/env python3
"""
Ejemplo práctico: Simulación de web scraping con AsyncFileLock

Este ejemplo simula un escenario donde múltiples scrapers asíncronos
necesitan actualizar un archivo de resultados de forma exclusiva.
"""

import sys
import os
import asyncio
import json
import random
from datetime import datetime

# Agregar la carpeta src al path para importar
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from simple_filelock_async import AsyncFileLock


async def simular_scraping(url):
    """Simula el scraping de una URL"""
    print(f"    🌐 Obteniendo datos de {url}")
    
    # Simular tiempo de descarga variable
    tiempo_descarga = random.uniform(1, 3)
    await asyncio.sleep(tiempo_descarga)
    
    # Simular datos obtenidos
    datos = {
        "url": url,
        "titulo": f"Página {url.split('/')[-1]}",
        "palabras": random.randint(100, 1000),
        "timestamp": datetime.now().isoformat(),
        "tiempo_descarga": round(tiempo_descarga, 2)
    }
    
    return datos


async def scraper_worker(worker_id, urls, archivo_resultados):
    """
    Worker que procesa una lista de URLs y guarda los resultados
    """
    print(f"[Scraper-{worker_id}] Iniciado con {len(urls)} URLs")
    
    resultados_locales = []
    
    # Procesar cada URL asíncronamente
    for url in urls:
        try:
            print(f"[Scraper-{worker_id}] Procesando: {url}")
            datos = await simular_scraping(url)
            resultados_locales.append(datos)
            print(f"[Scraper-{worker_id}] ✅ Completado: {url}")
            
        except Exception as e:
            print(f"[Scraper-{worker_id}] ❌ Error en {url}: {e}")
            continue
    
    # Guardar todos los resultados de forma atómica
    if resultados_locales:
        await guardar_resultados(worker_id, resultados_locales, archivo_resultados)
    
    print(f"[Scraper-{worker_id}] 🏁 Finalizado - {len(resultados_locales)} URLs procesadas")


async def guardar_resultados(worker_id, nuevos_resultados, archivo_resultados):
    """
    Guarda los resultados en el archivo compartido usando AsyncFileLock
    """
    lockfile_path = f"{archivo_resultados}.lock"
    
    try:
        async with AsyncFileLock(lockfile_path, timeout=15, debug=True):
            print(f"[Scraper-{worker_id}] 💾 Guardando {len(nuevos_resultados)} resultados...")
            
            # Leer resultados existentes
            if os.path.exists(archivo_resultados):
                with open(archivo_resultados, 'r', encoding='utf-8') as f:
                    datos_existentes = json.load(f)
            else:
                datos_existentes = {
                    "metadata": {
                        "creado": datetime.now().isoformat(),
                        "total_urls": 0,
                        "scrapers": {}
                    },
                    "resultados": []
                }
            
            # Actualizar estadísticas
            worker_key = f"scraper_{worker_id}"
            if worker_key not in datos_existentes["metadata"]["scrapers"]:
                datos_existentes["metadata"]["scrapers"][worker_key] = {
                    "urls_procesadas": 0,
                    "ultima_actualizacion": None
                }
            
            # Agregar nuevos resultados
            datos_existentes["resultados"].extend(nuevos_resultados)
            datos_existentes["metadata"]["total_urls"] += len(nuevos_resultados)
            datos_existentes["metadata"]["scrapers"][worker_key]["urls_procesadas"] += len(nuevos_resultados)
            datos_existentes["metadata"]["scrapers"][worker_key]["ultima_actualizacion"] = datetime.now().isoformat()
            
            # Guardar archivo actualizado
            with open(archivo_resultados, 'w', encoding='utf-8') as f:
                json.dump(datos_existentes, f, indent=2, ensure_ascii=False)
            
            print(f"[Scraper-{worker_id}] ✅ Resultados guardados exitosamente")
            
    except TimeoutError:
        print(f"[Scraper-{worker_id}] ⏰ Timeout al intentar guardar resultados")
    except Exception as e:
        print(f"[Scraper-{worker_id}] ❌ Error guardando resultados: {e}")


async def main():
    print("=== Simulación de Web Scraping con AsyncFileLock ===")
    
    archivo_resultados = "/tmp/scraping_results.json"
    
    # Limpiar archivo anterior
    if os.path.exists(archivo_resultados):
        os.remove(archivo_resultados)
    
    # Simular listas de URLs para diferentes scrapers
    urls_base = [
        "https://example.com/page1",
        "https://example.com/page2", 
        "https://example.com/page3",
        "https://example.com/page4",
        "https://example.com/page5",
        "https://example.com/page6",
        "https://example.com/page7",
        "https://example.com/page8",
        "https://example.com/page9",
        "https://example.com/page10"
    ]
    
    # Dividir URLs entre scrapers
    scrapers = []
    chunk_size = 3
    for i in range(0, len(urls_base), chunk_size):
        urls_chunk = urls_base[i:i + chunk_size]
        scraper_id = (i // chunk_size) + 1
        
        scraper = asyncio.create_task(
            scraper_worker(scraper_id, urls_chunk, archivo_resultados)
        )
        scrapers.append(scraper)
    
    print(f"Iniciando {len(scrapers)} scrapers concurrentes...")
    print(f"Archivo de resultados: {archivo_resultados}\n")
    
    # Ejecutar todos los scrapers concurrentemente
    await asyncio.gather(*scrapers)
    
    print("\n=== Scraping Completado ===")
    
    # Mostrar resultados finales
    if os.path.exists(archivo_resultados):
        with open(archivo_resultados, 'r', encoding='utf-8') as f:
            datos_finales = json.load(f)
        
        print(f"Total de URLs procesadas: {datos_finales['metadata']['total_urls']}")
        print("Estadísticas por scraper:")
        for scraper_id, stats in datos_finales['metadata']['scrapers'].items():
            print(f"  - {scraper_id}: {stats['urls_procesadas']} URLs")
        
        print(f"\nPrimeras 3 resultados:")
        for i, resultado in enumerate(datos_finales['resultados'][:3]):
            print(f"  {i+1}. {resultado['url']} - {resultado['palabras']} palabras")


if __name__ == "__main__":
    asyncio.run(main())