import sounddevice as sd
import soundfile as sf
import numpy as np

def list_microphones():
    devices = sd.query_devices()
    mics = []
    seen = set()
    for i, dev in enumerate(devices):
        if dev['max_input_channels'] > 0:
            # Limpiar nombre base removiendo cositas de la api de windows
            name = dev['name']
            if name not in seen:
                seen.add(name)
                mics.append((i, name))
    return mics

def record_audio(max_duration=6, device_index=None, filename="temp.wav", sample_rate=16000, silence_threshold=0.005, silence_duration=2.0):
    frames = []
    chunk_size = int(sample_rate * 0.1) # 100ms chunks
    silence_frames_count = 0
    max_frames = int(max_duration * sample_rate / chunk_size)
    
    try:
        with sd.InputStream(samplerate=sample_rate, channels=1, dtype='float32', device=device_index) as stream:
            for _ in range(max_frames):
                data, overflowed = stream.read(chunk_size)
                frames.append(data)
                
                # RMS amplitude
                rms = np.sqrt(np.mean(data**2))
                
                if rms < silence_threshold:
                    silence_frames_count += 1
                else:
                    silence_frames_count = 0
                    
                if silence_frames_count > (silence_duration / 0.1):
                    # Cut early due to silence
                    break
                    
        audio_data = np.concatenate(frames, axis=0)
        sf.write(filename, audio_data, sample_rate)
        return filename
    except Exception as e:
        import logging
        logging.error(f"Error recording audio: {e}")
        return None
