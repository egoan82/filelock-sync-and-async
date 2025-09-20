#!/usr/bin/env python3
"""
Ejemplo avanzado: Contador distribuido con FileLock

Este ejemplo implementa un contador distribuido que puede ser usado
por múltiples procesos de forma segura usando FileLock.
"""

import sys
import os
import json
import time
import threading
import random
from datetime import datetime

# Agregar la carpeta src al path para importar
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from simple_filelock import FileLock


class DistributedCounter:
    """
    Contador distribuido que usa FileLock para sincronización
    """
    
    def __init__(self, counter_file, timeout=10):
        self.counter_file = counter_file
        self.lockfile = f"{counter_file}.lock"
        self.timeout = timeout
        
        # Inicializar archivo si no existe
        self._initialize_counter()
    
    def _initialize_counter(self):
        """Inicializa el archivo contador si no existe"""
        if not os.path.exists(self.counter_file):
            initial_data = {
                "value": 0,
                "created": datetime.now().isoformat(),
                "operations": [],
                "clients": {}
            }
            
            try:
                os.makedirs(os.path.dirname(self.counter_file), exist_ok=True)
                with FileLock(self.lockfile, timeout=self.timeout):
                    if not os.path.exists(self.counter_file):  # Double-check
                        with open(self.counter_file, 'w') as f:
                            json.dump(initial_data, f, indent=2)
            except Exception as e:
                print(f"Error inicializando contador: {e}")
    
    def increment(self, client_id, amount=1):
        """
        Incrementa el contador de forma thread-safe
        """
        try:
            with FileLock(self.lockfile, timeout=self.timeout, debug=False):
                # Leer estado actual
                with open(self.counter_file, 'r') as f:
                    data = json.load(f)
                
                # Actualizar valor
                old_value = data["value"]
                data["value"] += amount
                
                # Registrar operación
                operation = {
                    "type": "increment",
                    "client_id": client_id,
                    "amount": amount,
                    "old_value": old_value,
                    "new_value": data["value"],
                    "timestamp": datetime.now().isoformat()
                }
                data["operations"].append(operation)
                
                # Actualizar estadísticas del cliente
                if client_id not in data["clients"]:
                    data["clients"][client_id] = {
                        "total_operations": 0,
                        "total_increments": 0,
                        "first_seen": datetime.now().isoformat()
                    }
                
                data["clients"][client_id]["total_operations"] += 1
                data["clients"][client_id]["total_increments"] += amount
                data["clients"][client_id]["last_seen"] = datetime.now().isoformat()
                
                # Mantener solo las últimas 100 operaciones
                if len(data["operations"]) > 100:
                    data["operations"] = data["operations"][-100:]
                
                # Escribir estado actualizado
                with open(self.counter_file, 'w') as f:
                    json.dump(data, f, indent=2)
                
                print(f"[Client-{client_id}] Incremento +{amount}: {old_value} → {data['value']}")
                return data["value"]
                
        except TimeoutError:
            print(f"[Client-{client_id}] ⏰ Timeout al intentar incrementar")
            return None
        except Exception as e:
            print(f"[Client-{client_id}] ❌ Error: {e}")
            return None
    
    def decrement(self, client_id, amount=1):
        """
        Decrementa el contador de forma thread-safe
        """
        try:
            with FileLock(self.lockfile, timeout=self.timeout, debug=False):
                # Leer estado actual
                with open(self.counter_file, 'r') as f:
                    data = json.load(f)
                
                # Actualizar valor (no permitir valores negativos)
                old_value = data["value"]
                data["value"] = max(0, data["value"] - amount)
                actual_decrement = old_value - data["value"]
                
                # Registrar operación
                operation = {
                    "type": "decrement",
                    "client_id": client_id,
                    "requested_amount": amount,
                    "actual_amount": actual_decrement,
                    "old_value": old_value,
                    "new_value": data["value"],
                    "timestamp": datetime.now().isoformat()
                }
                data["operations"].append(operation)
                
                # Actualizar estadísticas del cliente
                if client_id not in data["clients"]:
                    data["clients"][client_id] = {
                        "total_operations": 0,
                        "total_increments": 0,
                        "total_decrements": 0,
                        "first_seen": datetime.now().isoformat()
                    }
                
                if "total_decrements" not in data["clients"][client_id]:
                    data["clients"][client_id]["total_decrements"] = 0
                
                data["clients"][client_id]["total_operations"] += 1
                data["clients"][client_id]["total_decrements"] += actual_decrement
                data["clients"][client_id]["last_seen"] = datetime.now().isoformat()
                
                # Mantener solo las últimas 100 operaciones
                if len(data["operations"]) > 100:
                    data["operations"] = data["operations"][-100:]
                
                # Escribir estado actualizado
                with open(self.counter_file, 'w') as f:
                    json.dump(data, f, indent=2)
                
                print(f"[Client-{client_id}] Decremento -{actual_decrement}: {old_value} → {data['value']}")
                return data["value"]
                
        except TimeoutError:
            print(f"[Client-{client_id}] ⏰ Timeout al intentar decrementar")
            return None
        except Exception as e:
            print(f"[Client-{client_id}] ❌ Error: {e}")
            return None
    
    def get_value(self):
        """
        Obtiene el valor actual del contador
        """
        try:
            with FileLock(self.lockfile, timeout=self.timeout, debug=False):
                with open(self.counter_file, 'r') as f:
                    data = json.load(f)
                return data["value"]
        except Exception:
            return None
    
    def get_stats(self):
        """
        Obtiene estadísticas completas del contador
        """
        try:
            with FileLock(self.lockfile, timeout=self.timeout, debug=False):
                with open(self.counter_file, 'r') as f:
                    data = json.load(f)
                return data
        except Exception:
            return None


