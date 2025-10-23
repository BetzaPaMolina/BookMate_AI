from flask import Flask, render_template, request, jsonify
from book_agent import BookAgent

app = Flask(__name__)
agent = BookAgent()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recomendar', methods=['POST'])
def recomendar():
    try:
        data = request.get_json()
        estado_animo = data.get('estado_animo', '').strip()
        genero = data.get('genero', '').strip()
        
        if not estado_animo or not genero:
            return jsonify({'error': 'Por favor completa ambos campos'}), 400
        
        resultado = agent.recomendar(estado_animo, genero)
        
        return jsonify({
            'success': True,
            'recommendation': resultado
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health')
def health():
    return jsonify({'status': 'active', 'service': 'BookMate AI'})

if __name__ == '__main__':
    print("🚀 Iniciando BookMate AI...")
    print("📖 Abre tu navegador en: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)