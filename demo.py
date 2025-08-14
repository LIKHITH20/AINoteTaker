#!/usr/bin/env python3
"""
Demo script for AI Interview Note Taker
This script demonstrates how to use the application programmatically
"""

import os
import time
import json
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()

def demo_transcription():
    """Demo transcription using OpenAI Whisper API"""
    print("🎤 Demo: Audio Transcription")
    print("=" * 40)
    
    # Check if API key is configured
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key or api_key == 'your_openai_api_key_here':
        print("❌ OpenAI API key not configured")
        print("Please add your API key to the .env file")
        return False
    
    # Configure OpenAI
    openai.api_key = api_key
    
    print("✅ OpenAI API configured")
    print("📝 This demo shows how the transcription works")
    print("   In the real app, audio is recorded from microphone")
    
    return True

def demo_candidate_analysis():
    """Demo candidate detail extraction using GPT-4"""
    print("\n🤖 Demo: Candidate Analysis")
    print("=" * 40)
    
    # Sample interview transcript
    sample_transcript = """
    Interviewer: Hi Sarah, thanks for joining us today. Can you tell us about your background?
    
    Sarah: Hi! I'm Sarah Johnson, I have about 5 years of experience in software development. 
    I started as a junior developer at TechCorp and worked my way up to a senior position. 
    I'm currently working on a large-scale e-commerce platform using React and Node.js.
    
    Interviewer: That's great! What are your strongest technical skills?
    
    Sarah: I'm very proficient in JavaScript, both frontend and backend. I've worked extensively 
    with React, Node.js, and MongoDB. I also have experience with Python for data processing 
    and some DevOps work with Docker and AWS.
    
    Interviewer: Can you tell us about a challenging project you've worked on?
    
    Sarah: Sure! Last year, I led a team of 4 developers to rebuild our legacy payment system. 
    It was a critical project that had to handle thousands of transactions daily. We used 
    microservices architecture and implemented proper error handling and monitoring. 
    The project was completed on time and reduced payment failures by 95%.
    
    Interviewer: What are your career goals?
    
    Sarah: I'm looking to move into a technical leadership role where I can mentor other 
    developers and help shape technical decisions. I'm also interested in learning more 
    about machine learning and AI applications.
    """
    
    print("📝 Sample Interview Transcript:")
    print("-" * 30)
    print(sample_transcript[:200] + "...")
    print("-" * 30)
    
    try:
        # Extract candidate details using GPT-4
        prompt = f"""
        Based on the following interview transcript, extract and organize the candidate's details in a structured format:

        Transcript:
        {sample_transcript}

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
        
        # Parse and display results
        try:
            candidate_details = json.loads(response.choices[0].message.content)
            print("\n✅ Candidate Analysis Results:")
            print("-" * 30)
            
            for key, value in candidate_details.items():
                if key != 'transcript':
                    formatted_key = key.replace('_', ' ').title()
                    print(f"{formatted_key}: {value}")
            
        except json.JSONDecodeError:
            print("\n⚠️  Raw GPT Response:")
            print(response.choices[0].message.content)
            
    except Exception as e:
        print(f"❌ Error in candidate analysis: {e}")
        return False
    
    return True

def demo_features():
    """Demo the main features of the application"""
    print("\n🚀 Demo: Application Features")
    print("=" * 40)
    
    features = [
        "🎙️ Real-time Audio Recording",
        "📊 Live Audio Visualization",
        "📝 OpenAI Whisper Transcription",
        "🤖 GPT-4 Candidate Analysis",
        "💻 Modern Web Interface",
        "📱 Responsive Design",
        "🔒 Secure Audio Processing",
        "⚡ Real-time Updates"
    ]
    
    for feature in features:
        print(f"  {feature}")
    
    print("\n📋 How it works:")
    print("  1. User starts recording interview audio")
    print("  2. Audio is captured in real-time with visualization")
    print("  3. When stopped, audio is sent to OpenAI Whisper")
    print("  4. Transcript is analyzed by GPT-4 for candidate details")
    print("  5. Results are displayed in a structured format")

def main():
    """Run the demo"""
    print("🎤 AI Interview Note Taker - Demo")
    print("=" * 50)
    
    # Run demos
    demos = [
        ("Transcription", demo_transcription),
        ("Candidate Analysis", demo_candidate_analysis),
        ("Features Overview", demo_features)
    ]
    
    for demo_name, demo_func in demos:
        try:
            if not demo_func():
                print(f"⚠️  {demo_name} demo had issues")
        except Exception as e:
            print(f"❌ {demo_name} demo failed: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Demo Complete!")
    print("\nTo run the full application:")
    print("1. Make sure your .env file has your OpenAI API key")
    print("2. Run: python app.py")
    print("3. Open http://localhost:5000 in your browser")
    print("4. Start recording your interview!")

if __name__ == "__main__":
    main()