def cliente_worker(client_id, counter, operaciones=10):
    """
    Simula un cliente que realiza operaciones en el contador distribuido
    """
    print(f"[Client-{client_id}] Iniciado - realizará {operaciones} operaciones")
    
    for i in range(operaciones):
        # Decidir aleatoriamente entre incrementar o decrementar
        if random.choice([True, False, True]):  # 66% probabilidad de incrementar
            amount = random.randint(1, 5)
            counter.increment(client_id, amount)
        else:
            amount = random.randint(1, 3)
            counter.decrement(client_id, amount)
        
        # Pausa aleatoria entre operaciones
        time.sleep(random.uniform(0.1, 0.5))
    
    print(f"[Client-{client_id}] 🏁 Finalizado")


def main():
    print("=== Contador Distribuido con FileLock ===")
    
    counter_file = "/tmp/distributed_counter.json"
    
    # Limpiar estado anterior
    for ext in ['', '.lock']:
        file_path = counter_file + ext
        if os.path.exists(file_path):
            os.remove(file_path)
    
    print(f"Archivo del contador: {counter_file}")
    
    # Crear instancia del contador distribuido
    counter = DistributedCounter(counter_file)
    
    print(f"Valor inicial del contador: {counter.get_value()}")
    print()
    
    # Crear múltiples clientes concurrentes
    clientes = []
    num_clientes = 4
    operaciones_por_cliente = 8
    
    print(f"Iniciando {num_clientes} clientes concurrentes...")
    print(f"Cada cliente realizará {operaciones_por_cliente} operaciones aleatorias\n")
    
    for i in range(1, num_clientes + 1):
        cliente = threading.Thread(
            target=cliente_worker, 
            args=(i, counter, operaciones_por_cliente)
        )
        clientes.append(cliente)
        cliente.start()
        time.sleep(0.1)  # Pequeña pausa entre inicios
    
    # Esperar a que todos terminen
    for cliente in clientes:
        cliente.join()
    
    print("\n=== Resultados Finales ===")
    
    # Obtener estadísticas finales
    stats = counter.get_stats()
    if stats:
        print(f"Valor final del contador: {stats['value']}")
        print(f"Total de operaciones: {len(stats['operations'])}")
        print()
        
        print("Estadísticas por cliente:")
        for client_id, client_stats in stats['clients'].items():
            increments = client_stats.get('total_increments', 0)
            decrements = client_stats.get('total_decrements', 0)
            operations = client_stats.get('total_operations', 0)
            
            print(f"  Client-{client_id}:")
            print(f"    Operaciones: {operations}")
            print(f"    Incrementos totales: +{increments}")
            print(f"    Decrementos totales: -{decrements}")
            print(f"    Contribución neta: {increments - decrements}")
        
        print("\nÚltimas 10 operaciones:")
        for i, op in enumerate(stats['operations'][-10:], 1):
            tipo = op['type']
            client = op['client_id']
            if tipo == 'increment':
                print(f"  {i:2d}. Client-{client} +{op['amount']}: "
                      f"{op['old_value']} → {op['new_value']}")
            else:
                print(f"  {i:2d}. Client-{client} -{op['actual_amount']}: "
                      f"{op['old_value']} → {op['new_value']}")


if __name__ == "__main__":
    main()