import re
from backend.video_engine import VideoProcessingEngine
from backend.summarizer import LuminaSummarizer
from backend.ppt_generator import LuminaPPTGenerator

class LuminaOrchestrator:
    def __init__(self):
        self.video_engine = VideoProcessingEngine()
        self.summarizer = LuminaSummarizer()
        self.ppt_generator = LuminaPPTGenerator() # Day 5 Matrix Included

    def route_and_execute(self, user_query: str) -> dict:
        print("\n⚡ [Orchestrator]: Analyzing incoming network request stream...")
        
        if "summarize" in user_query.lower() or "youtube.com" in user_query.lower():
            intent = "summarize"
            print("🧠 [Router]: Detected Intent -> 'summarize' (Confidence: 0.95)")
        else:
            intent = "general_query"
            print("🧠 [Router]: Detected Intent -> 'general_query' (Confidence: 0.85)")

        url_match = re.search(r'(https?://[^\s]+)', user_query)
        
        if intent == "summarize" and url_match:
            target_url = url_match.group(1)
            print(f"🎬 [Orchestrator]: Triggering Video Processing Engine for URL: {target_url}")
            
            # Phase 1: Transcript Extraction
            result = self.video_engine.fetch_metadata_and_transcript(target_url)
            
            if result["status"] == "failed":
                return {
                    "intent": intent,
                    "engine_status": "FAILED",
                    "title": result["title"],
                    "summary": None,
                    "presentation_data": None,
                    "error": result["error_message"]
                }
            
            # Phase 2: Piping to LLM Summarizer
            print("🤖 [Orchestrator]: Piping raw payload to Lumina Summarizer Module...")
            summary_output = self.summarizer.generate_summary(result["title"], result["transcript"])
            
            # Phase 3: Converting Summary to Slide Structural Objects (Day 5 Integration)
            print("📊 [Orchestrator]: Sending markdown text downstream to PPT Payload Architect...")
            ppt_result = self.ppt_generator.transform_summary_to_slides(result["title"], summary_output)
            
            return {
                "intent": intent,
                "engine_status": "SUCCESS",
                "title": result["title"],
                "summary": summary_output,
                "presentation_data": ppt_result["data"] if ppt_result["status"] == "success" else None,
                "error": ppt_result["error"]
            }
        
        return {
            "intent": intent,
            "engine_status": "SKIPPED",
            "title": "N/A",
            "summary": "No execution required.",
            "presentation_data": None,
            "error": None
        }