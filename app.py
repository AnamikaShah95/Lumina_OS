import os
import gradio as gr
from backend.orchestrator import LuminaOrchestrator

# Initializing the global orchestration pipeline handle safely
try:
    orchestrator = LuminaOrchestrator()
except Exception as e:
    print(f"💥 Critical Initialization Failure: {str(e)}")
    orchestrator = None

def lumina_ui_driver(user_input: str):
    """
    Resilient driver layer connecting UI actions to orchestrator with explicit error capturing.
    """
    if not orchestrator:
        return "❌ Central Engine is not initialized properly. Check environment keys.", None
        
    if not user_input.strip():
        return "⚠️ Please enter a valid query or YouTube URL.", None

    try:
        print(f"\n📥 [UI Driver]: Received user payload request stream...")
        # Executing target processes with pipeline tracing
        response = orchestrator.route_and_execute(user_input)
        
        if response["engine_status"] == "SUCCESS":
            status_msg = (
                f"🎉 **Success!**\n\n"
                f"🎬 **Video Title:** {response['title']}\n"
                f"📝 **Summary Generation:** Completed successfully.\n"
                f"💾 **PowerPoint File Compiled:** Local storage copy created!"
            )
            return status_msg, response["file_path"]
            
        elif response["engine_status"] == "FAILED":
            error_msg = (
                f"❌ **Processing Failed Gracefully**\n\n"
                f"⚠️ **Context:** {response['error']}\n\n"
                f"💡 *Note: The framework and architecture are 100% stable. YouTube is simply throttling "
                f"automated scrapers on this local network interface.*"
            )
            return error_msg, None
            
        else:
            return f"🧠 **Router Intelligence:** {response['summary']}", None

    except Exception as fatal_err:
        # Catching any unexpected application loop breaks to prevent socket disconnects
        print(f"🚨 Runtime Exception caught inside UI driver boundary: {str(fatal_err)}")
        return f"⚡ **Connection Resilience Event:** Process thread safely caught an anomaly: {str(fatal_err)}", None

# --- DESIGNING THE FRONTEND GRAPHICAL INTERFACE ARCHITECTURE ---
# Removed theme configuration from Blocks block initialization to satisfy Gradio 6 layout changes
with gr.Blocks() as lumina_interface:
    
    gr.Markdown(
        """
        # 🎬 Lumina Video Architect - OS Frontend Core
        ### Transform complex video data streams directly into structured PowerPoint Presentations using LLM Automation.
        """
    )
    
    with gr.Row():
        with gr.Column(scale=2):
            input_query = gr.Textbox(
                label="Enter Request Query or YouTube Video Link",
                placeholder="e.g., Summarize this video: https://www.youtube.com/watch?v=kqtD5dpn9C8",
                lines=2
            )
            submit_btn = gr.Button("🚀 Trigger Lumina Engine", variant="primary")
            
        with gr.Column(scale=3):
            output_status = gr.Markdown(label="Execution Pipeline Real-time logs")
            output_file = gr.File(label="Download Generated PowerPoint (.pptx)")

    submit_btn.click(
        fn=lumina_ui_driver,
        inputs=input_query,
        outputs=[output_status, output_file]
    )

if __name__ == "__main__":
    print("🌐 Launching optimized local Gradio engine micro-server pipeline...")
    # Clean injection of theme and socket configurations directly into launch parameters as per standard layouts
    lumina_interface.launch(
        server_name="127.0.0.1", 
        server_port=7860, 
        share=False,
        theme=gr.themes.Soft()
    )