#!/usr/bin/env python3
"""
validate_all.py - Ejecuta todas las validaciones del proyecto
Simula lo que hace GitHub Actions de forma local

Uso:
    python validate_all.py
"""

import os
import sys
import subprocess
from pathlib import Path

def print_header(text):
    """Imprime un encabezado"""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70)

def run_command(cmd, description):
    """Ejecuta un comando y reporta el resultado"""
    print(f"\n▶ {description}...")
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            capture_output=True, 
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            print(f"✅ {description}")
            return True
        else:
            print(f"❌ {description}")
            if result.stderr:
                print(f"   Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} - Excepción: {e}")
        return False

def check_files_exist():
    """Verificar que archivos clave existan"""
    print("\n▶ Verificando existencia de archivos...")
    
    required_files = {
        "app.py": "Aplicación Flask",
        "Procfile": "Configuración de despliegue",
        "requirements.txt": "Dependencias",
        "docs/adr/ADR-001.md": "ADR: Framework Web",
        "docs/adr/ADR-002.md": "ADR: Servidor WSGI",
        "docs/adr/ADR-003.md": "ADR: Plataforma",
        "check_adr.py": "Validador ADR",
        "check_architecture.py": "Validador arquitectura",
        ".pre-commit-config.yaml": "Configuración pre-commit",
    }
    
    all_exist = True
    for filepath, description in required_files.items():
        if Path(filepath).exists():
            print(f"  ✅ {description}: {filepath}")
        else:
            print(f"  ❌ {description}: {filepath} NO EXISTE")
            all_exist = False
    
    return all_exist

def main():
    """Función principal"""
    
    print_header("VALIDACIÓN COMPLETA DEL PROYECTO")
    print("Ejecutando todas las validaciones como lo haría GitHub Actions...\n")
    
    results = {}
    
    # 1. Verificar archivos
    print_header("1. VERIFICAR ARCHIVOS REQUERIDOS")
    results["Archivos"] = check_files_exist()
    
    # 2. Validar Python
    print_header("2. VERIFICAR SINTAXIS PYTHON")
    results["Python Syntax"] = run_command(
        "python -m py_compile app.py check_adr.py check_architecture.py",
        "Compilación Python"
    )
    
    # 3. Validar ADRs
    print_header("3. VALIDAR ARCHITECTURE DECISION RECORDS")
    results["ADR Validation"] = run_command(
        "python check_adr.py",
        "Validación de ADRs"
    )
    
    # 4. Validar coherencia
    print_header("4. VALIDAR COHERENCIA ARQUITECTURA-CÓDIGO")
    results["Architecture Coherence"] = run_command(
        "python check_architecture.py",
        "Validación de coherencia"
    )
    
    # 5. Verificar Procfile
    print_header("5. VERIFICAR PROCFILE PARA DESPLIEGUE")
    procfile_ok = Path("Procfile").exists()
    if procfile_ok:
        content = Path("Procfile").read_text()
        if "gunicorn app:app" in content:
            print("✅ Procfile contiene: web: gunicorn app:app")
        else:
            print("⚠️  Procfile existe pero no tiene gunicorn config")
            procfile_ok = False
    else:
        print("❌ Procfile no existe")
    results["Procfile"] = procfile_ok
    
    # 6. Verificar estructura ADRs
    print_header("6. VERIFICAR ESTRUCTURA DE ADRs")
    adr_dir = Path("docs/adr")
    if adr_dir.exists():
        adr_files = list(adr_dir.glob("ADR-*.md"))
        print(f"✅ Encontrados {len(adr_files)} ADRs")
        for adr in sorted(adr_files):
            print(f"  ✅ {adr.name}")
        results["ADR Structure"] = len(adr_files) >= 3
    else:
        print("❌ Directorio docs/adr no existe")
        results["ADR Structure"] = False
    
    # 7. Verificar requirements.txt
    print_header("7. VERIFICAR DEPENDENCIAS")
    req_file = Path("requirements.txt")
    if req_file.exists():
        content = req_file.read_text()
        checks = {
            "Flask": "Flask" in content,
            "Flask-SQLAlchemy": "Flask-SQLAlchemy" in content,
            "Gunicorn": "gunicorn" in content.lower(),
        }
        for pkg, exists in checks.items():
            print(f"  {'✅' if exists else '❌'} {pkg}")
        results["Requirements"] = all(checks.values())
    else:
        print("❌ requirements.txt no existe")
        results["Requirements"] = False
    
    # Resumen final
    print_header("RESUMEN DE VALIDACIÓN")
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    
    for check, result in results.items():
        status = "✅" if result else "❌"
        print(f"{status} {check}")
    
    print("\n" + "="*70)
    print(f"Resultados: {passed}/{total} validaciones pasaron")
    print("="*70)
    
    if passed == total:
        print("\n✅ PROYECTO VALIDADO EXITOSAMENTE")
        print("   Listo para commit, push y despliegue")
        print("="*70)
        return 0
    else:
        failed = total - passed
        print(f"\n❌ {failed} validación(es) fallaron")
        print("   Revisa los errores arriba")
        print("="*70)
        return 1

if __name__ == "__main__":
    sys.exit(main())
