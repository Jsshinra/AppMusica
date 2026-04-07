from faster_whisper import WhisperModel
import logging
import os
import math

class STTEngine:
    def __init__(self, model_size="base"):
        self.model_size = model_size
        logging.info(f"Cargando modelo whisper: {model_size}")
        # Forzar CPU de entrada para evitar el crash de "cublas64_12.dll" nativo de ctranslate2
        try:
            self.model = WhisperModel(model_size, device="cpu", compute_type="int8")
        except Exception as e:
            logging.error(f"Error loading model with int8 en cpu, trying compute_type='default': {e}")
            self.model = WhisperModel(model_size, device="cpu", compute_type="default")
        
    def transcribe(self, audio_path):
        try:
            segments, info = self.model.transcribe(audio_path, language="es", beam_size=5, vad_filter=True, condition_on_previous_text=False)
            # Evaluar confianza: combinamos probabilidad de idioma con promedios de 'no_speech_prob' u otros
            # Por simplicidad usamos info.language_probability que nos da que tan seguro esta del idioma
            # pero es mejor apoyarnos en que los segmentos tengan buen average log prob
            
            segs = list(segments)
            text = " ".join([segment.text for segment in segs]).strip()
            
            # Whisper da 'no_speech_prob' (probabilidad de que sea solo ruido)
            # Vamos a devolver la confianza basandonos en que NO es ruido
            if not segs:
                return text, 0.0
                
            # Calculamos la probabilidad de que sí sea voz hablada real
            is_speech_probs = [(1.0 - s.no_speech_prob) for s in segs]
            avg_speech_conf = sum(is_speech_probs) / len(is_speech_probs)
            
            return text, avg_speech_conf
        except Exception as e:
            logging.error(f"Error en transcripción: {e}")
            return "", 0.0
