from flask import Flask, render_template, jsonify
import redis
import pandas as pd
import json

app = Flask(__name__)

# Configuration Redis
def get_redis_connection():
    try:
        r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
        r.ping()  # Test de connexion
        return r
    except redis.ConnectionError:
        print("Erreur: Impossible de se connecter à Redis")
        return None

# Routes principales
@app.route('/')
def dashboard():
    """Route principale du dashboard original"""
    return render_template('dashboard.html')

@app.route('/enhanced')
def enhanced_dashboard():
    """Dashboard amélioré avec analyses supplémentaires"""
    return render_template('dashboard_enhanced.html')

@app.route('/api')
def api_test():
    """Page de test des APIs"""
    return render_template('api_test.html')

# API Endpoints
@app.route('/api/stats')
def get_stats():
    """API pour les statistiques générales"""
    r = get_redis_connection()
    if not r:
        return jsonify({'error': 'Redis connection failed'})
    
    try:
        total_patients = r.dbsize() // 10  # Approximation basée sur le nombre de clés
        diabetic_patients = r.scard('patients:diabetes')
        non_diabetic_patients = total_patients - diabetic_patients
        diabetes_rate = round((diabetic_patients / total_patients * 100), 1) if total_patients > 0 else 0
        
        stats = {
            'total_patients': total_patients,
            'diabetic_patients': diabetic_patients,
            'non_diabetic_patients': non_diabetic_patients,
            'diabetes_rate': diabetes_rate
        }
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/age_groups')
def get_age_groups():
    """API pour les groupes d'âge"""
    r = get_redis_connection()
    if not r:
        return jsonify({'error': 'Redis connection failed'})
    
    try:
        age_groups = ['Jeune', 'Adulte', 'Mature', 'Senior']
        data = []
        
        for group in age_groups:
            total = r.scard(f'age_group:{group}')
            if total > 0:
                # Intersection pour diabétiques
                r.sinterstore(f'temp:diabetic_age_{group}', 'patients:diabetes', f'age_group:{group}')
                diabetic = r.scard(f'temp:diabetic_age_{group}')
                r.delete(f'temp:diabetic_age_{group}')
                
                non_diabetic = total - diabetic
                rate = (diabetic / total * 100) if total > 0 else 0
                
                data.append({
                    'age_group': group,
                    'total': total,
                    'diabetic': diabetic,
                    'non_diabetic': non_diabetic,
                    'rate': round(rate, 1)
                })
        
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/bmi_categories')
def get_bmi_categories():
    """API pour les catégories BMI"""
    r = get_redis_connection()
    if not r:
        return jsonify({'error': 'Redis connection failed'})
    
    try:
        bmi_categories = ['Insuffisant', 'Normal', 'Surpoids', 'Obèse']
        data = []
        
        for category in bmi_categories:
            total = r.scard(f'bmi_category:{category}')
            if total > 0:
                # Intersection pour diabétiques
                r.sinterstore(f'temp:diabetic_bmi_{category}', 'patients:diabetes', f'bmi_category:{category}')
                diabetic = r.scard(f'temp:diabetic_bmi_{category}')
                r.delete(f'temp:diabetic_bmi_{category}')
                
                non_diabetic = total - diabetic
                rate = (diabetic / total * 100) if total > 0 else 0
                
                data.append({
                    'category': category,
                    'total': total,
                    'diabetic': diabetic,
                    'non_diabetic': non_diabetic,
                    'rate': round(rate, 1)
                })
        
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/pregnant_analysis')
def get_pregnant_analysis():
    """API pour l'analyse des femmes enceintes"""
    r = get_redis_connection()
    if not r:
        return jsonify({'error': 'Redis connection failed'})
    
    try:
        # Créer un set temporaire pour les femmes enceintes
        all_patient_keys = r.keys('patient:*')
        r.delete('temp:pregnant_women')
        
        for patient_key in all_patient_keys:
            patient_data = r.hgetall(patient_key)
            pregnancies = patient_data.get('Pregnancies', '0')
            try:
                if int(pregnancies) > 0:
                    patient_id = patient_key.split(':')[1]
                    r.sadd('temp:pregnant_women', patient_id)
            except:
                continue
        
        total_pregnant = r.scard('temp:pregnant_women')
        
        if total_pregnant > 0:
            # Intersection avec diabétiques
            r.sinterstore('temp:pregnant_diabetic', 'temp:pregnant_women', 'patients:diabetes')
            diabetic_pregnant = r.scard('temp:pregnant_diabetic')
            non_diabetic_pregnant = total_pregnant - diabetic_pregnant
            diabetes_rate = round((diabetic_pregnant / total_pregnant * 100), 1)
            
            # Nettoyage
            r.delete('temp:pregnant_women')
            r.delete('temp:pregnant_diabetic')
        else:
            diabetic_pregnant = 0
            non_diabetic_pregnant = 0
            diabetes_rate = 0
        
        data = {
            'total_pregnant': total_pregnant,
            'diabetic_pregnant': diabetic_pregnant,
            'non_diabetic_pregnant': non_diabetic_pregnant,
            'diabetes_rate': diabetes_rate
        }
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/top_glucose')
def get_top_glucose():
    """API pour le top des patients avec glucose élevé"""
    r = get_redis_connection()
    if not r:
        return jsonify({'error': 'Redis connection failed'})
    
    try:
        # Récupérer les 10 premiers patients avec glucose le plus élevé
        top_patients = r.zrevrange('patients:by_glucose', 0, 9, withscores=True)
        
        data = []
        for i, (patient_id, glucose) in enumerate(top_patients, 1):
            # Vérifier si diabétique
            is_diabetic = r.sismember('patients:diabetes', patient_id)
            
            data.append({
                'rank': i,
                'patient_id': patient_id,
                'glucose': glucose,
                'outcome': 'Diabétique' if is_diabetic else 'Non-diabétique'
            })
        
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/top_bmi')
def get_top_bmi():
    """API pour le top des patients avec BMI élevé"""
    r = get_redis_connection()
    if not r:
        return jsonify({'error': 'Redis connection failed'})
    
    try:
        # Récupérer les 10 premiers patients avec BMI le plus élevé
        top_patients = r.zrevrange('patients:by_bmi', 0, 9, withscores=True)
        
        data = []
        for i, (patient_id, bmi) in enumerate(top_patients, 1):
            # Vérifier si diabétique
            is_diabetic = r.sismember('patients:diabetes', patient_id)
            
            data.append({
                'rank': i,
                'patient_id': patient_id,
                'bmi': round(bmi, 1),
                'outcome': 'Diabétique' if is_diabetic else 'Non-diabétique'
            })
        
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/high_risk_analysis')
def get_high_risk_analysis():
    """API pour l'analyse des patients à haut risque"""
    r = get_redis_connection()
    if not r:
        return jsonify({'error': 'Redis connection failed'})
    
    try:
        # Créer sets temporaires
        all_patient_keys = r.keys('patient:*')
        r.delete('temp:pregnant_women')
        
        for patient_key in all_patient_keys:
            patient_data = r.hgetall(patient_key)
            pregnancies = patient_data.get('Pregnancies', '0')
            try:
                if int(pregnancies) > 0:
                    patient_id = patient_key.split(':')[1]
                    r.sadd('temp:pregnant_women', patient_id)
            except:
                continue
        
        # Triple intersection
        r.sinterstore('temp:high_risk_women', 
                     'temp:pregnant_women', 
                     'bmi_category:Obèse', 
                     'patients:diabetes')
        
        high_risk_count = r.scard('temp:high_risk_women')
        
        # Nettoyage
        r.delete('temp:pregnant_women')
        r.delete('temp:high_risk_women')
        
        return jsonify({'high_risk_count': high_risk_count})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/glucose_analysis')
