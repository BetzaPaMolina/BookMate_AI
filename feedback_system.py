"""
Sistema de Retroalimentación Inteligente para BookMate AI
Permite que el usuario califique recomendaciones y el sistema aprenda de ello
"""

import json
import os
from datetime import datetime
from collections import defaultdict

class FeedbackSystem:
    """
    Sistema que:
    1. Captura feedback del usuario (positivo/negativo/neutral)
    2. Ajusta scores de libros, emociones y contextos
    3. Explica cómo usa el feedback en futuras recomendaciones
    """
    
    def __init__(self, history_file='smart_history.json'):
        self.history_file = history_file
        self.feedback_file = 'feedback_data.json'
        self.load_feedback_data()
    
    def load_feedback_data(self):
        """Carga datos de feedback persistentes"""
        if os.path.exists(self.feedback_file):
            try:
                with open(self.feedback_file, 'r', encoding='utf-8') as f:
                    self.feedback_data = json.load(f)
            except:
                self.feedback_data = self.init_feedback_data()
        else:
            self.feedback_data = self.init_feedback_data()
    
    def init_feedback_data(self):
        """Inicializa estructura de feedback"""
        return {
            'book_ratings': defaultdict(lambda: {'positive': 0, 'negative': 0, 'neutral': 0}),
            'emotion_accuracy': defaultdict(lambda: {'correct': 0, 'incorrect': 0}),
            'context_effectiveness': defaultdict(lambda: {'helpful': 0, 'not_helpful': 0}),
            'total_feedback_count': 0,
            'learning_adjustments': []
        }
    
    def save_feedback_data(self):
        """Guarda feedback de manera persistente"""
        # Convertir defaultdicts a dicts normales
        save_data = {
            'book_ratings': dict(self.feedback_data['book_ratings']),
            'emotion_accuracy': dict(self.feedback_data['emotion_accuracy']),
            'context_effectiveness': dict(self.feedback_data['context_effectiveness']),
            'total_feedback_count': self.feedback_data['total_feedback_count'],
            'learning_adjustments': self.feedback_data['learning_adjustments'][-50:]  # Últimos 50
        }
        
        try:
            with open(self.feedback_file, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"❌ Error guardando feedback: {e}")
    
    def process_feedback(self, recommendation_data, feedback_type, user_comment=None):
        """
        Procesa feedback del usuario y ajusta el modelo
        
        Args:
            recommendation_data: Diccionario con la recomendación original
            feedback_type: 'positive', 'negative', 'neutral', 'wrong_emotion'
            user_comment: Comentario opcional del usuario
        
        Returns:
            dict con ajustes realizados y explicación
        """
        adjustments = {
            'timestamp': datetime.now().isoformat(),
            'feedback_type': feedback_type,
            'adjustments_made': []
        }
        
        libro = recommendation_data['libro']
        analisis = recommendation_data['analisis']
        book_id = f"{libro['titulo']}_{libro['autor']}"
        emotion = analisis['emotion']
        special_contexts = analisis.get('special_contexts', [])
        
        # 1. AJUSTAR SCORE DEL LIBRO
        if feedback_type == 'positive':
            adjustment = +0.5
            self.feedback_data['book_ratings'][book_id]['positive'] += 1
            adjustments['adjustments_made'].append(
                f"📈 Score de '{libro['titulo']}' aumentado +{adjustment}"
            )
        elif feedback_type == 'negative':
            adjustment = -0.3
            self.feedback_data['book_ratings'][book_id]['negative'] += 1
            adjustments['adjustments_made'].append(
                f"📉 Score de '{libro['titulo']}' reducido {adjustment}"
            )
        else:  # neutral
            adjustment = 0.0
            self.feedback_data['book_ratings'][book_id]['neutral'] += 1
        
        # 2. AJUSTAR PRECISIÓN EMOCIONAL
        if feedback_type == 'wrong_emotion':
            self.feedback_data['emotion_accuracy'][emotion]['incorrect'] += 1
            adjustments['adjustments_made'].append(
                f"⚠️ La emoción '{emotion}' no fue precisa. Necesito mejorar su detección."
            )
        else:
            self.feedback_data['emotion_accuracy'][emotion]['correct'] += 1
            adjustments['adjustments_made'].append(
                f"✅ Emoción '{emotion}' correctamente identificada"
            )
        
        # 3. AJUSTAR EFECTIVIDAD DE CONTEXTOS
        for context in special_contexts:
            if feedback_type == 'positive':
                self.feedback_data['context_effectiveness'][context]['helpful'] += 1
                adjustments['adjustments_made'].append(
                    f"🎯 Contexto '{context}' fue efectivo para tu recomendación"
                )
            elif feedback_type == 'negative':
                self.feedback_data['context_effectiveness'][context]['not_helpful'] += 1
                adjustments['adjustments_made'].append(
                    f"⚠️ Contexto '{context}' no fue útil, ajustando su peso"
                )
        
        # 4. REGISTRAR AJUSTE EN HISTORIAL
        self.feedback_data['total_feedback_count'] += 1
        adjustment_record = {
            'timestamp': datetime.now().isoformat(),
            'book': libro['titulo'],
            'emotion': emotion,
            'feedback': feedback_type,
            'adjustment_value': adjustment,
            'user_comment': user_comment
        }
        self.feedback_data['learning_adjustments'].append(adjustment_record)
        
        # 5. ACTUALIZAR SCORES EN smart_history.json
        self.update_history_scores(book_id, adjustment, emotion, feedback_type)
        
        # 6. GUARDAR
        self.save_feedback_data()
        
        # 7. GENERAR EXPLICACIÓN
        explanation = self.generate_learning_explanation(adjustments, feedback_type, libro['titulo'])
        adjustments['explanation'] = explanation
        
        return adjustments
    
    def update_history_scores(self, book_id, adjustment, emotion, feedback_type):
        """Actualiza scores en smart_history.json según feedback"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    history = json.load(f)
                
                # Ajustar score del libro
                if 'book_scores' not in history:
                    history['book_scores'] = {}
                
                current_score = history['book_scores'].get(book_id, 0.0)
                history['book_scores'][book_id] = current_score + adjustment
                
                # Ajustar preferencias emocionales
                if 'preferences' not in history:
                    history['preferences'] = {}
                
                if feedback_type == 'positive':
                    history['preferences'][emotion] = history['preferences'].get(emotion, 0.0) + 0.3
                elif feedback_type == 'negative':
                    history['preferences'][emotion] = history['preferences'].get(emotion, 0.0) - 0.2
                
                # Guardar
                with open(self.history_file, 'w', encoding='utf-8') as f:
                    json.dump(history, f, ensure_ascii=False, indent=2)
                
                print(f"✅ Scores actualizados en {self.history_file}")
            
        except Exception as e:
            print(f"❌ Error actualizando scores: {e}")
    
    def generate_learning_explanation(self, adjustments, feedback_type, book_title):
        """Genera explicación clara de cómo el sistema aprendió"""
        
        if feedback_type == 'positive':
            explanation = f"✅ **¡Gracias por tu feedback positivo!**\n\n"
            explanation += f"He aprendido que '{book_title}' es una buena opción para situaciones similares.\n\n"
            explanation += "**Ajustes realizados:**\n"
            for adj in adjustments['adjustments_made']:
                explanation += f"  • {adj}\n"
            explanation += "\n💡 En futuras recomendaciones similares, priorizaré este tipo de libro."
        
        elif feedback_type == 'negative':
            explanation = f"⚠️ **Entendido, tomaré nota.**\n\n"
            explanation += f"He aprendido que '{book_title}' no fue la mejor opción para ti.\n\n"
            explanation += "**Ajustes realizados:**\n"
            for adj in adjustments['adjustments_made']:
                explanation += f"  • {adj}\n"
            explanation += "\n💡 Reduciré la probabilidad de recomendar este libro en contextos similares."
        
        elif feedback_type == 'wrong_emotion':
            explanation = f"🔍 **Necesito mejorar mi detección emocional.**\n\n"
            explanation += "He registrado que interpreté mal tu estado de ánimo.\n\n"
            explanation += "**Ajustes realizados:**\n"
            for adj in adjustments['adjustments_made']:
                explanation += f"  • {adj}\n"
            explanation += "\n💡 Trabajaré en detectar mejor este tipo de emociones."
        
        else:  # neutral
            explanation = f"📝 **Feedback registrado.**\n\n"
            explanation += "He anotado tu respuesta neutral. Esto me ayuda a calibrar mis recomendaciones.\n\n"
            explanation += "💡 Seguiré aprendiendo de tus preferencias."
        
        return explanation
    
    def get_feedback_stats(self):
        """Retorna estadísticas de feedback para mostrar al usuario"""
        
        total = self.feedback_data['total_feedback_count']
        
        # Calcular libros mejor y peor calificados
        book_rankings = []
        for book_id, ratings in self.feedback_data['book_ratings'].items():
            score = ratings['positive'] - ratings['negative']
            total_ratings = ratings['positive'] + ratings['negative'] + ratings['neutral']
            book_rankings.append({
                'book': book_id.split('_')[0],  # Solo el título
                'score': score,
                'total_ratings': total_ratings,
                'positive': ratings['positive'],
                'negative': ratings['negative']
            })
        
        book_rankings.sort(key=lambda x: x['score'], reverse=True)
        
        # Precisión emocional
        emotion_accuracy = []
        for emotion, accuracy in self.feedback_data['emotion_accuracy'].items():
            total_checks = accuracy['correct'] + accuracy['incorrect']
            if total_checks > 0:
                precision = (accuracy['correct'] / total_checks) * 100
                emotion_accuracy.append({
                    'emotion': emotion,
                    'precision': precision,
                    'total_checks': total_checks
                })
        
        emotion_accuracy.sort(key=lambda x: x['precision'], reverse=True)
        
        # Últimos ajustes
        recent_adjustments = self.feedback_data['learning_adjustments'][-5:]
        
        return {
            'total_feedback': total,
            'top_books': book_rankings[:5],
            'worst_books': book_rankings[-5:] if len(book_rankings) > 5 else [],
            'emotion_accuracy': emotion_accuracy,
            'recent_adjustments': recent_adjustments,
            'context_effectiveness': dict(self.feedback_data['context_effectiveness'])
        }
    
    def get_confidence_explanation(self, libro_titulo):
        """Explica por qué el sistema tiene cierta confianza en un libro"""
        book_id = None
        for bid in self.feedback_data['book_ratings'].keys():
            if libro_titulo in bid:
                book_id = bid
                break
        
        if not book_id:
            return "Este es un libro nuevo para el sistema. No tengo feedback previo."
        
        ratings = self.feedback_data['book_ratings'][book_id]
        total = ratings['positive'] + ratings['negative'] + ratings['neutral']
        
        if total == 0:
            return "No he recibido feedback sobre este libro aún."
        
        positive_rate = (ratings['positive'] / total) * 100
        
        explanation = f"He recomendado este libro {total} vez(ces) antes:\n"
        explanation += f"  ✅ Feedback positivo: {ratings['positive']}\n"
        explanation += f"  ⚠️ Feedback negativo: {ratings['negative']}\n"
        explanation += f"  📝 Feedback neutral: {ratings['neutral']}\n"
        explanation += f"\n💡 Tasa de satisfacción: {positive_rate:.0f}%"
        
        return explanation


# ========================
# EJEMPLO DE USO
# ========================

if __name__ == "__main__":
    feedback_sys = FeedbackSystem()
    
    # Simular una recomendación
    recommendation = {
        'libro': {
            'titulo': 'Pedro Páramo',
            'autor': 'Juan Rulfo'
        },
        'analisis': {
            'emotion': 'triste',
            'emotion_confidence': 0.85,
            'score': 6.5,
            'special_contexts': ['catarsis', 'intenso']
        }
    }
    
    print("=" * 80)
    print("SIMULACIÓN DE FEEDBACK")
    print("=" * 80)
    
    # Caso 1: Feedback positivo
    print("\n1️⃣ Usuario da feedback POSITIVO")
    result = feedback_sys.process_feedback(
        recommendation, 
        'positive',
        user_comment="Me encantó, justo lo que necesitaba"
    )
    print(result['explanation'])
    
    print("\n" + "=" * 80)
    
    # Caso 2: Feedback negativo
    print("\n2️⃣ Usuario da feedback NEGATIVO")
    result = feedback_sys.process_feedback(
        recommendation, 
        'negative',
        user_comment="No era lo que buscaba"
    )
    print(result['explanation'])
    
    print("\n" + "=" * 80)
    
    # Caso 3: Emoción incorrecta
    print("\n3️⃣ Usuario indica que la EMOCIÓN fue mal detectada")
    result = feedback_sys.process_feedback(
        recommendation, 
        'wrong_emotion',
        user_comment="No estaba triste, estaba reflexivo"
    )
    print(result['explanation'])
    
    print("\n" + "=" * 80)
    
    # Mostrar estadísticas
    print("\n📊 ESTADÍSTICAS DE APRENDIZAJE")
    print("=" * 80)
    stats = feedback_sys.get_feedback_stats()
    print(f"\nTotal de feedback recibido: {stats['total_feedback']}")
    
    if stats['top_books']:
        print("\n📚 Libros mejor calificados:")
        for book in stats['top_books']:
            print(f"  • {book['book']}: +{book['positive']} / -{book['negative']}")
    
    if stats['emotion_accuracy']:
        print("\n🎭 Precisión emocional:")
        for emotion in stats['emotion_accuracy']:
            print(f"  • {emotion['emotion']}: {emotion['precision']:.0f}% ({emotion['total_checks']} checks)")
    
    print("\n💡 El sistema ahora sabe:")
    print("  1. Qué libros funcionan mejor para cada emoción")
    print("  2. Qué tan precisa es su detección emocional")
    print("  3. Qué contextos son más efectivos")
    print("\n✅ Estos ajustes se aplican en tiempo real a futuras recomendaciones")