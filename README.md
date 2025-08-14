# 🎤 AI Interview Note Taker - Real-time

A sophisticated AI-powered application that provides **real-time audio transcription** and intelligent candidate analysis during interviews. Built with Flask, WebSocket support, and OpenAI's advanced AI models.

## ✨ Features

- **🎙️ Real-time Audio Recording**: Capture interview audio with live visualization
- **⚡ Live Transcription**: **NEW!** Generate transcripts in real-time as the conversation happens (every 3 seconds)
- **📝 Continuous Updates**: See transcript chunks appear live during the interview
- **🤖 AI-Powered Analysis**: Extract candidate details using GPT-4
- **📊 Audio Visualization**: Real-time audio level monitoring and waveform display
- **💻 Modern Web Interface**: Responsive design with intuitive controls
- **🔒 Secure Processing**: Local audio processing with secure API calls
- **⚙️ Configurable**: Easy to adjust transcription intervals and settings

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- OpenAI API key
- Microphone access
- Modern web browser

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai-interview-note-taker
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env file with your OpenAI API key
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:5000`

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=your_openai_api_key_here
FLASK_SECRET_KEY=your_secret_key_here
FLASK_ENV=development
```

### Real-time Transcription Settings

Edit `config.py` to customize transcription behavior:

```python
TRANSCRIPTION_CONFIG = {
    'interval': 3.0,             # Transcription interval in seconds
    'min_audio_length': 1.0,     # Minimum audio length to transcribe
    'max_audio_length': 10.0,    # Maximum audio length per chunk
    'overlap': 0.5               # Overlap between chunks
}
```

### OpenAI API Setup

1. Visit [OpenAI Platform](https://platform.openai.com/)
2. Create an account and get your API key
3. Add the API key to your `.env` file

## 📱 Usage

### Recording an Interview

1. **Start Recording**: Click the "🎙️ Start Recording" button
2. **Grant Microphone Access**: Allow browser access to your microphone
3. **Watch Live Transcription**: See transcript chunks appear every 3 seconds
4. **Monitor Audio**: Watch real-time audio visualization and levels
5. **Stop Recording**: Click "⏹️ Stop Recording" when finished

### Real-time Transcription

**NEW!** The application now provides live transcription:

- **Continuous Processing**: Audio is transcribed every 3 seconds (configurable)
- **Live Updates**: Transcript chunks appear in real-time during the interview
- **Timestamped**: Each transcript chunk shows when it was captured
- **Immediate Feedback**: See what's being said as the conversation happens
- **No Waiting**: No need to wait until the end to see partial results

### Viewing Results

After stopping the recording, the application will:

1. **Process Final Audio**: Convert remaining audio to text
2. **Combine Transcripts**: Merge all live transcript chunks
3. **Analyze Content**: Extract candidate details using GPT-4
4. **Display Results**: Show complete transcript and structured candidate information

### Candidate Details Extracted

- **Personal Information**: Name, experience, education
- **Professional Background**: Current role, skills, achievements
- **Interview Assessment**: Strengths, concerns, overall evaluation
- **Technical Skills**: Programming languages, tools, frameworks
- **Soft Skills**: Communication, leadership, problem-solving

## 🏗️ Architecture

### Backend (Flask + Python)

- **Real-time Audio Processing**: Continuous audio capture and chunking
- **Live Transcription**: Background worker processes audio every 3 seconds
- **AI Integration**: OpenAI Whisper for transcription, GPT-4 for analysis
- **WebSocket Support**: Real-time communication with frontend
- **REST API**: Endpoints for recording control and result retrieval

### Frontend (HTML + JavaScript)

- **Real-time Audio**: Web Audio API for live audio processing
- **Live Transcript Display**: Shows transcript chunks as they arrive
- **Visualization**: Canvas-based audio waveform display
- **Responsive Design**: Mobile-friendly interface
- **Socket.IO**: Real-time updates and communication

### AI Models Used

- **OpenAI Whisper**: High-quality speech-to-text transcription
- **GPT-4**: Intelligent candidate detail extraction and analysis

## ⚙️ Configuration Options

### Audio Settings

```python
AUDIO_CONFIG = {
    'sample_rate': 16000,        # Audio quality
    'chunk_size': 1024,          # Processing chunk size
    'channels': 1,               # Mono recording
    'format': 'paFloat32'        # Audio format
}
```

### Transcription Settings

```python
TRANSCRIPTION_CONFIG = {
    'interval': 3.0,             # How often to transcribe
    'min_audio_length': 1.0,     # Minimum audio for transcription
    'max_audio_length': 10.0,    # Maximum chunk size
    'overlap': 0.5               # Overlap between chunks
}
```

### OpenAI Settings

```python
OPENAI_CONFIG = {
    'whisper_model': 'whisper-1',    # Transcription model
    'gpt_model': 'gpt-4',            # Analysis model
    'max_tokens': 1000,              # Response length
    'temperature': 0.3                # Creativity level
}
```

## 🔒 Security Features

- **Local Audio Processing**: Audio is processed locally before API calls
- **Secure API Communication**: HTTPS-only API calls to OpenAI
- **Temporary File Handling**: Secure cleanup of audio files
- **Environment Variable Protection**: Sensitive data stored in .env files

## 🛠️ Development

### Project Structure

```
ai-interview-note-taker/
├── app.py                 # Main Flask application
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── templates/            # HTML templates
│   └── index.html       # Main interface
├── setup.sh              # Linux/Mac setup script
├── setup.bat             # Windows setup script
├── test_setup.py         # Setup verification script
├── demo.py               # Demo and testing script
└── README.md            # This file
```

### Adding New Features

1. **Audio Processing**: Extend `RealTimeAudioProcessor` class in `app.py`
2. **Transcription**: Modify transcription interval and processing in `config.py`
3. **AI Analysis**: Modify `extract_candidate_details` function
4. **UI Components**: Add new cards and sections in `index.html`
5. **Real-time Updates**: Use Socket.IO events for live features

### Testing

```bash
# Run the application
python app.py

# Test real-time transcription
# Test live transcript updates
# Test candidate detail extraction
```

## 📊 Performance Considerations

- **Audio Quality**: 16kHz sample rate for optimal Whisper performance
- **Chunk Processing**: Configurable intervals for real-time processing
- **Memory Management**: Efficient audio data handling and cleanup
- **API Rate Limits**: Respect OpenAI API usage limits
- **Real-time Latency**: 3-second transcription delay (configurable)

## 🐛 Troubleshooting

### Common Issues

1. **Microphone Access Denied**
   - Check browser permissions
   - Ensure microphone is not in use by other applications

2. **Audio Recording Issues**
   - Verify PyAudio installation
   - Check system audio drivers

3. **OpenAI API Errors**
   - Verify API key in .env file
   - Check API usage limits and billing

4. **Transcription Quality**
   - Ensure clear audio input
   - Reduce background noise
   - Speak clearly and at normal pace

5. **Real-time Transcription Not Working**
   - Check browser console for errors
   - Verify WebSocket connection
   - Check transcription interval in config.py

### Debug Mode

Enable debug mode by setting `FLASK_ENV=development` in your `.env` file.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- OpenAI for providing powerful AI models
- Flask community for the excellent web framework
- Web Audio API for real-time audio processing capabilities

## 📞 Support

For questions, issues, or feature requests:

1. Check the troubleshooting section
2. Search existing issues
3. Create a new issue with detailed information

---

**Happy Interviewing with Real-time Transcription! 🎤⚡✨**