import os
import re
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

class VideoProcessingEngine:
    def __init__(self):
        self.formatter = TextFormatter()

    def extract_video_id(self, url: str) -> str:
        reg_exp = r'(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|shorts\/|[^#]*[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})'
        match = re.search(reg_exp, url)
        return match.group(1) if match else None

    def fetch_metadata_and_transcript(self, url: str) -> dict:
        """
        Day 12 Advanced Patch: Implements double-fault tolerance.
        If track locking succeeds but fetch() fails due to empty network elements,
        the system aggressively falls back to the next available stream.
        """
        video_id = self.extract_video_id(url)
        if not video_id:
            return {"status": "failed", "title": "Unknown Title", "transcript": None, "error_message": "Invalid YouTube URL syntax."}

        mock_title = f"YouTube Stream Architecture ({video_id})"

        try:
            print(f"📡 [Video Engine]: Inspecting transcript list metadata for ID: {video_id}")
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            
            clean_transcript = None
            selected_lang = None

            # 1. First Pass: Targeted Strategy with internal fetch verification
            language_priority = ['en', 'en-US', 'hi']
            for lang_code in language_priority:
                try:
                    print(f"🔍 [Video Engine]: Evaluating track availability for: [{lang_code}]")
                    target_transcript = transcript_list.find_transcript([lang_code])
                    
                    # Defensively verifying the network stream before committing
                    raw_data = target_transcript.fetch()
                    if raw_data:
                        formatted_text = self.formatter.format_transcript(raw_data)
                        clean_transcript = " ".join(formatted_text.split())
                        selected_lang = lang_code
                        print(f"🎯 [Video Engine]: Successfully locked and downloaded track: [{selected_lang}]")
                        break
                except Exception as fetch_err:
                    print(f"⚠️ [Video Engine Trace]: Track [{lang_code}] fetching failed or returned empty payload. Skipping...")
                    continue

            # 2. Second Pass: Absolute Fallback Matrix if prioritized strings fail at fetch level
            if not clean_transcript:
                print("🚨 [Video Engine]: Priority tracks exhausted or broken. Attempting structural fallback queue...")
                for transcript in transcript_list:
                    try:
                        print(f"🌐 [Video Engine Fallback]: Attempting stream download for code: [{transcript.language_code}]")
                        raw_data = transcript.fetch()
                        if raw_data:
                            formatted_text = self.formatter.format_transcript(raw_data)
                            clean_transcript = " ".join(formatted_text.split())
                            selected_lang = transcript.language_code
                            print(f"✅ [Video Engine]: Deep fallback successfully rescued script stream using code: [{selected_lang}]")
                            break
                    except Exception:
                        continue

            if not clean_transcript:
                raise ValueError("All available transcript backend streams returned empty or unparseable data blocks.")

            return {
                "status": "success",
                "title": f"{mock_title} [{selected_lang.upper()} Track]",
                "transcript": clean_transcript,
                "error_message": None
            }

        except Exception as e:
            print(f"❌ [Video Engine Fault]: Final pipeline failure -> {str(e)}")
            return {
                "status": "failed",
                "title": mock_title,
                "transcript": None,
                "error_message": f"Transcript extraction failed: {str(e)}"
            }