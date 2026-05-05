# GitHub Hooks y ADR - Guía de Implementación

## Resumen del Proyecto

Este proyecto implementa un sistema completo de **Arquitectura Decision Records (ADRs)** integrado con **GitHub Hooks** para garantizar coherencia entre decisiones arquitectónicas y código implementado.

---

## Arquitectura - Decisiones Documentadas

### ADR-001: Framework Web - Flask
**Decisión:** Usar Flask como framework web principal
- app.py contiene instancia Flask
- requirements.txt tiene Flask==3.0.3
- Ver: [docs/adr/ADR-001.md](docs/adr/ADR-001.md)

### ADR-002: Servidor WSGI - Gunicorn
**Decisión:** Usar Gunicorn como servidor WSGI en producción
- Procfile contiene: `web: gunicorn app:app`
- requirements.txt contiene gunicorn==21.2.0
- Coherencia debug vs producción documentada
- Ver: [docs/adr/ADR-002.md](docs/adr/ADR-002.md)

### ADR-003: Plataforma de Despliegue - Heroku
**Decisión:** Usar Heroku (o alternativas: Render, Railway)
- Procfile está presente
- Aplicación lista para `git push heroku main`
- Ver: [docs/adr/ADR-003.md](docs/adr/ADR-003.md)

---

## GitHub Hooks Locales

### Instalación de Pre-commit Hooks

```bash
# 1. Instalar pre-commit
pip install pre-commit

# 2. Instalar los hooks en tu repositorio local
pre-commit install

# 3. (Opcional) Ejecutar hooks en todos los archivos
pre-commit run --all-files
```

### Hooks Configurados

Los siguientes validadores se ejecutan **automáticamente** antes de cada commit:

| Hook | Función |
|------|---------|
| `trailing-whitespace` | Elimina espacios finales |
| `end-of-file-fixer` | Asegura salto de línea final |
| `check-yaml` | Valida sintaxis YAML |
| `check-added-large-files` | Rechaza archivos > 512KB |
| `flake8` | Linting Python |
| `black` | Formato de código Python |
| `isort` | Organización de imports |
| `check-adr` | Valida que todos los ADRs existan |
| `check-architecture` | Valida coherencia arquitectura-código |

### Uso Manual de Hooks

```bash
# Ejecutar validación ADR
python check_adr.py

# Ejecutar validación coherencia arquitectura
python check_architecture.py

# Ejecutar todos los hooks (sin commit)
pre-commit run --all-files
```

---

## GitHub Actions - CI/CD Automático

### Workflow: Validación de Proyecto

**Archivo:** `.github/workflows/validacion.yml`

Se ejecuta automáticamente en:
- Cada push a `main` o `develop`
- Cada Pull Request a `main` o `develop`

### Validaciones Automáticas

1. **Sintaxis Python:** Verifica que app.py sea válido
2. **Formato:** Black, isort, flake8
3. **ADRs:** Verifica que todos existan y sean válidos
4. **Coherencia:** Verifica que decisiones estén en código
5. **Procfile:** Valida despliegue
6. **Tests:** Ejecuta pytest si existen

### Requisitos para Merge

Para hacer merge a `main` o `develop`:

```
Requerido Automático:
  Todos los validadores de GitHub Actions pasen
  Validación de ADRs exitosa
  Validación de coherencia arquitectura exitosa

Requerido Manual:
  Revisión de código (1+ reviewers)
  Aprobación del PR
```

---

## Criterios de Aceptación

### Capa Técnica 
- [x] Archivo app.py funcional
- [x] Endpoint raíz `/` disponible
- [x] requirements.txt presente
- [x] Procfile presente
- [x] Aplicación desplegable

### Capa Arquitectónica 
- [x] ADR-001 (Framework Web) - Flask
- [x] ADR-002 (Servidor WSGI) - Gunicorn
- [x] ADR-003 (Plataforma) - Heroku
- [x] Cada ADR tiene: Contexto, Opciones, Decisión, Rationale, Consecuencias

