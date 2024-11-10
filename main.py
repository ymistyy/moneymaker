import praw
import json
import os
import random
from gtts import gTTS
from moviepy.editor import *
from moviepy.video.fx.resize import resize
from moviepy.video.tools.subtitles import SubtitlesClip
from PIL import Image, ImageDraw, ImageFont
import tempfile
from tqdm import tqdm
import numpy as np
import pyautogui
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Reddit API credentials from environment variables
REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
REDDIT_USER_AGENT = os.getenv('REDDIT_USER_AGENT')

subreddits = [
    'AskReddit',
    'AmItheAsshole',
    'scarystories',
    'Horror_stories',
    'LifeProTips'
]

CLIPS_DIR = 'your/clips/directory'
OUTPUT_DIR = 'your/videos/directory'
FONTS_DIR = 'your/fonts/directory'
ANIMATIONS_DIR = 'your/animations/directory'
MUSIC_DIR = 'your/music/directory'

def fetch_reddit_posts(subreddit_name, limit=5):
    """Fetches posts from a specified subreddit."""
    reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent=REDDIT_USER_AGENT
    )

    subreddit = reddit.subreddit(subreddit_name)
    posts = []

    for submission in subreddit.top(limit=limit):
        if submission.is_self:
            post = {
                "title": submission.title,
                "text": submission.selftext,
                "url": submission.url,
                "id": submission.id,
                "comments": [comment.body for comment in submission.comments if isinstance(comment, praw.models.Comment) and not comment.stickied and comment.body != "[deleted]"]
            }
            posts.append(post)

    return posts

def text_to_speech(text, output_file):
    """Convert text to speech and save it as an MP3 file."""
    tts = gTTS(text=text, lang='en', slow=False)
    tts.save(output_file)

def create_subtitles(text, tts_audio):
    """Generate subtitles from text aligned with TTS audio."""
    words = text.split()
    subs = []
    duration = AudioFileClip(tts_audio).duration
    words_per_second = len(words) / duration

    current_time = 0
    for i, word in enumerate(words):
        start = current_time
        end = start + (1 / words_per_second)
        current_time = end
        subs.append(((start, end), word))
    
    return subs

def render_subtitles(subs, video_size):
    """Create a subtitles clip from subtitle lines."""
    def generator(txt):
        img = Image.new("RGBA", (video_size[0], 120), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        font_path = os.path.join(FONTS_DIR, 'arial.ttf')
        try:
            font = ImageFont.truetype(font_path, 50)
        except IOError:
            print(f"Font not found: {font_path}. Standaard font used.")
            font = ImageFont.load_default()

        text_bbox = d.textbbox((0, 0), txt, font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        position = ((video_size[0] - text_width) // 2, (120 - text_height) // 2)
        d.text(position, txt, font=font, fill=(255, 255, 0), stroke_width=2, stroke_fill=(0, 0, 0))
        return ImageClip(np.array(img))

    subtitles = SubtitlesClip(subs, generator)
    return subtitles.set_position(("center", "bottom")).set_position((0, video_size[1] * 0.6))

def create_animation_clip():
    """Create a clip from a random animation (photo or gif)."""
    animation_files = [f for f in os.listdir(ANIMATIONS_DIR) if f.endswith(('.png', '.jpg', '.gif'))]
    selected_animation = random.choice(animation_files)
    animation_path = os.path.join(ANIMATIONS_DIR, selected_animation)
    animation_clip = ImageClip(animation_path).set_duration(3).fadeout(1)
    return animation_clip.set_position("center")

def create_tiktok_video(post, clip_path, video_index, background_music=None):
    """Create a TikTok-style video from a Reddit post and a specified gameplay clip."""
    gameplay_clip = VideoFileClip(clip_path)
    
    # Resize the gameplay clip to a 9:16 aspect ratio for TikTok (phone screen format)
    gameplay_clip = gameplay_clip.resize(height=1920).crop(width=1080, height=1920, x_center=gameplay_clip.w/2, y_center=gameplay_clip.h/2)

    # Generate TTS
    tts_text = f"{post['title']}. {post['text']}. " + " ".join(post["comments"][:5])
    audio_file = tempfile.NamedTemporaryFile(suffix='.mp3', delete=False).name
    text_to_speech(tts_text, audio_file)

    # Limit the video duration to the length of the TTS audio
    tts_audio = AudioFileClip(audio_file)
    duration = tts_audio.duration
    gameplay_clip = gameplay_clip.subclip(0, min(duration, gameplay_clip.duration))

    # Create subtitles
    subtitles = create_subtitles(tts_text, audio_file)
    subtitle_clip = render_subtitles(subtitles, gameplay_clip.size).set_duration(duration)

    # Create the animation clip
    animation_clip = create_animation_clip()

    # Background music
    if background_music and background_music != 'None':
        music_path = os.path.join(MUSIC_DIR, background_music)
        music = AudioFileClip(music_path).volumex(0.1)  # Reduce volume
        final_audio = CompositeAudioClip([tts_audio, music.set_duration(tts_audio.duration)])
    else:
        final_audio = tts_audio

    # Combine all clips
    final_video = CompositeVideoClip([
        gameplay_clip.set_audio(final_audio),
        subtitle_clip,
        animation_clip.set_start(0)
    ])

    # Ensure video duration matches audio duration
    final_video = final_video.set_duration(duration)

    # Save the video with an incremental name
    video_name = f"{OUTPUT_DIR}/video{video_index}.mp4"
    with tqdm(total=int(final_video.duration), desc="Rendering Video", unit="s") as pbar:
        final_video.write_videofile(video_name, codec='libx264', audio_codec='aac', fps=24)

    os.remove(audio_file)

# Main execution
if __name__ == "__main__":
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    print("Fetching posts...")
    reddit_posts = fetch_reddit_posts(random.choice(subreddits), limit=5)
    
    # Display available Reddit posts
    print("\nAvailable Reddit Posts:")
    for i, post in enumerate(reddit_posts):
        print(f"{i + 1}. {post['title']}")

    post_choice = int(input("Select a Reddit post to use (enter the number): ")) - 1
    chosen_post = reddit_posts[post_choice]

    # Display available gameplay clips
    gameplay_clips = [os.path.join(CLIPS_DIR, clip) for clip in os.listdir(CLIPS_DIR) if clip.endswith('.mp4')]
    print("\nAvailable Gameplay Clips:")
    for i, clip in enumerate(gameplay_clips):
        print(f"{i + 1}. {clip}")

    clip_choice = int(input("Select a gameplay clip to use (enter the number): ")) - 1
    chosen_clip = gameplay_clips[clip_choice]

    # Display available background music options
    music_files = [f for f in os.listdir(MUSIC_DIR) if f.endswith(('.mp3', '.wav'))]
    print("\nAvailable Background Music:")
    print("0. None")
    for i, music in enumerate(music_files):
        print(f"{i + 1}. {music}")

    music_choice = int(input("Select a background music (enter the number): ")) - 1
    background_music = None if music_choice == -1 else music_files[music_choice]

    # Create the video
    video_index = len([name for name in os.listdir(OUTPUT_DIR) if name.endswith('.mp4')]) + 1
    create_tiktok_video(chosen_post, chosen_clip, video_index, background_music)
