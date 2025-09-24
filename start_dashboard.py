#!/usr/bin/env python
"""
Script de démarrage pour le dashboard Flask
Dashboard d'analyse des données Diabète avec Redis
"""

import sys
import subprocess
import os

def check_redis_connection():
    """Vérifier si Redis est accessible"""
    try:
        import redis
        r = redis.Redis(host='localhost', port=6379, decode_responses=True, db=0)
        r.ping()
        print("✓ Connexion Redis OK")
        return True
    except Exception as e:
        print(f"✗ Erreur connexion Redis: {e}")
        print("  Assurez-vous que Redis Stack est démarré sur le port 6379")
        return False

def install_requirements():
    """Installer les dépendances si nécessaire"""
    try:
        import flask
        print("✓ Flask déjà installé")
    except ImportError:
        print("Installation des dépendances...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Dépendances installées")

def main():
    print("=" * 60)
    print("Dashboard Analyse Diabète - Redis")
    print("=" * 60)
    
    # Vérifier les dépendances
    install_requirements()
    
    # Vérifier Redis
    if not check_redis_connection():
        print("\n Veuillez démarrer Redis Stack avant de lancer le dashboard")
        print("   Command: redis-stack-server")
        return
    
    print("\n Démarrage du dashboard Flask...")
    print("   URL: http://localhost:5000")
    print("   Appuyez sur Ctrl+C pour arrêter")
    print("-" * 60)
    
    # Lancer Flask
    try:
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n\n Dashboard arrêté")
    except Exception as e:
        print(f"\n Erreur lors du démarrage: {e}")

if __name__ == "__main__":
    main()