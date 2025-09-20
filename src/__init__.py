"""
FileLock - Biblioteca para manejo de bloqueos de archivo sincronos y asincronos
"""

from .simple_filelock import FileLock
from .simple_filelock_async import AsyncFileLock

__version__ = "1.1.0"
__all__ = ["FileLock", "AsyncFileLock"]