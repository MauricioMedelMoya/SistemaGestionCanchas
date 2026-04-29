#!/usr/bin/env python3
"""
check_architecture.py - Validador de Coherencia Arquitectura-Código
Verifica que las decisiones en ADRs estén reflejadas en el código.

Uso:
    python check_architecture.py
"""

import sys
import io
from pathlib import Path

# Configurar salida UTF-8 para Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def check_framework_coherence():
    """
    ADR-001: Verifica que Flask esté importado en app.py
    """
    print("\n[ADR-001] Framework Web (Flask)")
    
    app_py = Path("app.py")
    if not app_py.exists():
        print("  [ERROR] app.py no existe")
        return False
    
    content = app_py.read_text(encoding='utf-8')
    
    checks = [
        ("from flask import Flask" in content, "Import Flask en app.py"),
        ("Flask-SQLAlchemy" in open("requirements.txt").read(), "Flask-SQLAlchemy en requirements.txt"),
        ('app = Flask(__name__)' in content, "Instancia Flask creada"),
    ]
    
    all_ok = True
    for check, description in checks:
        if check:
            print(f"  ✅ {description}")
        else:
            print(f"  ❌ {description}")
            all_ok = False
    
    return all_ok


def check_wsgi_coherence():
    """
    ADR-002: Verifica que Gunicorn esté en Procfile y requirements.txt
    """
    print("\n[ADR-002] Servidor WSGI (Gunicorn)")
    
    checks = []
    
    # Verificar Procfile
    procfile = Path("Procfile")
    if procfile.exists():
        content = procfile.read_text(encoding='utf-8')
        checks.append(
            ("gunicorn app:app" in content, "Procfile contiene 'gunicorn app:app'")
        )
    else:
        print("  [ERROR] Procfile no existe")
        return False
    
    # Verificar requirements.txt
    req_file = Path("requirements.txt")
    if req_file.exists():
        content = req_file.read_text(encoding='utf-8')
        checks.append(
            ("gunicorn" in content.lower(), "Gunicorn en requirements.txt")
        )
    else:
        print("  [ERROR] requirements.txt no existe")
        return False
    
    all_ok = True
    for check, description in checks:
        if check:
            print(f"  [OK] {description}")
        else:
            print(f"  [ERROR] {description}")
            all_ok = False
    
    return all_ok


def check_deployment_coherence():
    """
    ADR-003: Verifica que la plataforma de despliegue esté documentada
    """
    print("\n[ADR-003] Plataforma de Despliegue (Heroku)")
    
    # Verificar que existe Procfile (requisito para Heroku)
    procfile = Path("Procfile")
    check1 = procfile.exists()
    print(f"  {'[OK]' if check1 else '[ERROR]'} Procfile existe (requerido por Heroku)")
    
    # Verificar que ADR documenta la decisión
    adr_file = Path("docs/adr/ADR-003.md")
    check2 = adr_file.exists()
    print(f"  {'[OK]' if check2 else '[ERROR]'} ADR-003.md documenta la decisión")
    
    return check1 and check2


def check_git_integration():
    """
    Verifica que el repositorio esté configurado para GitHub
    """
    print("\n[Integración] GitHub Configuration")
    
    checks = []
    
    # Verificar .git existe
    git_dir = Path(".git")
    if git_dir.exists():
        print(f"  [OK] Repositorio Git inicializado")
        checks.append(True)
    else:
        print(f"  [ADVERTENCIA] Git no inicializado (ejecuta: git init)")
        checks.append(False)
    
    # Verificar .gitignore
    gitignore = Path(".gitignore")
    if gitignore.exists():
        content = gitignore.read_text(encoding='utf-8')
        has_venv = "venv" in content
        has_pycache = "__pycache__" in content
        print(f"  {'[OK]' if has_venv else '[ADVERTENCIA]'} .gitignore ignora venv")
        print(f"  {'[OK]' if has_pycache else '[ADVERTENCIA]'} .gitignore ignora __pycache__")
        checks.append(has_venv or has_pycache)
    else:
        print(f"  [ADVERTENCIA] .gitignore no existe")
    
    return all(checks)


def main():
    """Función principal."""
    print("=" * 70)
    print("VALIDACION DE COHERENCIA: ARQUITECTURA <> CODIGO")
    print("=" * 70)
    
    results = {
        "ADR-001 (Framework Web)": check_framework_coherence(),
        "ADR-002 (Servidor WSGI)": check_wsgi_coherence(),
        "ADR-003 (Plataforma)": check_deployment_coherence(),
        "GitHub Integration": check_git_integration(),
    }
    
    print("\n" + "=" * 70)
    print("RESUMEN DE VALIDACION")
    print("=" * 70)
    
    for check, result in results.items():
        print(f"{'[OK]' if result else '[ERROR]'} {check}")
    
    print("=" * 70)
    
    if all(results.values()):
        print("[OK] VALIDACION EXITOSA: Arquitectura coherente con codigo")
        print("=" * 70)
        return 0
    else:
        print("[ERROR] VALIDACION FALLIDA: Existen inconsistencias")
        print("=" * 70)
        return 1


if __name__ == "__main__":
    sys.exit(main())
