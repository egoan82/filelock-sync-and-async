# FileLock - Biblioteca para Bloqueos de Archivo Síncronos y Asíncronos

Una biblioteca Python simple y robusta para manejar bloqueos de archivo usando `fcntl.flock`, con soporte tanto para operaciones síncronas como asíncronas.

## 🚀 Características

- **Bloqueos síncronos**: Clase `FileLock` para uso en código síncrono
- **Bloqueos asíncronos**: Clase `AsyncFileLock` para uso con `asyncio`
- **Context managers**: Uso seguro con `with` y `async with`
- **Timeouts configurables**: Evita esperas indefinidas
- **Debugging**: Mensajes opcionales para debugging
- **Thread-safe**: Seguro para uso concurrente
- **Tipado completo**: Soporte completo de type hints para mejor IDE experience
- **Sin dependencias**: Solo usa la biblioteca estándar de Python

## 📋 Requisitos

- Python 3.7+
- Sistema operativo Unix/Linux/macOS (requiere `fcntl`)
- No requiere dependencias externas

## 📦 Instalación

### Opción 1: Uso básico (sin dependencias)
```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/filelock-sync-and-async.git
cd filelock-sync-and-async

# La biblioteca no requiere instalación adicional
# Solo asegúrate de tener Python 3.7+ instalado
```

### Opción 2: Con UV (recomendado para desarrollo)
```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/filelock-sync-and-async.git
cd filelock-sync-and-async

# Crear entorno virtual con uv
uv venv
source .venv/bin/activate  # Linux/macOS

# Instalar dependencias de desarrollo (opcional)
uv pip install -e ".[dev]"
```

> 📋 **Para instrucciones detalladas de uv**, consulta [UV_SETUP.md](UV_SETUP.md)

## 🏗️ Estructura del Proyecto

```
filelock-sync-and-async/
├── src/                          # Código fuente principal
│   ├── __init__.py              # Módulo principal
│   ├── simple_filelock.py       # Clase FileLock (síncrona)
│   └── simple_filelock_async.py # Clase AsyncFileLock (asíncrona)
├── examples/                     # Ejemplos de uso
│   ├── sync/                    # Ejemplos síncronos
│   │   ├── 01_basic_usage.py
│   │   ├── 02_timeout_example.py
│   │   └── 03_file_processing.py
│   ├── async/                   # Ejemplos asíncronos
│   │   ├── 01_basic_async.py
│   │   ├── 02_concurrent_tasks.py
│   │   └── 03_web_scraping_simulation.py
│   ├── advanced/                # Casos de uso avanzados
│   │   ├── 01_mixed_sync_async.py
│   │   ├── 02_distributed_counter.py
│   │   └── 03_job_queue.py
│   ├── typing_example.py        # Ejemplo de tipado y valores por defecto
│   └── run_all_examples.py      # Script para ejecutar todos los ejemplos
├── tests/                       # Tests (TODO)
├── pyproject.toml              # Configuración del proyecto y dependencias
├── requirements-dev.txt        # Dependencias de desarrollo
├── UV_SETUP.md                 # Guía detallada para usar con uv
├── CONTRIBUTING.md             # Guía de contribución
└── README.md                   # Este archivo
```

## 🔧 Uso Básico

### FileLock (Síncrono)

```python
from src.simple_filelock import FileLock

# Uso básico con context manager
with FileLock("/tmp/mi_app.lock"):
    # Sección crítica - solo un proceso puede ejecutar esto a la vez
    print("Ejecutando operación que requiere exclusividad...")
    hacer_algo_importante()

# Uso con timeout
try:
    with FileLock("/tmp/mi_app.lock", timeout=10, debug=True):
        # Máximo 10 segundos esperando el lock
        procesar_archivo_compartido()
except TimeoutError:
    print("No se pudo obtener el lock en 10 segundos")
```

### AsyncFileLock (Asíncrono)

```python
import asyncio
from src.simple_filelock_async import AsyncFileLock

async def tarea_asincrona():
    async with AsyncFileLock("/tmp/mi_app_async.lock", timeout=5):
        # Sección crítica asíncrona
        print("Ejecutando tarea asíncrona exclusiva...")
        await procesar_datos_async()

# Ejecutar
asyncio.run(tarea_asincrona())
```

