# Dashboard Flask - Analyse Diabète avec Redis

Ce projet contient un dashboard web interactif pour visualiser les analyses des données de diabète stockées dans Redis.

##  Fonctionnalités

- **Statistiques générales** : Nombre total de patients, taux de diabète, moyennes
- **Analyses par groupe d'âge** : Distribution des patients diabétiques par tranche d'âge
- **Analyses par BMI** : Répartition selon les catégories d'indice de masse corporelle
- **Analyse des femmes enceintes** : Taux de diabète chez les femmes ayant eu des grossesses
- **Top patients** : Classements par glucose et BMI les plus élevés
- **Patients à haut risque** : Identification des cas critiques (enceintes + obèses + diabétiques)

##  Installation et Démarrage

### Prérequis
1. **Redis Stack** doit être installé et en cours d'exécution sur le port 6379
2. **Python 3.8+** installé
3. Les **données diabète** doivent être chargées dans Redis (via le notebook)

### Étape 1 : Installer les dépendances
```bash
pip install -r requirements.txt
```

### Étape 2 : Vérifier Redis
Assurez-vous que Redis Stack est démarré :
```bash
redis-stack-server
```

### Étape 3 : Démarrer le dashboard
```bash
python start_dashboard.py
```

Ou directement :
```bash
python app.py
```

### Étape 4 : Accéder au dashboard
Ouvrez votre navigateur à l'adresse : **http://localhost:5000**

## Structure du Dashboard

### Section 1 : Statistiques Générales
- Total des patients
- Nombre de diabétiques
- Âge moyen
- Glucose moyen

### Section 2 : Graphiques Interactifs
- **Graphique en secteurs** : Distribution par groupe d'âge
- **Graphique en barres** : Distribution par catégorie BMI

### Section 3 : Analyses Spécialisées
- **Femmes enceintes** : Graphique + statistiques
- **Top 5 Glucose élevé** : Tableau avec détails
- **Top 5 BMI élevé** : Tableau avec détails

### Section 4 : Alerte Haut Risque
- Nombre de patientes à surveiller (enceintes + obèses + diabétiques)

## 🔧 API Endpoints

Le dashboard expose plusieurs endpoints API :

- `GET /api/stats` - Statistiques générales
- `GET /api/age_groups` - Données par groupe d'âge
- `GET /api/bmi_categories` - Données par catégorie BMI
- `GET /api/top_glucose` - Top patients glucose élevé
- `GET /api/top_bmi` - Top patients BMI élevé
- `GET /api/pregnant_analysis` - Analyse femmes enceintes
- `GET /api/high_risk_analysis` - Analyse haut risque

##  Structure du Projet

```
Redis-BDD/
├── app.py                      # Application Flask principale
├── start_dashboard.py          # Script de démarrage
├── requirements.txt            # Dépendances Python
├── templates/
│   └── dashboard.html         # Interface web du dashboard
└── static/
    └── css/
        └── dashboard.css      # Styles personnalisés
```

## Technologies Utilisées

- **Backend** : Flask (Python)
- **Base de données** : Redis
- **Frontend** : HTML5, CSS3, JavaScript
- **Graphiques** : Chart.js
- **UI Framework** : Bootstrap 5
- **Icônes** : Font Awesome

## 🔄 Mise à Jour des Données

Le dashboard se met à jour automatiquement toutes les 30 secondes. Vous pouvez aussi actualiser manuellement la page.

##  Dépannage

### Problème : "Redis connection failed"
- Vérifiez que Redis Stack est démarré : `redis-cli ping`
- Vérifiez le port (6379 par défaut)
- Redémarrez Redis si nécessaire

### Problème : Données vides
- Assurez-vous d'avoir exécuté le notebook d'analyse diabetes
- Vérifiez que les données sont bien dans Redis : `redis-cli DBSIZE`

### Problème : Flask ne démarre pas
- Installez les dépendances : `pip install -r requirements.txt`
- Vérifiez la version Python (3.8+ requis)

## 📈 Utilisation Avancée

Pour personnaliser le dashboard :
1. Modifiez `app.py` pour ajouter de nouveaux endpoints
2. Éditez `dashboard.html` pour modifier l'interface
3. Ajustez `dashboard.css` pour personnaliser le style

##  Support

En cas de problème, vérifiez :
1. La connexion Redis
2. Les logs Flask dans le terminal
3. La console du navigateur (F12) pour les erreurs JavaScript