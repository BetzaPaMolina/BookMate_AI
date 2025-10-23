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
const moodBtns = document.querySelectorAll('.mood-btn');
const estadoAnimoInput = document.getElementById('estado_animo');
const sendBtn = document.getElementById('send-btn');

// Mood selection
moodBtns.forEach(btn => {
    btn.addEventListener('click', function() {
        moodBtns.forEach(b => b.classList.remove('active'));
        this.classList.add('active');
        estadoAnimoInput.value = this.dataset.mood;
    });
});

// Form submission
form.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const estadoAnimo = estadoAnimoInput.value;
    const genero = document.getElementById('genero').value;
    
    if (!estadoAnimo || !genero) {
        addMessage('bot', '⚠️ Por favor selecciona tu estado de ánimo y género preferido.');
        return;
    }

    // Add user message
    const generoText = document.getElementById('genero').selectedOptions[0].text;
    addMessage('user', `Estoy ${estadoAnimo} y me gustaría leer ${generoText}`);
    
    // Show typing indicator
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
                estado_animo: estadoAnimo,
                genero: genero
            })
        });
        
        const data = await response.json();
        
        // Remove typing indicator
        document.getElementById('typing')?.remove();
        
        if (data.success) {
            displayRecommendation(data.recommendation);
        } else {
            addMessage('bot', '❌ ' + data.error);
        }
        
    } catch (error) {
        document.getElementById('typing')?.remove();
        addMessage('bot', '❌ Error de conexión con el servidor');
        console.error('Error:', error);
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
            ${data.proceso.razonamiento.explicacion}
        </div>
        <div class="quick-actions">
            <button class="quick-btn" onclick="alert('Función en desarrollo')">📚 Más info</button>
            <button class="quick-btn" onclick="alert('Función en desarrollo')">🔖 Guardar</button>
        </div>
        <div class="message-time">${new Date().toLocaleTimeString('es-ES', {hour: '2-digit', minute:'2-digit'})}</div>
    `;
    
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
    
    // Show process info
    setTimeout(() => {
        addMessage('bot', `
            📊 <strong>Proceso del Agente:</strong><br><br>
            👀 <strong>Observación:</strong> Detecté que estás ${data.proceso.observacion.estado_animo} y buscas ${data.proceso.observacion.genero}<br><br>
            🤔 <strong>Razonamiento:</strong> ${data.proceso.razonamiento.regla}<br><br>
            ✅ <strong>Acción:</strong> ${data.proceso.accion}
        `);
    }, 500);
}

function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}