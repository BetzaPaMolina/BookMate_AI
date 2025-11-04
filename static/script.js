let allBooks = [];
let currentCategory = 'todos';
let learningStats = null;

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

// Load recent books
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
    }
}

// Load learning stats
async function loadLearningStats() {
    try {
        const response = await fetch('/api/user-stats');
        const data = await response.json();
        
        if (data.success) {
            learningStats = data.stats;
            displayLearningStats();
        }
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

// Display learning stats
function displayLearningStats() {
    if (!learningStats) return;
    
    const statsContainer = document.getElementById('learning-stats');
    if (!statsContainer) return;
    
    const total = learningStats.total_interactions;
    const sessionCount = learningStats.session_recommended;
    
    let statsHTML = `
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value">${total}</div>
                <div class="stat-label">📚 Interacciones totales</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${sessionCount}</div>
                <div class="stat-label">💬 En esta sesión</div>
            </div>
        </div>
    `;
    
    // Top emotions
    if (learningStats.top_emotions && learningStats.top_emotions.length > 0) {
        statsHTML += '<div class="stat-section"><h4>🎭 Emociones más frecuentes</h4><div class="emotion-bars">';
        learningStats.top_emotions.forEach(item => {
            const percentage = total > 0 ? (item.count / total * 100).toFixed(0) : 0;
            statsHTML += `
                <div class="emotion-bar">
                    <span>${item.emotion}</span>
                    <div class="bar-bg">
                        <div class="bar-fill" style="width: ${percentage}%"></div>
                    </div>
                    <span>${item.count}</span>
                </div>
            `;
        });
        statsHTML += '</div></div>';
    }
    
    // Top books
    if (learningStats.top_books && learningStats.top_books.length > 0) {
        statsHTML += '<div class="stat-section"><h4>⭐ Libros más recomendados</h4><ul class="top-books-list">';
        learningStats.top_books.forEach(item => {
            statsHTML += `<li>${item.book} <span>(${item.count}x)</span></li>`;
        });
        statsHTML += '</ul></div>';
    }
    
    statsContainer.innerHTML = statsHTML;
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
                displayBooks(allBooks);
            }
        });
    });
    
    // Suggestion chips
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
    loadLearningStats();
});

function showAllBooks() {
    displayBooks(allBooks);
}

// Reset session button
async function resetSession() {
    try {
        const response = await fetch('/api/reset-session', {
            method: 'POST'
        });
        const data = await response.json();
        
        if (data.success) {
            addMessage('bot', '🔄 ' + data.message);
            loadLearningStats(); // Actualizar stats
        }
    } catch (error) {
        console.error('Error resetting session:', error);
    }
}

// Chat functionality
const form = document.getElementById('recommendation-form');
const chatMessages = document.getElementById('chat-messages');
const userMessageInput = document.getElementById('user-message');
const sendBtn = document.getElementById('send-btn');

form.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const userMessage = userMessageInput.value.trim();
    
    if (!userMessage) {
        addMessage('bot', '⚠️ Por favor escribe algo sobre lo que buscas.');
        return;
    }

    addMessage('user', userMessage);
    userMessageInput.value = '';
    
    // Typing indicator
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message bot typing-indicator';
    typingDiv.id = 'typing';
    typingDiv.innerHTML = '<div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div>';
    chatMessages.appendChild(typingDiv);
    scrollToBottom();

    sendBtn.disabled = true;

    try {
        const response = await fetch('/recomendar', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: userMessage
            })
        });
        
        const data = await response.json();
        
        document.getElementById('typing')?.remove();
        
        if (data.success) {
            displayRecommendation(data.recommendation);
            // Actualizar stats después de cada recomendación
            setTimeout(() => loadLearningStats(), 500);
        } else {
            addMessage('bot', '❌ ' + data.error);
        }
        
    } catch (error) {
        console.error('❌ Error:', error);
        document.getElementById('typing')?.remove();
        addMessage('bot', '❌ Error de conexión: ' + error.message);
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
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot';
    
    const confidence = (data.confianza * 100).toFixed(0);
    const confidenceColor = data.confianza > 0.7 ? 'var(--green)' : data.confianza > 0.5 ? 'var(--yellow)' : 'var(--coral)';
    
    // Score de aprendizaje
    const score = data.analisis.score || 0;
    const scoreColor = score > 5 ? 'var(--green)' : score > 2 ? 'var(--yellow)' : 'var(--coral)';
    
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
                <div style="margin-top: 8px; font-size: 11px; display: flex; gap: 5px; flex-wrap: wrap;">
                    <span style="background: ${confidenceColor}; color: white; padding: 3px 8px; border-radius: 10px;">
                        Confianza: ${confidence}%
                    </span>
                    <span style="background: ${scoreColor}; color: white; padding: 3px 8px; border-radius: 10px;">
                        🧠 Score: ${score.toFixed(1)}
                    </span>
                </div>
            </div>
        </div>
        <div style="margin-top: 10px; font-size: 13px; background: rgba(255,255,255,0.2); padding: 10px; border-radius: 10px;">
            <strong>💡 ¿Por qué este libro?</strong><br>
            ${data.explicacion}
        </div>
    `;
    
    // Alternativas
    if (data.alternativas && data.alternativas.length > 0) {
        messageDiv.innerHTML += `
            <div style="margin-top: 10px; font-size: 12px;">
                <strong>📚 Alternativas:</strong> ${data.alternativas.join(', ')}
            </div>
        `;
    }
    
    messageDiv.innerHTML += `
        <div class="quick-actions">
            <button class="quick-btn" onclick="resetSession()">🔄 Reiniciar</button>
            <button class="quick-btn" onclick="loadLearningStats()">📊 Ver stats</button>
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
                'motivado': '💪', 'aburrido': '😴', 'ansioso': '😰', 
                'curioso': '🧐', 'romántico': '💕'
            };
            
            const emoji = emotion_emojis[data.analisis.emotion] || '🎭';
            
            addMessage('bot', `
                🤖 <strong>Análisis del sistema:</strong><br><br>
                ${emoji} <strong>Estado detectado:</strong> ${data.analisis.emotion}<br>
                🎯 <strong>Confianza emocional:</strong> ${(data.analisis.emotion_confidence * 100).toFixed(0)}%<br>
                🧠 <strong>Score de aprendizaje:</strong> ${data.analisis.score.toFixed(2)}<br>
                <small style="opacity: 0.8;">Este score se basa en tu historial y preferencias</small>
            `);
        }, 500);
    }
}

function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}