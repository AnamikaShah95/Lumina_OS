import re
from backend.video_engine import VideoProcessingEngine
from backend.summarizer import LuminaSummarizer
from backend.ppt_generator import LuminaPPTGenerator

class LuminaOrchestrator:
    def __init__(self):
        self.video_engine = VideoProcessingEngine()
        self.summarizer = LuminaSummarizer()
        self.ppt_generator = LuminaPPTGenerator()

    def route_and_execute(self, user_query: str, target_slides: int = 7, audience_level: str = "Advanced Engineering") -> dict:
        """
        Day 10 Upgrade: Added explicit named arguments to route variables seamlessly without text appending hacks.
        """
        print("\n⚡ [Orchestrator]: Analyzing incoming network request stream...")
        
        if "summarize" in user_query.lower() or "youtube.com" in user_query.lower():
            intent = "summarize"
        else:
            intent = "general_query"

        url_match = re.search(r'(https?://[^\s]+)', user_query)
        
        if intent == "summarize" and url_match:
            target_url = url_match.group(1)
            print(f"🎬 [Orchestrator]: Triggering Video Processing Engine for URL: {target_url}")
            
            # Phase 1: Transcript Extraction
            result = self.video_engine.fetch_metadata_and_transcript(target_url)
            
            if result["status"] == "failed":
                return {
                    "intent": intent, "engine_status": "FAILED", "title": result["title"],
                    "file_path": None, "error": result["error_message"]
                }
            
            # Phase 2: Summarizer
            print("🤖 [Orchestrator]: Piping raw payload to Lumina Summarizer Module...")
            summary_output = self.summarizer.generate_summary(result["title"], result["transcript"])
            
            # Phase 3: Context-Injected Slide Payload Blueprint Generation
            print("📊 [Orchestrator]: Injecting user rules directly down into PPT Payload Architect...")
            ppt_result = self.ppt_generator.transform_summary_to_slides(
                video_title=result["title"], 
                summary_text=summary_output, 
                target_slides=target_slides, 
                audience_level=audience_level
            )
            
            if ppt_result["status"] == "failed":
                return {
                    "intent": intent, "engine_status": "FAILED", "title": result["title"],
                    "file_path": None, "error": ppt_result["error"]
                }
            
            # Phase 4: Physical PPTX File Generation
            file_path = self.ppt_generator.generate_actual_pptx(ppt_result["data"], "Lumina_Presentation.pptx")
            
            return {
                "intent": intent, "engine_status": "SUCCESS", "title": result["title"],
                "file_path": file_path, "error": None
            }
        
        return {
            "intent": intent, "engine_status": "SKIPPED", "title": "N/A", "summary": "No execution required.", "file_path": None, "error": None
        }