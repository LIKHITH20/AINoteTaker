# 🎤 AI Interview Note Taker

A sophisticated AI-powered application that provides real-time audio transcription and intelligent candidate analysis during interviews. Built with Flask, WebSocket support, and OpenAI's advanced AI models.

## ✨ Features

- **🎙️ Real-time Audio Recording**: Capture interview audio with live visualization
- **📝 Live Transcription**: Generate transcripts using OpenAI Whisper API
- **🤖 AI-Powered Analysis**: Extract candidate details using GPT-4
- **📊 Audio Visualization**: Real-time audio level monitoring and waveform display
- **💻 Modern Web Interface**: Responsive design with intuitive controls
- **🔒 Secure Processing**: Local audio processing with secure API calls

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

### OpenAI API Setup

1. Visit [OpenAI Platform](https://platform.openai.com/)
2. Create an account and get your API key
3. Add the API key to your `.env` file

## 📱 Usage

### Recording an Interview

1. **Start Recording**: Click the "🎙️ Start Recording" button
2. **Grant Microphone Access**: Allow browser access to your microphone
3. **Monitor Audio**: Watch real-time audio visualization and levels
4. **Stop Recording**: Click "⏹️ Stop Recording" when finished

### Viewing Results

After stopping the recording, the application will:

1. **Process Audio**: Convert audio to text using Whisper
2. **Analyze Content**: Extract candidate details using GPT-4
3. **Display Results**: Show transcript and structured candidate information

### Candidate Details Extracted

- **Personal Information**: Name, experience, education
- **Professional Background**: Current role, skills, achievements
- **Interview Assessment**: Strengths, concerns, overall evaluation
- **Technical Skills**: Programming languages, tools, frameworks
- **Soft Skills**: Communication, leadership, problem-solving

## 🏗️ Architecture

### Backend (Flask + Python)

- **Audio Processing**: Real-time audio capture and processing
- **AI Integration**: OpenAI Whisper for transcription, GPT-4 for analysis
- **WebSocket Support**: Real-time communication with frontend
- **REST API**: Endpoints for recording control and result retrieval

### Frontend (HTML + JavaScript)

- **Real-time Audio**: Web Audio API for live audio processing
- **Visualization**: Canvas-based audio waveform display
- **Responsive Design**: Mobile-friendly interface
- **Socket.IO**: Real-time updates and communication

### AI Models Used

- **OpenAI Whisper**: High-quality speech-to-text transcription
- **GPT-4**: Intelligent candidate detail extraction and analysis

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
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── templates/            # HTML templates
│   └── index.html       # Main interface
└── README.md            # This file
```

### Adding New Features

1. **Audio Processing**: Extend `AudioProcessor` class in `app.py`
2. **AI Analysis**: Modify `extract_candidate_details` function
3. **UI Components**: Add new cards and sections in `index.html`
4. **Real-time Updates**: Use Socket.IO events for live features

### Testing

```bash
# Run the application
python app.py

# Test recording functionality
# Test transcription accuracy
# Test candidate detail extraction
```

## 📊 Performance Considerations

- **Audio Quality**: 16kHz sample rate for optimal Whisper performance
- **Chunk Processing**: 1024 sample chunks for real-time processing
- **Memory Management**: Efficient audio data handling and cleanup
- **API Rate Limits**: Respect OpenAI API usage limits

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

**Happy Interviewing! 🎤✨**