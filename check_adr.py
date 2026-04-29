#!/usr/bin/env python3
"""
check_adr.py - Validador de ADR (Architecture Decision Records)
Verifica que todos los ADRs requeridos existan y sean válidos.

Uso:
    python check_adr.py
"""

import os
import sys
import io
from pathlib import Path

# Configurar salida UTF-8 para Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def check_adr_files():
    """Verifica que existan todos los archivos ADR requeridos."""
    required_adrs = [
        "ADR-001.md",  # Framework Web
        "ADR-002.md",  # Servidor WSGI
        "ADR-003.md",  # Plataforma de despliegue
    ]
    
    adr_dir = Path("docs/adr")
    
    if not adr_dir.exists():
        print("[ERROR] Directorio docs/adr no existe")
        return False
    
    all_exist = True
    for adr_file in required_adrs:
        adr_path = adr_dir / adr_file
        if not adr_path.exists():
            print(f"[ERROR] {adr_file} no existe")
            all_exist = False
        else:
            print(f"[OK] {adr_file} existe")
    
    return all_exist


def check_adr_structure():
    """Verifica que cada ADR tenga estructura correcta."""
    adr_dir = Path("docs/adr")
    required_sections = ["Contexto", "Opciones Consideradas", "Decisión", "Rationale", "Consecuencias"]
    
    adr_files = sorted(adr_dir.glob("ADR-*.md"))
    
    if not adr_files:
        print("[ERROR] No se encontraron archivos ADR")
        return False
    
    all_valid = True
    for adr_file in adr_files:
        print(f"\nValidando {adr_file.name}:")
        content = adr_file.read_text(encoding='utf-8')
        
        for section in required_sections:
            if section in content:
                print(f"  [OK] Sección '{section}' existe")
            else:
                print(f"  [ERROR] Sección '{section}' falta")
                all_valid = False
    
    return all_valid


def main():
    """Función principal."""
    print("=" * 60)
    print("VALIDACIÓN DE ARCHITECTURE DECISION RECORDS (ADRs)")
    print("=" * 60)
    
    print("\n1. Verificando existencia de archivos ADR...")
    files_ok = check_adr_files()
    
    print("\n2. Verificando estructura de ADRs...")
    structure_ok = check_adr_structure()
    
    print("\n" + "=" * 60)
    if files_ok and structure_ok:
        print("[OK] VALIDACIÓN EXITOSA: Todos los ADRs son válidos")
        print("=" * 60)
        return 0
    else:
        print("[ERROR] VALIDACIÓN FALLIDA: Existen problemas en los ADRs")
        print("=" * 60)
        return 1


if __name__ == "__main__":
    sys.exit(main())
