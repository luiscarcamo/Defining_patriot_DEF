import pandas as pd
import re
from collections import Counter

# Cargar el archivo
df = pd.read_csv('Copia_acotada de patria_igram_18ago.xlsx - patria_igram_18ago.csv')

# Extraer el año para ver evolución si es necesario
def extract_year(date_str):
    try:
        return date_str.split(',')[1].strip().split(' ')[0]
    except:
        return None

df['Year'] = df['Date'].apply(extract_year)

# Definir diccionarios simplificados de léxico emocional (Heurístico)
# Basado en palabras clave comunes en el contexto del dataset
lexico_emociones = {
    'Orgullo/Patriotismo': ['patria', 'orgullo', 'honor', 'valiente', 'héroe', 'gloria', 'chilenidad', 'emoción', 'agradecidos', 'corazón'],
    'Miedo/Inseguridad': ['miedo', 'crimen', 'narco', 'peligro', 'amenaza', 'delincuencia', 'droga', 'robo', 'inseguridad', 'violencia', 'atentado'],
    'Enojo/Conflicto': ['odio', 'rechazo', 'funar', 'protesta', 'conflicto', 'ataque', 'vandalismo', 'indignación', 'tensión', 'pelea'],
    'Esperanza/Optimismo': ['esperanza', 'futuro', 'crecer', 'mejorar', 'avances', 'logro', 'éxito', 'oportunidad', 'paz', 'unión'],
    'Tristeza/Preocupación': ['preocupación', 'crisis', 'sequía', 'cesantía', 'pobreza', 'tragedia', 'víctima', 'dolor', 'luto', 'falta']
}

def analyze_emotions(text):
    text = str(text).lower()
    counts = {emocion: 0 for emocion in lexico_emociones}
    for emocion, palabras in lexico_emociones.items():
        for palabra in palabras:
            # Buscar palabra completa
            if re.search(r'\b' + palabra + r'\b', text):
                counts[emocion] += 1
    return counts

# Combinar columnas C y D
df['TextCombined'] = df['ImageText'].fillna('') + " " + df['Description'].fillna('')

# Aplicar análisis
emociones_df = df['TextCombined'].apply(analyze_emotions).apply(pd.Series)

# Resumen general
resumen_emociones = emociones_df.sum().sort_values(ascending=False)
resumen_por_año = pd.concat([df['Year'], emociones_df], axis=1).groupby('Year').sum()

print("Resumen General de Emociones (Frecuencia de términos asociados):")
print(resumen_emociones)
print("\nEvolución por Año:")
print(resumen_por_año)