### Capa de Coherencia 
- [x] ADR-001 (Flask) → code imports Flask 
- [x] ADR-002 (Gunicorn) → Procfile contiene `gunicorn app:app` 
- [x] ADR-003 (Heroku) → Procfile presente 

### Capa de Rationale 
- [x] Justificación de Gunicorn documentada en ADR-002
- [x] Diferencia debug vs producción documentada
- [x] Uso de Procfile justificado en ADR-003

---

## Workflow de Desarrollo Típico

### 1. Clonar y Configurar
```bash
git clone <tu-repo>
cd Arriendo_de_canchas
pip install -r requirements.txt
pre-commit install
```

### 2. Hacer Cambios
```bash
# Editar código
code app.py

# Pre-commit valida automáticamente
git add .
git commit -m "feat: agregar nueva feature"
# Se ejecutan automáticamente:
#   - check_adr.py
#   - check_architecture.py
#   - black, flake8, isort
```

### 3. Push y Pull Request
```bash
git push origin feature-branch
# Abre PR en GitHub
# GitHub Actions ejecuta:
#   - Validación completa automática
#   - No se puede mergear sin pasar validaciones
```

### 4. Desplegar (Heroku)
```bash
git push heroku main
```

---

## Cómo Agregar Nuevos ADRs

Si necesitas una nueva decisión arquitectónica:

### 1. Crear nuevo archivo ADR
```bash
touch docs/adr/ADR-004-Tu-Decision.md
```

### 2. Template Básico
```markdown
# ADR-004: [Título de la Decisión]

**Estado:** Aceptado/Propuesto
**Fecha:** YYYY-MM-DD
**Decisor:** Equipo

## Contexto
[Descripción del problema]

## Opciones Consideradas
1. [Opción A]
2. [Opción B]

## Decisión
[Tu decisión]

## Rationale
[Por qué esta decisión]

## Consecuencias
**Positivas:**
- [+]

**Negativas:**
- [-]
```

### 3. Validar
```bash
python check_adr.py
python check_architecture.py
```

---

## Rubrica de Evaluación

| Criterio | Bajo | Medio | Alto |
|----------|------|-------|------|
| Técnico | No funciona | Funciona parcialmente | Funciona correctamente |
| ADR | Incompleto | Completo sin profundidad | Completo y bien justificado |
| Coherencia | Inconsistente | Parcial | Totalmente alineado |
| Rationale | Ausente | Básico | Profundo y crítico |

---

## Troubleshooting

### Pre-commit falla: "check_adr.py no encontrado"
```bash
# Asegurarse que estás en el directorio raíz del proyecto
cd Arriendo_de_canchas

# Reinstalar pre-commit
pre-commit uninstall
pre-commit install
```

### GitHub Actions falla: "ADR no válido"
```bash
# Ejecutar localmente
python check_adr.py
python check_architecture.py

# Verificar estructura docs/adr/
ls -la docs/adr/
```

### Procfile error en Heroku
```bash
# Verificar Procfile
cat Procfile
# Debe contener: web: gunicorn app:app

# Test local
gunicorn app:app
```

---

## Recursos

- **ADR Metodología:** Documenting Architecture Decisions (Michael Nygard)
- **Heroku:** https://devcenter.heroku.com/articles/procfile
- **Gunicorn:** https://gunicorn.org/
- **Pre-commit:** https://pre-commit.com/

---

## Validación Final

Antes de entregar tu proyecto:

```bash
# 1. Ejecutar validaciones locales
python check_adr.py
python check_architecture.py

# 2. Ejecutar todos los PreCommit hooks
pre-commit run --all-files

# 3. Hacer commit (esto ejecuta hooks automáticamente)
git add .
git commit -m "chore: cumplimiento criterios de aceptación"

# 4. Push a GitHub
git push origin main

# 5. Verificar que GitHub Actions pasó en GitHub UI
# → Actions → Validación Proyecto → All checks passed
```

---

**Última actualización:** 2026-04-29  
**Estado:** Listo para Producción
