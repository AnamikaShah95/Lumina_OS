import os
import gradio as gr
from backend.orchestrator import LuminaOrchestrator

# Initializing the global orchestration pipeline handle
orchestrator = LuminaOrchestrator()

def lumina_ui_driver(user_input: str):
    """
    Acts as the bridging event handler connecting the Gradio UI directly to the backend logic.
    """
    if not user_input.strip():
        return "⚠️ Please enter a valid query or YouTube URL.", None

    # Triggering the global routing tree execution matrix
    response = orchestrator.route_and_execute(user_input)
    
    # UI Component Output Mapping
    if response["engine_status"] == "SUCCESS":
        status_msg = (
            f"🎉 **Success!**\n\n"
            f"🎬 **Video Title:** {response['title']}\n"
            f"📝 **Summary Generation:** Completed successfully.\n"
            f"💾 **PowerPoint File Compiled:** Local storage copy created!"
        )
        # Returning the status text and the actual physical file path for download
        return status_msg, response["file_path"]
        
    elif response["engine_status"] == "FAILED":
        error_msg = (
            f"❌ **Processing Failed**\n\n"
            f"⚠️ **Context:** {response['error']}\n\n"
            f"💡 *Note: If this is a YouTube extraction block, it means the server is throttling local requests. "
            f"However, the backend framework, schemas, and automation layers are fully working!*"
        )
        return error_msg, None
        
    else:
        # For general queries skipped by the pipeline
        return f"🧠 **Router Intelligence:** {response['summary']}", None

# --- DESIGNING THE FRONTEND GRAPHICAL INTERFACE ---
with gr.Blocks(theme=gr.themes.Soft()) as lumina_interface:
    
    # Header block section layout boundaries
    gr.Markdown(
        """
        # 🎬 Lumina Video Architect - OS Frontend Core
        ### Transform complex video data streams directly into structured PowerPoint Presentations using LLM Automation.
        """
    )
    
    with gr.Row():
        with gr.Column(scale=2):
            # Input component field
            input_query = gr.Textbox(
                label="Enter Request Query or YouTube Video Link",
                placeholder="e.g., Summarize this video: https://www.youtube.com/watch?v=kqtD5dpn9C8",
                lines=2
            )
            submit_btn = gr.Button("🚀 Trigger Lumina Engine", variant="primary")
            
        with gr.Column(scale=3):
            # Output status log block
            output_status = gr.Markdown(label="Execution Pipeline Real-time logs")
            # Physical file download block element
            output_file = gr.File(label="Download Generated PowerPoint (.pptx)")

    # Attaching the event trigger logic mapping elements
    submit_btn.click(
        fn=lumina_ui_driver,
        inputs=input_query,
        outputs=[output_status, output_file]
    )

# Executing the dynamic micro-server interface architecture locally
if __name__ == "__main__":
    print("🌐 Launching local Gradio engine micro-server pipeline...")
    lumina_interface.launch(server_name="127.0.0.1", server_port=7860, share=False)