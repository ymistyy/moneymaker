# moneymaker
A Python script that automates the creation of TikTok-style brainrot videos using popular Reddit posts. This tool fetches content from subreddits, generates audio using text-to-speech (TTS), adds synchronized subtitles, and combines everything with gameplay footage and animations for short videos.

Table of Contents

    Features
    Installation
    Usage
    Directory Structure
    Environment Variables
    Requirements

Features

    Fetches top posts and comments from subreddits.
    Converts post content to audio using Google Text-to-Speech (gTTS).
    Generates synchronized subtitles for videos.
    Combines gameplay clips, subtitles, and optional background music.
    Customizable for different video styles and subreddits.

Installation
1. Clone the Repository

git clone https://github.com/ymistyy/moneymaker.git
<p>cd moneymaker</p>

2. Set Up Python Environment

Ensure Python 3.7 or higher is installed. It is recommended to use a virtual environment:

python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. Install Dependencies

pip install -r requirements.txt

4. Set Up Reddit API Credentials

    Create an application on Reddit's Developer Portal.
    Copy the client_id, client_secret, and user_agent provided by Reddit.
    Create a .env file in the project root and add:

REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USER_AGENT=your_user_agent

Usage
1. Prepare Directories

Ensure you have these directories in the project root:

    clips/ for gameplay footage (.mp4 files)
    fonts/ for font files (e.g., arial.ttf)
    animations/ for images/animations (.png, .jpg, .gif)
    music/ for background music (.mp3, .wav)

2. Run the Script

python main.py

3. Select Content

    The script will prompt you to select a Reddit post and a gameplay clip.
    Optionally, choose background music or proceed without it.

4. Output

The generated video will be saved in the output/ directory as video{n}.mp4, where {n} is the video index.
Directory Structure

Ensure your project structure follows:

reddit-tiktok-video-generator/
│
├── main.py
├── requirements.txt
├── .env
├── clips/                  # Gameplay videos
├── fonts/                  # Font files (e.g., arial.ttf)
├── animations/             # Images or animations
├── music/                  # Background music files
└── output/                 # Generated videos (created by script)

Environment Variables

Add your Reddit credentials to the .env file:

REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USER_AGENT=your_user_agent

Requirements

All required Python libraries are listed in requirements.txt:

    praw
    moviepy
    gtts
    Pillow
    tqdm
    numpy
    python-dotenv

To install all required packages:

pip install -r requirements.txt

Support

If you encounter any issues or have questions about this project, please open an issue. Contributions, suggestions, and feedback are always welcome!
