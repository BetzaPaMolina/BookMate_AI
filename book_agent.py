import json
from datetime import datetime

class BookAgent:
    def __init__(self):
        self.books = {
            "distopia": {
                "titulo": "1984", 
                "autor": "George Orwell",
                "descripcion": "Clásico distópico sobre control gubernamental y libertad individual"
            },
            "esperanzador": {
                "titulo": "El Alquimista", 
                "autor": "Paulo Coelho",
                "descripcion": "Viaje inspirador sobre seguir tus sueños y encontrar tu propósito"
            },
            "filosofia": {
                "titulo": "El Mundo de Sofía", 
                "autor": "Jostein Gaarder",
                "descripcion": "Novela que introduce la filosofía de manera accesible y reflexiva"
            },
            "aventura": {
                "titulo": "La Isla del Tesoro", 
                "autor": "Robert Louis Stevenson",
                "descripcion": "Emocionante aventura sobre búsquedas de tesoros y viajes épicos"
            },
            "default": {
                "titulo": "Cien Años de Soledad", 
                "autor": "Gabriel García Márquez",
                "descripcion": "Obra maestra del realismo mágico latinoamericano"
            }
        }
    
    def recomendar(self, estado_animo, genero):
        print(f"🔍 OBSERVACIÓN: Estado ánimo='{estado_animo}', Género='{genero}'")
        
        # OBSERVACIÓN
        observacion = {
            "estado_animo": estado_animo,
            "genero": genero,
            "timestamp": datetime.now().isoformat()
        }
        
        # RAZONAMIENTO - Reglas condicionales
        if genero.lower() == "distopia":
            libro = self.books["distopia"]
            regla = "IF género == 'distopia' → Prioridad ALTA"
            razon = "Género específico detectado - recomendar clásico del género"
            
        elif estado_animo.lower() == "triste":
            libro = self.books["esperanzador"]
            regla = "IF estado_animo == 'triste' → Prioridad MEDIA" 
            razon = "Estado triste detectado - recomendar lectura esperanzadora"
            
        elif estado_animo.lower() == "pensativo":
            libro = self.books["filosofia"]
            regla = "IF estado_animo == 'pensativo' → Prioridad MEDIA"
            razon = "Estado pensativo detectado - recomendar obra reflexiva"
            
        elif estado_animo.lower() == "feliz" or estado_animo.lower() == "aventurero":
            libro = self.books["aventura"]
            regla = "IF estado_animo == 'feliz/aventurero' → Prioridad MEDIA"
            razon = "Estado positivo detectado - recomendar aventura emocionante"
            
        else:
            libro = self.books["default"]
            regla = "ELSE → Prioridad BAJA"
            razon = "Recomendación por defecto - obra maestra universal"
        
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
                "accion": "Generar recomendación personalizada"
            }
        }
        
        return recomendacion

# Para probar el agente directamente
if __name__ == "__main__":
    agente = BookAgent()
    prueba = agente.recomendar("triste", "novela")
    print("\n📖 RECOMENDACIÓN:", prueba["libro"]["titulo"])