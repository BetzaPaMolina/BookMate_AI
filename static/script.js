let allBooks = [];
let currentCategory = 'todos';

// Load library books on page load
async function loadLibrary() {
    try {
        const response = await fetch('/api/biblioteca');
        const data = await response.json();
        
        if (data.success) {
            allBooks = data.libros;
            displayBooks(allBooks);
        }
    } catch (error) {
        console.error('Error loading library:', error);
        document.getElementById('library-books').innerHTML = '<p style="text-align:center; color: var(--text-light); padding: 20px;">Error al cargar la biblioteca</p>';
    }
}

// Display books in grid
function displayBooks(books) {
    const booksGrid = document.getElementById('library-books');
    booksGrid.innerHTML = '';
    
    if (books.length === 0) {
        booksGrid.innerHTML = '<p style="text-align:center; color: var(--text-light); padding: 20px;">No hay libros en esta categoría</p>';
        return;
    }
    
    books.forEach(book => {
        const bookCard = document.createElement('div');
        bookCard.className = 'book-card';
        bookCard.innerHTML = `
            <div class="book-cover" style="background: linear-gradient(135deg, ${book.color}, ${book.color}dd);">
                <div style="font-size: 48px;">${book.emoji}</div>
                <div class="bookmark-icon">🔖</div>
            </div>
            <div class="book-title">${book.titulo}</div>
            <div class="book-author">${book.autor}</div>
        `;
        booksGrid.appendChild(bookCard);
    });
}

// Load recent books with reviews
async function loadRecentBooks() {
    try {
        const response = await fetch('/api/libros-recientes');
        const data = await response.json();
        
        if (data.success) {
            const listContainer = document.getElementById('recent-books-list');
            listContainer.innerHTML = '';
            
            data.libros.forEach(libro => {
                const item = document.createElement('div');
                item.className = 'recent-book-item';
                item.innerHTML = `
                    <h4>${libro.titulo}</h4>
                    <p>${libro.autor} • ${libro.anio}</p>
                    <p style="margin-top: 4px;">${libro.descripcion}</p>
                    <p class="source">📊 ${libro.fuente}</p>
                `;
                listContainer.appendChild(item);
            });
        }
    } catch (error) {
        console.error('Error loading recent books:', error);
        document.getElementById('recent-books-list').innerHTML = '<p style="text-align:center; color: var(--text-light); padding: 10px;">Error al cargar reseñas</p>';
    }
}

// Category filter
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.category-chip').forEach(chip => {
        chip.addEventListener('click', function() {
            document.querySelectorAll('.category-chip').forEach(c => c.classList.remove('active'));
            this.classList.add('active');
            
            currentCategory = this.dataset.category;
            
            if (currentCategory === 'todos') {
                displayBooks(allBooks);
            } else {
                // Filtrar libros por categoría (implementación simple)
                displayBooks(allBooks);
            }
        });
    });
    
    // Suggestion chips click handler
    document.querySelectorAll('.suggestion-chip').forEach(chip => {
        chip.addEventListener('click', function() {
            const userMessageInput = document.getElementById('user-message');
            userMessageInput.value = this.dataset.text;
            userMessageInput.focus();
        });
    });
    
    // Load initial data
    loadLibrary();
    loadRecentBooks();
});

function showAllBooks() {
    displayBooks(allBooks);
}

// Chat functionality
const form = document.getElementById('recommendation-form');
const chatMessages = document.getElementById('chat-messages');
const userMessageInput = document.getElementById('user-message');
const sendBtn = document.getElementById('send-btn');

// Form submission
form.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const userMessage = userMessageInput.value.trim();
    
    console.log('📝 Formulario enviado:', userMessage);  // Debug
    
    if (!userMessage) {
        addMessage('bot', '⚠️ Por favor escribe algo sobre lo que buscas.');
        return;
    }

    // Add user message
    addMessage('user', userMessage);
    userMessageInput.value = '';
    
    // Show typing indicator
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message bot typing-indicator';
    typingDiv.id = 'typing';
    typingDiv.innerHTML = '<div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div>';
    chatMessages.appendChild(typingDiv);
    scrollToBottom();

    sendBtn.disabled = true;

    try {
        console.log('🚀 Enviando petición...');  // Debug
        
        const response = await fetch('/recomendar', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: userMessage
            })
        });
        
        console.log('📨 Respuesta recibida:', response.status);  // Debug
        
        const data = await response.json();
        console.log('📦 Datos:', data);  // Debug
        
        // Remove typing indicator
        document.getElementById('typing')?.remove();
        
        if (data.success) {
            displayRecommendation(data.recommendation);
        } else {
            addMessage('bot', '❌ ' + data.error);
        }
        
    } catch (error) {
        console.error('❌ Error completo:', error);  // Debug
        document.getElementById('typing')?.remove();
        addMessage('bot', '❌ Error de conexión con el servidor: ' + error.message);
    } finally {
        sendBtn.disabled = false;
    }
});

function addMessage(type, text) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    messageDiv.innerHTML = `
        <div>${text}</div>
        <div class="message-time">${new Date().toLocaleTimeString('es-ES', {hour: '2-digit', minute:'2-digit'})}</div>
    `;
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

function displayRecommendation(data) {
    console.log('🎯 Mostrando recomendación:', data);  // Debug
    
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot';
    
    const confidence = (data.confianza * 100).toFixed(0);
    const confidenceColor = data.confianza > 0.7 ? 'var(--green)' : data.confianza > 0.5 ? 'var(--yellow)' : 'var(--coral)';
    
    messageDiv.innerHTML = `
        <div>🎯 ¡Tengo la recomendación perfecta para ti!</div>
        <div class="book-recommendation">
            <div class="rec-cover" style="background: linear-gradient(135deg, ${data.libro.color}, ${data.libro.color}dd);">
                ${data.libro.emoji}
            </div>
            <div class="rec-info">
                <h4>${data.libro.titulo}</h4>
                <p style="color: var(--purple); margin-bottom: 5px;">${data.libro.autor}</p>
                <p>${data.libro.descripcion}</p>
                <div style="margin-top: 8px; font-size: 11px;">
                    <span style="background: ${confidenceColor}; color: white; padding: 3px 8px; border-radius: 10px;">
                        Confianza: ${confidence}%
                    </span>
                </div>
            </div>
        </div>
        <div style="margin-top: 10px; font-size: 13px; background: rgba(255,255,255,0.2); padding: 10px; border-radius: 10px;">
            <strong>💡 ¿Por qué este libro?</strong><br>
            ${data.explicacion}
        </div>
        <div class="quick-actions">
            <button class="quick-btn" onclick="alert('Función en desarrollo')">📚 Más info</button>
            <button class="quick-btn" onclick="alert('Función en desarrollo')">🔖 Guardar</button>
        </div>
        <div class="message-time">${new Date().toLocaleTimeString('es-ES', {hour: '2-digit', minute:'2-digit'})}</div>
    `;
    
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
    
    // Show AI analysis
    if (data.analisis) {
        setTimeout(() => {
            const emotion_emojis = {
                'feliz': '😊', 'triste': '😢', 'pensativo': '🤔', 
                'motivado': '💪', 'aburrido': '😴', 'ansioso': '😰', 'curioso': '🧐'
            };
            
            const emoji = emotion_emojis[data.analisis.emotion] || '🎭';
            
            addMessage('bot', `
                🤖 <strong>Análisis:</strong><br><br>
                ${emoji} <strong>Estado detectado:</strong> ${data.analisis.emotion}<br>
                📚 <strong>Género inferido:</strong> ${data.analisis.genre}
            `);
        }, 500);
    }
}

function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}