## 📚 Ejemplos Detallados

### 🔗 Ejemplos Síncronos

1. **[Uso Básico](examples/sync/01_basic_usage.py)** - Ejemplo más simple de uso
2. **[Manejo de Timeouts](examples/sync/02_timeout_example.py)** - Múltiples procesos compitiendo por el mismo lock
3. **[Procesamiento de Archivos](examples/sync/03_file_processing.py)** - Caso práctico con archivo JSON compartido

### ⚡ Ejemplos Asíncronos

1. **[AsyncFileLock Básico](examples/async/01_basic_async.py)** - Introducción a bloqueos asíncronos
2. **[Tareas Concurrentes](examples/async/02_concurrent_tasks.py)** - Múltiples workers asíncronos
3. **[Simulación Web Scraping](examples/async/03_web_scraping_simulation.py)** - Caso práctico con scrapers concurrentes

### 🚀 Ejemplos Avanzados

1. **[Coordinación Mixta](examples/advanced/01_mixed_sync_async.py)** - Procesos síncronos y asíncronos coordinándose
2. **[Contador Distribuido](examples/advanced/02_distributed_counter.py)** - Sistema de contador thread-safe
3. **[Cola de Trabajos](examples/advanced/03_job_queue.py)** - Cola de trabajos distribuida completa

### ▶️ Ejecutar Todos los Ejemplos

```bash
# Ejecutar el script que prueba todos los ejemplos
python examples/run_all_examples.py

# Con Makefile (si tienes uv instalado)
make examples
```

### ⚡ Comandos Rápidos con UV y Make

Si tienes `uv` instalado, puedes usar estos comandos para una experiencia más fluida:

```bash
# Configuración inicial completa
make setup && source .venv/bin/activate && make install-dev

# Ejecutar ejemplos
make examples

# Verificación completa antes de commit
make dev-check

# Formatear código
make format

# Ver todos los comandos disponibles
make help
```

## 📖 API Reference

### FileLock (Síncrono)

```python
class FileLock:
    def __init__(self, lockfile_path: str, timeout: Optional[float] = None, debug: bool = False) -> None:
        """
        Crea una instancia de FileLock.
        
        Args:
            lockfile_path: Ruta del archivo de lock
            timeout: Timeout en segundos. None = esperar indefinidamente
            debug: Si True, imprime mensajes de debug
        """
        
    def __enter__(self) -> 'FileLock':
        """Adquiere el lock (usado con 'with')"""
        
    def __exit__(self, exc_type: Optional[type], exc_val: Optional[BaseException], exc_tb: Optional[TracebackType]) -> None:
        """Libera el lock automáticamente"""
        
    def is_locked(self) -> bool:
        """Verifica si el archivo está bloqueado (solo para debugging)"""
```

### AsyncFileLock (Asíncrono)

```python
class AsyncFileLock:
    def __init__(self, lockfile_path: str, timeout: Optional[float] = None, debug: bool = False) -> None:
        """
        Crea una instancia de AsyncFileLock.
        
        Args:
            lockfile_path: Ruta del archivo de lock
            timeout: Timeout en segundos. None = esperar indefinidamente
            debug: Si True, imprime mensajes de debug
        """
        
    async def __aenter__(self) -> 'AsyncFileLock':
        """Adquiere el lock de forma asíncrona (usado con 'async with')"""
        
    async def __aexit__(self, exc_type: Optional[type], exc_val: Optional[BaseException], exc_tb: Optional[TracebackType]) -> None:
        """Libera el lock automáticamente"""
        
    async def is_locked(self) -> bool:
        """Verifica si el archivo está bloqueado (solo para debugging)"""
```

## 🎯 Tipado y Soporte de IDEs

Las clases `FileLock` y `AsyncFileLock` incluyen tipado completo con **type hints** para una mejor experiencia de desarrollo:

```python
from typing import Optional
from src.simple_filelock import FileLock
from src.simple_filelock_async import AsyncFileLock

# Tipado explícito para mejor autocompletado
lockfile_path: str = "/tmp/mi_app.lock"
timeout_segundos: Optional[float] = 5.0
debug_mode: bool = True

# El IDE puede inferir tipos automáticamente
with FileLock(lockfile_path, timeout=timeout_segundos, debug=debug_mode) as lock:
    # lock es de tipo FileLock
    is_locked: bool = lock.is_locked()  # Retorna bool
```

