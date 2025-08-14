import os
import json
import tempfile
import threading
import time
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import openai
from dotenv import load_dotenv
import pyaudio
import numpy as np
import soundfile as sf
from pydub import AudioSegment
import librosa

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
socketio = SocketIO(app, cors_allowed_origins="*")

# Configure OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

class AudioProcessor:
    def __init__(self):
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.is_recording = False
        self.audio_chunks = []
        self.sample_rate = 16000
        self.chunk_size = 1024
        self.channels = 1
        
    def start_recording(self):
        if self.is_recording:
            return
            
        self.is_recording = True
        self.audio_chunks = []
        
        self.stream = self.audio.open(
            format=pyaudio.paFloat32,
            channels=self.channels,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk_size
        )
        
        def record_audio():
            while self.is_recording:
                try:
                    data = self.stream.read(self.chunk_size, exception_on_overflow=False)
                    audio_data = np.frombuffer(data, dtype=np.float32)
                    self.audio_chunks.append(audio_data)
                    
                    # Send audio data to client for visualization
                    socketio.emit('audio_data', {
                        'data': audio_data.tolist(),
                        'timestamp': time.time()
                    })
                    
                except Exception as e:
                    print(f"Error recording audio: {e}")
                    break
                    
        self.record_thread = threading.Thread(target=record_audio)
        self.record_thread.start()
        
    def stop_recording(self):
        self.is_recording = False
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        if self.record_thread:
            self.record_thread.join()
            
    def get_audio_data(self):
        if not self.audio_chunks:
            return None
        return np.concatenate(self.audio_chunks)
    
    def save_audio(self, filename):
        audio_data = self.get_audio_data()
        if audio_data is not None:
            sf.write(filename, audio_data, self.sample_rate)
            return filename
        return None

# Initialize audio processor
audio_processor = AudioProcessor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_recording', methods=['POST'])
def start_recording():
    try:
        audio_processor.start_recording()
        return jsonify({'status': 'success', 'message': 'Recording started'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/stop_recording', methods=['POST'])
def stop_recording():
    try:
        audio_processor.stop_recording()
        
        # Save audio to temporary file
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
            audio_file = audio_processor.save_audio(temp_file.name)
        
        if audio_file:
            # Process audio with OpenAI Whisper for transcription
            transcript = transcribe_audio(audio_file)
            
            # Extract candidate details using GPT
            candidate_details = extract_candidate_details(transcript)
            
            # Clean up temporary file
            os.unlink(audio_file)
            
            return jsonify({
                'status': 'success',
                'transcript': transcript,
                'candidate_details': candidate_details
            })
        else:
            return jsonify({'status': 'error', 'message': 'No audio data recorded'})
            
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

def transcribe_audio(audio_file_path):
    """Transcribe audio using OpenAI Whisper API"""
    try:
        with open(audio_file_path, 'rb') as audio_file:
            transcript = openai.Audio.transcribe(
                model="whisper-1",
                file=audio_file,
                response_format="text"
            )
        return transcript
    except Exception as e:
        print(f"Error transcribing audio: {e}")
        return "Error transcribing audio"

def extract_candidate_details(transcript):
    """Extract candidate details using GPT-4"""
    try:
        prompt = f"""
        Based on the following interview transcript, extract and organize the candidate's details in a structured format:

        Transcript:
        {transcript}

        Please provide the following information in JSON format:
        - name: Candidate's name (if mentioned)
        - experience: Years of experience and relevant background
        - skills: Technical and soft skills mentioned
        - education: Educational background
        - current_role: Current or most recent position
        - key_achievements: Notable accomplishments mentioned
        - interview_notes: General observations and notes
        - strengths: Key strengths demonstrated
        - areas_of_concern: Any concerns or areas for improvement
        - overall_assessment: Brief overall assessment
        """

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert HR analyst. Extract candidate details from interview transcripts in a structured format."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.3
        )
        
        # Try to parse JSON response
        try:
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            # If JSON parsing fails, return the raw response
            return {
                "raw_response": response.choices[0].message.content,
                "transcript": transcript
            }
            
    except Exception as e:
        print(f"Error extracting candidate details: {e}")
        return {
            "error": str(e),
            "transcript": transcript
        }

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)