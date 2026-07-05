import json
import os
from google import genai
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from config.settings import GEMINI_API_KEY
from backend.presentation_engine import PresentationPayload

class LuminaPPTGenerator:
    def __init__(self):
        if not GEMINI_API_KEY:
            raise ValueError("❌ Critical Error: GEMINI_API_KEY is missing in environment.")
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.model_name = 'gemini-2.5-flash'

        # Day 15 Professional Theme Tokens Grid (Kawaii Deep Dark Theme Aesthetics)
        self.COLOR_BG = RGBColor(30, 32, 44)         # Deep Charcoal Navy
        self.COLOR_TEXT_MAIN = RGBColor(248, 248, 242) # Pure Light Pearl
        self.COLOR_ACCENT = RGBColor(189, 147, 249)    # Kawaii Radiant Purple
        self.COLOR_MUTED = RGBColor(139, 233, 253)     # Cyber Cyan Accent

    def transform_summary_to_slides(self, video_title: str, summary_text: str, target_slides: int, audience_level: str) -> dict:
        print(f"🎨 [PPT Engine]: Instructing strict arrays parsing matching -> Targets: {target_slides} slides.")
        prompt = f"""
        You are an expert Enterprise AI Slide Architect. Parse the summary block and structure it into a JSON schema payload matching the exact shape.

        CRITICAL CONSTRAINTS:
        1. Create exactly {target_slides} individual items inside the 'slides' list array.
        2. Set the 'total_slides' field integer value to exactly equal {target_slides}.
        3. Target Depth Profile: '{audience_level}'.
        4. Inside every slide object, the 'bullet_points' array MUST contain between 3 to 5 clear talking strings.

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
            print(f"✅ [PPT Engine]: Generation successful. Metadata bounds locked.")
            return {"status": "success", "data": structured_data, "error": None}
        except Exception as e:
            return {"status": "failed", "data": None, "error": str(e)}

    def _apply_background(self, slide):
        """Day 15 UI Addition: Injects full-bleed custom rectangular shape masks to mimic canvas fills."""
        left = top = Inches(0)
        width = Inches(10)
        height = Inches(7.5)
        bg_shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
        bg_shape.fill.solid()
        bg_shape.fill.fore_color.rgb = self.COLOR_BG
        bg_shape.line.fill.background() # Clear borders array outline

    def generate_actual_pptx(self, structured_data: dict, output_filename: str = "presentation.pptx") -> str:
        print("🛠️ [PPT Engine]: Compiling structural layout tokens via python-pptx presentation core...")
        prs = Presentation()
        prs.slide_width = Inches(10)
        prs.slide_height = Inches(7.5)

        # ----------------------------------------------------------------------
        # TITLE SLIDE ARCHITECTURE
        # ----------------------------------------------------------------------
        blank_layout = prs.slide_layouts[6] # Absolute blank layout container logic
        slide = prs.slides.add_slide(blank_layout)
        self._apply_background(slide)

        # Title Box Element Configuration
        txBox = slide.shapes.add_textbox(Inches(0.75), Inches(2.2), Inches(8.5), Inches(2.0))
        tf = txBox.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = structured_data.get("topic", "Lumina OS Ecosystem").upper()
        p.font.name = 'Segoe UI'
        p.font.size = Pt(40)
        p.font.bold = True
        p.font.color.rgb = self.COLOR_ACCENT
        p.alignment = PP_ALIGN.LEFT

        # Subtitle Subsystem Injection
        p2 = tf.add_paragraph()
        p2.text = f"Automated Architecture Analytics Engine\nAudience Level Profile: Active System Matrix | Slides: {structured_data.get('total_slides', 0)}"
        p2.font.name = 'Segoe UI'
        p2.font.size = Pt(14)
        p2.font.color.rgb = self.COLOR_MUTED
        p2.space_before = Pt(24)

        # ----------------------------------------------------------------------
        # CONTENT SLIDES MATRIX GENERATION LOOP
        # ----------------------------------------------------------------------
        for slide_data in structured_data.get("slides", []):
            slide = prs.slides.add_slide(blank_layout)
            self._apply_background(slide)

            # Slide Individual Title
            title_box = slide.shapes.add_textbox(Inches(0.75), Inches(0.6), Inches(8.5), Inches(1.0))
            tf_title = title_box.text_frame
            tf_title.word_wrap = True
            p_title = tf_title.paragraphs[0]
            p_title.text = f"{slide_data.get('slide_number')}. {slide_data.get('title')}"
            p_title.font.name = 'Segoe UI'
            p_title.font.size = Pt(26)
            p_title.font.bold = True
            p_title.font.color.rgb = self.COLOR_ACCENT

            # Content Bullet Point Bounding Box
            body_box = slide.shapes.add_textbox(Inches(0.75), Inches(2.0), Inches(8.5), Inches(4.5))
            tf_body = body_box.text_frame
            tf_body.word_wrap = True

            points = slide_data.get("bullet_points", [])
            for i, pt_text in enumerate(points):
                p_pt = tf_body.paragraphs[0] if i == 0 else tf_body.add_paragraph()
                p_pt.text = f"•  {pt_text}"
                p_pt.font.name = 'Calibri'
                p_pt.font.size = Pt(16)
                p_pt.font.color.rgb = self.COLOR_TEXT_MAIN
                p_pt.space_after = Pt(14)
                p_pt.level = 0

        output_dir = "output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        final_path = os.path.join(output_dir, output_filename)
        prs.save(final_path)
        print(f"💾 [PPT Engine]: Themed template saved successfully at: {final_path}")
        return final_path