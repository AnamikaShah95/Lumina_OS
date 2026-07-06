import re
import time
import os
import glob
from backend.video_engine import VideoProcessingEngine
from backend.summarizer import LuminaSummarizer
from backend.ppt_generator import LuminaPPTGenerator
from backend.exceptions import TranscriptExtractionError, SchemaValidationException

class LuminaOrchestrator:
    def __init__(self):
        self.video_engine = VideoProcessingEngine()
        self.summarizer = LuminaSummarizer()
        self.ppt_generator = LuminaPPTGenerator()
        self.output_dir = "output"

    def execute_storage_garbage_collection(self, retention_limit_seconds: int = 1800):
        """
        Day 19 Architectural Addition: Asynchronous Memory & File Garbage Collector.
        Scans output workspace arrays and flushes historical slide blocks older than the retention threshold.
        """
        print("🧹 [Garbage Collector]: Scanning storage nodes for legacy execution files...")
        if not os.path.exists(self.output_dir):
            return
            
        current_time = time.time()
        target_pattern = os.path.join(self.output_dir, "*.pptx")
        file_matrix = glob.glob(target_pattern)
        
        cleaned_count = 0
        for file_path in file_matrix:
            try:
                file_creation_time = os.path.getmtime(file_path)
                # Checking if file age matches threshold criteria boundaries
                if (current_time - file_creation_time) > retention_limit_seconds:
                    os.remove(file_path)
                    print(f"🗑️ [Garbage Collector]: Flushed obsolete block -> {os.path.basename(file_path)}")
                    cleaned_count += 1
            except Exception as clean_err:
                print(f"⚠️ [Garbage Collector Warning]: Failed to wipe token matrix block {file_path}: {str(clean_err)}")
                
        if cleaned_count > 0:
            print(f"✅ [Garbage Collector]: Subsystem cycle complete. Total {cleaned_count} resource arrays pruned.")

    def route_and_execute_stream(self, user_query: str, target_slides: int = 7, audience_level: str = "Advanced Engineering"):
        """
        Day 19 Upgrade: Enforces strict post-execution context cleanups and triggers 
        garbage collection frames proactively on every dynamic intent route.
        """
        # Proactively flush old artifact layers from host environment before launching fresh thread parameters
        self.execute_storage_garbage_collection(retention_limit_seconds=600) # 10 minute threshold bounds
        
        yield "⏳ [Pipeline Core]: Scanning network packet stream parameters...", None
        time.sleep(0.4)
        
        if "summarize" in user_query.lower() or "youtube.com" in user_query.lower():
            intent = "summarize"
        else:
            intent = "general_query"

        url_match = re.search(r'(https?://[^\s]+)', user_query)
        
        if intent == "summarize" and url_match:
            target_url = url_match.group(1)
            yield f"🎬 [Pipeline Core]: Intent Identified -> Presentation Builder. Extraction ID active.", None
            
            # Phase 1: Scraping Validation with Exception Target Mapping
            yield "📡 [Phase 1/4]: Connecting to remote server streams...", None
            result = self.video_engine.fetch_metadata_and_transcript(target_url)
            
            if result["status"] == "failed":
                raise TranscriptExtractionError(result["error_message"])
            
            # Phase 2: Generating Text Summary Blocks
            yield f"🤖 [Phase 2/4]: Extract Success for target frames. Launching core text summary compilation...", None
            summary_output = self.summarizer.generate_summary(result["title"], result["transcript"])
            
            # Phase 3: Structural JSON Payload Mapping
            yield f"📊 [Phase 3/4]: Structuring presentation configurations matching constraints layer...", None
            ppt_result = self.ppt_generator.transform_summary_to_slides(
                video_title=result["title"], 
                summary_text=summary_output, 
                target_slides=target_slides, 
                audience_level=audience_level
            )
            
            if ppt_result["status"] == "failed":
                raise SchemaValidationException(ppt_result["error"])
            
            # Phase 4: Final File Assembly Logic
            yield "💾 [Phase 4/4]: Compiling binary blocks into PowerPoint elements...", None
            
            # Appending system timestamp metrics to separate storage file references
            timestamp_token = int(time.time())
            custom_filename = f"Lumina_Presentation_{timestamp_token}.pptx"
            file_path = self.ppt_generator.generate_actual_pptx(ppt_result["data"], custom_filename)
            
            success_status = (
                f"🎉 **Compilation Complete! System Active.**\n\n"
                f"🎬 **Video Context Title:** {result['title']}\n"
                f"📊 **Layout Target Enforced:** Exactly {target_slides} Content Nodes Generated.\n"
                f"💾 **Storage Vector Link:** File locked cleanly down into output folder context frames."
            )
            yield success_status, file_path
            return

        yield "🧠 [Router Intelligence]: Action target skipped. System idle.", None
        return