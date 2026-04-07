import re
import unicodedata

def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])

def parse_intent(transcribed_text):
    text = transcribed_text.lower()
    text = remove_accents(text)
    # Remove filler words or leading words
    # Punctuation cleaning
    text = re.sub(r'[^\w\s]', '', text)
    
    is_playlist = False
    if "playlist" in text or "lista" in text:
        is_playlist = True
    
    # Priority patterns (more specific to less specific)
    patterns = [
        r'quiero escuchar la playlist (.*)',
        r'quiero escuchar la cancion (.*)',
        r'quiero escuchar la lista (.*)',
        r'quiero escuchar (.*)',
        r'reproducir la playlist (.*)',
        r'reproducir la cancion (.*)',
        r'reproducir la lista (.*)',
        r'reproducir mi playlist (.*)',
        r'reproducir (.*)',
        r'reproduci (.*)',
        r'poneme la playlist (.*)',
        r'poneme la de (.*)',
        r'poneme (.*)',
        r'pone la playlist (.*)',
        r'pone la cancion (.*)',
        r'pone la lista (.*)',
        r'pone (.*)',
        r'busca la playlist (.*)',
        r'busca la cancion (.*)',
        r'buscar (.*)',
        r'busca (.*)'
    ]
    
    query = text.strip()
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            query = match.group(1).strip()
            break
            
    # Clean the word playlist if it's still in the query
    if is_playlist:
        query = query.replace("playlist", "").replace("lista", "").strip()
        # Si quedó vacío el query o es irrelevante
        if not query or query in ["de", "mi", "musica"]:
            query = text.strip()

    return query, is_playlist
