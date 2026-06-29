import json
import os
from google import genai
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from config.settings import GEMINI_API_KEY
from backend.presentation_engine import PresentationPayload

class LuminaPPTGenerator:
    def __init__(self):
        if not GEMINI_API_KEY:
            raise ValueError("❌ Critical Error: GEMINI_API_KEY is missing in environment.")
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.model_name = 'gemini-2.5-flash'

    def transform_summary_to_slides(self, video_title: str, summary_text: str) -> dict:
        print("🎨 [PPT Generator]: Structuring markdown summary into dynamic slide layout blocks...")
        prompt = f"""
        You are a Master Presentation Designer. Convert the following technical video summary into a clean, slide-by-slide presentation structure.
        The presentation should be highly structured, engaging, and perfect for engineering students.
        
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
        """
        Converts Structured JSON Data physically into a beautiful .pptx file.
        """
        print("🛠️ [PPT Generator]: Creating physical PowerPoint slides via python-pptx...")
        
        prs = Presentation()
        
        # 1. Title Slide (Slide Layout 0)
        title_slide_layout = prs.slide_layouts[0]
        slide = prs.slides.add_slide(title_slide_layout)
        
        title = slide.shapes.title
        subtitle = slide.placeholders[1]
        
        title.text = structured_data.get("topic", "Lumina OS Presentation")
        subtitle.text = f"Automated Engineering Analytics\nTotal Slides: {structured_data.get('total_slides', 0)}"
        
        # 2. Content Slides Loop
        for slide_data in structured_data.get("slides", []):
            # Using blank layout (6) or title+content layout (1) for custom precise styling
            blank_layout = prs.slide_layouts[1]
            slide = prs.slides.add_slide(blank_layout)
            
            # Slide Heading
            slide_title = slide.shapes.title
            slide_title.text = f"{slide_data.get('slide_number')}. {slide_data.get('title')}"
            
            # Slide Body Points
            body_shape = slide.placeholders[1]
            tf = body_shape.text_frame
            tf.clear()  # Clear default text
            
            points = slide_data.get("bullet_points", [])
            for i, pt_text in enumerate(points):
                p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
                p.text = pt_text
                p.level = 0
                p.space_after = Pt(10)
                
        # Ensuring output directory exists securely
        output_dir = "output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        final_path = os.path.join(output_dir, output_filename)
        prs.save(final_path)
        print(f"💾 [PPT Generator]: File saved successfully at: {final_path}")
        return final_path