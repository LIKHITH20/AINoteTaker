import os
import json
import tempfile
import threading
import time
import queue
import base64
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from openai import OpenAI
from dotenv import load_dotenv
import pyaudio
import numpy as np
import soundfile as sf
from pydub import AudioSegment
import librosa
import io
from config import AUDIO_CONFIG, TRANSCRIPTION_CONFIG, OPENAI_CONFIG, FLASK_CONFIG, SPEAKER_CONFIG, REALTIME_CONFIG

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = FLASK_CONFIG['secret_key']
socketio = SocketIO(app, cors_allowed_origins="*")

# Configure OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

class RealTimeAudioProcessor:
    def __init__(self):
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.is_recording = False
        self.audio_chunks = []
        self.sample_rate = AUDIO_CONFIG['sample_rate']
        self.chunk_size = AUDIO_CONFIG['chunk_size']
        self.channels = AUDIO_CONFIG['channels']
        
        # Real-time transcription settings
        self.transcription_interval = TRANSCRIPTION_CONFIG['interval']
        self.audio_buffer = []
        self.last_transcription_time = 0
        self.transcription_queue = queue.Queue()
        self.transcription_thread = None
        
        # Store live transcripts with speaker information
        self.live_transcripts = []
        self.transcript_lock = threading.Lock()
        
        # Speaker diarization settings
        self.speaker_count = SPEAKER_CONFIG['speaker_count']
        self.speaker_labels = SPEAKER_CONFIG['speaker_labels']
        self.diarization_method = SPEAKER_CONFIG['diarization_method']
        self.confidence_threshold = SPEAKER_CONFIG['confidence_threshold']
        
    def start_recording(self):
        if self.is_recording:
            return
            
        self.is_recording = True
        self.audio_chunks = []
        self.audio_buffer = []
        self.last_transcription_time = time.time()
        
        # Clear previous transcripts
        with self.transcript_lock:
            self.live_transcripts = []
        
        self.stream = self.audio.open(
            format=getattr(pyaudio, AUDIO_CONFIG['format']),
            channels=self.channels,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk_size
        )
        
        # Start transcription thread
        self.transcription_thread = threading.Thread(target=self._transcription_worker)
        self.transcription_thread.daemon = True
        self.transcription_thread.start()
        
        def record_audio():
            while self.is_recording:
                try:
                    data = self.stream.read(self.chunk_size, exception_on_overflow=False)
                    audio_data = np.frombuffer(data, dtype=np.float32)
                    self.audio_chunks.append(audio_data)
                    self.audio_buffer.append(audio_data)
                    
                    # Send audio data to client for visualization
                    socketio.emit('audio_data', {
                        'data': audio_data.tolist(),
                        'timestamp': time.time()
                    })
                    
                    # Check if it's time for transcription
                    current_time = time.time()
                    if current_time - self.last_transcription_time >= self.transcription_interval:
                        self._schedule_transcription()
                        self.last_transcription_time = current_time
                    
                except Exception as e:
                    print(f"Error recording audio: {e}")
                    break
                    
        self.record_thread = threading.Thread(target=record_audio)
        self.record_thread.start()
        
    def _schedule_transcription(self):
        """Schedule audio buffer for transcription with speaker diarization"""
        if len(self.audio_buffer) > 0:
            # Convert buffer to audio data
            audio_data = np.concatenate(self.audio_buffer)
            
            # Convert to 16-bit PCM for Whisper
            audio_data_16bit = (audio_data * 32767).astype(np.int16)
            
            # Create temporary audio file
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                sf.write(temp_file.name, audio_data_16bit, self.sample_rate)
                self.transcription_queue.put(temp_file.name)
            
            # Clear buffer for next chunk
            self.audio_buffer = []
    
    def _transcription_worker(self):
        """Background worker for transcription with speaker diarization"""
        while self.is_recording:
            try:
                # Get audio file from queue
                audio_file = self.transcription_queue.get(timeout=1)
                if audio_file:
                    # Transcribe the audio chunk with speaker diarization
                    transcript_data = self._transcribe_with_speakers(audio_file)
                    
                    if transcript_data and hasattr(transcript_data, 'segments') and transcript_data.segments:
                        # Store transcript with speaker information
                        with self.transcript_lock:
                            for i, segment in enumerate(transcript_data.segments):
                                # Create a copy of segment data that we can modify
                                segment_data = {
                                    'text': segment.text.strip(),
                                    'start': getattr(segment, 'start', 0),
                                    'end': getattr(segment, 'end', 0),
                                    'speaker': self._assign_speaker(i)
                                }
                                
                                transcript_item = {
                                    'text': segment_data['text'],
                                    'speaker': segment_data['speaker'],
                                    'start_time': segment_data['start'],
                                    'end_time': segment_data['end'],
                                    'timestamp': time.time(),
                                    'time': time.strftime('%H:%M:%S')
                                }
                                self.live_transcripts.append(transcript_item)
                                
                                # Send real-time transcript update to client
                                socketio.emit('live_transcript', {
                                    'text': transcript_item['text'],
                                    'speaker': transcript_item['speaker'],
                                    'timestamp': transcript_item['timestamp'],
                                    'time': transcript_item['time']
                                })
                                
                                print(f"Live transcript sent: {transcript_item['speaker']}: {transcript_item['text']}")
                    
                    # Clean up temporary file
                    try:
                        os.unlink(audio_file)
                    except:
                        pass
                        
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Error in transcription worker: {e}")
                continue
    
    def _assign_speaker(self, segment_index):
        """Assign speaker label based on segment index"""
        if segment_index % 2 == 0:
            return self.speaker_labels[0]  # Interviewer
        else:
            return self.speaker_labels[1]  # Candidate
    
    def _transcribe_with_speakers(self, audio_file_path):
        """Transcribe audio with speaker diarization using OpenAI Whisper"""
        try:
            # First, transcribe with timestamps using new OpenAI API
            with open(audio_file_path, 'rb') as audio_file:
                response = client.audio.transcriptions.create(
                    model=OPENAI_CONFIG['whisper_model'],
                    file=audio_file,
                    response_format="verbose_json",
                    timestamp_granularities=["segment"]
                )
            
            print(f"Transcription response received with {len(response.segments) if hasattr(response, 'segments') else 0} segments")
            return response
            
        except Exception as e:
            print(f"Error transcribing audio with speakers: {e}")
            return None
        
    def stop_recording(self):
        self.is_recording = False
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        if self.record_thread:
            self.record_thread.join()
        
        # Process final audio buffer
        if len(self.audio_buffer) > 0:
            self._schedule_transcription()
        
        # Wait for transcription queue to empty
        if self.transcription_thread:
            self.transcription_thread.join(timeout=5)
            
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
    
    def get_full_transcript(self):
        """Get the complete transcript from all recorded chunks with speaker information"""
        with self.transcript_lock:
            if not self.live_transcripts:
                return "No transcript available"
            
            # Combine all transcripts with speaker information
            full_text = ""
            for item in self.live_transcripts:
                speaker_label = item.get('speaker', 'Unknown')
                full_text += f"[{item['time']}] {speaker_label}: {item['text']}\n\n"
            
            return full_text.strip()
    
    def get_transcript_summary(self):
        """Get a summary of all transcripts for analysis"""
        with self.transcript_lock:
            if not self.live_transcripts:
                return ""
            
            # Combine all transcripts into one text for GPT analysis
            return " ".join([item['text'] for item in self.live_transcripts])
    
    def get_speaker_statistics(self):
        """Get statistics about speaker participation"""
        with self.transcript_lock:
            if not self.live_transcripts:
                return {}
            
            speaker_stats = {}
            for item in self.live_transcripts:
                speaker = item.get('speaker', 'Unknown')
                if speaker not in speaker_stats:
                    speaker_stats[speaker] = {
                        'segments': 0,
                        'words': 0,
                        'total_duration': 0
                    }
                
                speaker_stats[speaker]['segments'] += 1
                speaker_stats[speaker]['words'] += len(item['text'].split())
                duration = item.get('end_time', 0) - item.get('start_time', 0)
                speaker_stats[speaker]['total_duration'] += duration
            
            return speaker_stats

