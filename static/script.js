document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('recommendation-form');
    const moodBtns = document.querySelectorAll('.mood-btn');
    const estadoAnimoInput = document.getElementById('estado_animo');
    const processSection = document.getElementById('process-section');
    const resultSection = document.getElementById('result-section');
    const loadingElement = document.getElementById('loading');

    // Selección de estado de ánimo
    moodBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            moodBtns.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            estadoAnimoInput.value = this.dataset.mood;
        });
    });

    // Envío del formulario
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const estadoAnimo = estadoAnimoInput.value;
        const genero = document.getElementById('genero').value;
        
        if (!estadoAnimo || !genero) {
            alert('Por favor selecciona tu estado de ánimo y género preferido');
            return;
        }
        
        showLoading();
        hideSections();
        
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
            
            if (data.success) {
                displayResults(data.recommendation);
            } else {
                alert('Error: ' + data.error);
            }
            
        } catch (error) {
            console.error('Error:', error);
            alert('Error de conexión con el servidor');
        } finally {
            hideLoading();
        }
    });
    
    function displayResults(data) {
        // Mostrar proceso del agente
        document.getElementById('observation-content').innerHTML = `
            <p><strong>Estado de ánimo:</strong> ${data.proceso.observacion.estado_animo}</p>
            <p><strong>Género preferido:</strong> ${data.proceso.observacion.genero}</p>
        `;
        
        document.getElementById('reasoning-content').innerHTML = `
            <p><strong>Regla aplicada:</strong> ${data.proceso.razonamiento.regla}</p>
            <p><strong>Explicación:</strong> ${data.proceso.razonamiento.explicacion}</p>
        `;
        
        document.getElementById('action-content').innerHTML = `
            <p><strong>Acción:</strong> ${data.proceso.accion}</p>
            <p><strong>Libro seleccionado:</strong> ${data.libro.titulo}</p>
        `;
        
        // Mostrar recomendación
        document.getElementById('book-title').textContent = data.libro.titulo;
        document.getElementById('book-author').textContent = `por ${data.libro.autor}`;
        document.getElementById('book-description').textContent = data.libro.descripcion;
        document.getElementById('recommendation-reason').innerHTML = `
            <strong>🤖 Por qué este libro:</strong><br>
            ${data.proceso.razonamiento.explicacion}
        `;
        
        // Mostrar secciones
        processSection.style.display = 'block';
        resultSection.style.display = 'block';
        
        // Scroll suave a los resultados
        resultSection.scrollIntoView({ behavior: 'smooth' });
    }
    
    function showLoading() {
        loadingElement.style.display = 'block';
    }
    
    function hideLoading() {
        loadingElement.style.display = 'none';
    }
    
    function hideSections() {
        processSection.style.display = 'none';
        resultSection.style.display = 'none';
    }
});