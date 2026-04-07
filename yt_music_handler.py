from ytmusicapi import YTMusic
import logging
import re

class YTMusicHandler:
    def __init__(self):
        self.yt = YTMusic()
        
    def search_and_process(self, query, search_type="song"):
        try:
            if search_type == "playlist":
                results = self.yt.search(query, filter="playlists")
                if not results:
                    return {"type": "none", "results": []}
                # Return the top playlists
                return {
                    "type": "playlist",
                    "results": results[:5] 
                }
            elif search_type == "album":
                results = self.yt.search(query, filter="albums")
                if not results:
                    return {"type": "none", "results": []}
                return {
                    "type": "album",
                    "results": results[:5] 
                }
            elif search_type == "artist":
                results = self.yt.search(query, filter="artists")
                if not results:
                    return {"type": "none", "results": []}
                return {
                    "type": "artist",
                    "results": results[:5] 
                }
                
            results = self.yt.search(query, filter="songs")
            if not results:
                results = self.yt.search(query, filter="videos")
                
            if not results:
                return {"type": "none", "results": []}
                
            bad_words = ['live', 'slowed', 'nightcore', 'remix', '8d', 'en vivo', 'instrumental']
            query_lower = query.lower()
            
            clean_results = []
            for r in results:
                title = r.get('title', '').lower()
                is_bad = any(bad in title for bad in bad_words)
                if is_bad and not any(bad in query_lower for bad in bad_words):
                    continue
                clean_results.append(r)
                
            if not clean_results:
                clean_results = results[:5]
                
            top_5 = clean_results[:5]
            
            exact_match = False
            best_res = top_5[0]
            title = best_res.get('title', '').lower()
            artist_name = best_res.get('artists', [{}])[0].get('name', '').lower()
            
            if artist_name and artist_name in query_lower and title in query_lower:
                exact_match = True
            elif query_lower == title or query_lower == f"{title} de {artist_name}":
                exact_match = True
                
            return {
                "type": "exact" if exact_match else "multiple",
                "results": top_5
            }
            
        except Exception as e:
            logging.error(f"Error en ytmusic búsqueda: {e}")
            return {"type": "none", "results": []}
            
    def get_url(self, item):
        # item can be a song (videoId), a playlist (browseId) or an album (playlistId or browseId)
        if 'videoId' in item and item['videoId']:
            return f"https://music.youtube.com/watch?v={item['videoId']}"
        elif 'shuffleId' in item:
            # Para reproducir automáticamente las mejores canciones de un artista
            return f"https://music.youtube.com/watch?list={item['shuffleId']}"
        elif 'radioId' in item:
            return f"https://music.youtube.com/watch?list={item['radioId']}"
        elif 'playlistId' in item:
            # Para albums o playlists que devuelven un playlistId, usar watch?list= para auto-play de la lista
            return f"https://music.youtube.com/watch?list={item['playlistId']}"
        elif 'browseId' in item:
            pl_id = item['browseId']
            if pl_id.startswith('VL'):
                pl_id = pl_id[2:]
            elif pl_id.startswith('MPREb_'):
                # Los álbumes que no listan playlistId a veces se pueden reproducir pasándolos con el prefijo correcto
                pass
            # Usar watch para que reproduzca la lista (auto-play)
            return f"https://music.youtube.com/watch?list={pl_id}"
        return "https://music.youtube.com"
