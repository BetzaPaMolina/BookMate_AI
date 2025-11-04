"""
Script para probar LOS CASOS REALES que mencionaste
"""

import os
import json
from smart_recommender import SmartRecommender

def print_sep():
    print("\n" + "="*80 + "\n")

def show_rec(user_msg, rec):
    print(f"\n👤 Usuario: '{user_msg}'")
    print(f"🎭 Emoción detectada: {rec['analisis']['emotion']} (confianza: {rec['analisis']['emotion_confidence']:.2f})")
    
    if rec['analisis'].get('special_contexts'):
        print(f"🎯 Contextos especiales: {', '.join(rec['analisis']['special_contexts'])}")
    
    print(f"📖 Libro recomendado: {rec['libro']['titulo']}")
    print(f"   Autor: {rec['libro']['autor']}")
    print(f"   Impacto: {rec['libro'].get('impacto', 'N/A')}")
    print(f"   Emociones del libro: {', '.join(rec['libro'].get('emociones', []))}")
    print(f"🧠 Score: {rec['analisis']['score']:.2f}")
    print(f"💡 {rec['explicacion']}")
    
    if rec.get('alternativas'):
        print(f"📚 Alternativas: {', '.join(rec['alternativas'][:2])}")

# Limpiar historial para empezar de cero
if os.path.exists('smart_history.json'):
    os.remove('smart_history.json')
    print("🧹 Historial limpiado para empezar de cero\n")

recommender = SmartRecommender()

print_sep()
print("🧪 PRUEBAS DE ANÁLISIS EMOCIONAL")
print_sep()

# Test 1: Nostálgica con esperanza
print("\n🔹 Test 1: Emoción mixta (nostalgia + esperanza)")
rec1 = recommender.recommend("Me siento nostálgica, pero con ganas de esperanza. ¿Qué me recomiendas?")
show_rec("Me siento nostálgica, pero con ganas de esperanza", rec1)

# Verificación
expected_impact = 'esperanzador'
actual_impact = rec1['libro'].get('impacto')
if actual_impact == expected_impact:
    print(f"\n✅ CORRECTO: Detectó que quieres esperanza (impacto: {actual_impact})")
else:
    print(f"\n⚠️ Detectó impacto '{actual_impact}' (esperaba '{expected_impact}')")

print_sep()

# Test 2: Enojada
print("\n🔹 Test 2: Emoción de enojo/frustración")
rec2 = recommender.recommend("Estoy enojada con el mundo. Quiero algo que me ayude a canalizarlo.")
show_rec("Estoy enojada con el mundo", rec2)

# Verificación
if rec2['analisis']['emotion'] in ['ansioso', 'pensativo']:
    print(f"\n✅ CORRECTO: Detectó emoción intensa ({rec2['analisis']['emotion']})")
else:
    print(f"\n⚠️ Detectó '{rec2['analisis']['emotion']}' (debería ser ansioso/pensativo)")

print_sep()

# Test 3: Vacía
print("\n🔹 Test 3: Sentimiento de vacío existencial")
rec3 = recommender.recommend("Hoy me siento vacía, como si nada tuviera sentido. ¿Tienes algo que me acompañe en eso?")
show_rec("Me siento vacía, como si nada tuviera sentido", rec3)

# Verificación
expected_books = ['Pedro Páramo', 'Memorias del subsuelo', 'Los hermanos Karamázov']
actual_book = rec3['libro']['titulo']
if actual_book in expected_books:
    print(f"\n✅ CORRECTO: Recomendó libro existencial ({actual_book})")
else:
    print(f"\n⚠️ Recomendó '{actual_book}' (esperaba uno de: {', '.join(expected_books)})")

print_sep()

# Test 4: Contradicción emocional
print("\n🔹 Test 4: Contradicción (feliz pero quiero llorar)")
rec4 = recommender.recommend("Estoy feliz, pero quiero algo que me haga llorar.")
show_rec("Estoy feliz, pero quiero algo que me haga llorar", rec4)

# Verificación
expected_emotions = ['triste', 'pensativo']
actual_emotion = rec4['analisis']['emotion']
if actual_emotion in expected_emotions:
    print(f"\n✅ CORRECTO: Detectó que realmente quieres tristeza ({actual_emotion})")
else:
    print(f"\n⚠️ Detectó '{actual_emotion}' (debería priorizar tristeza)")

print_sep()
print("🔁 PRUEBAS DE VARIABILIDAD Y MEMORIA")
print_sep()

# Test 5: Ya leí este libro
print("\n🔹 Test 5: Evitar libro ya leído")
# Marcar Pedro Páramo como ya recomendado
recommender.session_recommended.add('Pedro Páramo')
rec5 = recommender.recommend("Ya leí Pedro Páramo. Dame otra opción igual de triste pero diferente.")
show_rec("Ya leí Pedro Páramo, dame otra opción", rec5)

