from flask import Flask, render_template, request, jsonify
from smart_recommender import SmartRecommender
from feedback_system import FeedbackSystem

feedback_sys = FeedbackSystem()
app = Flask(__name__)

# Instanciar el recomendador inteligente
recommender = SmartRecommender()

@app.route('/api/feedback', methods=['POST'])
def submit_feedback():
    """Usuario califica la última recomendación"""
    try:
        data = request.get_json()
        recommendation = data.get('recommendation')
        feedback_type = data.get('feedback_type')  # 'positive', 'negative', 'neutral', 'wrong_emotion'
        comment = data.get('comment', None)
        
        result = feedback_sys.process_feedback(recommendation, feedback_type, comment)
        
        return jsonify({
            'success': True,
            'result': result
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/feedback-stats')
def get_feedback_stats():
    """Retorna estadísticas de aprendizaje"""
    try:
        stats = feedback_sys.get_feedback_stats()
        return jsonify({
            'success': True,
            'stats': stats
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/feedback', methods=['POST'])
def submit_feedback():
    data = request.get_json()
    book_id = data.get('book_id')
    feedback_type = data.get('feedback_type')
    
    # Procesar con FeedbackSystem
    result = feedback_sys.process_feedback(
        data.get('recommendation'),
        feedback_type
    )
    
    return jsonify({'success': True, 'result': result})

@app.route('/api/add-book', methods=['POST'])
def add_book():
    book_data = request.get_json()
    
    # Agregar a smart_recommender
    recommender.add_custom_book(book_data)
    
    return jsonify({
        'success': True,
        'message': f"Libro '{book_data['titulo']}' agregado"
    })

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recomendar', methods=['POST'])
def recomendar():
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        print(f"📨 Mensaje recibido: {user_message}")
        
        if not user_message:
            return jsonify({'error': 'Por favor escribe un mensaje'}), 400
        
        # Usar el recomendador inteligente
        resultado = recommender.recommend(user_message)
        
        return jsonify({
            'success': True,
            'recommendation': resultado
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
        libros = recommender.get_all_books_flat()
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
    """Busca libros populares que NO están en la biblioteca"""
    try:
        import requests
        from datetime import datetime
        
        # Obtener títulos existentes
        libros_existentes = [libro['titulo'].lower() for libro in recommender.get_all_books_flat()]
        
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
                url = f"https://www.googleapis.com/books/v1/volumes?q={query}&orderBy=relevance&maxResults=10"
                response = requests.get(url, timeout=5)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if 'items' in data:
                        for item in data['items']:
                            volume_info = item.get('volumeInfo', {})
                            titulo = volume_info.get('title', '')
                            
                            if titulo and titulo.lower() not in libros_existentes and titulo not in libros_unicos:
                                libros_unicos.add(titulo)
                                
                                autores = volume_info.get('authors', ['Autor desconocido'])
                                autor = ', '.join(autores[:2])
                                
                                descripcion = volume_info.get('description', 'Sin descripción disponible')
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
                                
                                if len(libros_encontrados) >= 6:
                                    break
            except Exception as e:
                print(f"Error buscando con query '{query}': {e}")
                continue
            
            if len(libros_encontrados) >= 6:
                break
        
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
            'libros': libros_encontrados[:6],
            'total': len(libros_encontrados[:6]),
            'fuente': 'Google Books API',
            'nota': 'Libros que no están en tu biblioteca actual'
        })
        
    except Exception as e:
        print(f"Error en /api/libros-recientes: {e}")
        return jsonify({
            'success': True,
            'libros': [{
                "titulo": "No se pudieron cargar libros recientes",
                "autor": "Sistema",
                "anio": "2024",
                "descripcion": "Intenta recargar la página",
                "fuente": "Error de conexión"
            }],
            'total': 1
        })

@app.route('/api/user-stats')
def get_user_stats():
    """Retorna estadísticas REALES del aprendizaje"""
    try:
        stats = recommender.get_learning_stats()
        return jsonify({
            'success': True,
            'stats': stats
        })
    except Exception as e:
        print(f"Error obteniendo stats: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/reset-session', methods=['POST'])
def reset_session():
    """Reinicia las recomendaciones de la sesión"""
    try:
        recommender.reset_session()
        return jsonify({
            'success': True,
            'message': 'Sesión reiniciada. Puedo recomendarte libros nuevamente.'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health')
def health():
    return jsonify({
        'status': 'active', 
        'service': 'BookMate AI (Smart Learning)',
        'total_books': len(recommender.get_all_books_flat()),
        'total_interactions': len(recommender.history.get('interactions', []))
    })



if __name__ == '__main__':
    print("🚀 Iniciando BookMate AI (Smart Learning)...")
    print("📖 Abre tu navegador en: http://localhost:5000")
    print(f"📚 Biblioteca: {len(recommender.get_all_books_flat())} libros")
    print(f"🧠 Historial: {len(recommender.history.get('interactions', []))} interacciones previas")
    app.run(debug=True, host='0.0.0.0', port=5000)