import os
import gradio as gr

from backend.orchestrator import LuminaOrchestrator
from backend.exceptions import TranscriptExtractionError, SchemaValidationException, LuminaCoreException

try:
    orchestrator = LuminaOrchestrator()
except Exception as e:
    print(f"💥 Critical Initialization Failure: {str(e)}")
    orchestrator = None

def lumina_ui_driver(user_input: str, slide_count: int, audience_level: str):
    """
    Day 14 UI Driver: Iterates through the streaming orchestrator logs.
    Intercepts custom domain exceptions and outputs visually rich Markdown alerts.
    """
    if not orchestrator:
        yield "❌ Central Engine is not initialized properly. Check environment keys.", None
        return
        
    if not user_input.strip():
        yield "⚠️ Please enter a valid query or YouTube URL.", None
        return

    try:
        print(f"\n📥 [UI Driver]: Triggering async error-aware orchestration stream...")
        for log_update, target_file_path in orchestrator.route_and_execute_stream(
            user_query=user_input, 
            target_slides=slide_count, 
            audience_level=audience_level
        ):
            yield log_update, target_file_path

    except TranscriptExtractionError as tex:
        print(f"🚨 [UI Interceptor]: Caught expected Scraper Anomaly -> {str(tex)}")
        alert_layout = (
            f"### 📯 System Alert: Video Transcript Missing\n"
            f"```x86asm\n[STATUS: TRANSCRIPT_EXTRACTION_FAILURE | LEVEL: {tex.alert_level}]\n```\n"
            f"⚠️ **Context Diagnostics:** {tex.message}\n\n"
            f"💡 *Developer Troubleshooting Note: The pipeline structure is perfectly intact. The remote video target layout is simply empty or restricts automation bots.*"
        )
        yield alert_layout, None

    except SchemaValidationException as sve:
        print(f"🚨 [UI Interceptor]: Caught expected Schema Mismatch -> {str(sve)}")
        alert_layout = (
            f"### 💣 System Alert: JSON Validation Anomaly\n"
            f"```x86asm\n[STATUS: Pydantic_SCHEMA_VIOLATION | LEVEL: {sve.alert_level}]\n```\n"
            f"❌ **Parser Error Stack:** {sve.message}\n\n"
            f"💡 *Developer Troubleshooting Note: Gemini response tokens generated a schema variance breaking the Pydantic type validator definitions.*"
        )
        yield alert_layout, None

    except Exception as fatal_err:
        print(f"🚨 [UI Interceptor]: Unmanaged Critical Fatal Crash -> {str(fatal_err)}")
        yield f"💥 **Fatal Core Anomaly:** System Thread Level Crash Managed: {str(fatal_err)}", None

with gr.Blocks() as lumina_interface:
    gr.Markdown(
        """
        # 🎬 Lumina Video Architect - OS Frontend Core v2.3 (Toast Engine)
        ### Transform video data streams into custom, automated PowerPoint presentations with fine-tuned user controls.
        """
    )
    with gr.Row():
        with gr.Column(scale=2):
            input_query = gr.Textbox(
                label="Enter Request Query or YouTube Video Link",
                placeholder="e.g., Summarize this video: https://www.youtube.com/watch?v=kqtD5dpn9C8",
                lines=2
            )
            
            with gr.Accordion("⚙️ Advanced Presentation Settings", open=True):
                slide_slider = gr.Slider(minimum=3, maximum=15, value=7, step=1, label="Target Slide Count")
                audience_dropdown = gr.Dropdown(
                    choices=["Beginner Student", "Advanced Engineering", "Executive Overview"], 
                    value="Advanced Engineering", 
                    label="Audience Depth Level"
                )
            submit_btn = gr.Button("🚀 Trigger Lumina Engine", variant="primary")
            
        with gr.Column(scale=3):
            output_status = gr.Markdown(label="Execution Pipeline Real-time logs")
            output_file = gr.File(label="Download Generated PowerPoint (.pptx)")

    submit_btn.click(
        fn=lumina_ui_driver,
        inputs=[input_query, slide_slider, audience_dropdown],
        outputs=[output_status, output_file]
    )

if __name__ == "__main__":
    print("🌐 Launching custom-configured local Gradio interface engine...")
    lumina_interface.launch(server_name="127.0.0.1", server_port=7860, share=False, theme=gr.themes.Soft())
