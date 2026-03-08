"""
main.py - Entry point for Personal Finance Manager
Run this file to start the application: python main.py
"""

import sys
import os

# Ensure the project root is on the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.menu import run_app

if __name__ == "__main__":
    try:
        run_app()
    except KeyboardInterrupt:
        print("\n\n  ⚡ Application interrupted. Goodbye!\n")
        sys.exit(0)
