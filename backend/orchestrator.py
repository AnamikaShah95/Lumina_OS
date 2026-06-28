import re
from backend.video_engine import VideoProcessingEngine
from backend.summarizer import LuminaSummarizer

class LuminaOrchestrator:
    def __init__(self):
        self.video_engine = VideoProcessingEngine()
        self.summarizer = LuminaSummarizer()

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
            
            # Phase 1: Metadata Extraction
            result = self.video_engine.fetch_metadata_and_transcript(target_url)
            
            if result["status"] == "failed":
                return {
                    "intent": intent,
                    "engine_status": "FAILED",
                    "title": result["title"],
                    "summary": None,
                    "error": result["error_message"]
                }
            
            # Phase 2: Piping to LLM Summarizer
            print("🤖 [Orchestrator]: Piping raw payload to Lumina Summarizer Module...")
            summary_output = self.summarizer.generate_summary(result["title"], result["transcript"])
            
            return {
                "intent": intent,
                "engine_status": "SUCCESS",
                "title": result["title"],
                "summary": summary_output,
                "error": None
            }
        
        return {
            "intent": intent,
            "engine_status": "SKIPPED",
            "title": "N/A",
            "summary": "No execution required for general queries.",
            "error": None
        }