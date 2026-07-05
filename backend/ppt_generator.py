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
        Day 13 Schema Tuning Upgrade: Injects rigid formatting boundaries directly matching Pydantic definitions.
        """
        print(f"🎨 [PPT Generator]: Aligning explicit strict arrays -> Targets: {target_slides} slides ({audience_level})")
        
        # Structuring a zero-deviation instructions matrix to secure Pydantic compilation layers
        prompt = f"""
        You are an expert Enterprise AI Slide Architect. Your sole directive is to parse the source technical summary block and structure it into a valid JSON schema payload matching the exact shape required.

        CRITICAL CONSTRAINTS:
        1. You must create exactly {target_slides} individual items inside the 'slides' list block array. No more, no less.
        2. Set the 'total_slides' field integer value to exactly equal {target_slides}.
        3. Customize the content depth density precisely targeting the linguistic footprint profile of an expert tracking: '{audience_level}'.
        4. Inside every slide object entity, the 'bullet_points' array field MUST contain a strict count list between 3 to 5 clear strings.

        Metadata Context:
        Master Title: {video_title}
        Source Text Component Payload:
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
            print(f"✅ [PPT Generator]: LLM Generation succeeded. Array length confirmed at: {len(structured_data.get('slides', []))}")
            return {"status": "success", "data": structured_data, "error": None}
        except Exception as e:
            print(f"🚨 [Schema Fault]: Generation serialization anomaly: {str(e)}")
            return {"status": "failed", "data": None, "error": f"Schema Presentation Structuring Failed: {str(e)}"}

    def generate_actual_pptx(self, structured_data: dict, output_filename: str = "presentation.pptx") -> str:
        print("🛠️ [PPT Generator]: Building file blocks via python-pptx presentation core...")
        prs = Presentation()
        
        # Title Slide Frame Layout
        title_slide_layout = prs.slide_layouts[0]
        slide = prs.slides.add_slide(title_slide_layout)
        title = slide.shapes.title
        subtitle = slide.placeholders[1]
        
        title.text = structured_data.get("topic", "Lumina OS Presentation")
        subtitle.text = f"Automated Engineering Analytics\nTarget Audience Profile: Open Ecosystem\nTotal Content Structures: {structured_data.get('total_slides', 0)}"
        
        # Generating Slide Loop Framework Rows
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