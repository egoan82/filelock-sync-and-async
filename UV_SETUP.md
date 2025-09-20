# 🚀 Configuración con UV

Esta guía te muestra cómo configurar y usar el proyecto con `uv`, la herramienta rápida de gestión de paquetes y entornos virtuales para Python.

## 📋 Prerrequisitos

### Instalar uv

Si no tienes `uv` instalado:

```bash
# En Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# Con pip
pip install uv

# Con pipx
pipx install uv

# Con Homebrew (macOS)
brew install uv
```

## 🔧 Configuración del Proyecto

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/filelock-sync-and-async.git
cd filelock-sync-and-async
```

### 2. Configurar entorno virtual con uv

```bash
# Crear entorno virtual con la versión de Python especificada
uv venv

# Activar el entorno virtual
source .venv/bin/activate  # Linux/macOS
# o en Windows:
# .venv\Scripts\activate
```

### 3. Opciones de instalación

#### 🟢 **Uso básico** (solo funcionalidad principal)
```bash
# No requiere dependencias - usa solo biblioteca estándar
# ¡Ya puedes usar las clases FileLock y AsyncFileLock!
```

#### 🔧 **Desarrollo completo** (con herramientas de desarrollo)
```bash
# Instalar dependencias de desarrollo
uv pip install -r requirements-dev.txt

# O usando pyproject.toml (recomendado)
uv pip install -e ".[dev]"
```

#### 📚 **Solo documentación**
```bash
uv pip install -e ".[docs]"
```

#### 🎯 **Todo incluido**
```bash
uv pip install -e ".[dev,docs]"
```

## 📝 Comandos Útiles con UV

### Gestión de dependencias

```bash
# Instalar una nueva dependencia
uv pip install nueva-dependencia

# Instalar dependencia de desarrollo
uv pip install pytest --dev

# Actualizar dependencias
uv pip install --upgrade -r requirements-dev.txt

# Ver dependencias instaladas
uv pip list

# Generar requirements.txt actualizado
uv pip freeze > requirements-frozen.txt
```

### Sincronización de dependencias

```bash
# Generar archivo de lock
uv lock

# Sincronizar entorno con lock file
uv sync

# Instalar desde lock file
uv pip sync uv.lock
```

## 🧪 Ejecutar Pruebas y Herramientas

### Ejecutar ejemplos

```bash
# Activar entorno si no está activo
source .venv/bin/activate

# Ejecutar ejemplo específico
python examples/sync/01_basic_usage.py

# Ejecutar todos los ejemplos
python examples/run_all_examples.py

# Ejecutar ejemplo de tipado
python examples/typing_example.py
```

### Herramientas de desarrollo (si instalaste dependencias dev)

```bash
# Ejecutar tests
pytest

# Ejecutar tests con cobertura
pytest --cov=src

# Formatear código con black
black src/ examples/

# Ordenar imports
isort src/ examples/

# Verificar tipos con mypy
mypy src/

# Linting con flake8
flake8 src/ examples/
```

## 🔄 Workflow típico de desarrollo

```bash
# 1. Configurar entorno
uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"

# 2. Hacer cambios al código
# ... editar archivos ...

# 3. Verificar calidad del código
black src/
isort src/
mypy src/
flake8 src/

# 4. Ejecutar tests
pytest

# 5. Probar ejemplos
python examples/run_all_examples.py
```

## ⚡ Ventajas de usar UV

### 🚀 **Velocidad**
- Hasta 10-100x más rápido que pip
- Resolución de dependencias paralela
- Cache inteligente de paquetes

### 🎯 **Simplicidad**
- Un solo comando para múltiples operaciones
- Gestión automática de entornos virtuales
- Compatible con pip y requirements.txt

### 🔒 **Reproducibilidad** 
- Lock files para dependencias exactas
- Soporte para múltiples versiones de Python
- Builds determinísticos

## 🛠️ Comandos específicos para este proyecto

### Desarrollo diario
```bash
# Inicio rápido
uv venv && source .venv/bin/activate

# Instalar para desarrollo
uv pip install -e ".[dev]"

# Ejecutar suite completa de pruebas
python examples/run_all_examples.py
```

### Verificación antes de commit
```bash
# Formateo y linting completo
black src/ examples/ && isort src/ examples/
mypy src/
flake8 src/ examples/
pytest
```

### Producción/distribución
```bash
# Instalar solo lo necesario
uv pip install .

# Crear lock file para reproducibilidad
uv lock
```

## 🔧 Configuración específica de UV

### .python-version
```
3.11
```
*Especifica la versión de Python preferida*

### pyproject.toml
```toml
[project.optional-dependencies]
dev = ["pytest>=7.0.0", "black>=23.0.0", ...]
docs = ["mkdocs>=1.4.0", ...]
```
*Define dependencias opcionales por categoría*

## 🆘 Resolución de problemas

### Error: "uv not found"
```bash
# Reinstalar uv
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc  # o ~/.zshrc
```

### Error: versión de Python no encontrada
```bash
# Instalar Python con uv
uv python install 3.11

# O usar versión disponible
uv venv --python python3.10
```

### Entorno virtual corrupto
```bash
# Recrear entorno
rm -rf .venv
uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"
```

### Dependencias conflictivas
```bash
# Limpiar cache y reinstalar
uv cache clean
rm -rf .venv
uv venv
uv pip install -e ".[dev]" --force-reinstall
```

## 📚 Recursos adicionales

- [Documentación oficial de uv](https://docs.astral.sh/uv/)
- [Guía de migración desde pip](https://docs.astral.sh/uv/pip/)
- [Comparación de rendimiento](https://astral.sh/blog/uv)

---

¡Con esta configuración tendrás un entorno de desarrollo rápido y eficiente usando `uv`! 🎉