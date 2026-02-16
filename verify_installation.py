#!/usr/bin/env python
"""
Installation and environment verification script.
Checks all dependencies, configurations, and readiness.
"""
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check Python version."""
    print("Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 9:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro} OK\n")
        return True
    else:
        print(f"✗ Python 3.9+ required (found {version.major}.{version.minor})\n")
        return False

def check_module(module_name, display_name=None):
    """Check if a Python module is installed."""
    display_name = display_name or module_name
    try:
        __import__(module_name)
        print(f"  ✓ {display_name}")
        return True
    except ImportError:
        print(f"  ✗ {display_name} (missing)")
        return False

def check_dependencies():
    """Check all required Python packages."""
    print("Checking Python dependencies...")
    
    required = [
        ("fastapi", "FastAPI"),
        ("uvicorn", "Uvicorn"),
        ("pydantic", "Pydantic"),
        ("streamlit", "Streamlit"),
        ("plotly", "Plotly"),
        ("requests", "Requests"),
        ("spacy", "spaCy"),
        ("sentence_transformers", "sentence-transformers"),
        ("pdfplumber", "pdfplumber"),
        ("docx", "python-docx"),
        ("fuzzywuzzy", "fuzzywuzzy"),
    ]
    
    all_ok = True
    for module, display_name in required:
        if not check_module(module, display_name):
            all_ok = False
    
    print()
    return all_ok

def check_spacy_model():
    """Check if spaCy English model is installed."""
    print("Checking spaCy model...")
    try:
        import spacy
        nlp = spacy.load("en_core_web_sm")
        print("✓ spaCy en_core_web_sm model OK\n")
        return True
    except Exception as e:
        print(f"✗ spaCy model not found or broken")
        print("  Run: python -m spacy download en_core_web_sm\n")
        return False

def check_project_structure():
    """Check if project structure is correct."""
    print("Checking project structure...")
    
    required_dirs = [
        "backend",
        "backend/api",
        "backend/nlp",
        "backend/services",
        "backend/utils",
        "backend/models",
        "frontend",
        "tests",
        "sample_data",
    ]
    
    required_files = [
        "backend/main.py",
        "backend/config.py",
        "backend/api/routes.py",
        "backend/nlp/extraction.py",
        "backend/services/analyzer.py",
        "backend/utils/parser.py",
        "backend/models/schemas.py",
        "frontend/streamlit_app.py",
        "requirements.txt",
        "README.md",
    ]
    
    all_ok = True
    base_path = Path(".")
    
    for dir_path in required_dirs:
        if (base_path / dir_path).exists():
            print(f"  ✓ {dir_path}/")
        else:
            print(f"  ✗ {dir_path}/ (missing)")
            all_ok = False
    
    print()
    
    for file_path in required_files:
        if (base_path / file_path).exists():
            print(f"  ✓ {file_path}")
        else:
            print(f"  ✗ {file_path} (missing)")
            all_ok = False
    
    print()
    return all_ok

def check_ports():
    """Check if required ports are available."""
    print("Checking ports...")
    
    ports = {
        8000: "Backend API",
        8501: "Streamlit Frontend",
    }
    
    import socket
    
    all_ok = True
    for port, service in ports.items():
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1', port))
        sock.close()
        
        if result == 0:
            print(f"  ⚠ Port {port} ({service}) is in use")
            all_ok = False
        else:
            print(f"  ✓ Port {port} ({service}) available")
    
    print()
    return all_ok

def check_disk_space():
    """Check available disk space."""
    print("Checking disk space...")
    
    try:
        import shutil
        total, used, free = shutil.disk_usage(".")
        free_gb = free / (1024**3)
        
        if free_gb > 2:
            print(f"  ✓ {free_gb:.1f}GB free space available\n")
            return True
        else:
            print(f"  ✗ Only {free_gb:.1f}GB free (need ~2GB for NLP models)\n")
            return False
    except Exception as e:
        print(f"  ⚠ Could not check disk space: {e}\n")
        return True

def main():
    """Run all checks."""
    print("\n" + "="*60)
    print("Resume Analyzer - Installation Verification")
    print("="*60 + "\n")
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("spaCy Model", check_spacy_model),
        ("Project Structure", check_project_structure),
        ("Available Ports", check_ports),
        ("Disk Space", check_disk_space),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"✗ Error checking {name}: {e}\n")
            results.append((name, False))
    
    # Summary
    print("="*60)
    print("Verification Summary")
    print("="*60)
    
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{name:25} {status}")
    
    all_passed = all(result[1] for result in results)
    
    print("="*60 + "\n")
    
    if all_passed:
        print("✓ All checks passed! You're ready to run the application.\n")
        print("Next steps:")
        print("  1. Terminal 1: cd backend && python main.py")
        print("  2. Terminal 2: streamlit run frontend/streamlit_app.py")
        print("  3. Open: http://localhost:8501")
        print()
    else:
        print("✗ Some checks failed. Fix issues above before running.\n")
        print("Installation help:")
        print("  pip install -r requirements.txt")
        print("  python -m spacy download en_core_web_sm")
        print()

if __name__ == "__main__":
    main()
