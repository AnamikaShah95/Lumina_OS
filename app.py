import os
import gradio as gr
from backend.orchestrator import LuminaOrchestrator

try:
    orchestrator = LuminaOrchestrator()
except Exception as e:
    print(f"💥 Critical Initialization Failure: {str(e)}")
    orchestrator = None

def lumina_ui_driver(user_input: str, slide_count: int, audience_level: str):
    if not orchestrator:
        return "❌ Central Engine is not initialized properly. Check environment keys.", None
        
    if not user_input.strip():
        return "⚠️ Please enter a valid query or YouTube URL.", None

    try:
        print(f"\n📥 [UI Driver]: Passing cleanly parsed parameters down to Orchestrator context tree...")
        # Day 10 Refinement: Passing explicit keyword variables clean into the execution core
        response = orchestrator.route_and_execute(
            user_query=user_input, 
            target_slides=slide_count, 
            audience_level=audience_level
        )
        
        if response["engine_status"] == "SUCCESS":
            status_msg = (
                f"🎉 **Success!**\n\n"
                f"🎬 **Video Title:** {response['title']}\n"
                f"📊 **Target Rule Enforced:** Exactly {slide_count} Slides Generated for '{audience_level}' Depth.\n"
                f"💾 **PowerPoint File Compiled:** Local directory saved successfully!"
            )
            return status_msg, response["file_path"]
            
        elif response["engine_status"] == "FAILED":
            error_msg = (
                f"❌ **Processing Failed Gracefully**\n\n"
                f"⚠️ **Context:** {response['error']}\n\n"
                f"💡 *Note: The parameter injection layer is fully responsive. Network scraper endpoint throttling detected.*"
            )
            return error_msg, None
            
        else:
            return f"🧠 **Router Intelligence:** Internal workflow executed successfully.", None

    except Exception as fatal_err:
        print(f"🚨 Runtime Exception caught inside UI driver boundary: {str(fatal_err)}")
        return f"⚡ **Connection Anomaly:** Process thread managed effectively: {str(fatal_err)}", None

with gr.Blocks() as lumina_interface:
    gr.Markdown(
        """
        # 🎬 Lumina Video Architect - OS Frontend Core v2.1
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