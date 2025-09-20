# simple_filelock_async.py

import fcntl
import asyncio
import os
import time
import logging
from typing import Optional, Union, TextIO, Any
from types import TracebackType

logging.basicConfig(level=logging.DEBUG)

class AsyncFileLock:
    """
    Clase asíncrona para manejar bloqueos de archivo usando fcntl.flock.
    Diseñada para usarse con 'async with'.

    Ejemplo:
        lock = AsyncFileLock("/tmp/mi_app.lock", timeout=10, debug=True)
        async with lock:
            await hacer_algo_async()
    """

    def __init__(self, lockfile_path: str, timeout: Optional[float] = None, debug: bool = False) -> None:
        """
        Inicializa una instancia de AsyncFileLock.
        
        :param lockfile_path: Ruta del archivo de lock.
        :param timeout: Tiempo máximo en segundos para adquirir el lock.
        :param debug: Si True, imprime mensajes de debug.
        """
        self.lockfile_path: str = lockfile_path
        self.timeout: Optional[float] = timeout
        self.debug: bool = debug
        self.lockfile: Optional[TextIO] = None
        self._loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()

    async def __aenter__(self) -> 'AsyncFileLock':
        # Crear directorio si no existe
        await self._loop.run_in_executor(None, lambda: os.makedirs(os.path.dirname(self.lockfile_path), exist_ok=True))

        # Abrir archivo
        self.lockfile = await self._loop.run_in_executor(None, lambda: open(self.lockfile_path, 'w'))

        if self.debug:
            logging.debug(f"🔒 Intentando adquirir lock en: {self.lockfile_path}")

        start_time = time.time()

        while True:
            try:
                # Ejecutar fcntl.flock en threadpool (no bloquea event loop)
                await self._loop.run_in_executor(None, lambda: fcntl.flock(self.lockfile, fcntl.LOCK_EX | fcntl.LOCK_NB))
                if self.debug:
                    logging.debug("✅ Lock adquirido.")
                break
            except BlockingIOError:
                if self.timeout and (time.time() - start_time) > self.timeout:
                    await self._loop.run_in_executor(None, self.lockfile.close)
                    raise TimeoutError(f"No se pudo obtener el lock en {self.timeout} segundos.")
                await asyncio.sleep(0.1)  # Ceder control al event loop

        return self

    async def __aexit__(self, exc_type: Optional[type], exc_val: Optional[BaseException], exc_tb: Optional[TracebackType]) -> None:
        if self.lockfile:
            try:
                await self._loop.run_in_executor(None, lambda: fcntl.flock(self.lockfile, fcntl.LOCK_UN))
                if self.debug:
                    logging.debug("🔓 Lock liberado.")
            except Exception as e:
                if self.debug:
                    logging.debug(f"⚠️  Error liberando lock: {e}")
            finally:
                await self._loop.run_in_executor(None, self.lockfile.close)
                self.lockfile = None

    async def is_locked(self) -> bool:
        """Verifica si el archivo está bloqueado (solo para debugging)"""
        if not self.lockfile:
            return False
        try:
            await self._loop.run_in_executor(None, lambda: fcntl.flock(self.lockfile, fcntl.LOCK_EX | fcntl.LOCK_NB))
            await self._loop.run_in_executor(None, lambda: fcntl.flock(self.lockfile, fcntl.LOCK_UN))
            return False
        except BlockingIOError:
            return True