import json
import os
from google import genai
from pptx import Presentation
from pptx.util import Inches, Pt
from config.settings import GEMINI_API_KEY
from backend.presentation_engine import PresentationPayload

class LuminaPPTGenerator:
    def __init__(self):
        if not GEMINI_API_KEY:
            raise ValueError("❌ Critical Error: GEMINI_API_KEY is missing in environment.")
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.model_name = 'gemini-2.5-flash'

    def transform_summary_to_slides(self, video_title: str, summary_text: str, target_slides: int, audience_level: str) -> dict:
        """
        Day 10 Upgrade: Injects dynamic user configurations directly into the LLM context stream.
        """
        print(f"🎨 [PPT Generator]: Injecting pipeline parameters -> Target Slides: {target_slides} | Depth: {audience_level}")
        
        # Crafting an adaptive, context-aware prompt matrix
        prompt = f"""
        You are a Master Presentation Designer. Convert the following technical video summary into a clean, slide-by-slide presentation structure.
        
        CRITICAL CUSTOM RULES:
        1. You MUST generate EXACTLY {target_slides} structured content slides (excluding title slide logic).
        2. Tailor the language complexity, depth, and technical density specifically for an audience level of: '{audience_level}'.
        
        Video Title: {video_title}
        Source Summary Text:
        {summary_text}
        """
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config={
                    'response_mime_type': 'application/json',
                    'response_schema': PresentationPayload,
                }
            )
            structured_data = json.loads(response.text)
            return {"status": "success", "data": structured_data, "error": None}
        except Exception as e:
            return {"status": "failed", "data": None, "error": f"Presentation Layer Structuring Failed: {str(e)}"}

    def generate_actual_pptx(self, structured_data: dict, output_filename: str = "presentation.pptx") -> str:
        print("🛠️ [PPT Generator]: Creating physical PowerPoint slides via python-pptx...")
        prs = Presentation()
        
        # Title Slide (Slide Layout 0)
        title_slide_layout = prs.slide_layouts[0]
        slide = prs.slides.add_slide(title_slide_layout)
        title = slide.shapes.title
        subtitle = slide.placeholders[1]
        
        title.text = structured_data.get("topic", "Lumina OS Presentation")
        subtitle.text = f"Automated Engineering Analytics\nTotal Slides: {structured_data.get('total_slides', 0)}"
        
        # Content Slides Loop
        for slide_data in structured_data.get("slides", []):
            blank_layout = prs.slide_layouts[1]
            slide = prs.slides.add_slide(blank_layout)
            
            slide_title = slide.shapes.title
            slide_title.text = f"{slide_data.get('slide_number')}. {slide_data.get('title')}"
            
            body_shape = slide.placeholders[1]
            tf = body_shape.text_frame
            tf.clear()
            
            points = slide_data.get("bullet_points", [])
            for i, pt_text in enumerate(points):
                p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
                p.text = pt_text
                p.level = 0
                p.space_after = Pt(10)
                
        output_dir = "output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        final_path = os.path.join(output_dir, output_filename)
        prs.save(final_path)
        print(f"💾 [PPT Generator]: File saved successfully at: {final_path}")
        return final_path