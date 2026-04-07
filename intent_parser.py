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
    
    search_type = "song"
    if "playlist" in text or "lista" in text:
        search_type = "playlist"
    elif "album" in text or "álbum" in text or "disco" in text:
        search_type = "album"
    
    # Priority patterns (more specific to less specific)
    patterns = [
        r'quiero escuchar la playlist (.*)',
        r'quiero escuchar el album (.*)',
        r'quiero escuchar el disco (.*)',
        r'quiero escuchar la cancion (.*)',
        r'quiero escuchar la lista (.*)',
        r'quiero escuchar (.*)',
        r'reproducir la playlist (.*)',
        r'reproducir el album (.*)',
        r'reproducir el disco (.*)',
        r'reproducir la cancion (.*)',
        r'reproducir la lista (.*)',
        r'reproducir mi playlist (.*)',
        r'reproducir (.*)',
        r'reproduci (.*)',
        r'poneme la playlist (.*)',
        r'poneme el album (.*)',
        r'poneme el disco (.*)',
        r'poneme la de (.*)',
        r'poneme (.*)',
        r'pone la playlist (.*)',
        r'pone el album (.*)',
        r'pone el disco (.*)',
        r'pone la cancion (.*)',
        r'pone la lista (.*)',
        r'pone (.*)',
        r'busca la playlist (.*)',
        r'busca el album (.*)',
        r'busca el disco (.*)',
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
            
    # Clean the keyword if it's still in the query
    if search_type == "playlist":
        query = query.replace("playlist", "").replace("lista", "").strip()
    elif search_type == "album":
        query = query.replace("album", "").replace("álbum", "").replace("disco", "").strip()
        
    if not query or query in ["de", "mi", "musica"]:
        query = text.strip()

    return query, search_type
