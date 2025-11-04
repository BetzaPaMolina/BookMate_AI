import json
import os
from datetime import datetime
from collections import defaultdict
import re

class SmartRecommender:
    """
    Sistema de recomendación inteligente MEJORADO con:
    - Más emociones detectables
    - Análisis de contextos complejos
    - Mejor manejo de contradicciones
    """
    
    def __init__(self):
        self.history_file = 'smart_history.json'
        self.session_recommended = set()
        self.conversation_context = []
        
        self.history = self.load_history()
        self.books = self.build_library()
        
        # Mapeo emocional EXPANDIDO
        self.emotion_keywords = {
            'triste': ['triste', 'melancólico', 'deprimido', 'solo', 'nostálgico', 'decaído', 'desanimado', 'vacía', 'vacío', 'pérdida', 'duelo'],
            'feliz': ['feliz', 'alegre', 'contento', 'emocionado', 'optimista', 'energético', 'bien', 'genial'],
            'pensativo': ['pensativo', 'reflexivo', 'filosófico', 'pensar', 'reflexionar', 'meditar', 'profundo'],
            'motivado': ['motivado', 'inspirado', 'determinado', 'energía', 'productivo', 'cambio', 'transformar'],
            'aburrido': ['aburrido', 'cansado', 'hastiado', 'monótono', 'desconectar', 'rutina'],
            'ansioso': ['ansioso', 'nervioso', 'preocupado', 'estresado', 'inquieto', 'molesta', 'molesto', 'enojada', 'enojado', 'frustrado', 'ira'],
            'curioso': ['curioso', 'interesado', 'aprender', 'descubrir', 'explorar', 'sorprender', 'sorpréndeme'],
            'romántico': ['romántico', 'amor', 'sentimental', 'pasión', 'enamorado'],
            'confundido': ['confundido', 'perdido', 'no sé', 'inseguro', 'sin sentido'],
            'nostálgico': ['nostálgico', 'añoranza', 'recuerdos', 'pasado', 'era']
        }
        
        # Contextos especiales (frases que cambian la recomendación)
        self.special_contexts = {
            'esperanza': ['esperanza', 'superar', 'salir', 'mejor', 'luz'],
            'catarsis': ['llorar', 'profundizar', 'sentir', 'acompañe', 'sumergir'],
            'intenso': ['fuerte', 'intenso', 'profundo', 'transforme'],
            'no_empeorar': ['no quiero', 'sin', 'evitar', 'no me gusta', 'menos']
        }
        
        print("✅ SmartRecommender MEJORADO inicializado")
        print(f"📊 Historial: {len(self.history.get('interactions', []))} interacciones previas")
    
    def build_library(self):
        """Biblioteca con clasificación emocional expandida"""
        return {
            "filosofia": [
                {
                    "titulo": "Memorias del subsuelo",
                    "autor": "Fiódor Dostoievski",
                    "descripcion": "Un monólogo visceral sobre la alienación, la soledad y la naturaleza humana",
                    "color": "#6B9BC4",
                    "emoji": "🧠",
                    "emociones": ["pensativo", "triste", "confundido"],
                    "impacto": "catártico",
                    "intensidad": "alta",
                    "temas": ["existencial", "introspección", "soledad"]
                },
                {
                    "titulo": "Crimen y castigo",
                    "autor": "Fiódor Dostoievski",
                    "descripcion": "Exploración profunda de la culpa, la moral y la redención a través del sufrimiento",
                    "color": "#9B8BC4",
                    "emoji": "⚖️",
                    "emociones": ["pensativo", "ansioso", "confundido"],
                    "impacto": "reflexivo",
                    "intensidad": "alta",
                    "temas": ["moral", "culpa", "redención"]
                },
                {
                    "titulo": "Siddharta",
                    "autor": "Hermann Hesse",
                    "descripcion": "Un viaje de autodescubrimiento que ofrece paz y sabiduría",
                    "color": "#E0C47A",
                    "emoji": "🕉️",
                    "emociones": ["pensativo", "curioso", "confundido"],
                    "impacto": "esperanzador",
                    "intensidad": "media",
                    "temas": ["búsqueda", "espiritualidad", "paz"]
                },
                {
                    "titulo": "Demian",
                    "autor": "Hermann Hesse",
                    "descripcion": "Historia de crecimiento personal y descubrimiento del verdadero yo",
                    "color": "#7BC4A4",
                    "emoji": "🌱",
                    "emociones": ["pensativo", "motivado", "confundido"],
                    "impacto": "transformador",
                    "intensidad": "media",
                    "temas": ["identidad", "crecimiento", "transformación"]
                }
            ],
            "romance": [
                {
                    "titulo": "María",
                    "autor": "Jorge Isaacs",
                    "descripcion": "Amor imposible y melancolía profunda en el romanticismo latinoamericano",
                    "color": "#E07A7A",
                    "emoji": "💔",
                    "emociones": ["triste", "romántico", "nostálgico"],
                    "impacto": "catártico",
                    "intensidad": "alta",
                    "temas": ["amor", "pérdida", "melancolía"]
                },
                {
                    "titulo": "Jane Eyre",
                    "autor": "Charlotte Brontë",
                    "descripcion": "Historia de amor y superación con una protagonista fuerte e independiente",
                    "color": "#D4A5C4",
                    "emoji": "💝",
                    "emociones": ["romántico", "motivado", "ansioso"],
                    "impacto": "esperanzador",
                    "intensidad": "media",
                    "temas": ["amor", "independencia", "fortaleza"]
                },
                {
                    "titulo": "Anna Karenina",
                    "autor": "León Tolstói",
                    "descripcion": "Tragedia sobre amor, pasión y las convenciones sociales",
                    "color": "#E07AA4",
                    "emoji": "🌹",
                    "emociones": ["triste", "pensativo", "romántico"],
                    "impacto": "reflexivo",
                    "intensidad": "alta",
                    "temas": ["amor", "sociedad", "tragedia"]
                }
            ],
            "distopia": [
                {
                    "titulo": "1984",
                    "autor": "George Orwell",
                    "descripcion": "Crítica devastadora al totalitarismo y la manipulación del pensamiento",
                    "color": "#6B7BC4",
                    "emoji": "👁️",
                    "emociones": ["pensativo", "ansioso", "confundido"],
                    "impacto": "reflexivo",
                    "intensidad": "alta",
                    "temas": ["control", "vigilancia", "opresión"]
                },
                {
                    "titulo": "Fahrenheit 451",
                    "autor": "Ray Bradbury",
                    "descripcion": "Sobre la censura, la quema de libros y la importancia del pensamiento libre",
                    "color": "#E0C47A",
                    "emoji": "🔥",
                    "emociones": ["pensativo", "motivado", "ansioso"],
                    "impacto": "reflexivo",
                    "intensidad": "alta",
                    "temas": ["censura", "libertad", "conocimiento"]
                },
                {
                    "titulo": "Un mundo feliz",
                    "autor": "Aldous Huxley",
                    "descripcion": "Distopía sobre control social mediante la felicidad artificial",
                    "color": "#7BC4A4",
                    "emoji": "💊",
                    "emociones": ["pensativo", "curioso", "confundido"],
                    "impacto": "reflexivo",
                    "intensidad": "media",
                    "temas": ["control", "felicidad", "sociedad"]
                }
            ],
            "clasica": [
                {
                    "titulo": "Los miserables",
                    "autor": "Victor Hugo",
                    "descripcion": "Épica historia de redención, justicia social y esperanza en medio del sufrimiento",
                    "color": "#9B8BC4",
                    "emoji": "⚜️",
                    "emociones": ["triste", "motivado", "pensativo"],
                    "impacto": "esperanzador",
                    "intensidad": "alta",
                    "temas": ["redención", "justicia", "esperanza"]
                },
                {
                    "titulo": "Los hermanos Karamázov",
                    "autor": "Fiódor Dostoievski",
                    "descripcion": "Obra maestra sobre fe, duda, moralidad y conflictos familiares profundos",
                    "color": "#6B9BC4",
                    "emoji": "👥",
                    "emociones": ["pensativo", "triste", "ansioso"],
                    "impacto": "reflexivo",
                    "intensidad": "alta",
                    "temas": ["fe", "moral", "familia"]
                }
            ],
            "realismo_magico": [
                {
                    "titulo": "Pedro Páramo",
                    "autor": "Juan Rulfo",
                    "descripcion": "Viaje entre la vida y la muerte que explora el vacío, la memoria y los fantasmas del pasado",
                    "color": "#9B8BC4",
                    "emoji": "👻",
                    "emociones": ["triste", "pensativo", "confundido"],
                    "impacto": "catártico",
                    "intensidad": "alta",
                    "temas": ["muerte", "vacío", "memoria"]
                }
            ],
            "motivacional": [
                {
                    "titulo": "El líder mentor",
                    "autor": "Tony Dungy",
                    "descripcion": "Liderazgo, propósito y cómo encontrar esperanza en momentos difíciles",
                    "color": "#7BC4A4",
                    "emoji": "💼",
                    "emociones": ["motivado", "triste"],
                    "impacto": "esperanzador",
                    "intensidad": "baja",
                    "temas": ["liderazgo", "propósito", "superación"]
                }
            ],
            "humor": [
                {
                    "titulo": "Soy un gato",
                    "autor": "Natsume Sōseki",
                    "descripcion": "Sátira irónica de la sociedad desde la perspectiva de un gato observador",
                    "color": "#E0C47A",
                    "emoji": "🐱",
                    "emociones": ["aburrido", "curioso"],
                    "impacto": "entretenimiento",
                    "intensidad": "baja",
                    "temas": ["humor", "sociedad", "crítica"]
                }
            ],
            "aventura": [
                {
                    "titulo": "La Odisea",
                    "autor": "Homero",
                    "descripcion": "Épica aventura de regreso a casa llena de desafíos y descubrimientos",
                    "color": "#6B9BC4",
                    "emoji": "⛵",
                    "emociones": ["feliz", "curioso", "motivado"],
                    "impacto": "entretenimiento",
                    "intensidad": "media",
                    "temas": ["aventura", "hogar", "heroísmo"]
                },
                {
                    "titulo": "Moby Dick",
                    "autor": "Herman Melville",
                    "descripcion": "Obsesión destructiva y aventura filosófica en alta mar",
                    "color": "#6B7BC4",
                    "emoji": "🐋",
                    "emociones": ["pensativo", "curioso", "ansioso"],
                    "impacto": "reflexivo",
                    "intensidad": "alta",
                    "temas": ["obsesión", "naturaleza", "destino"]
                }
            ]
        }
    
    def load_history(self):
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Convertir a defaultdict
                    if 'preferences' in data:
                        data['preferences'] = defaultdict(float, data['preferences'])
                    if 'book_scores' in data:
                        data['book_scores'] = defaultdict(float, data['book_scores'])
                    return data
            except:
                pass
        return {
            'interactions': [],
            'preferences': defaultdict(float),
            'book_scores': defaultdict(float)
        }
    
    def save_history(self):
        save_data = {
            'interactions': self.history['interactions'][-100:],
            'preferences': dict(self.history['preferences']),
            'book_scores': dict(self.history['book_scores'])
        }
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"❌ Error guardando: {e}")
    
    def detect_special_context(self, text):
        """Detecta contextos especiales que modifican la recomendación"""
        text_lower = text.lower()
        contexts = []
        
        for context_name, keywords in self.special_contexts.items():
            if any(keyword in text_lower for keyword in keywords):
                contexts.append(context_name)
        
        return contexts
    
    def analyze_emotion(self, text):
        """Análisis emocional mejorado con contexto"""
        text_lower = text.lower()
        scores = defaultdict(float)
        
        # Análisis por keywords
        for emotion, keywords in self.emotion_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    scores[emotion] += 1.0
        
        # Contexto conversacional
        if self.conversation_context:
            prev_emotion = self.conversation_context[-1].get('emotion')
            if prev_emotion and prev_emotion in scores:
                scores[prev_emotion] += 0.3
        
        # Detectar negaciones y contradicciones
        # Caso: "Estoy feliz pero quiero llorar"
        if re.search(r'\bfeliz\b.*\b(llorar|triste|melanc)', text_lower):
            scores['triste'] += 2.0  # Priorizar la tristeza
            scores['feliz'] = max(0, scores['feliz'] - 1.0)
        
        # Caso: "Estoy triste pero no quiero empeorar"
        if re.search(r'\btriste\b.*\b(no quiero|sin|evitar)', text_lower):
            scores['motivado'] += 1.5  # Agregar motivación
        
        # Caso: "Me siento vacía"
        if any(word in text_lower for word in ['vacía', 'vacío', 'sin sentido', 'nada']):
            scores['triste'] += 2.0
            scores['confundido'] += 1.5
        
        # Determinar emoción dominante
        if not scores:
            return 'neutral', 0.0
        
        best_emotion = max(scores, key=scores.get)
        confidence = scores[best_emotion] / sum(scores.values())
        
        return best_emotion, confidence
    
    def get_all_books_flat(self):
        books = []
        for category, book_list in self.books.items():
            for book in book_list:
                book_copy = book.copy()
                book_copy['categoria'] = category
                books.append(book_copy)
        return books
    
    def calculate_book_score(self, book, emotion, user_message, special_contexts):
        """Calcula puntuación con contextos especiales"""
        score = 0.0
        
        # 1. Match emocional directo
        if emotion in book.get('emociones', []):
            score += 3.0
        
        # 2. Historial de preferencias
        for book_emotion in book.get('emociones', []):
            score += self.history['preferences'].get(book_emotion, 0) * 0.5
        
        # 3. Puntaje histórico del libro
        book_id = f"{book['titulo']}_{book['autor']}"
        score += self.history['book_scores'].get(book_id, 0) * 0.3
        
        # 4. Penalización por repetición
        if book['titulo'] in self.session_recommended:
            score -= 10.0
        
        # 5. Contextos especiales
        message_lower = user_message.lower()
        
        # Contexto: Esperanza (quiere salir de la tristeza)
        if 'esperanza' in special_contexts:
            if book.get('impacto') == 'esperanzador':
                score += 3.0
            elif book.get('impacto') == 'catártico':
                score -= 2.0  # Evitar libros que profundizan
        
        # Contexto: Catarsis (quiere profundizar en la emoción)
        if 'catarsis' in special_contexts:
            if book.get('impacto') == 'catártico':
                score += 3.0
            elif book.get('impacto') == 'esperanzador':
                score -= 1.0
        
        # Contexto: Intenso (quiere algo fuerte)
        if 'intenso' in special_contexts:
            if book.get('intensidad') == 'alta':
                score += 2.0
        
        # Contexto: No empeorar (evitar libros muy tristes)
        if 'no_empeorar' in special_contexts:
            if book.get('impacto') == 'catártico':
                score -= 2.0
            if book.get('impacto') == 'esperanzador':
                score += 2.0
        
        # 6. Búsqueda por temas específicos
        if 'feminista' in message_lower and 'protagonista' in message_lower:
            if 'Jane Eyre' in book['titulo']:
                score += 3.0
        
        if 'duelo' in message_lower or 'pérdida' in message_lower:
            if 'duelo' in book.get('temas', []) or 'pérdida' in book.get('temas', []):
                score += 2.5
        
        if 'vacío' in message_lower or 'vacía' in message_lower:
            if 'vacío' in book.get('temas', []) or 'muerte' in book.get('temas', []):
                score += 2.5
        
        # 7. Diversidad
        categoria = book.get('categoria', '')
        recent_categories = [i.get('categoria', '') for i in self.history['interactions'][-5:]]
        if categoria not in recent_categories:
            score += 1.0
        
        return score
    
    def recommend(self, user_message):
        """Recomendación inteligente mejorada"""
        
        # 1. Detectar contextos especiales
        special_contexts = self.detect_special_context(user_message)
        
        # 2. Analizar emoción
        emotion, confidence = self.analyze_emotion(user_message)
        
        print(f"🔍 Emoción: {emotion} (confianza: {confidence:.2f})")
        print(f"🎯 Contextos especiales: {special_contexts}")
        
        # 3. Calcular scores
        all_books = self.get_all_books_flat()
        book_scores = []
        
        for book in all_books:
            score = self.calculate_book_score(book, emotion, user_message, special_contexts)
            book_scores.append((book, score))
        
        # 4. Ordenar
        book_scores.sort(key=lambda x: x[1], reverse=True)
        
        if not book_scores or book_scores[0][1] < -5:
            return self.handle_no_recommendations(emotion)
        
        best_book, best_score = book_scores[0]
        
        print(f"📖 Mejor match: {best_book['titulo']} (score: {best_score:.2f})")
        
        # 5. Registrar
        self.session_recommended.add(best_book['titulo'])
        
        interaction = {
            'timestamp': datetime.now().isoformat(),
            'user_message': user_message,
            'emotion': emotion,
            'confidence': confidence,
            'recommended': best_book['titulo'],
            'categoria': best_book.get('categoria'),
            'score': best_score,
            'special_contexts': special_contexts
        }
        
        self.conversation_context.append(interaction)
        self.history['interactions'].append(interaction)
        
        # 6. Aprendizaje
        self.history['preferences'][emotion] += 0.2
        for book_emotion in best_book.get('emociones', []):
            self.history['preferences'][book_emotion] += 0.1
        
        book_id = f"{best_book['titulo']}_{best_book['autor']}"
        self.history['book_scores'][book_id] += 0.1
        
        self.save_history()
        
        # 7. Explicación
        explanation = self.generate_explanation(best_book, emotion, best_score, user_message, special_contexts)
        
        return {
            'libro': best_book,
            'confianza': float(confidence),
            'analisis': {
                'emotion': emotion,
                'emotion_confidence': float(confidence),
                'score': float(best_score),
                'special_contexts': special_contexts
            },
            'explicacion': explanation,
            'alternativas': [b[0]['titulo'] for b in book_scores[1:4]]
        }
    
    def generate_explanation(self, book, emotion, score, user_message, special_contexts):
        """Genera explicación personalizada con contextos"""
        
        impact = book.get('impacto', 'interesante')
        
        explanation = f"Basándome en tu estado '{emotion}'"
        
        # Mencionar contextos especiales
        if 'esperanza' in special_contexts:
            explanation += " y tu deseo de esperanza"
        if 'catarsis' in special_contexts:
            explanation += " y tu necesidad de catarsis"
        if 'no_empeorar' in special_contexts:
            explanation += " (evitando libros muy oscuros)"
        
        explanation += f", te recomiendo '{book['titulo']}' de {book['autor']}. "
        explanation += f"{book['descripcion']} "
        
        # Explicar por qué este impacto
        if impact == 'catártico' and 'catarsis' in special_contexts:
            explanation += "Este libro te permitirá profundizar en tus emociones y liberarlas."
        elif impact == 'esperanzador' and 'esperanza' in special_contexts:
            explanation += "Este libro te acompañará en tu tristeza pero te mostrará luz al final."
        
        if score > 4.0:
            explanation += " (El sistema ha aprendido que este tipo de libro te gusta)"
        
        return explanation
    
    def handle_no_recommendations(self, emotion):
        return {
            'libro': {
                'titulo': 'Sin recomendaciones disponibles',
                'autor': 'Sistema',
                'descripcion': 'Ya recomendé todos los libros disponibles. ¿Quieres reiniciar?',
                'color': '#9B8BC4',
                'emoji': '🤔'
            },
            'confianza': 0.0,
            'analisis': {'emotion': emotion, 'emotion_confidence': 0.0, 'score': 0.0, 'special_contexts': []},
            'explicacion': 'He agotado las opciones. Puedo reiniciar si quieres.',
            'alternativas': []
        }
    
    def get_learning_stats(self):
        total = len(self.history['interactions'])
        
        emotion_counts = defaultdict(int)
        for interaction in self.history['interactions']:
            emotion = interaction.get('emotion')
            if emotion:
                emotion_counts[emotion] += 1
        
        top_emotions = sorted(emotion_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        
        book_counts = defaultdict(int)
        for interaction in self.history['interactions']:
            book = interaction.get('recommended')
            if book:
                book_counts[book] += 1
        
        top_books = sorted(book_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        
        return {
            'total_interactions': total,
            'session_recommended': len(self.session_recommended),
            'top_emotions': [{'emotion': e, 'count': c} for e, c in top_emotions],
            'top_books': [{'book': b, 'count': c} for b, c in top_books],
            'preferences': dict(self.history['preferences'])
        }
    
    def reset_session(self):
        self.session_recommended.clear()
        self.conversation_context.clear()
        print("🔄 Sesión reiniciada")