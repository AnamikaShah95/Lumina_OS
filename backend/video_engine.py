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

# 2. Main Processing Core Engine Execution Block
class VideoProcessingEngine:
    def __init__(self):
        pass

    def extract_video_id(self, url: str) -> Optional[str]:
        """
        Extracts the 11-character YouTube video ID using regex boundary patterns.
        """
        pattern = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
        match = re.search(pattern, url)
        return match.group(1) if match else None

    def fetch_metadata_and_transcript(self, url: str) -> dict:
        """
        Extracts title via yt-dlp and downloads transcript, formatting output into structural dict matching the BaseModel.
        """
        video_id = self.extract_video_id(url)
        if not video_id:
            return {
                "status": "failed",
                "video_id": "N/A",
                "title": "Unknown Title",
                "transcript": None,
                "error_message": "Invalid YouTube URL format."
            }

        # Fetching Video Title securely via yt-dlp metadata boundary
        video_title = "Unknown Title"
        ydl_opts = {'quiet': True, 'skip_download': True}
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                video_title = info.get('title', 'Unknown Title')
        except Exception as e:
            print(f"⚠️ Metadata extraction warning: {str(e)}")

        # Fetching Video Subtitles via transcript engine socket
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'en-US'])
            full_transcript = " ".join([chunk['text'] for chunk in transcript_list])
            
            # Formatting structural dictionary data matching Pydantic expectations
            return {
                "status": "success",
                "video_id": video_id,
                "title": video_title,
                "transcript": full_transcript,
                "error_message": None
            }
        except Exception as e:
            return {
                "status": "failed",
                "video_id": video_id,
                "title": video_title,
                "transcript": None,
                "error_message": f"Transcript extraction failed: {str(e)}"
            }