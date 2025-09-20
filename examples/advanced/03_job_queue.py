#!/usr/bin/env python3
"""
Ejemplo avanzado: Cola de trabajos con FileLock

Este ejemplo implementa una cola de trabajos distribuida que puede ser
usada por múltiples workers de forma concurrente y segura.
"""

import sys
import os
import json
import time
import threading
import random
import uuid
from datetime import datetime, timedelta
from enum import Enum

# Agregar la carpeta src al path para importar
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from simple_filelock import FileLock


class JobStatus(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    EXPIRED = "expired"


class DistributedJobQueue:
    """
    Cola de trabajos distribuida que usa FileLock para sincronización
    """
    
    def __init__(self, queue_file, timeout=10, job_timeout=30):
        self.queue_file = queue_file
        self.lockfile = f"{queue_file}.lock"
        self.timeout = timeout
        self.job_timeout = job_timeout  # Timeout para jobs en procesamiento
        
        # Inicializar cola si no existe
        self._initialize_queue()
    
    def _initialize_queue(self):
        """Inicializa el archivo de cola si no existe"""
        if not os.path.exists(self.queue_file):
            initial_data = {
                "jobs": {},
                "stats": {
                    "total_jobs": 0,
                    "pending_jobs": 0,
                    "completed_jobs": 0,
                    "failed_jobs": 0,
                    "expired_jobs": 0
                },
                "workers": {},
                "created": datetime.now().isoformat()
            }
            
            try:
                os.makedirs(os.path.dirname(self.queue_file), exist_ok=True)
                with FileLock(self.lockfile, timeout=self.timeout):
                    if not os.path.exists(self.queue_file):
                        with open(self.queue_file, 'w') as f:
                            json.dump(initial_data, f, indent=2)
            except Exception as e:
                print(f"Error inicializando cola: {e}")
    
    def add_job(self, job_data, priority=1):
        """
        Añade un nuevo trabajo a la cola
        """
        job_id = str(uuid.uuid4())[:8]  # ID corto
        
        try:
            with FileLock(self.lockfile, timeout=self.timeout, debug=False):
                with open(self.queue_file, 'r') as f:
                    data = json.load(f)
                
                # Crear nuevo job
                job = {
                    "id": job_id,
                    "data": job_data,
                    "priority": priority,
                    "status": JobStatus.PENDING.value,
                    "created": datetime.now().isoformat(),
                    "started": None,
                    "completed": None,
                    "worker_id": None,
                    "result": None,
                    "error": None
                }
                
                # Añadir a la cola
                data["jobs"][job_id] = job
                data["stats"]["total_jobs"] += 1
                data["stats"]["pending_jobs"] += 1
                
                # Escribir estado actualizado
                with open(self.queue_file, 'w') as f:
                    json.dump(data, f, indent=2)
                
                print(f"📝 Job {job_id} añadido a la cola (prioridad: {priority})")
                return job_id
                
        except TimeoutError:
            print(f"⏰ Timeout al añadir job")
            return None
        except Exception as e:
            print(f"❌ Error añadiendo job: {e}")
            return None
    
    def get_next_job(self, worker_id):
        """
        Obtiene el próximo trabajo disponible para procesar
        """
        try:
            with FileLock(self.lockfile, timeout=self.timeout, debug=False):
                with open(self.queue_file, 'r') as f:
                    data = json.load(f)
                
                # Buscar job pendiente con mayor prioridad
                pending_jobs = [
                    (job_id, job) for job_id, job in data["jobs"].items()
                    if job["status"] == JobStatus.PENDING.value
                ]
                
                if not pending_jobs:
                    return None
                
                # Ordenar por prioridad (mayor prioridad primero)
                pending_jobs.sort(key=lambda x: x[1]["priority"], reverse=True)
                job_id, job = pending_jobs[0]
                
                # Marcar como en procesamiento
                job["status"] = JobStatus.PROCESSING.value
                job["started"] = datetime.now().isoformat()
                job["worker_id"] = worker_id
                
                # Actualizar estadísticas
                data["stats"]["pending_jobs"] -= 1
                
                # Registrar worker si no existe
                if worker_id not in data["workers"]:
                    data["workers"][worker_id] = {
                        "jobs_processed": 0,
                        "jobs_completed": 0,
                        "jobs_failed": 0,
                        "first_seen": datetime.now().isoformat()
                    }
                
                data["workers"][worker_id]["last_seen"] = datetime.now().isoformat()
                
                # Escribir estado actualizado
                with open(self.queue_file, 'w') as f:
                    json.dump(data, f, indent=2)
                
                print(f"[Worker-{worker_id}] 📦 Obtenido job {job_id} (prioridad: {job['priority']})")
                return job_id, job["data"]
                
        except TimeoutError:
            print(f"[Worker-{worker_id}] ⏰ Timeout obteniendo job")
            return None
        except Exception as e:
            print(f"[Worker-{worker_id}] ❌ Error obteniendo job: {e}")
            return None
    
    def complete_job(self, job_id, worker_id, result=None):
        """
        Marca un trabajo como completado
        """
        try:
            with FileLock(self.lockfile, timeout=self.timeout, debug=False):
                with open(self.queue_file, 'r') as f:
                    data = json.load(f)
                
                if job_id not in data["jobs"]:
                    print(f"[Worker-{worker_id}] ❌ Job {job_id} no encontrado")
                    return False
                
                job = data["jobs"][job_id]
                
                if job["status"] != JobStatus.PROCESSING.value:
                    print(f"[Worker-{worker_id}] ❌ Job {job_id} no está en procesamiento")
                    return False
                
                # Marcar como completado
                job["status"] = JobStatus.COMPLETED.value
                job["completed"] = datetime.now().isoformat()
                job["result"] = result
                
                # Actualizar estadísticas
                data["stats"]["completed_jobs"] += 1
                data["workers"][worker_id]["jobs_processed"] += 1
                data["workers"][worker_id]["jobs_completed"] += 1
                
                # Escribir estado actualizado
                with open(self.queue_file, 'w') as f:
                    json.dump(data, f, indent=2)
                
                print(f"[Worker-{worker_id}] ✅ Job {job_id} completado")
                return True
                
        except TimeoutError:
            print(f"[Worker-{worker_id}] ⏰ Timeout completando job")
            return False
        except Exception as e:
            print(f"[Worker-{worker_id}] ❌ Error completando job: {e}")
            return False
    
    def fail_job(self, job_id, worker_id, error_msg):
        """
        Marca un trabajo como fallido
        """
        try:
            with FileLock(self.lockfile, timeout=self.timeout, debug=False):
                with open(self.queue_file, 'r') as f:
                    data = json.load(f)
                
                if job_id not in data["jobs"]:
                    print(f"[Worker-{worker_id}] ❌ Job {job_id} no encontrado")
                    return False
                
                job = data["jobs"][job_id]
                
                # Marcar como fallido
                job["status"] = JobStatus.FAILED.value
                job["completed"] = datetime.now().isoformat()
                job["error"] = error_msg
                
                # Actualizar estadísticas
                data["stats"]["failed_jobs"] += 1
                data["workers"][worker_id]["jobs_processed"] += 1
                data["workers"][worker_id]["jobs_failed"] += 1
                
                # Escribir estado actualizado
                with open(self.queue_file, 'w') as f:
                    json.dump(data, f, indent=2)
                
                print(f"[Worker-{worker_id}] ❌ Job {job_id} marcado como fallido: {error_msg}")
                return True
                
        except Exception as e:
            print(f"[Worker-{worker_id}] ❌ Error marcando job como fallido: {e}")
            return False
    
    def get_stats(self):
        """Obtiene estadísticas de la cola"""
        try:
            with FileLock(self.lockfile, timeout=self.timeout, debug=False):
                with open(self.queue_file, 'r') as f:
                    data = json.load(f)
                return data
        except Exception:
            return None


def job_producer(queue, total_jobs=20):
    """
    Productor que añade jobs a la cola
    """
    print("[Producer] Iniciando producción de jobs...")
    
    job_types = [
        {"type": "data_processing", "size": "small"},
        {"type": "data_processing", "size": "medium"}, 
        {"type": "data_processing", "size": "large"},
        {"type": "email_sending", "count": 10},
        {"type": "report_generation", "format": "pdf"},
        {"type": "backup_operation", "target": "database"},
    ]
    
    for i in range(total_jobs):
        job_data = random.choice(job_types).copy()
        job_data["batch_id"] = f"batch_{i//5}"  # Agrupar en batches
        job_data["sequence"] = i
        
        priority = random.choice([1, 1, 1, 2, 2, 3])  # Más jobs de prioridad baja
        
        job_id = queue.add_job(job_data, priority)
        if job_id:
            print(f"[Producer] ✅ Job {job_id} creado: {job_data['type']}")
        
        time.sleep(random.uniform(0.1, 0.3))  # Pausa entre creaciones
    
    print(f"[Producer] 🏁 Producción completada - {total_jobs} jobs creados")


def job_worker(worker_id, queue, max_jobs=None):
    """
    Worker que procesa jobs de la cola
    """
    print(f"[Worker-{worker_id}] Iniciado")
    jobs_processed = 0
    
    while True:
        if max_jobs and jobs_processed >= max_jobs:
            break
        
        # Obtener próximo job
        result = queue.get_next_job(worker_id)
        if not result:
            print(f"[Worker-{worker_id}] No hay jobs disponibles, esperando...")
            time.sleep(1)
            continue
        
        job_id, job_data = result
        jobs_processed += 1
        
        try:
            # Simular procesamiento del job
            job_type = job_data.get("type", "unknown")
            print(f"[Worker-{worker_id}] 🔄 Procesando job {job_id}: {job_type}")
            
            # Tiempo de procesamiento basado en el tipo y tamaño
            if job_type == "data_processing":
                size = job_data.get("size", "small")
                processing_time = {"small": 1, "medium": 2, "large": 4}.get(size, 1)
            elif job_type == "backup_operation":
                processing_time = 3
            else:
                processing_time = random.uniform(0.5, 2)
            
            # Simular posible falla (5% de probabilidad)
            if random.random() < 0.05:
                raise Exception("Falla simulada durante el procesamiento")
            
            time.sleep(processing_time)
            
            # Completar job exitosamente
            result_data = {
                "processing_time": processing_time,
                "processed_by": worker_id,
                "processed_at": datetime.now().isoformat()
            }
            
            queue.complete_job(job_id, worker_id, result_data)
            
        except Exception as e:
            # Marcar job como fallido
            queue.fail_job(job_id, worker_id, str(e))
        
        # Pequeña pausa antes del siguiente job
        time.sleep(random.uniform(0.1, 0.3))
    
    print(f"[Worker-{worker_id}] 🏁 Finalizado - {jobs_processed} jobs procesados")


def main():
    print("=== Cola de Trabajos Distribuida con FileLock ===")
    
    queue_file = "/tmp/job_queue.json"
    
    # Limpiar estado anterior
    for ext in ['', '.lock']:
        file_path = queue_file + ext
        if os.path.exists(file_path):
            os.remove(file_path)
    
    print(f"Archivo de cola: {queue_file}\n")
    
    # Crear instancia de la cola
    queue = DistributedJobQueue(queue_file)
    
    # Iniciar productor en un hilo separado
    producer_thread = threading.Thread(target=job_producer, args=(queue, 15))
    producer_thread.start()
    
    # Esperar un poco antes de iniciar workers
    time.sleep(1)
    
    # Crear múltiples workers
    workers = []
    num_workers = 3
    
    print(f"Iniciando {num_workers} workers concurrentes...\n")
    
    for i in range(1, num_workers + 1):
        worker = threading.Thread(
            target=job_worker, 
            args=(i, queue, 8)  # Máximo 8 jobs por worker
        )
        workers.append(worker)
        worker.start()
        time.sleep(0.2)
    
    # Esperar a que termine el productor
    producer_thread.join()
    
    # Esperar a que terminen los workers
    for worker in workers:
        worker.join()
    
    print("\n=== Estadísticas Finales ===")
    
    # Obtener estadísticas finales
    stats = queue.get_stats()
    if stats:
        print("Estado de la cola:")
        for status, count in stats["stats"].items():
            print(f"  {status.replace('_', ' ').title()}: {count}")
        
        print("\nEstadísticas por worker:")
        for worker_id, worker_stats in stats["workers"].items():
            processed = worker_stats.get("jobs_processed", 0)
            completed = worker_stats.get("jobs_completed", 0)
            failed = worker_stats.get("jobs_failed", 0)
            
            print(f"  Worker-{worker_id}:")
            print(f"    Total procesados: {processed}")
            print(f"    Completados: {completed}")
            print(f"    Fallidos: {failed}")
        
        # Mostrar algunos jobs completados
        completed_jobs = [
            job for job in stats["jobs"].values()
            if job["status"] == JobStatus.COMPLETED.value
        ]
        
        print(f"\nPrimeros 5 jobs completados:")
        for job in completed_jobs[:5]:
            job_type = job["data"].get("type", "unknown")
            worker = job.get("worker_id", "unknown")
            print(f"  {job['id']}: {job_type} (Worker-{worker})")


if __name__ == "__main__":
    main()