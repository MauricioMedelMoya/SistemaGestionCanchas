# INDICE - Documentacion del Proyecto

Este archivo sirve como guia de lectura para entender la documentacion tecnica del proyecto **Arriendo de Canchas**. Su objetivo es indicar que contiene cada archivo y en que orden conviene revisarlo.

---

## Documentacion Principal

### Orden Sugerido de Lectura

1. **[README.md](README.md)** - Instalacion, ejecucion local, credenciales de prueba y funcionalidades principales.
2. **[ENTREGA_FINAL.md](ENTREGA_FINAL.md)** - Resumen de la implementacion, evidencias de cumplimiento y estado general del proyecto.
3. **[GITHUB_HOOKS_ADR.md](GITHUB_HOOKS_ADR.md)** - Guia tecnica sobre ADR, hooks locales, GitHub Actions y validaciones.
4. **[QUICK_START.md](QUICK_START.md)** - Comandos rapidos para configurar, validar y ejecutar el flujo de trabajo.

### Documentacion Complementaria

| Archivo | Proposito |
|---------|-----------|
| [README.md](README.md) | Guia inicial para instalar y ejecutar la aplicacion Flask. |
| [ENTREGA_FINAL.md](ENTREGA_FINAL.md) | Documento de cierre con resumen de archivos, validaciones y cumplimiento tecnico. |
| [GITHUB_HOOKS_ADR.md](GITHUB_HOOKS_ADR.md) | Explica la estrategia de decisiones arquitectonicas, hooks y CI/CD. |
| [QUICK_START.md](QUICK_START.md) | Referencia breve de comandos frecuentes. |
| [RESUMEN_EJECTUVO.md](RESUMEN_EJECTUVO.md) | Resumen ejecutivo historico de la implementacion. |

---

## Architecture Decision Records (ADRs)

Los ADR documentan las decisiones arquitectonicas principales del proyecto. Se encuentran en `docs/adr/`.

| ADR | Titulo | Decision | Estado |
|-----|--------|----------|--------|
| [ADR-001](docs/adr/ADR-001.md) | Framework Web | Uso de Flask como framework principal | Aceptado |
| [ADR-002](docs/adr/ADR-002.md) | Servidor WSGI | Uso de Gunicorn para produccion | Aceptado |
| [ADR-003](docs/adr/ADR-003.md) | Plataforma de Despliegue | Uso de Heroku, con Render como alternativa | Aceptado |

Cada ADR incluye:
- Contexto del problema
- Opciones consideradas
- Decision tomada
- Justificacion tecnica
- Consecuencias positivas y negativas

---

## Scripts de Validacion

Estos scripts permiten verificar que la documentacion arquitectonica y el codigo se mantengan coherentes.

| Archivo | Proposito | Uso |
|---------|-----------|-----|
| [check_adr.py](check_adr.py) | Valida que los ADR requeridos existan y tengan la estructura esperada. | `python check_adr.py` |
| [check_architecture.py](check_architecture.py) | Valida coherencia entre decisiones arquitectonicas y archivos del proyecto. | `python check_architecture.py` |
| [validate_all.py](validate_all.py) | Ejecuta una validacion general del proyecto. | `python validate_all.py` |

---

## GitHub Hooks y CI/CD

### Hooks Locales

**Archivo:** [.pre-commit-config.yaml](.pre-commit-config.yaml)

Configura validaciones que se ejecutan antes de cada commit, incluyendo:
- Revision de espacios finales y fin de archivo
- Validacion YAML
- Control de archivos grandes
- Deteccion de conflictos de merge
- Linting con flake8
- Formato con black
- Orden de imports con isort
- Validacion de ADR
- Validacion de coherencia arquitectura-codigo

Instalacion:

```bash
pip install pre-commit
pre-commit install
```

### GitHub Actions

**Archivo:** [.github/workflows/validacion.yml](.github/workflows/validacion.yml)

Ejecuta validaciones automaticas en push y pull request hacia `main` o `develop`.

Valida:
- Sintaxis Python
- Formato de codigo
- Imports
- ADR
- Coherencia arquitectura-codigo
- Procfile
- Tests, si existen

---

## Configuracion de Despliegue

| Archivo | Proposito |
|---------|-----------|
| [Procfile](Procfile) | Define el comando de arranque para plataformas compatibles con Heroku. |
| [requirements.txt](requirements.txt) | Lista las dependencias necesarias para instalar y ejecutar el proyecto. |
| [.gitignore](.gitignore) | Evita versionar archivos generados, entorno virtual y base de datos local. |

Comando definido en `Procfile`:

```text
web: gunicorn app:app
```

---

## Estructura General

```text
Arriendo_de_canchas/
|
|-- Documentacion
|   |-- README.md
|   |-- INDICE.md
|   |-- ENTREGA_FINAL.md
|   |-- GITHUB_HOOKS_ADR.md
|   |-- QUICK_START.md
|   |-- RESUMEN_EJECTUVO.md
|
|-- ADR
|   |-- docs/adr/ADR-001.md
|   |-- docs/adr/ADR-002.md
|   |-- docs/adr/ADR-003.md
|
|-- Validacion
|   |-- check_adr.py
|   |-- check_architecture.py
|   |-- validate_all.py
|
|-- GitHub
|   |-- .pre-commit-config.yaml
|   |-- .github/workflows/validacion.yml
|
|-- Aplicacion
|   |-- app.py
|   |-- templates/
|   |-- instance/
|
|-- Despliegue
|   |-- Procfile
|   |-- requirements.txt
|   |-- .gitignore
```

---

## Checklist de Revision

- [x] README con instrucciones de instalacion y ejecucion
- [x] ADR-001 documenta la decision del framework web
- [x] ADR-002 documenta la decision del servidor WSGI
- [x] ADR-003 documenta la decision de despliegue
- [x] Hooks locales configurados en `.pre-commit-config.yaml`
- [x] GitHub Actions configurado en `.github/workflows/validacion.yml`
- [x] Scripts de validacion disponibles
- [x] Procfile configurado para despliegue
- [x] Documentacion tecnica organizada

---

## Referencias Rapidas

### Validaciones

```bash
python check_adr.py
python check_architecture.py
python validate_all.py
pre-commit run --all-files
```

### Ejecucion Local

```bash
python app.py
```

### Flujo Git Basico

```bash
git status
git add .
git commit -m "feat: descripcion del cambio"
git push origin main
```

---

**Ultima actualizacion:** 2026-05-04  
**Estado:** Documentacion organizada para revision y entrega
