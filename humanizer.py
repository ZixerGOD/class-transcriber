import re

def humanize_text(text):
    """
    Humaniza texto generado por IA, haciéndolo más natural y legible
    """
    if not text:
        return ""
    
    # Eliminar espacios múltiples
    text = re.sub(r'\s+', ' ', text)
    
    # Capitalizar primera letra de cada oración
    sentences = text.split('.')
    humanized_sentences = []
    
    for sentence in sentences:
        sentence = sentence.strip()
        if sentence:
            # Capitalizar primera letra
            sentence = sentence[0].upper() + sentence[1:] if len(sentence) > 1 else sentence.upper()
            humanized_sentences.append(sentence)
    
    text = '. '.join(humanized_sentences)
    
    # Agregar punto final si no existe
    if text and not text.endswith('.'):
        text += '.'
    
    # Mejorar puntuación común
    text = re.sub(r'\s+([.,!?;:])', r'\1', text)  # Eliminar espacios antes de puntuación
    text = re.sub(r'([.,!?;:])\s*', r'\1 ', text)  # Agregar espacio después de puntuación
    text = re.sub(r'\s+', ' ', text)  # Limpiar espacios múltiples nuevamente
    
    # Mejorar palabras comunes mal escritas
    replacements = {
        r'\beh\b': 'eh',
        r'\bum\b': '',
        r'\buh\b': '',
        r'\bemm\b': '',
        r'\bahh\b': '',
        r'\s+': ' ',
    }
    
    for pattern, replacement in replacements.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    
    # Limpiar espacios finales
    text = text.strip()
    
    # Organizar en párrafos (cada 3-4 oraciones)
    sentences = text.split('. ')
    paragraphs = []
    current_paragraph = []
    
    for i, sentence in enumerate(sentences):
        current_paragraph.append(sentence)
        if (i + 1) % 4 == 0 or i == len(sentences) - 1:
            paragraphs.append('. '.join(current_paragraph) + ('.' if not sentence.endswith('.') else ''))
            current_paragraph = []
    
    text = '\n\n'.join(paragraphs)
    
    return text

def improve_readability(text):
    """
    Mejora la legibilidad del texto agregando formato y estructura
    """
    if not text:
        return ""
    
    # Eliminar muletillas y repeticiones excesivas
    text = re.sub(r'\b(\w+)\s+\1\b', r'\1', text, flags=re.IGNORECASE)
    
    # Mejorar conectores
    text = re.sub(r'\s+y\s+y\s+', ' y ', text)
    text = re.sub(r'\s+pero\s+pero\s+', ' pero ', text)
    
    # Capitalizar nombres propios comunes en educación
    proper_nouns = ['Python', 'JavaScript', 'Java', 'SQL', 'HTML', 'CSS', 'React', 
                    'Node', 'Git', 'Linux', 'Windows', 'Mac', 'Google', 'Microsoft']
    
    for noun in proper_nouns:
        text = re.sub(rf'\b{noun}\b', noun, text, flags=re.IGNORECASE)
    
    return text

if __name__ == "__main__":
    # Ejemplo de uso
    sample_text = "eh bueno entonces um vamos a hablar sobre python  python es un lenguaje de programación  muy popular  eh muy usado en ciencia de datos  y  y machine learning"
    
    print("Texto original:")
    print(sample_text)
    print("\nTexto humanizado:")
    print(humanize_text(sample_text))
