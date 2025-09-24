# Dashboard Analyse Diabète avec Redis

Ce projet analyse des données médicales de diabète en utilisant Redis comme base de données NoSQL et Flask pour créer un dashboard web interactif.

## Description

Le projet contient une analyse complète de 768 patients diabétiques avec des variables comme le glucose, BMI, âge, grossesses, pression artérielle, etc. Les données sont stockées et analysées dans Redis pour des performances optimales, puis visualisées via un dashboard web moderne.

## Fonctionnalités

- Analyse des groupes d'âge et distribution des patients diabétiques
- Classification par catégories BMI (Insuffisant, Normal, Surpoids, Obèse)
- Analyse des femmes enceintes et facteurs de risque
- Identification des patients à haut risque
- Top 10 des patients avec glucose et BMI les plus élevés
- Corrélation âge-glucose-diabète
- Statistiques de performance Redis en temps réel
- Dashboard web avec graphiques interactifs
- APIs REST pour accéder aux données


  <img width="1890" height="905" alt="image" src="https://github.com/user-attachments/assets/32f67c4c-4a88-40f2-a60c-bbbdb308bbc9" />



## Structure du Projet

```
Redis-BDD/
├── diabetes.csv                    # Dataset original des patients
├── patient.csv                     # Données patients formatées
├── diabetes_redis_analysis.ipynb   # Notebook d'analyse et chargement Redis
├── app.py                          # Application Flask backend
├── start_dashboard.py              # Script de démarrage
├── start_dashboard.bat             # Script Windows pour démarrage
├── requirements.txt                # Dépendances Python
├── README_DASHBOARD.md             # Documentation détaillée du dashboard
├── templates/
│   ├── dashboard.html              # Interface dashboard original
│   ├── dashboard_enhanced.html     # Interface dashboard améliorée
│   └── api_test.html               # Page de test des APIs
└── static/
    └── css/
        └── dashboard.css           # Styles personnalisés
```

## Installation

### Prérequis
- Python 3.8 ou plus récent
- Redis Stack installé et fonctionnel
- Navigateur web moderne

### Étapes d'installation

1. Cloner le projet
```bash
git clone https://github.com/jebalisoumaya/Redis-BDD.git
cd Redis-BDD
```

2. Installer les dépendances Python
```bash
pip install -r requirements.txt
```

3. Démarrer Redis Stack
```bash
docker run -d --name redis-stack -p 6379:6379 -p 8001:8001 redis/redis-stack:latest

```

4. Charger les données dans Redis
Ouvrir et exécuter le notebook `diabetes_redis_analysis.ipynb` pour charger les données

5. Démarrer le dashboard
```bash
python start_dashboard.py
```

## Utilisation

<img width="1895" height="1092" alt="image" src="https://github.com/user-attachments/assets/7acafa9c-3325-4493-a16f-67479d249cef" />

### Dashboard Web
- Accéder au dashboard principal : http://localhost:5000
- Dashboard amélioré avec analyses supplémentaires : http://localhost:5000/enhanced
- Page de test des APIs : http://localhost:5000/api

  <img width="1897" height="973" alt="image" src="https://github.com/user-attachments/assets/9f399578-303c-4ba7-ab6c-244ae9f5543c" />

  <img width="1892" height="982" alt="image" src="https://github.com/user-attachments/assets/1150e521-e4ce-44ab-baa7-2b947f8b3a4d" />



### APIs Disponibles

Le projet expose plusieurs endpoints REST :

- `/api/stats` - Statistiques générales des patients
- `/api/age_groups` - Distribution par groupes d'âge
- `/api/bmi_categories` - Distribution par catégories BMI
- `/api/pregnant_analysis` - Analyse des femmes enceintes
- `/api/top_glucose` - Top patients avec glucose élevé
- `/api/top_bmi` - Top patients avec BMI élevé
- `/api/high_risk_analysis` - Patients à haut risque
- `/api/glucose_analysis` - Analyse des niveaux de glucose
- `/api/age_glucose_correlation` - Corrélation âge-glucose
- `/api/redis_performance` - Performance Redis
- `/api/detailed_patient_analysis` - Analyses détaillées par plages

## Technologies Utilisées

### Backend
- Python 3.8+
- Flask (framework web)
- Redis (base de données NoSQL)
- Pandas (manipulation de données)

### Frontend
- HTML5, CSS3, JavaScript
- Bootstrap 5 (framework UI)
- Chart.js (graphiques interactifs)
- Font Awesome (icônes)

### Base de Données
- Redis Stack avec structures optimisées :
  - Sets pour les classifications
  - Sorted Sets pour les classements
  - Hashes pour les données patients
  - Intersections pour les analyses multicritères

## Analyses Réalisées

### Analyses de Base
- Distribution des patients par tranche d'âge (Jeune, Adulte, Mature, Senior)
- Classification par catégories BMI avec taux de diabète
- Analyse spécifique des femmes enceintes
- Identification des patients à haut risque (enceintes + obèses + diabétiques)

### Analyses Avancées
- Corrélation entre âge, glucose moyen et taux de diabète
- Segmentation fine des niveaux de glucose (Normal, Prédiabète, Diabète léger, Diabète sévère)
- Analyse détaillée par plages de BMI
- Classements des patients avec valeurs extrêmes
- Métriques de performance Redis

## Fonctionnalités Techniques

- Refresh automatique du dashboard toutes les 30 secondes
- Interface responsive adaptée mobile et desktop
- Gestion d'erreurs et reconnexion automatique Redis
- APIs REST documentées et testables
- Architecture modulaire et extensible
- Optimisation des requêtes Redis pour performance

## Dépannage

### Erreur de connexion Redis
- Vérifier que Redis Stack est démarré : `redis-cli ping`
- Vérifier le port par défaut : 6379
- Redémarrer Redis si nécessaire

### Dashboard vide ou erreurs
- S'assurer que les données ont été chargées via le notebook
- Vérifier les logs Flask dans le terminal
- Consulter la console développeur du navigateur (F12)

### Problèmes d'installation
- Vérifier la version Python : `python --version`
- Installer les dépendances : `pip install -r requirements.txt`
- Utiliser un environnement virtuel si nécessaire

## Performance

- Analyse en temps réel de 768 patients
- Réponse API moyenne < 50ms
- Support de milliers de requêtes simultanées
- Utilisation optimale de la mémoire Redis
- Cache intelligent avec hit ratio élevé

## Extensions Possibles

- Ajout de nouveaux datasets médicaux
- Intégration d'algorithmes de machine learning
- Notifications automatiques pour patients à risque
- Export des données et rapports
- Interface d'administration
- Authentification et gestion des utilisateurs

## Auteur

Projet développé pour l'analyse de données médicales avec Redis et visualisation web interactive.
