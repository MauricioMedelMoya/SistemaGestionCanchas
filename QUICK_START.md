# QUICK START - GitHub Hooks y ADR

## 1. PRIMEROS PASOS

### Inicializar Git
```bash
cd Arriendo_de_canchas
git init
git add .
git commit -m "feat: implementacion ADR y GitHub Hooks"
```

### Instalar Pre-commit
```bash
pip install pre-commit
pre-commit install
```

### Verificar Validaciones
```bash
python check_adr.py           # Debe pasar
python check_architecture.py  # Debe pasar
```

---

## 2. WORKFLOW DIARIO

```bash
# 1. Hacer cambios
code app.py

# 2. Validar manualmente (opcional)
python check_adr.py
python check_architecture.py

# 3. Commit (auto-ejecuta hooks)
git add .
git commit -m "feat: descripcion del cambio"
# Pre-commit automaticamente:
#   Valida ADRs
#   Valida coherencia
#   Formatea codigo (black)
#   Organiza imports (isort)
#   Lint (flake8)

# 4. Push a GitHub
git push origin main
# GitHub Actions automaticamente:
#   Ejecuta tests
#   Valida ADRs
#   Valida coherencia
```

---

## 3. ARCHIVOS CLAVE

| Archivo | Propósito |
|---------|-----------|
| `docs/adr/ADR-001.md` | Framework Web (Flask) |
| `docs/adr/ADR-002.md` | Servidor WSGI (Gunicorn) |
| `docs/adr/ADR-003.md` | Plataforma (Heroku) |
| `Procfile` | `web: gunicorn app:app` |
| `requirements.txt` | Dependencias (con gunicorn) |
| `.pre-commit-config.yaml` | Configuracion hooks locales |
| `.github/workflows/validacion.yml` | GitHub Actions CI/CD |
| `check_adr.py` | Validador de ADRs |
| `check_architecture.py` | Validador de coherencia |

---

## 4. TROUBLESHOOTING

### Error: "pre-commit: command not found"
```bash
pip install pre-commit
```

### Error: "check_adr.py no encontrado"
```bash
# Asegurate de estar en la raiz del proyecto
cd Arriendo_de_canchas
python check_adr.py
```

### Pre-commit falla, quiero saltarlo (no recomendado)
```bash
git commit --no-verify  # Solo en emergencias
```

### Ver que hace cada hook
```bash
pre-commit run --all-files  # Ejecuta todos manualmente
```

---

## 5. DESPLIEGUE

### En Heroku
```bash
heroku create arriendo-canchas
git push heroku main
heroku logs --tail
```

### En Render (alternativa)
```bash
# Conectar repo en render.com
# La app se despliega automaticamente en cada push a main
```

---

## 6. VALIDACION RAPIDA

```bash
# Verificar que todo esta bien
./check_all.sh  # Este script valida todo

# O manualmente:
python check_adr.py && python check_architecture.py && echo "TODO OK"
```

---

## CHECKLIST PRE-ENTREGA

- [ ] `python check_adr.py` pasa
- [ ] `python check_architecture.py` pasa
- [ ] `pre-commit run --all-files` pasa
- [ ] Cambios commiteados a main
- [ ] Push a GitHub realizado
- [ ] GitHub Actions paso (Actions tab)
- [ ] Documentacion actualizada
- [ ] Procfile funciona localmente: `gunicorn app:app`

---

**Recursos:**
- [GITHUB_HOOKS_ADR.md](GITHUB_HOOKS_ADR.md) - Documentacion completa
- [RESUMEN_EJECUTIVO.md](RESUMEN_EJECTUVO.md) - Resumen de implementacion
