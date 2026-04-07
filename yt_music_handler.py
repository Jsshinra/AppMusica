from ytmusicapi import YTMusic
import logging
import re

class YTMusicHandler:
    def __init__(self):
        self.yt = YTMusic()
        
    def search_and_process(self, query, is_playlist=False):
        try:
            if is_playlist:
                results = self.yt.search(query, filter="playlists")
                if not results:
                    return {"type": "none", "results": []}
                # Return the top playlists
                return {
                    "type": "playlist",
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
        # item can be a song (videoId) or a playlist (browseId)
        if 'videoId' in item:
            # En youtube music un song se reproduce asi (a veces con un playlist dict)
            return f"https://music.youtube.com/watch?v={item['videoId']}"
        elif 'browseId' in item:
            # Playlists se pueden reproducir pasandolo como parametro un playlistId format
            # browseId for playlists usually starts with VLPL or PL
            # we need to get the real playlist id if it starts with VL
            pl_id = item['browseId']
            if pl_id.startswith('VL'):
                pl_id = pl_id[2:]
            return f"https://music.youtube.com/playlist?list={pl_id}"
        return "https://music.youtube.com"
