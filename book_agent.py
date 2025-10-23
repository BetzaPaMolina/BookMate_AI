import json
from datetime import datetime

class BookAgent:
    def __init__(self):
        # Biblioteca completa de libros organizados por categoría
        self.books = {
            "filosofia": [
                {
                    "titulo": "Memorias del subsuelo",
                    "autor": "Fiódor Dostoievski",
                    "descripcion": "Existencialismo, alienación e introspección profunda",
                    "color": "#6B9BC4",
                    "emoji": "🧠"
                },
                {
                    "titulo": "Crimen y castigo",
                    "autor": "Fiódor Dostoievski",
                    "descripcion": "Culpa, moral y redención en la Rusia zarista",
                    "color": "#9B8BC4",
                    "emoji": "⚖️"
                },
                {
                    "titulo": "Demian",
                    "autor": "Hermann Hesse",
                    "descripcion": "Identidad, crecimiento y espiritualidad",
                    "color": "#7BC4A4",
                    "emoji": "🌱"
                },
                {
                    "titulo": "Siddharta",
                    "autor": "Hermann Hesse",
                    "descripcion": "Búsqueda espiritual y sabiduría oriental",
                    "color": "#E0C47A",
                    "emoji": "🕉️"
                },
                {
                    "titulo": "El retrato de Dorian Gray",
                    "autor": "Oscar Wilde",
                    "descripcion": "Narcisismo, moralidad y decadencia del arte",
                    "color": "#9B8BC4",
                    "emoji": "🖼️"
                }
            ],
            "romance": [
                {
                    "titulo": "María",
                    "autor": "Jorge Isaacs",
                    "descripcion": "Amor imposible y romanticismo clásico latinoamericano",
                    "color": "#E07A7A",
                    "emoji": "💔"
                },
                {
                    "titulo": "Jane Eyre",
                    "autor": "Charlotte Brontë",
                    "descripcion": "Amor, independencia y fortaleza moral",
                    "color": "#D4A5C4",
                    "emoji": "💝"
                },
                {
                    "titulo": "Anna Karenina",
                    "autor": "León Tolstói",
                    "descripcion": "Amor, sociedad y dilemas morales en la Rusia imperial",
                    "color": "#E07AA4",
                    "emoji": "🌹"
                }
            ],
            "distopia": [
                {
                    "titulo": "1984",
                    "autor": "George Orwell",
                    "descripcion": "Totalitarismo, vigilancia masiva y control del pensamiento",
                    "color": "#6B7BC4",
                    "emoji": "👁️"
                },
                {
                    "titulo": "Rebelión en la granja",
                    "autor": "George Orwell",
                    "descripcion": "Corrupción del poder a través de una sátira animal",
                    "color": "#E07A7A",
                    "emoji": "🐷"
                },
                {
                    "titulo": "Fahrenheit 451",
                    "autor": "Ray Bradbury",
                    "descripcion": "Censura, quema de libros y libertad de pensamiento",
                    "color": "#E0C47A",
                    "emoji": "🔥"
                },
                {
                    "titulo": "Un mundo feliz",
                    "autor": "Aldous Huxley",
                    "descripcion": "Manipulación genética y felicidad artificial",
                    "color": "#7BC4A4",
                    "emoji": "💊"
                }
            ],
            "aventura": [
                {
                    "titulo": "La Odisea",
                    "autor": "Homero",
                    "descripcion": "Épica aventura de Odiseo regresando a casa",
                    "color": "#6B9BC4",
                    "emoji": "⛵"
                },
                {
                    "titulo": "Moby Dick",
                    "autor": "Herman Melville",
                    "descripcion": "Obsesión y aventura en los mares",
                    "color": "#6B7BC4",
                    "emoji": "🐋"
                }
            ],
            "clasica": [
                {
                    "titulo": "Los miserables",
                    "autor": "Victor Hugo",
                    "descripcion": "Justicia, redención y amor en la Francia revolucionaria",
                    "color": "#9B8BC4",
                    "emoji": "⚜️"
                },
                {
                    "titulo": "Los hermanos Karamázov",
                    "autor": "Fiódor Dostoievski",
                    "descripcion": "Ética, fe y dilemas morales familiares",
                    "color": "#6B9BC4",
                    "emoji": "👥"
                },
                {
                    "titulo": "La Divina Comedia",
                    "autor": "Dante Alighieri",
                    "descripcion": "Viaje épico por el infierno, purgatorio y paraíso",
                    "color": "#E07A7A",
                    "emoji": "🔱"
                }
            ],
            "realismo_magico": [
                {
                    "titulo": "Pedro Páramo",
                    "autor": "Juan Rulfo",
                    "descripcion": "Muerte, memoria y fantasmas en Comala",
                    "color": "#9B8BC4",
                    "emoji": "👻"
                }
            ],
            "motivacional": [
                {
                    "titulo": "El líder mentor",
                    "autor": "Tony Dungy",
                    "descripcion": "Liderazgo, fe y propósito de vida",
                    "color": "#7BC4A4",
                    "emoji": "💼"
                }
            ],
            "humor": [
                {
                    "titulo": "Soy un gato",
                    "autor": "Natsume Sōseki",
                    "descripcion": "Filosofía cotidiana e ironía social desde la perspectiva de un gato",
                    "color": "#E0C47A",
                    "emoji": "🐱"
                }
            ]
        }
        
        # Biblioteca completa como lista para mostrar en UI
        self.all_books = []
        for categoria in self.books.values():
            self.all_books.extend(categoria)
    
    def get_all_books(self):
        """Retorna todos los libros de la biblioteca"""
        return self.all_books
    
    def recomendar(self, estado_animo, genero):
        print(f"🔍 OBSERVACIÓN: Estado ánimo='{estado_animo}', Género='{genero}'")
        
        # OBSERVACIÓN
        observacion = {
            "estado_animo": estado_animo,
            "genero": genero,
            "timestamp": datetime.now().isoformat()
        }
        
        # RAZONAMIENTO - Reglas condicionales mejoradas
        libro = None
        regla = ""
        razon = ""
        
        # Prioridad 1: Género específico
        if genero.lower() in ["distopia", "distopía"]:
            libro = self.books["distopia"][0]  # 1984
            regla = "IF género == 'distopia' → Prioridad ALTA"
            razon = "Género distópico detectado - recomendando clásico del control totalitario"
            
        elif genero.lower() in ["filosofia", "filosofía"]:
            if estado_animo.lower() == "pensativo":
                libro = self.books["filosofia"][0]  # Memorias del subsuelo
                regla = "IF género == 'filosofia' AND estado == 'pensativo' → Prioridad ALTA"
                razon = "Estado pensativo + filosofía - obra existencialista perfecta para reflexión profunda"
            else:
                libro = self.books["filosofia"][3]  # Siddharta
                regla = "IF género == 'filosofia' → Prioridad ALTA"
                razon = "Búsqueda filosófica - obra sobre sabiduría y autodescubrimiento"
                
        elif genero.lower() == "aventura":
            libro = self.books["aventura"][0]  # La Odisea
            regla = "IF género == 'aventura' → Prioridad ALTA"
            razon = "Género aventura - épica clásica llena de viajes y hazañas heroicas"
            
        elif genero.lower() in ["clasica", "clásica"]:
            libro = self.books["clasica"][0]  # Los miserables
            regla = "IF género == 'clasica' → Prioridad ALTA"
            razon = "Literatura clásica - obra maestra sobre justicia y redención"
            
        elif genero.lower() == "romance" or genero.lower() == "novela":
            if estado_animo.lower() == "triste":
                libro = self.books["romance"][1]  # Jane Eyre
                regla = "IF género == 'romance' AND estado == 'triste' → Prioridad ALTA"
                razon = "Estado triste + romance - historia de amor que inspira fortaleza y superación"
            else:
                libro = self.books["romance"][0]  # María
                regla = "IF género == 'romance' → Prioridad ALTA"
                razon = "Romance clásico latinoamericano lleno de belleza y melancolía"
        
        # Prioridad 2: Estado de ánimo si no hay género específico o género no encontrado
        if not libro:
            if estado_animo.lower() == "triste":
                libro = self.books["motivacional"][0]  # El líder mentor
                regla = "IF estado_animo == 'triste' → Prioridad MEDIA"
                razon = "Estado triste detectado - libro motivacional para recuperar el ánimo y encontrar propósito"
                
            elif estado_animo.lower() == "pensativo":
                libro = self.books["filosofia"][0]  # Memorias del subsuelo
                regla = "IF estado_animo == 'pensativo' → Prioridad MEDIA"
                razon = "Estado pensativo - obra filosófica para introspección profunda"
                
            elif estado_animo.lower() == "feliz":
                libro = self.books["aventura"][0]  # La Odisea
                regla = "IF estado_animo == 'feliz' → Prioridad MEDIA"
                razon = "Estado feliz - aventura épica para disfrutar con energía positiva"
                
            elif estado_animo.lower() == "motivado":
                libro = self.books["clasica"][0]  # Los miserables
                regla = "IF estado_animo == 'motivado' → Prioridad MEDIA"
                razon = "Estado motivado - historia inspiradora de lucha y superación"
                
            elif estado_animo.lower() == "aburrido":
                libro = self.books["humor"][0]  # Soy un gato
                regla = "IF estado_animo == 'aburrido' → Prioridad MEDIA"
                razon = "Aburrimiento detectado - obra irónica y humorística para entretenerte con perspectiva única"
                
            else:
                libro = self.books["filosofia"][3]  # Siddharta (default)
                regla = "ELSE → Prioridad BAJA"
                razon = "Recomendación versátil - obra sobre búsqueda personal y sabiduría universal"
        
        print(f"🤔 RAZONAMIENTO: {regla}")
        print(f"🎯 ACCIÓN: Recomendar '{libro['titulo']}'")
        
        # ACCIÓN
        recomendacion = {
            "libro": libro,
            "proceso": {
                "observacion": observacion,
                "razonamiento": {
                    "regla": regla, 
                    "explicacion": razon
                },
                "accion": "Generar recomendación personalizada basada en biblioteca literaria"
            }
        }
        
        return recomendacion

# Para probar el agente directamente
if __name__ == "__main__":
    agente = BookAgent()
    print(f"📚 Total de libros en biblioteca: {len(agente.all_books)}")
    prueba = agente.recomendar("aburrido", "cualquiera")
    print("\n📖 RECOMENDACIÓN:", prueba["libro"]["titulo"])