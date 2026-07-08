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
        Day 26 Architectural Upgrade: Microsecond Latency Tracking Sockets.
        Tracks precise code block operational velocity to expose optimization profiles.
        """
        # Starting high-precision global pipeline clock reference
        global_pipeline_start = time.perf_counter()
        
        self.execute_storage_garbage_collection(retention_limit_seconds=600)
        
        yield "⏳ [Pipeline Core]: Scanning network packet stream parameters...", None
        time.sleep(0.2)
        
        if "summarize" in user_query.lower() or "youtube.com" in user_query.lower():
            intent = "summarize"
        else:
            intent = "general_query"

        url_match = re.search(r'(https?://[^\s]+)', user_query)
        
        if intent == "summarize" and url_match:
            target_url = url_match.group(1)
            yield f"🎬 [Pipeline Core]: Intent Identified -> Presentation Builder. Extraction ID active.", None
            
            # --- Phase 1 Speed Analytics Tracking ---
            p1_start = time.perf_counter()
            yield "📡 [Phase 1/4]: Connecting to remote server streams and extraction blocks...", None
            result = self.video_engine.fetch_metadata_and_transcript(target_url)
            p1_latency = time.perf_counter() - p1_start
            print(f"⏱️  [Performance Profiler]: Phase 1 Transcript Fetch Duration -> {p1_latency:.4f} seconds")
            
            if result["status"] == "failed":
                raise TranscriptExtractionError(result["error_message"])
            
            # --- Phase 2 Speed Analytics Tracking ---
            p2_start = time.perf_counter()
            yield f"🤖 [Phase 2/4]: Extract Success. Launching AI core text summary compilation...", None
            summary_output = self.summarizer.generate_summary(result["title"], result["transcript"])
            p2_latency = time.perf_counter() - p2_start
            print(f"⏱️  [Performance Profiler]: Phase 2 AI Core Generation Duration -> {p2_latency:.4f} seconds")
            
            # --- Phase 3 Speed Analytics Tracking ---
            p3_start = time.perf_counter()
            yield f"📊 [Phase 3/4]: Structuring presentation schema configurations via Gemini...", None
            ppt_result = self.ppt_generator.transform_summary_to_slides(
                video_title=result["title"], 
                summary_text=summary_output, 
                target_slides=target_slides, 
                audience_level=audience_level
            )
            p3_latency = time.perf_counter() - p3_start
            print(f"⏱️  [Performance Profiler]: Phase 3 Structural Schema Load Duration -> {p3_latency:.4f} seconds")
            
            if ppt_result["status"] == "failed":
                raise SchemaValidationException(ppt_result["error"])
            
            # --- Phase 4 Speed Analytics Tracking ---
            p4_start = time.perf_counter()
            yield "💾 [Phase 4/4]: Compiling binary blocks into PowerPoint layers...", None
            
            timestamp_token = int(time.time())
            custom_filename = f"Lumina_Presentation_{timestamp_token}.pptx"
            file_path = self.ppt_generator.generate_actual_pptx(ppt_result["data"], custom_filename)
            p4_latency = time.perf_counter() - p4_start
            print(f"⏱️  [Performance Profiler]: Phase 4 PPTX Binary Compilation Duration -> {p4_latency:.4f} seconds")
            
            # End total global benchmarking stream
            total_elapsed_time = time.perf_counter() - global_pipeline_start
            print(f"🏎️  [Performance Profiler]: TOTAL COMPILATION PIPELINE TIME -> {total_elapsed_time:.4f} seconds")
            
            success_status = (
                f"🎉 **Compilation Complete! Speed Tuned Engine Active.**\n\n"
                f"⏱️ **Performance Metrics:** Total Pipeline Process in **{total_elapsed_time:.2f}s**\n"
                f"📡 Phase 1 (Scraper): {p1_latency:.2f}s | 🤖 Phase 2 (Summary): {p2_latency:.2f}s\n"
                f"📊 Phase 3 (Schema): {p3_latency:.2f}s | 💾 Phase 4 (Binary Build): {p4_latency:.2f}s\n\n"
                f"🎬 **Video Context Title:** {result['title']}\n"
                f"💾 **Storage Vector Link:** File optimized and locked down into workspace frames."
            )
            yield success_status, file_path
            return

        yield "🧠 [Router Intelligence]: Action target skipped. System idle.", None
        return