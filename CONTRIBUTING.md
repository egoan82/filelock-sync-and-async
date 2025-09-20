# Guía de Contribución

¡Gracias por tu interés en contribuir a FileLock! Esta guía te ayudará a comenzar.

## 🚀 Primeros Pasos

1. **Fork** el repositorio en GitHub
2. **Clona** tu fork localmente:
   ```bash
   git clone https://github.com/tu-usuario/filelock-sync-and-async.git
   cd filelock-sync-and-async
   ```
3. **Crea una rama** para tu contribución:
   ```bash
   git checkout -b feature/nueva-caracteristica
   ```

## 🧪 Ejecutar Pruebas

Antes de hacer cambios, asegúrate de que todo funciona:

```bash
# Ejecutar todos los ejemplos
python examples/run_all_examples.py

# Probar un ejemplo específico
python examples/sync/01_basic_usage.py
```

## 📝 Tipos de Contribuciones

### 🐛 Reportar Bugs

Si encuentras un bug, por favor:

1. Verifica que no esté ya reportado en los [issues](https://github.com/tu-usuario/filelock-sync-and-async/issues)
2. Crea un nuevo issue incluyendo:
   - Descripción clara del problema
   - Pasos para reproducirlo
   - Versión de Python y sistema operativo
   - Mensaje de error completo (si aplica)

### ✨ Nuevas Características

Para proponer nuevas características:

1. Abre un issue para discutir la propuesta
2. Espera feedback antes de comenzar a programar
3. Asegúrate de que esté alineada con los objetivos del proyecto

### 📚 Documentación

Mejoras a la documentación son siempre bienvenidas:

- Corregir typos o errores
- Mejorar explicaciones
- Agregar nuevos ejemplos
- Traducir a otros idiomas

## 🔧 Estándares de Código

### Estilo de Código

- Sigue [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Usa nombres descriptivos para variables y funciones
- Agrega docstrings a funciones y clases nuevas
- Mantén líneas de máximo 88 caracteres

### Estructura de Commits

Usa mensajes de commit descriptivos:

```bash
# Bueno
git commit -m "Agregar soporte para timeout infinito en AsyncFileLock"

# Malo
git commit -m "Fix bug"
```

### Ejemplos

Si agregas nuevas características, incluye ejemplos:

- Crea un archivo en `examples/` que demuestre la funcionalidad
- Usa nombres descriptivos para los archivos
- Incluye comentarios explicativos
- Asegúrate de que funcionen correctamente

## 🧪 Testing

### Crear Nuevos Tests

Si agregas funcionalidad nueva:

1. Crea tests en la carpeta `tests/` (TODO)
2. Usa `pytest` como framework de testing
3. Incluye tests tanto para casos exitosos como de error
4. Asegúrate de que los tests pasen en tu sistema

### Verificar Compatibilidad

- Prueba en diferentes versiones de Python (3.7+)
- Verifica que funcione en Linux/macOS
- No uses características específicas de Windows

## 📋 Checklist para Pull Requests

Antes de enviar tu PR, verifica:

- [ ] Los cambios están en una rama separada
- [ ] El código sigue los estándares del proyecto
- [ ] Los ejemplos existentes siguen funcionando
- [ ] Se agregaron ejemplos para nuevas características
- [ ] La documentación está actualizada
- [ ] Los mensajes de commit son descriptivos
- [ ] No hay archivos innecesarios (por ejemplo, `__pycache__/`)

## 🎯 Proceso de Review

1. **Envía el PR** con una descripción clara
2. **Espera el review** - puede tomar unos días
3. **Responde a feedback** - haz los cambios solicitados
4. **Actualiza tu rama** si hay conflictos
5. **Merge** - ¡tu contribución será incluida!

## 💡 Ideas para Contribuir

Si buscas inspiración, aquí hay algunas ideas:

### 🚀 Características Nuevas

- Soporte para locks de lectura/escritura
- Integración con systemd locks
- Métricas y estadísticas de uso
- Pool de locks reutilizables

### 🧪 Testing

- Suite de tests automatizados
- Tests de rendimiento
- Tests de concurrencia
- Integración continua

### 📚 Documentación

- Más ejemplos de casos de uso
- Guías de mejores prácticas
- Comparación con otras bibliotecas
- Tutoriales paso a paso

### 🔧 Herramientas

- Script de instalación
- Herramientas de debugging
- Benchmarking tools
- Linting automático

## 🤝 Comunidad

- Se respetuoso y constructivo en las discusiones
- Ayuda a otros usuarios en los issues
- Comparte tus casos de uso interesantes
- Reporta bugs y problemas de seguridad responsablemente

## 📞 Contacto

Si tienes preguntas sobre contribuir:

- Abre un [issue](https://github.com/tu-usuario/filelock-sync-and-async/issues)
- Menciona `@maintainer` en GitHub
- Revisa discusiones existentes

¡Gracias por contribuir! 🎉