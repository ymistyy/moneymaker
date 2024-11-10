#Moneymaker
    <p>A Python script that automates the creation of TikTok-style brainrot videos using popular Reddit posts. This tool fetches content from subreddits, generates audio using text-to-speech (TTS), adds synchronized subtitles, and combines everything with gameplay footage and animations for short videos.</p>
    
<h2>Table of Contents</h2>
    <ul>
        <li><a href="#installation">Installation</a></li>
        <li><a href="#usage">Usage</a></li>
        <li><a href="#directory-structure">Directory Structure</a></li>
        <li><a href="#environment-variables">Environment Variables</a></li>
        <li><a href="#requirements">Requirements</a></li>
    </ul>

<h2 id="installation">Installation</h2>
    <ol>
        <li><strong>Clone the Repository</strong>
            <pre><code>git clone https://github.com/ymistyy/moneymaker.git
cd moneymaker</code></pre>
        </li>
        <li><strong>Set Up Python Environment</strong>
            <p>Ensure Python 3.7 or higher is installed. It is recommended to use a virtual environment:</p>
            <pre><code>python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`</code></pre>
        </li>
        <li><strong>Install Dependencies</strong>
            <p>Install the required dependencies listed in <code>requirements.txt</code>:</p>
            <pre><code>pip install -r requirements.txt</code></pre>
        </li>
        <li><strong>Set Up Reddit API Credentials</strong>
            <ol>
                <li>Create an application on Reddit's <a href="https://www.reddit.com/prefs/apps" target="_blank">Developer Portal</a>.</li>
                <li>Copy the <code>client_id</code>, <code>client_secret</code>, and <code>user_agent</code> provided by Reddit.</li>
                <li>Create a <code>.env</code> file in the project root and add the following:</li>
            </ol>
            <pre><code>REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USER_AGENT=your_user_agent</code></pre>
        </li>
    </ol>

<h2 id="usage">Usage</h2>
    <ol>
        <li><strong>Prepare Directories</strong>
            <p>Ensure you have these directories in the project root:</p>
            <ul>
                <li><strong>clips/</strong> for gameplay footage (.mp4 files)</li>
                <li><strong>fonts/</strong> for font files (e.g., arial.ttf)</li>
                <li><strong>animations/</strong> for images/animations (.png, .jpg, .gif)</li>
                <li><strong>music/</strong> for background music (.mp3, .wav)</li>
            </ul>
        </li>
        <li><strong>Run the Script</strong>
            <p>Run the script by executing:</p>
            <pre><code>python main.py</code></pre>
        </li>
        <li><strong>Select Content</strong>
            <p>The script will prompt you to:</p>
            <ul>
                <li>Select a Reddit post.</li>
                <li>Select a gameplay clip.</li>
                <li>Optionally, choose background music or proceed without it.</li>
            </ul>
        </li>
        <li><strong>Output</strong>
            <p>The generated video will be saved in the <strong>output/</strong> directory as <code>video{n}.mp4</code>, where <code>{n}</code> is the video index.</p>
        </li>
    </ol>

<h2 id="directory-structure">Directory Structure</h2>
<pre><code>reddit-tiktok-video-generator/
│
├── main.py
├── requirements.txt
├── .env
├── clips/                  # Gameplay videos
├── fonts/                  # Font files (e.g., arial.ttf)
├── animations/             # Images or animations
├── music/                  # Background music files
└── output/                 # Generated videos (created by script)
</code></pre>

<h2 id="environment-variables">Environment Variables</h2>
    <p>Add your Reddit credentials to the <code>.env</code> file:</p>
    <pre><code>REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USER_AGENT=your_user_agent</code></pre>

<h2 id="requirements">Requirements</h2>
    <p>All required Python libraries are listed in <code>requirements.txt</code>:</p>
    <ul>
        <li><code>praw</code></li>
        <li><code>moviepy</code></li>
        <li><code>gtts</code></li>
        <li><code>Pillow</code></li>
        <li><code>tqdm</code></li>
        <li><code>numpy</code></li>
        <li><code>python-dotenv</code></li>
    </ul>
    <p>To install all required packages:</p>
    <pre><code>pip install -r requirements.txt</code></pre>

<h2>Support</h2>
    <p>If you encounter any issues or have questions about this project, please open an issue. Contributions, suggestions, and feedback are always welcome!</p>
    
</body>
</html>
