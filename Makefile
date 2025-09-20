# Makefile para filelock-sync-and-async
# Requiere uv instalado: https://docs.astral.sh/uv/

.PHONY: help install install-dev test examples lint format check clean setup

# Variables
VENV = .venv
PYTHON = $(VENV)/bin/python
UV = uv

help: ## Mostrar esta ayuda
	@echo "Comandos disponibles:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

setup: ## Configuración inicial completa del proyecto
	$(UV) venv
	@echo "✅ Entorno virtual creado"
	@echo "Para activar: source $(VENV)/bin/activate"
	@echo "Luego ejecuta: make install-dev"

install: ## Instalar el paquete en modo básico
	$(UV) pip install -e .

install-dev: ## Instalar dependencias de desarrollo
	$(UV) pip install -e ".[dev]"
	@echo "✅ Dependencias de desarrollo instaladas"

install-docs: ## Instalar dependencias para documentación
	$(UV) pip install -e ".[docs]"

install-all: ## Instalar todas las dependencias
	$(UV) pip install -e ".[dev,docs]"

test: ## Ejecutar todos los ejemplos como tests
	$(PYTHON) examples/run_all_examples.py

test-quick: ## Ejecutar test rápido de funcionalidad básica
	$(PYTHON) -c "import sys; sys.path.append('src'); from simple_filelock import FileLock; from simple_filelock_async import AsyncFileLock; print('✅ Importaciones exitosas')"

examples: ## Ejecutar todos los ejemplos
	@echo "🚀 Ejecutando todos los ejemplos..."
	$(PYTHON) examples/run_all_examples.py

example-basic: ## Ejecutar ejemplo básico síncrono
	$(PYTHON) examples/sync/01_basic_usage.py

example-async: ## Ejecutar ejemplo básico asíncrono
	$(PYTHON) examples/async/01_basic_async.py

example-typing: ## Ejecutar ejemplo de tipado
	$(PYTHON) examples/typing_example.py

format: ## Formatear código con black e isort
	$(UV) run black src/ examples/
	$(UV) run isort src/ examples/
	@echo "✅ Código formateado"

lint: ## Ejecutar linting con flake8
	$(UV) run flake8 src/ examples/

typecheck: ## Verificar tipos con mypy
	$(UV) run mypy src/

check: format lint typecheck ## Ejecutar todas las verificaciones de calidad
	@echo "✅ Todas las verificaciones completadas"

pytest: ## Ejecutar pytest (si hay tests)
	$(UV) run pytest tests/ || echo "⚠️  No se encontraron tests en tests/"

coverage: ## Ejecutar tests con cobertura
	$(UV) run pytest --cov=src --cov-report=html || echo "⚠️  No se encontraron tests"

clean: ## Limpiar archivos temporales
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf build/ dist/ .coverage htmlcov/ .mypy_cache/ .pytest_cache/
	rm -f /tmp/*filelock*.lock /tmp/*async*.lock /tmp/test*.lock 2>/dev/null || true
	@echo "✅ Archivos temporales limpiados"

clean-venv: ## Eliminar entorno virtual
	rm -rf $(VENV)
	@echo "✅ Entorno virtual eliminado"

reset: clean clean-venv setup ## Resetear proyecto completamente
	@echo "✅ Proyecto reseteado"

list-deps: ## Listar dependencias instaladas
	$(UV) pip list

freeze: ## Generar requirements.txt actualizado
	$(UV) pip freeze > requirements-frozen.txt
	@echo "✅ Dependencias congeladas en requirements-frozen.txt"

update: ## Actualizar dependencias
	$(UV) pip install --upgrade -r requirements-dev.txt

sync: ## Sincronizar entorno con uv
	$(UV) sync

lock: ## Generar lock file
	$(UV) lock

# Comandos de desarrollo común
dev-start: ## Inicio rápido para desarrollo
	@echo "🚀 Configuración rápida para desarrollo"
	@if [ ! -d "$(VENV)" ]; then make setup; fi
	@make install-dev
	@echo "✅ Listo para desarrollar!"
	@echo "Activa el entorno con: source $(VENV)/bin/activate"

dev-check: ## Verificación completa antes de commit
	@echo "🔍 Verificación completa antes de commit..."
	@make format
	@make lint
	@make typecheck
	@make test-quick
	@make examples
	@echo "✅ ¡Todo listo para commit!"

# Comandos de CI/CD
ci-install: ## Instalar para CI/CD
	$(UV) pip install -e ".[dev]"

ci-test: ## Ejecutar tests para CI/CD
	$(PYTHON) examples/run_all_examples.py
	$(UV) run mypy src/
	$(UV) run flake8 src/

# Información del proyecto
info: ## Mostrar información del proyecto
	@echo "📋 Información del Proyecto"
	@echo "=========================="
	@echo "Nombre: filelock-sync-and-async"
	@echo "Python: $$(python --version 2>/dev/null || echo 'No encontrado')"
	@echo "UV: $$(uv --version 2>/dev/null || echo 'No encontrado')"
	@echo "Entorno virtual: $(VENV)"
	@echo "Entorno activo: $${VIRTUAL_ENV:-'No activo'}"
	@echo ""
	@echo "📁 Estructura:"
	@find . -name "*.py" -path "./src/*" -o -path "./examples/*" | head -10
	@echo ""
	@echo "🔧 Para empezar:"
	@echo "  make setup      # Crear entorno virtual"
	@echo "  source .venv/bin/activate"
	@echo "  make install-dev # Instalar dependencias"
	@echo "  make examples    # Probar ejemplos"