### Beneficios del Tipado

- 🎯 **Autocompletado mejorado** en IDEs como VS Code, PyCharm
- 🔍 **Detección temprana de errores** con herramientas como mypy
- 📝 **Documentación automática** de tipos esperados
- 🛡️ **Mayor seguridad** en refactoring y mantenimiento

### Validación con mypy

```bash
# Instalar mypy para validación de tipos
pip install mypy

# Validar tipos en tu código
mypy mi_script.py
```

## 💡 Casos de Uso Comunes

### 🔄 Sincronización de Procesos

```python
# Evitar que múltiples instancias de un script se ejecuten simultáneamente
with FileLock("/tmp/mi_script.lock", timeout=0):
    ejecutar_script_unico()
```

### 📊 Actualización de Archivos Compartidos

```python
# Múltiples procesos actualizando un archivo de configuración
with FileLock("/tmp/config.lock"):
    config = cargar_configuracion()
    config.update(nuevos_valores)
    guardar_configuracion(config)
```

### 🌐 Web Scraping Coordinado

```python
# Múltiples scrapers guardando en el mismo archivo de resultados
async with AsyncFileLock("/tmp/resultados.lock"):
    resultados = await cargar_resultados()
    resultados.extend(nuevos_datos)
    await guardar_resultados(resultados)
```

### 📋 Colas de Trabajos

```python
# Sistema de cola distribuida
with FileLock("/tmp/jobs.lock"):
    job = obtener_proximo_trabajo()
    if job:
        marcar_como_en_proceso(job)
```

## ⚠️ Consideraciones Importantes

### 🔒 Sobre los Bloqueos

- Los bloqueos son **por proceso**, no por hilo
- Los archivos de lock se crean automáticamente si no existen
- Los directorios padre también se crean automáticamente
- Los bloqueos se liberan automáticamente cuando el proceso termina

### 🐧 Compatibilidad de Plataformas

- ✅ **Linux**: Completamente soportado
- ✅ **macOS**: Completamente soportado  
- ✅ **Unix**: Completamente soportado
- ❌ **Windows**: No soportado (no tiene `fcntl`)

### ⚡ Rendimiento

- Los bloqueos son muy rápidos (microsegundos)
- No hay polling constante - usa bloqueos del sistema operativo
- Minimal overhead en aplicaciones high-performance

### 🔧 Debugging

```python
# Habilitar mensajes de debug
with FileLock("/tmp/test.lock", debug=True):
    # Verás mensajes como:
    # 🔒 Intentando adquirir lock en: /tmp/test.lock  
    # ✅ Lock adquirido.
    # 🔓 Lock liberado.
    pass
```

## 🤝 Contribuir

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-caracteristica`)
3. Commit tus cambios (`git commit -am 'Agregar nueva característica'`)
4. Push a la rama (`git push origin feature/nueva-caracteristica`)
5. Crea un Pull Request

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🆘 Soporte

Si tienes preguntas o encuentras problemas:

1. Revisa los [ejemplos](examples/) incluidos
2. Verifica que estás en un sistema Unix/Linux/macOS
3. Asegúrate de tener permisos de escritura en el directorio del lock
4. Abre un issue en GitHub si necesitas ayuda adicional

## 🔄 Changelog

### v1.1.0
- ✨ **Nuevo**: Tipado completo con type hints
- 🔧 **Mejorado**: Valores por defecto explícitos en constructores
- 📚 **Nuevo**: Ejemplo de tipado (`examples/typing_example.py`)
- 📖 **Mejorado**: Documentación de API con tipos
- 🎯 **Mejorado**: Soporte mejorado de IDEs
- 🚀 **Nuevo**: Soporte completo para `uv` con `pyproject.toml`
- 🛠️ **Nuevo**: Makefile con comandos automatizados
- 📋 **Nuevo**: Guía detallada UV_SETUP.md

### v1.0.0
- Implementación inicial de FileLock y AsyncFileLock
- Ejemplos completos de uso
- Documentación completa
- Soporte para timeouts y debugging