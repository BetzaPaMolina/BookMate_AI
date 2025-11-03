from flask import Flask, render_template, request, jsonify
from book_agent import BookAgent

app = Flask(__name__)
agent = BookAgent()

# Comentamos la IA por ahora, usaremos el agente simple
# from ai_engine import BookRecommendationAI
# ai_engine = BookRecommendationAI()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recomendar', methods=['POST'])
def recomendar():
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        print(f"📨 Mensaje recibido: {user_message}")  # Debug
        
        if not user_message:
            return jsonify({'error': 'Por favor escribe un mensaje'}), 400
        
        # Análisis simple del mensaje (sin IA pesada)
        user_message_lower = user_message.lower()
        
        # Detectar estado de ánimo
        estado_animo = "feliz"  # default
        if any(word in user_message_lower for word in ['triste', 'melancólico', 'deprimido', 'solo', 'nostálgico']):
            estado_animo = "triste"
        elif any(word in user_message_lower for word in ['pensativo', 'reflexivo', 'filosófico', 'pensar', 'reflexionar']):
            estado_animo = "pensativo"
        elif any(word in user_message_lower for word in ['motivado', 'inspirado', 'energía', 'determinado']):
            estado_animo = "motivado"
        elif any(word in user_message_lower for word in ['aburrido', 'cansado', 'hastiado', 'monótono']):
            estado_animo = "aburrido"
        elif any(word in user_message_lower for word in ['feliz', 'alegre', 'contento', 'emocionado']):
            estado_animo = "feliz"
        
        # Detectar género
        genero = "cualquiera"  # default
        if any(word in user_message_lower for word in ['filosofía', 'filosófico', 'existencial', 'reflexivo']):
            genero = "filosofia"
        elif any(word in user_message_lower for word in ['romance', 'amor', 'romántico', 'sentimental']):
            genero = "romance"
        elif any(word in user_message_lower for word in ['distopía', 'distópico', 'futuro', 'oscuro']):
            genero = "distopia"
        elif any(word in user_message_lower for word in ['aventura', 'viaje', 'épico', 'acción']):
            genero = "aventura"
        elif any(word in user_message_lower for word in ['clásico', 'clásica', 'literatura']):
            genero = "clasica"
        
        print(f"🔍 Detectado - Estado: {estado_animo}, Género: {genero}")  # Debug
        
        # Usar el agente simple para recomendar
        resultado = agent.recomendar(estado_animo, genero)
        
        # Adaptar la respuesta al nuevo formato
        return jsonify({
            'success': True,
            'recommendation': {
                'libro': resultado['libro'],
                'confianza': 0.85,  # Simulado
                'analisis': {
                    'emotion': estado_animo,
                    'emotion_confidence': 0.8,
                    'genre': genero,
                    'genre_confidence': 0.75
                },
                'explicacion': resultado['proceso']['razonamiento']['explicacion']
            }
        })
        
    except Exception as e:
        print(f"❌ Error en recomendación: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/biblioteca')
def get_biblioteca():
    """Retorna todos los libros de la biblioteca"""
    try:
        libros = agent.get_all_books()
        return jsonify({
            'success': True,
            'libros': libros,
            'total': len(libros)
        })
    except Exception as e:
        print(f"Error en /api/biblioteca: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/libros-recientes')
def get_libros_recientes():
    """
    Busca automáticamente en internet libros populares y bien valorados
    que NO están en la biblioteca actual
    """
    try:
        import requests
        from datetime import datetime
        
        # Obtener libros de la biblioteca actual
        libros_existentes = [libro['titulo'].lower() for libro in agent.get_all_books()]
        
        # Usar API de Google Books para buscar bestsellers recientes
        year = datetime.now().year
        
        queries = [
            f"bestseller books {year}",
            f"most popular books {year}",
            f"award winning books {year}"
        ]
        
        libros_encontrados = []
        libros_unicos = set()
        
        for query in queries:
            try:
                # API de Google Books (no requiere API key para búsquedas básicas)
                url = f"https://www.googleapis.com/books/v1/volumes?q={query}&orderBy=relevance&maxResults=10"
                response = requests.get(url, timeout=5)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if 'items' in data:
                        for item in data['items']:
                            volume_info = item.get('volumeInfo', {})
                            titulo = volume_info.get('title', '')
                            
                            # Verificar que el libro NO esté en nuestra biblioteca
                            if titulo and titulo.lower() not in libros_existentes:
                                # Evitar duplicados
                                if titulo not in libros_unicos:
                                    libros_unicos.add(titulo)
                                    
                                    autores = volume_info.get('authors', ['Autor desconocido'])
                                    autor = ', '.join(autores[:2])  # Máximo 2 autores
                                    
                                    descripcion = volume_info.get('description', 'Sin descripción disponible')
                                    # Limitar descripción a 150 caracteres
                                    if len(descripcion) > 150:
                                        descripcion = descripcion[:147] + '...'
                                    
                                    fecha = volume_info.get('publishedDate', str(year))
                                    anio = fecha[:4] if fecha else str(year)
                                    
                                    rating = volume_info.get('averageRating', 0)
                                    rating_count = volume_info.get('ratingsCount', 0)
                                    
                                    fuente = "Google Books"
                                    if rating > 0:
                                        fuente = f"⭐ {rating}/5 ({rating_count} reseñas)"
                                    
                                    libros_encontrados.append({
                                        "titulo": titulo,
                                        "autor": autor,
                                        "anio": anio,
                                        "descripcion": descripcion,
                                        "fuente": fuente
                                    })
                                    
                                    # Limitar a 6 libros únicos
                                    if len(libros_encontrados) >= 6:
                                        break
            except Exception as e:
                print(f"Error buscando con query '{query}': {e}")
                continue
            
            if len(libros_encontrados) >= 6:
                break
        
        # Si no se encontraron libros de la API, usar fallback
        if not libros_encontrados:
            libros_encontrados = [
                {
                    "titulo": "The Woman in Me",
                    "autor": "Britney Spears",
                    "anio": "2023",
                    "descripcion": "Memorias sinceras de la icónica estrella del pop",
                    "fuente": "Bestseller NY Times"
                },
                {
                    "titulo": "Holly",
                    "autor": "Stephen King",
                    "anio": "2023",
                    "descripcion": "Thriller con la detective Holly Gibney",
                    "fuente": "Bestseller internacional"
                }
            ]
        
        return jsonify({
            'success': True,
            'libros': libros_encontrados[:6],  # Máximo 6 libros
            'total': len(libros_encontrados[:6]),
            'fuente': 'Google Books API',
            'nota': 'Libros que no están en tu biblioteca actual'
        })
        
    except Exception as e:
        print(f"Error en /api/libros-recientes: {e}")
        # Fallback en caso de error
        return jsonify({
            'success': True,
            'libros': [
                {
                    "titulo": "No se pudieron cargar libros recientes",
                    "autor": "Sistema",
                    "anio": "2024",
                    "descripcion": "Intenta recargar la página",
                    "fuente": "Error de conexión"
                }
            ],
            'total': 1
        })

@app.route('/api/user-stats')
def get_user_stats():
    """Retorna estadísticas del usuario (simulado por ahora)"""
    try:
        return jsonify({
            'success': True,
            'stats': {
                'total_interactions': 0,
                'favorite_genres': [],
                'favorite_emotions': []
            }
        })
    except Exception as e:
        print(f"Error obteniendo stats: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/health')
def health():
    return jsonify({'status': 'active', 'service': 'BookMate AI'})

if __name__ == '__main__':
    print("🚀 Iniciando BookMate AI...")
    print("📖 Abre tu navegador en: http://localhost:5000")
    print(f"📚 Biblioteca cargada con {len(agent.all_books)} libros")
    app.run(debug=True, host='0.0.0.0', port=5000)