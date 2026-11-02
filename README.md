DwellReel-AI 🏡

AI-Powered Real Estate Video Generator

DwellReel-AI is an AI-powered real estate video generation platform that transforms property images and details into engaging promotional videos.

The application helps real estate professionals create attractive property showcase videos with AI-generated narration, background music, smooth transitions, and customised property information.

✨ Features

* AI Property Video Generation: Convert property images into promotional videos.
* AI Voice Narration: Generate voiceovers using AI text-to-speech.
* Multiple Voice Options: Choose from supported English and Hindi voices.
* Background Music Studio: Upload or record background music and customise audio settings.
* Smooth Transitions: Create visually engaging videos with animated transitions.
* Custom Property Details: Include property name, location, price, and other relevant information.
* Video Preview and Download: Preview and download the generated MP4.
* Responsive Interface: User-friendly interface designed for different screen sizes.

🛠️ Technology Stack

Frontend

* React.js
* Vite
* JavaScript
* CSS

Backend

* Python
* FastAPI
* FFmpeg

AI and Media Processing

* Edge TTS for AI-generated voice narration
* FFmpeg for video rendering and audio processing

📁 Project Structure

DwellReel-AI/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   └── services/
│   ├── uploads/
│   ├── outputs/
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
│
├── .gitignore
├── README.md
└── .env.example

⚙️ Installation and Setup

Prerequisites

Install the following before running the application:

* Python 3.12 or compatible version
* Node.js and npm
* FFmpeg
* Git

1. Clone the Repository

git clone https://github.com/YOUR-USERNAME/DwellReel-AI.git
cd DwellReel-AI

2. Backend Setup

Create and activate a virtual environment:

python3 -m venv .venv
source .venv/bin/activate

Install backend dependencies:

pip install -r backend/requirements.txt

Start the backend:

uvicorn backend.app.main:app --reload

The backend will run at:

http://127.0.0.1:8000

3. Frontend Setup

Open another terminal window:

cd DwellReel-AI/frontend
npm install
npm run dev

Open the local frontend URL displayed in your terminal.

🎬 How It Works

1. Open the DwellReel-AI application.
2. Enter the property information.
3. Upload property images.
4. Configure AI narration and select a voice.
5. Add background music and customise audio settings.
6. Generate the property promotional video.
7. Preview and download the final MP4 video.

🔊 Audio Capabilities

DwellReel-AI combines AI-generated narration with background music to create engaging property presentations.

Users can customise narration voices and background music settings to produce a more professional video experience.

📌 Notes

* AI voice generation through Edge TTS requires an active internet connection.
* FFmpeg must be installed and accessible to the backend.
* Generated videos are exported in MP4 format.
* Configure any required environment variables locally before starting the application.

👩‍💻 Developer

Saloni Gupta

B.Tech – Computer Science and Engineering
Specialisation: Artificial Intelligence and Machine Learning

⸻

DwellReel-AI – Transforming Property Images into Engaging Real Estate Videos.
