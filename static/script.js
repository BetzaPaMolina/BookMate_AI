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
            setTimeout(() => updateStats(), 500);
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
    const score = data.analisis.score || 0;
    
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
            </div>
        </div>
        <div style="margin-top: 10px; font-size: 13px; background: rgba(255,255,255,0.2); padding: 10px; border-radius: 10px;">
            <strong>💡 ¿Por qué este libro?</strong><br>
            ${data.explicacion}
        </div>
        <div class="feedback-buttons" data-recommendation='${JSON.stringify(data).replace(/'/g, "&apos;")}'>
            <p class="feedback-prompt">¿Fue útil esta recomendación?</p>
            <div class="feedback-btn-group">
                <button class="feedback-btn positive" onclick="submitFeedback('positive', this)">
                    👍 Perfecta
                </button>
                <button class="feedback-btn neutral" onclick="submitFeedback('neutral', this)">
                    😐 Regular
                </button>
                <button class="feedback-btn negative" onclick="submitFeedback('negative', this)">
                    👎 No era esto
                </button>
                <button class="feedback-btn wrong" onclick="submitFeedback('wrong_emotion', this)">
                    🎭 Emoción incorrecta
                </button>
            </div>
        </div>
        <div class="message-time">${new Date().toLocaleTimeString('es-ES', {hour: '2-digit', minute:'2-digit'})}</div>
    `;
    
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

async function submitFeedback(feedbackType, button) {
    const container = button.closest('.feedback-buttons');
    const recommendation = JSON.parse(container.dataset.recommendation.replace(/&apos;/g, "'"));
    
    // Deshabilitar botones
    container.querySelectorAll('.feedback-btn').forEach(btn => btn.disabled = true);
    
    try {
        const response = await fetch('/api/feedback', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                recommendation: recommendation,
                feedback_type: feedbackType
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            addMessage('bot', `🧠 ${data.result.explanation}`);
            updateStats();
        }
    } catch (error) {
        console.error('Error enviando feedback:', error);
        addMessage('bot', '❌ Error procesando tu feedback');
    }
}

async function updateStats() {
    try {
        const response = await fetch('/api/feedback-stats');
        const data = await response.json();
        
        if (data.success) {
            const stats = data.stats;
            
            document.getElementById('total-feedback').textContent = stats.total_feedback;
            document.getElementById('total-books').textContent = 18; // Ajusta según tu biblioteca
            
            // Top books
            const topBooksContainer = document.getElementById('top-books');
            if (stats.top_books && stats.top_books.length > 0) {
                topBooksContainer.innerHTML = stats.top_books.slice(0, 3).map(book => `
                    <div class="book-item">
                        <h4>${book.book}</h4>
                        <p>👍 ${book.positive} feedback positivos</p>
                        <span class="book-score score-positive">Score: +${book.score}</span>
                    </div>
                `).join('');
            } else {
                topBooksContainer.innerHTML = '<p style="text-align: center; color: var(--text-light); font-size: 12px; padding: 10px;">Aún no hay libros calificados</p>';
            }
            
            // Worst books
            const worstBooksContainer = document.getElementById('worst-books');
            if (stats.worst_books && stats.worst_books.length > 0) {
                worstBooksContainer.innerHTML = stats.worst_books.slice(0, 3).map(book => `
                    <div class="book-item">
                        <h4>${book.book}</h4>
                        <p>👎 ${book.negative} feedback negativos</p>
                        <span class="book-score score-negative">Score: ${book.score}</span>
                    </div>
                `).join('');
            } else {
                worstBooksContainer.innerHTML = '<p style="text-align: center; color: var(--text-light); font-size: 12px; padding: 10px;">Aún no hay libros con feedback negativo</p>';
            }
        }
    } catch (error) {
        console.error('Error cargando stats:', error);
    }
}

// Modal
function showAddBookModal() {
    document.getElementById('add-book-modal').classList.add('show');
}

function closeAddBookModal() {
    document.getElementById('add-book-modal').classList.remove('show');
    document.getElementById('add-book-form').reset();
}

document.getElementById('add-book-form').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const newBook = {
        titulo: document.getElementById('book-title').value,
        autor: document.getElementById('book-author').value,
        descripcion: document.getElementById('book-desc').value,
        categoria: document.getElementById('book-category').value,
        emociones: document.getElementById('book-emotions').value.split(',').map(e => e.trim())
    };
    
    try {
        const response = await fetch('/api/add-book', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(newBook)
        });
        
        const data = await response.json();
        
        if (data.success) {
            addMessage('bot', `✅ ${data.message}`);
            updateStats();
            closeAddBookModal();
        }
    } catch (error) {
        console.error('Error agregando libro:', error);
        addMessage('bot', '❌ Error agregando libro');
    }
});

function fillSuggestion(text) {
    document.getElementById('user-message').value = text;
    document.getElementById('user-message').focus();
}

function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Cargar stats al iniciar
window.addEventListener('DOMContentLoaded', updateStats);