# Configuration file for AI Interview Note Taker

# Audio Recording Settings
AUDIO_CONFIG = {
    'sample_rate': 16000,        # Audio sample rate (Hz)
    'chunk_size': 1024,          # Audio chunk size for processing
    'channels': 1,               # Number of audio channels (1 = mono, 2 = stereo)
    'format': 'paFloat32'        # Audio format (paFloat32, paInt16, etc.)
}

# Real-time Transcription Settings
TRANSCRIPTION_CONFIG = {
    'interval': 3.0,             # Transcription interval in seconds
    'min_audio_length': 1.0,     # Minimum audio length to transcribe (seconds)
    'max_audio_length': 10.0,    # Maximum audio length per chunk (seconds)
    'overlap': 0.5               # Overlap between chunks (seconds)
}

# OpenAI API Settings
OPENAI_CONFIG = {
    'whisper_model': 'whisper-1',    # Whisper model to use
    'gpt_model': 'gpt-4',            # GPT model for analysis
    'max_tokens': 1000,              # Maximum tokens for GPT response
    'temperature': 0.3                # Temperature for GPT response
}

# Flask Settings
FLASK_CONFIG = {
    'host': '0.0.0.0',
    'port': 5000,
    'debug': True,
    'secret_key': 'your-secret-key-here'
}

# Audio Processing Settings
PROCESSING_CONFIG = {
    'buffer_size': 48000,        # Audio buffer size (3 seconds at 16kHz)
    'silence_threshold': 0.01,   # Silence detection threshold
    'noise_reduction': True,     # Enable noise reduction
    'normalize_audio': True      # Normalize audio levels
}