import os
import re
from typing import Optional
from pydantic import BaseModel, Field
from youtube_transcript_api import YouTubeTranscriptApi
import yt_dlp

# 1. Output Structure for Video Data
class VideoDataPayload(BaseModel):
    video_id: str
    title: Optional[str] = Field(default="Unknown Title", description="Title of the YouTube video")
    transcript: Optional[str] = Field(default=None, description="Full extracted text transcript of the video")
    status: str = Field(description="Status of processing: 'success' or 'failed'")
    error_message: Optional[str] = Field(default=None)

def extract_video_id(url: str) -> Optional[str]:
    """
    Extracts the 11-character YouTube video ID from various URL formats.
    """
    match = re.search(r'(?:https?://)?(?:www\.)?(?:youtube\.com/(?:[^/]+/.+/|(?:v|e(?:mbed)?)/|.*[?&]v=)|youtu\.be/)([^"&?/ ]{11})', url)
    return match.group(1) if match else None

def fetch_video_data(video_url: str) -> VideoDataPayload:
    """
    Fetches Title and Transcripts from a YouTube URL and binds it into a structured payload.
    """
    video_id = extract_video_id(video_url)
    if not video_id:
        return VideoDataPayload(video_id="unknown", status="failed", error_message="Invalid YouTube URL format.")

    title = "Unknown Title"
    transcript_text = ""

    # Part A: Extract Title using yt-dlp
    try:
        ydl_opts = {'skip_download': True, 'quiet': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)
            title = info.get('title', 'Unknown Title')
    except Exception as e:
        print(f"⚠️ Metadata extraction warning: {str(e)}")

    # Part B: Extract Transcript
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'hi'])
        transcript_text = " ".join([item['text'] for item in transcript_list])
        
        return VideoDataPayload(
            video_id=video_id,
            title=title,
            transcript=transcript_text,
            status="success"
        )
    except Exception as e:
        return VideoDataPayload(
            video_id=video_id,
            title=title,
            status="failed",
            error_message=f"Transcript extraction failed: {str(e)}"
        )