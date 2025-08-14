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

# Speaker Diarization Settings
SPEAKER_CONFIG = {
    'enabled': True,             # Enable speaker diarization
    'speaker_count': 2,          # Expected number of speakers
    'speaker_labels': ['Interviewer', 'Candidate'],  # Speaker labels
    'diarization_method': 'simple',  # 'simple' or 'advanced'
    'confidence_threshold': 0.7,  # Minimum confidence for speaker assignment
    'segment_min_duration': 0.5,  # Minimum segment duration (seconds)
    'segment_max_duration': 30.0  # Maximum segment duration (seconds)
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

# Real-time Processing Settings
REALTIME_CONFIG = {
    'background_processing': True,    # Process transcription in background
    'show_live_updates': False,      # Don't show live transcript updates
    'store_intermediate_results': True,  # Store all transcription chunks
    'final_processing_delay': 1.0    # Delay before final processing (seconds)
}