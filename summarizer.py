import re
from collections import Counter

def summarize_text(text, percentage=30):
    """
    Genera un resumen del texto usando extracción de oraciones más importantes
    percentage: porcentaje del texto original a mantener (por defecto 30%)
    """
    if not text or len(text.strip()) < 100:
        return text
    
    # Dividir en oraciones
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    if len(sentences) < 3:
        return text
    
    # Calcular puntuación de oraciones
    words = re.findall(r'\b\w+\b', text.lower())
    word_freq = Counter(words)
    
    # Eliminar palabras comunes (stop words en español)
    stop_words = {
        'el', 'la', 'de', 'que', 'y', 'a', 'en', 'un', 'es', 'se', 'no', 'por',
        'con', 'su', 'para', 'una', 'o', 'del', 'al', 'lo', 'como', 'más',
        'pero', 'sus', 'le', 'ya', 'o', 'este', 'sí', 'porque', 'esta', 'son',
        'entre', 'está', 'cuando', 'muy', 'sin', 'sobre', 'ser', 'tiene',
        'también', 'me', 'hasta', 'hay', 'donde', 'han', 'quien', 'están',
        'estado', 'desde', 'todo', 'nos', 'durante', 'estados', 'todos',
        'uno', 'les', 'ni', 'contra', 'otros', 'fueron', 'ese', 'eso', 'había',
        'ante', 'ellos', 'era', 'éramos', 'eran', 'eras', 'eres', 'esa', 'esas',
        'este', 'estemos', 'esto', 'estos', 'estoy', 'estuvo', 'estuve',
        'estuviera', 'estuviese', 'estuviesen', 'estuviesemos', 'esté',
        'estéis', 'estén', 'estés', 'estábamos', 'estabais', 'estaban',
        'estabas', 'estaba', 'estada', 'estadas', 'estado', 'estados',
        'estatua'
    }
    
    for word in stop_words:
        word_freq.pop(word, None)
    
    # Puntuación de oraciones
    sentence_scores = {}
    for i, sentence in enumerate(sentences):
        words_in_sentence = re.findall(r'\b\w+\b', sentence.lower())
        score = sum(word_freq.get(word, 0) for word in words_in_sentence)
        sentence_scores[i] = score
    
    # Seleccionar top oraciones
    num_sentences = max(1, int(len(sentences) * percentage / 100))
    top_sentences = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)[:num_sentences]
    
    # Mantener orden original
    top_sentences = sorted(top_sentences, key=lambda x: x[0])
    
    # Reconstruir resumen
    summary = '. '.join([sentences[i] for i, _ in top_sentences])
    
    if summary and not summary.endswith('.'):
        summary += '.'
    
    return summary

def extract_keywords(text, num_keywords=10):
    """
    Extrae las palabras clave más importantes del texto
    """
    words = re.findall(r'\b\w+\b', text.lower())
    
    stop_words = {
        'el', 'la', 'de', 'que', 'y', 'a', 'en', 'un', 'es', 'se', 'no', 'por',
        'con', 'su', 'para', 'una', 'o', 'del', 'al', 'lo', 'como', 'más',
        'pero', 'sus', 'le', 'ya', 'este', 'sí', 'porque', 'esta', 'son',
        'entre', 'está', 'cuando', 'muy', 'sin', 'sobre', 'ser', 'tiene',
        'también', 'me', 'hasta', 'hay', 'donde', 'han', 'quien', 'están'
    }
    
    words = [w for w in words if w not in stop_words and len(w) > 3]
    word_freq = Counter(words)
    
    keywords = word_freq.most_common(num_keywords)
    return [word for word, _ in keywords]

def create_outline(text):
    """
    Crea un esquema o outline del texto basado en palabras clave
    """
    keywords = extract_keywords(text, num_keywords=15)
    
    # Agrupar párrafos por palabra clave
    paragraphs = text.split('\n\n')
    outline = {}
    
    for keyword in keywords:
        outline[keyword] = []
        for para in paragraphs:
            if keyword.lower() in para.lower():
                outline[keyword].append(para[:100] + '...')
    
    return outline

if __name__ == "__main__":
    sample_text = """
    Python es un lenguaje de programación versátil y poderoso. Se utiliza en una variedad de campos como 
    desarrollo web, ciencia de datos, inteligencia artificial y automatización. Python es conocido por su 
    sintaxis clara y legible que lo hace accesible para principiantes. Muchas empresas grandes como Google, 
    Facebook y Netflix utilizan Python en sus sistemas. El ecosistema de librerías de Python es muy rico, 
    con paquetes como NumPy, Pandas y TensorFlow que facilitan tareas complejas.
    """
    
    print("Texto original:")
    print(sample_text)
    print("\nResumen (30%):")
    print(summarize_text(sample_text, percentage=30))
    print("\nPalabras clave:")
    print(extract_keywords(sample_text))
