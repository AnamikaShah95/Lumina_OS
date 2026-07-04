import re
import time
from backend.video_engine import VideoProcessingEngine
from backend.summarizer import LuminaSummarizer
from backend.ppt_generator import LuminaPPTGenerator

class LuminaOrchestrator:
    def __init__(self):
        self.video_engine = VideoProcessingEngine()
        self.summarizer = LuminaSummarizer()
        self.ppt_generator = LuminaPPTGenerator()

    def route_and_execute_stream(self, user_query: str, target_slides: int = 7, audience_level: str = "Advanced Engineering"):
        """
        Day 11 Upgrade: Refactored from traditional returns to a Python Generator Matrix.
        Yields sequential state-logs dynamically to update frontend components asynchronously.
        """
        yield "⏳ [Pipeline]: Analyzing network request stream and analyzing intent...", None
        time.sleep(0.5)
        
        if "summarize" in user_query.lower() or "youtube.com" in user_query.lower():
            intent = "summarize"
        else:
            intent = "general_query"

        url_match = re.search(r'(https?://[^\s]+)', user_query)
        
        if intent == "summarize" and url_match:
            target_url = url_match.group(1)
            yield f"🎬 [Pipeline]: Intent Identified -> Video Processing Layer. Target URL: {target_url}", None
            
            # Phase 1: Scraping and Transcript download
            yield "📡 [Pipeline Phase 1]: Initializing stream scrapers to fetch metadata & transcripts...", None
            result = self.video_engine.fetch_metadata_and_transcript(target_url)
            
            if result["status"] == "failed":
                error_msg = f"❌ Processing Blocked: {result['error_message']}"
                yield error_msg, None
                return
            
            # Phase 2: Summarization Core
            yield f"🤖 [Pipeline Phase 2]: Extraction Success for '{result['title']}'. Piping to LLM Summarizer...", None
            summary_output = self.summarizer.generate_summary(result["title"], result["transcript"])
            
            # Phase 3: Slide Deck Payloads Architecture
            yield f"📊 [Pipeline Phase 3]: Injecting rules -> Enforcing {target_slides} slides ({audience_level} Depth)...", None
            ppt_result = self.ppt_generator.transform_summary_to_slides(
                video_title=result["title"], 
                summary_text=summary_output, 
                target_slides=target_slides, 
                audience_level=audience_level
            )
            
            if ppt_result["status"] == "failed":
                yield f"❌ Structuring Failed: {ppt_result['error']}", None
                return
            
            # Phase 4: Compiling Physical PPTX file
            yield "💾 [Pipeline Phase 4]: Compiling structural components into standard physical PowerPoint slides...", None
            file_path = self.ppt_generator.generate_actual_pptx(ppt_result["data"], "Lumina_Presentation.pptx")
            
            success_status = (
                f"🎉 **Success! Application Layer Complete.**\n\n"
                f"🎬 **Video Title:** {result['title']}\n"
                f"📊 **Rules Enforced:** Exactly {target_slides} Slides Generated for '{audience_level}' Depth.\n"
                f"💾 **File State:** Compiled safely in local system memory storage workspace."
            )
            yield success_status, file_path
            return

        yield "🧠 [Router Intelligence]: Routing criteria skipped. No background process required.", None
        return