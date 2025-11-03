import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import json
import os
from datetime import datetime

class BookRecommendationAI:
    """
    Motor de IA profesional para recomendación de libros usando:
    - Sentence Transformers para embeddings semánticos
    - Sistema de historial y aprendizaje
    - Análisis de similitud contextual
    """
    
    def __init__(self):
        print("🤖 Inicializando motor de IA...")
        
        # Cargar modelo de embeddings (pequeño y eficiente)
        self.model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        print("✅ Modelo cargado: paraphrase-multilingual-MiniLM-L12-v2")
        
        # Archivo para persistir historial
        self.history_file = 'user_history.json'
        self.user_history = self.load_history()
        
        # Embeddings de estados emocionales y géneros
        self.emotion_embeddings = {}
        self.genre_embeddings = {}
        self.book_embeddings = {}
        
        print("✅ Motor de IA listo")
    
    def load_history(self):
        """Carga el historial de interacciones del usuario"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {'interactions': [], 'preferences': {}}
        return {'interactions': [], 'preferences': {}}
    
    def save_history(self):
        """Guarda el historial de manera persistente"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.user_history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error guardando historial: {e}")
    
    def encode_books(self, books):
        """Genera embeddings para todos los libros de la biblioteca"""
        print("📚 Generando embeddings de libros...")
        
        for book in books:
            # Crear texto descriptivo del libro
            book_text = f"{book['titulo']} {book['autor']} {book['descripcion']}"
            embedding = self.model.encode(book_text)
            self.book_embeddings[book['titulo']] = {
                'embedding': embedding,
                'book': book
            }
        
        print(f"✅ {len(self.book_embeddings)} libros codificados")
    
    def understand_user_input(self, user_message):
        """
        Analiza el mensaje del usuario usando IA para extraer:
        - Estado emocional
        - Preferencias de género
        - Contexto adicional
        """
        user_embedding = self.model.encode(user_message)
        
        # Diccionario de estados emocionales con descripciones extensas
        emotions = {
            "feliz": "alegre contento emocionado entusiasmado positivo energético optimista radiante jubiloso animado",
            "triste": "melancólico deprimido desanimado nostálgico solitario apesadumbrado abatido decaído sombrío desesperanzado",
            "pensativo": "reflexivo filosófico introspectivo meditativo contemplativo analítico profundo",
            "motivado": "inspirado determinado ambicioso productivo enfocado enérgico dinámico decidido",
            "aburrido": "cansado hastiado sin interés monótono apático desganado fastidiado",
            "ansioso": "nervioso preocupado inquieto estresado tenso agitado intranquilo angustiado",
            "curioso": "interesado explorador inquisitivo ávido de aprender investigador descubridor",
            "romantico": "amoroso sentimental apasionado emotivo tierno soñador enamorado",
            "nostalgico": "añorante evocador remembrante retrospectivo sentimental del pasado",
            "confundido": "perdido desorientado indeciso incierto dubitativo perplejo",
            "valiente": "audaz intrépido corajudo heroico osado temerario aventurero",
            "tranquilo": "calmado sereno pacífico relajado sosegado apacible",
            "rebelde": "inconformista revolucionario contestatario crítico desafiante"
        }
        
        # Diccionario de géneros con descripciones extensas
        genres = {
            "filosofia": "filosófico existencial reflexivo pensamiento profundo sabiduría ética moral verdad conocimiento razón lógica",
            "romance": "amor romántico relaciones sentimientos pasión enamoramiento pareja intimidad corazón emotivo",
            "distopia": "futuro oscuro totalitario control social crítica apocalíptico opresión vigilancia",
            "aventura": "viaje exploración acción emoción épica hazaña expedición descubrimiento",
            "clasica": "literatura clásica obra maestra histórica universal atemporal tradición",
            "humor": "cómico gracioso irónico satírico entretenido divertido risas alegre",
            "misterio": "suspense enigma detective investigación intriga secreto crimen",
            "ciencia_ficcion": "futuro tecnología espacio aliens robots inteligencia artificial",
            "terror": "miedo horror suspenso escalofriante tenebroso oscuro",
            "biografia": "vida real persona histórica testimonio memorias experiencia",
            "autoayuda": "crecimiento personal desarrollo motivación superación coaching",
            "historica": "historia época pasado acontecimientos cronología",
            "fantasia": "magia dragones mundos imaginarios épica fantástica",
            "politica": "poder gobierno sociedad sistema estado democracia",
            "psicologia": "mente comportamiento emociones consciencia subconsciente"
        }
        
        # Calcular similitud con emociones
        best_emotion = None
        best_emotion_score = 0
        
        for emotion, description in emotions.items():
            emotion_embedding = self.model.encode(description)
            similarity = cosine_similarity(
                [user_embedding], 
                [emotion_embedding]
            )[0][0]
            
            if similarity > best_emotion_score:
                best_emotion_score = similarity
                best_emotion = emotion
        
        # Calcular similitud con géneros
        best_genre = None
        best_genre_score = 0
        
        for genre, description in genres.items():
            genre_embedding = self.model.encode(description)
            similarity = cosine_similarity(
                [user_embedding], 
                [genre_embedding]
            )[0][0]
            
            if similarity > best_genre_score:
                best_genre_score = similarity
                best_genre = genre
        
        return {
            'emotion': best_emotion,
            'emotion_confidence': float(best_emotion_score),
            'genre': best_genre,
            'genre_confidence': float(best_genre_score),
            'raw_message': user_message
        }
    
    def recommend_book(self, user_input, books_data):
        """
        Recomienda un libro usando IA semántica y historial
        """
        # Si no hay embeddings, generarlos
        if not self.book_embeddings:
            self.encode_books(books_data)
        
        # Analizar entrada del usuario
        analysis = self.understand_user_input(user_input)
        
        print(f"🔍 Análisis: Emoción={analysis['emotion']} ({analysis['emotion_confidence']:.2f}), "
              f"Género={analysis['genre']} ({analysis['genre_confidence']:.2f})")
        
        # Crear embedding del contexto completo del usuario
        context_text = f"{user_input} {analysis['emotion']} {analysis['genre']}"
        context_embedding = self.model.encode(context_text)
        
        # Calcular similitud con todos los libros
        similarities = {}
        for book_title, book_data in self.book_embeddings.items():
            similarity = cosine_similarity(
                [context_embedding],
                [book_data['embedding']]
            )[0][0]
            
            # Ajustar con historial (dar boost a géneros preferidos)
            if analysis['genre'] in self.user_history.get('preferences', {}):
                preference_weight = self.user_history['preferences'][analysis['genre']]
                similarity *= (1 + preference_weight * 0.2)
            
            similarities[book_title] = similarity
        
        # Obtener el libro más similar
        best_book_title = max(similarities, key=similarities.get)
        best_book = self.book_embeddings[best_book_title]['book']
        confidence = similarities[best_book_title]
        
        # Guardar en historial
        self.add_to_history(user_input, best_book, analysis, confidence)
        
        return {
            'libro': best_book,
            'confianza': float(confidence),
            'analisis': analysis,
            'explicacion': self.generate_explanation(best_book, analysis, confidence)
        }
    
    def generate_explanation(self, book, analysis, confidence):
        """Genera explicación natural de por qué se recomienda el libro"""
        
        emotion_texts = {
            "feliz": "tu estado de ánimo positivo",
            "triste": "que estás pasando por un momento difícil",
            "pensativo": "tu deseo de reflexionar profundamente",
            "motivado": "tu energía y determinación",
            "aburrido": "tu necesidad de algo estimulante",
            "ansioso": "tu necesidad de calma y perspectiva",
            "curioso": "tu curiosidad intelectual"
        }
        
        emotion_reason = emotion_texts.get(
            analysis['emotion'], 
            "tu estado actual"
        )
        
        explanation = (
            f"Basándome en {emotion_reason} y tu interés en {analysis['genre']}, "
            f"'{book['titulo']}' de {book['autor']} es perfecto para ti. "
            f"{book['descripcion']}"
        )
        
        if confidence > 0.7:
            explanation += " ¡Estoy muy seguro de que te encantará!"
        elif confidence > 0.5:
            explanation += " Creo que te gustará mucho."
        else:
            explanation += " Es una buena opción para explorar."
        
        return explanation
    
    def add_to_history(self, user_input, book, analysis, confidence):
        """Agrega interacción al historial para aprendizaje"""
        interaction = {
            'timestamp': datetime.now().isoformat(),
            'user_input': user_input,
            'emotion': analysis['emotion'],
            'genre': analysis['genre'],
            'recommended_book': book['titulo'],
            'confidence': float(confidence)
        }
        
        self.user_history['interactions'].append(interaction)
        
        # Actualizar preferencias (aprendizaje simple)
        if analysis['genre']:
            if analysis['genre'] not in self.user_history['preferences']:
                self.user_history['preferences'][analysis['genre']] = 0
            self.user_history['preferences'][analysis['genre']] += 0.1
        
        # Mantener solo últimas 50 interacciones
        if len(self.user_history['interactions']) > 50:
            self.user_history['interactions'] = self.user_history['interactions'][-50:]
        
        self.save_history()
    
    def get_user_stats(self):
        """Obtiene estadísticas del usuario para mostrar"""
        total_interactions = len(self.user_history['interactions'])
        
        if total_interactions == 0:
            return {
                'total_interactions': 0,
                'favorite_genres': [],
                'favorite_emotions': []
            }
        
        # Contar géneros
        genre_counts = {}
        emotion_counts = {}
        
        for interaction in self.user_history['interactions']:
            genre = interaction.get('genre')
            emotion = interaction.get('emotion')
            
            if genre:
                genre_counts[genre] = genre_counts.get(genre, 0) + 1
            if emotion:
                emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        # Ordenar por frecuencia
        favorite_genres = sorted(
            genre_counts.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:3]
        
        favorite_emotions = sorted(
            emotion_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )[:3]
        
        return {
            'total_interactions': total_interactions,
            'favorite_genres': [g[0] for g in favorite_genres],
            'favorite_emotions': [e[0] for e in favorite_emotions],
            'genre_counts': genre_counts,
            'emotion_counts': emotion_counts
        }