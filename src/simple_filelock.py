# simple_filelock.py

import fcntl
import time
import os
import logging
from typing import Optional, Union, TextIO
from types import TracebackType

logging.basicConfig(level=logging.DEBUG)

class FileLock:
    """
    Clase para manejar bloqueos de archivo usando fcntl.flock.
    Uso recomendado con 'with' para liberación automática.

    Ejemplo:
        with FileLock("/tmp/mi_app.lock", timeout=10):
            # Sección crítica
            hacer_algo_idempotente()
    """

    def __init__(self, lockfile_path: str, timeout: Optional[float] = None, debug: bool = False) -> None:
        """
        Inicializa una instancia de FileLock.
        
        :param lockfile_path: Ruta del archivo de lock (se crea si no existe).
        :param timeout: Tiempo máximo en segundos para esperar el lock. None = esperar indefinidamente.
        :param debug: Si True, imprime mensajes de adquisición/liberación.
        """
        self.lockfile_path: str = lockfile_path
        self.timeout: Optional[float] = timeout
        self.debug: bool = debug
        self.lockfile: Optional[TextIO] = None

    def __enter__(self) -> 'FileLock':
        # Crear directorio si no existe
        os.makedirs(os.path.dirname(self.lockfile_path), exist_ok=True)

        # Abrir archivo (crea si no existe)
        self.lockfile = open(self.lockfile_path, 'w')

        if self.debug:
            logging.debug(f"🔒 Intentando adquirir lock en: {self.lockfile_path}")

        start_time = time.time()

        while True:
            try:
                # Intentar obtener lock exclusivo
                fcntl.flock(self.lockfile, fcntl.LOCK_EX | fcntl.LOCK_NB)
                if self.debug:
                    logging.debug("✅ Lock adquirido.")
                break
            except BlockingIOError:
                if self.timeout and (time.time() - start_time) > self.timeout:
                    self.lockfile.close()
                    raise TimeoutError(f"No se pudo obtener el lock en {self.timeout} segundos.")
                time.sleep(0.1)  # Esperar un poco antes de reintentar

        return self

    def __exit__(self, exc_type: Optional[type], exc_val: Optional[BaseException], exc_tb: Optional[TracebackType]) -> None:
        if self.lockfile:
            try:
                fcntl.flock(self.lockfile, fcntl.LOCK_UN)
                if self.debug:
                    logging.debug("🔓 Lock liberado.")
            except Exception as e:
                if self.debug:
                    logging.debug(f"⚠️  Error liberando lock: {e}")
            finally:
                self.lockfile.close()
                self.lockfile = None

    def is_locked(self) -> bool:
        """Verifica si el archivo está actualmente bloqueado (no 100% confiable, solo para debugging)"""
        if not self.lockfile:
            return False
        try:
            fcntl.flock(self.lockfile, fcntl.LOCK_EX | fcntl.LOCK_NB)
            fcntl.flock(self.lockfile, fcntl.LOCK_UN)
            return False
        except BlockingIOError:
            return True