# Initialize audio processor
audio_processor = RealTimeAudioProcessor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_recording', methods=['POST'])
def start_recording():
    try:
        audio_processor.start_recording()
        return jsonify({'status': 'success', 'message': 'Recording started with real-time transcription'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/stop_recording', methods=['POST'])
def stop_recording():
    try:
        audio_processor.stop_recording()
        
        # Add delay before final processing if configured
        if REALTIME_CONFIG['final_processing_delay'] > 0:
            time.sleep(REALTIME_CONFIG['final_processing_delay'])
        
        # Save audio to temporary file
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
            audio_file = audio_processor.save_audio(temp_file.name)
        
        if audio_file:
            # Get the full transcript from all chunks
            full_transcript = audio_processor.get_full_transcript()
            transcript_summary = audio_processor.get_transcript_summary()
            speaker_stats = audio_processor.get_speaker_statistics()
            
            # Extract candidate details using GPT
            candidate_details = extract_candidate_details(transcript_summary)
            
            # Add speaker statistics to candidate details
            if speaker_stats:
                candidate_details['speaker_statistics'] = speaker_stats
            
            # Clean up temporary file
            os.unlink(audio_file)
            
            return jsonify({
                'status': 'success',
                'transcript': full_transcript,
                'candidate_details': candidate_details,
                'speaker_stats': speaker_stats
            })
        else:
            return jsonify({'status': 'error', 'message': 'No audio data recorded'})
            
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

def transcribe_audio(audio_file_path):
    """Transcribe audio using OpenAI Whisper API"""
    try:
        with open(audio_file_path, 'rb') as audio_file:
            response = client.audio.transcriptions.create(
                model=OPENAI_CONFIG['whisper_model'],
                file=audio_file,
                response_format="text"
            )
        return response
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

        response = client.chat.completions.create(
            model=OPENAI_CONFIG['gpt_model'],
            messages=[
                {"role": "system", "content": "You are an expert HR analyst. Extract candidate details from interview transcripts in a structured format."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=OPENAI_CONFIG['max_tokens'],
            temperature=OPENAI_CONFIG['temperature']
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
    socketio.run(app, debug=FLASK_CONFIG['debug'], host=FLASK_CONFIG['host'], port=FLASK_CONFIG['port'])