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
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# Reddit API credentials
REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
REDDIT_USER_AGENT = os.getenv('REDDIT_USER_AGENT')

subreddits = ['AskReddit', 'AmItheAsshole', 'scarystories', 'Horror_stories', 'LifeProTips']

# Replace paths with placeholders for GitHub
CLIPS_DIR = 'your/path/here/clips'
OUTPUT_DIR = 'your/path/here/videos'
FONTS_DIR = 'your/path/here/fonts'
ANIMATIONS_DIR = 'your/path/here/animations'
MUSIC_DIR = 'your/path/here/music'

def fetch_reddit_posts(subreddit_name, limit=5):
    """Get posts from a subreddit."""
    reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent=REDDIT_USER_AGENT
    )
    posts = []
    for submission in reddit.subreddit(subreddit_name).top(limit=limit):
        if submission.is_self:
            post = {
                "title": submission.title,
                "text": submission.selftext,
                "url": submission.url,
                "id": submission.id,
                "comments": [
                    comment.body for comment in submission.comments 
                    if isinstance(comment, praw.models.Comment) and not comment.stickied and comment.body != "[deleted]"
                ]
            }
            posts.append(post)
    return posts

def text_to_speech(text, output_file):
    """Convert text to speech."""
    tts = gTTS(text=text, lang='en')
    tts.save(output_file)

def create_subtitles(text, tts_audio):
    """Generate subtitles."""
    words = text.split()
    subs = []
    duration = AudioFileClip(tts_audio).duration
    words_per_second = len(words) / duration
    current_time = 0
    for word in words:
        start = current_time
        end = start + (1 / words_per_second)
        current_time = end
        subs.append(((start, end), word))
    return subs

def render_subtitles(subs, video_size):
    """Create subtitles clip."""
    def generator(txt):
        img = Image.new("RGBA", (video_size[0], 120), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        font_path = os.path.join(FONTS_DIR, 'arial.ttf')
        try:
            font = ImageFont.truetype(font_path, 50)
        except IOError:
            font = ImageFont.load_default()
        d.text((video_size[0] // 2, 60), txt, font=font, fill=(255, 255, 0), stroke_width=2, stroke_fill=(0, 0, 0))
        return ImageClip(np.array(img))
    
    return SubtitlesClip(subs, generator).set_position(("center", "bottom"))

def create_animation_clip():
    """Generate animation clip."""
    animation_files = [f for f in os.listdir(ANIMATIONS_DIR) if f.endswith(('.png', '.jpg', '.gif'))]
    selected_animation = random.choice(animation_files)
    return ImageClip(os.path.join(ANIMATIONS_DIR, selected_animation)).set_duration(3).fadeout(1)

def create_tiktok_video(post, clip_path, video_index, background_music=None):
    """Generate a TikTok-style video."""
    gameplay_clip = VideoFileClip(clip_path).resize(height=1920).crop(width=1080, height=1920, x_center=clip_path.w/2, y_center=clip_path.h/2)
    tts_text = f"{post['title']}. {post['text']}. " + " ".join(post["comments"][:5])
    audio_file = tempfile.NamedTemporaryFile(suffix='.mp3', delete=False).name
    text_to_speech(tts_text, audio_file)

    tts_audio = AudioFileClip(audio_file)
    gameplay_clip = gameplay_clip.subclip(0, min(tts_audio.duration, gameplay_clip.duration))

    subtitles = create_subtitles(tts_text, audio_file)
    subtitle_clip = render_subtitles(subtitles, gameplay_clip.size).set_duration(tts_audio.duration)
    animation_clip = create_animation_clip()

    if background_music:
        music_path = os.path.join(MUSIC_DIR, background_music)
        music = AudioFileClip(music_path).volumex(0.1)
        music = concatenate_audioclips([music] * (int(tts_audio.duration // music.duration) + 1)).set_duration(tts_audio.duration)
        final_audio = CompositeAudioClip([tts_audio, music])
    else:
        final_audio = tts_audio

    final_video = CompositeVideoClip([gameplay_clip.set_audio(final_audio), subtitle_clip, animation_clip.set_start(0)])
    final_video.set_duration(tts_audio.duration).write_videofile(f"{OUTPUT_DIR}/video{video_index}.mp4", codec='libx264', audio_codec='aac', fps=24)
    os.remove(audio_file)

# Run the main process
if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    reddit_posts = fetch_reddit_posts(random.choice(subreddits))
    for i, post in enumerate(reddit_posts):
        print(f"{i + 1}. {post['title']}")
    chosen_post = reddit_posts[int(input("Select a post: ")) - 1]
    gameplay_clips = [os.path.join(CLIPS_DIR, clip) for clip in os.listdir(CLIPS_DIR) if clip.endswith('.mp4')]
    chosen_clip = gameplay_clips[int(input("Select a clip: ")) - 1]
    music_files = [f for f in os.listdir(MUSIC_DIR) if f.endswith(('.mp3', '.wav'))]
    background_music = None if (music_choice := int(input("Select music (0 for none): "))) == 0 else music_files[music_choice - 1]
    video_index = len([name for name in os.listdir(OUTPUT_DIR) if name.endswith('.mp4')]) + 1
    create_tiktok_video(chosen_post, chosen_clip, video_index, background_music)