# Verificación
if rec5['libro']['titulo'] != 'Pedro Páramo':
    print(f"\n✅ CORRECTO: Evitó Pedro Páramo")
else:
    print(f"\n❌ ERROR: Repitió Pedro Páramo")

print_sep()

# Test 6: Sorpréndeme
print("\n🔹 Test 6: Solicitud de sorpresa/diversidad")
rec6 = recommender.recommend("Sorpréndeme con algo que nunca me hayas recomendado.")
show_rec("Sorpréndeme", rec6)

print_sep()
print("🧭 PRUEBAS DE CONTROL Y FILTROS")
print_sep()

# Test 7: Filtros específicos
print("\n🔹 Test 7: Filtro: feminista + protagonista fuerte")
rec7 = recommender.recommend("Quiero algo feminista, triste y con una protagonista fuerte.")
show_rec("Feminista con protagonista fuerte", rec7)

# Verificación
if 'Jane Eyre' in rec7['libro']['titulo']:
    print(f"\n✅ CORRECTO: Detectó los filtros y recomendó Jane Eyre")
else:
    print(f"\n⚠️ Recomendó '{rec7['libro']['titulo']}' (Jane Eyre sería ideal)")

print_sep()

# Test 8: Duelo sin deprimir
print("\n🔹 Test 8: Duelo pero esperanzador")
rec8 = recommender.recommend("¿Tienes algo sobre duelo, pero que no sea deprimente?")
show_rec("Duelo pero no deprimente", rec8)

# Verificación
expected_impact = 'esperanzador'
actual_impact = rec8['libro'].get('impacto')
has_no_empeorar = 'no_empeorar' in rec8['analisis'].get('special_contexts', [])

if actual_impact == expected_impact or has_no_empeorar:
    print(f"\n✅ CORRECTO: Detectó que no quieres algo deprimente (impacto: {actual_impact})")
else:
    print(f"\n⚠️ Recomendó impacto '{actual_impact}'")

print_sep()
print("🧪 PRUEBAS DE ESTRÉS Y CONTRADICCIÓN")
print_sep()

# Test 9: Triste pero no empeorar
print("\n🔹 Test 9: Triste pero no quiero empeorar")
rec9 = recommender.recommend("Estoy triste pero no quiero ponerme peor. ¿Qué me recomiendas?")
show_rec("Triste pero no quiero empeorar", rec9)

# Verificación
if 'no_empeorar' in rec9['analisis'].get('special_contexts', []):
    print(f"\n✅ CORRECTO: Detectó contexto 'no_empeorar'")
    
    if rec9['libro'].get('impacto') == 'esperanzador':
        print(f"✅ Recomendó libro esperanzador (correcto)")
    else:
        print(f"⚠️ Recomendó impacto '{rec9['libro'].get('impacto')}'")
else:
    print(f"\n⚠️ No detectó el contexto 'no_empeorar'")

print_sep()

# Test 10: Transformación
print("\n🔹 Test 10: Búsqueda de transformación")
rec10 = recommender.recommend("No sé cómo me siento. Solo recomiéndame algo que me transforme.")
show_rec("Algo que me transforme", rec10)

# Verificación
if rec10['libro'].get('impacto') == 'transformador' or 'intenso' in rec10['analisis'].get('special_contexts', []):
    print(f"\n✅ CORRECTO: Detectó búsqueda de transformación")
else:
    print(f"\n⚠️ Impacto: {rec10['libro'].get('impacto')}")

print_sep()
print("📊 ESTADÍSTICAS FINALES")
print_sep()

stats = recommender.get_learning_stats()
print(f"Total de interacciones: {stats['total_interactions']}")
print(f"Libros recomendados en sesión: {stats['session_recommended']}")

print("\n🎭 Top Emociones:")
for item in stats['top_emotions']:
    print(f"   {item['emotion']}: {item['count']} veces")

print("\n📚 Top Libros:")
for item in stats['top_books']:
    print(f"   {item['book']}: {item['count']} veces")

print("\n🧠 Preferencias Aprendidas:")
sorted_prefs = sorted(stats['preferences'].items(), key=lambda x: x[1], reverse=True)[:5]
for emotion, score in sorted_prefs:
    print(f"   {emotion}: {score:.2f}")

print_sep()
print("✅ PRUEBAS COMPLETADAS")
print("\nRevisa los resultados arriba. El sistema debería:")
print("  1. Detectar emociones complejas (nostalgia, vacío, enojo)")
print("  2. Entender contradicciones ('feliz pero quiero llorar')")
print("  3. Evitar repeticiones")
print("  4. Aplicar filtros específicos")
print("  5. Respetar contextos ('no empeorar', 'esperanza')")
print_sep()