def get_glucose_analysis():
    """API pour l'analyse des niveaux de glucose"""
    r = get_redis_connection()
    if not r:
        return jsonify({'error': 'Redis connection failed'})
    
    try:
        glucose_levels = ['Normal', 'Prédiabète', 'Diabète']
        data = []
        
        for level in glucose_levels:
            total = r.scard(f'glucose_level:{level}')
            if total > 0:
                # Intersection pour diabétiques
                r.sinterstore(f'temp:diabetic_glucose_{level}', 'patients:diabetes', f'glucose_level:{level}')
                diabetic = r.scard(f'temp:diabetic_glucose_{level}')
                r.delete(f'temp:diabetic_glucose_{level}')
                
                rate = (diabetic / total * 100) if total > 0 else 0
                
                data.append({
                    'level': level,
                    'total': total,
                    'diabetic': diabetic,
                    'non_diabetic': total - diabetic,
                    'rate': round(rate, 1)
                })
        
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/age_glucose_correlation')
def get_age_glucose_correlation():
    """API pour la corrélation âge-glucose"""
    r = get_redis_connection()
    if not r:
        return jsonify({'error': 'Redis connection failed'})
    
    try:
        age_groups = ['Jeune', 'Adulte', 'Mature', 'Senior']
        data = []
        
        for group in age_groups:
            patient_ids = r.smembers(f'age_group:{group}')
            if patient_ids:
                glucose_values = []
                diabetic_count = 0
                
                for patient_id in patient_ids:
                    patient_data = r.hgetall(f'patient:{patient_id}')
                    try:
                        glucose = float(patient_data.get('Glucose', 0))
                        glucose_values.append(glucose)
                        if patient_data.get('Outcome') == '1':
                            diabetic_count += 1
                    except:
                        continue
                
                if glucose_values:
                    avg_glucose = sum(glucose_values) / len(glucose_values)
                    data.append({
                        'age_group': group,
                        'avg_glucose': round(avg_glucose, 1),
                        'patient_count': len(glucose_values),
                        'diabetic_count': diabetic_count,
                        'diabetes_rate': round((diabetic_count / len(glucose_values) * 100), 1)
                    })
        
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/redis_performance')
def get_redis_performance():
    """API pour les statistiques de performance Redis"""
    r = get_redis_connection()
    if not r:
        return jsonify({'error': 'Redis connection failed'})
    
    try:
        info = r.info()
        memory_info = r.info('memory')
        
        data = {
            'total_keys': r.dbsize(),
            'used_memory_human': memory_info.get('used_memory_human', '0B'),
            'used_memory_peak_human': memory_info.get('used_memory_peak_human', '0B'),
            'connected_clients': info.get('connected_clients', 0),
            'total_commands_processed': info.get('total_commands_processed', 0),
            'keyspace_hits': info.get('keyspace_hits', 0),
            'keyspace_misses': info.get('keyspace_misses', 0),
            'redis_version': info.get('redis_version', 'Unknown')
        }
        
        # Calculer le hit ratio
        hits = data['keyspace_hits']
        misses = data['keyspace_misses']
        if hits + misses > 0:
            data['hit_ratio'] = round((hits / (hits + misses)) * 100, 2)
        else:
            data['hit_ratio'] = 0
            
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/detailed_patient_analysis')
def get_detailed_patient_analysis():
    """API pour l'analyse détaillée des patients"""
    r = get_redis_connection()
    if not r:
        return jsonify({'error': 'Redis connection failed'})
    
    try:
        # Analyse par plages de glucose
        glucose_ranges = [
            {'name': 'Normal', 'min': 0, 'max': 99},
            {'name': 'Prédiabète', 'min': 100, 'max': 125},
            {'name': 'Diabète léger', 'min': 126, 'max': 180},
            {'name': 'Diabète sévère', 'min': 181, 'max': 999}
        ]
        
        glucose_analysis = []
        for range_info in glucose_ranges:
            patient_ids = r.zrangebyscore('patients:by_glucose', range_info['min'], range_info['max'])
            diabetic_count = 0
            
            for patient_id in patient_ids:
                if r.sismember('patients:diabetes', patient_id):
                    diabetic_count += 1
            
            glucose_analysis.append({
                'range': range_info['name'],
                'total': len(patient_ids),
                'diabetic': diabetic_count,
                'non_diabetic': len(patient_ids) - diabetic_count,
                'rate': round((diabetic_count / len(patient_ids) * 100), 1) if len(patient_ids) > 0 else 0
            })
        
        # Analyse par plages de BMI
        bmi_ranges = [
            {'name': 'Sous-poids', 'min': 0, 'max': 18.4},
            {'name': 'Normal', 'min': 18.5, 'max': 24.9},
            {'name': 'Surpoids', 'min': 25, 'max': 29.9},
            {'name': 'Obésité', 'min': 30, 'max': 999}
        ]
        
        bmi_analysis = []
        for range_info in bmi_ranges:
            patient_ids = r.zrangebyscore('patients:by_bmi', range_info['min'], range_info['max'])
            diabetic_count = 0
            
            for patient_id in patient_ids:
                if r.sismember('patients:diabetes', patient_id):
                    diabetic_count += 1
            
            bmi_analysis.append({
                'range': range_info['name'],
                'total': len(patient_ids),
                'diabetic': diabetic_count,
                'non_diabetic': len(patient_ids) - diabetic_count,
                'rate': round((diabetic_count / len(patient_ids) * 100), 1) if len(patient_ids) > 0 else 0
            })
        
        return jsonify({
            'glucose_analysis': glucose_analysis,
            'bmi_analysis': bmi_analysis
        })
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)