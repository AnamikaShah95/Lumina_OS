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

        # Premium Layout Design Tokens Grid (Kawaii Dark Matrix)
        self.COLOR_BG = RGBColor(24, 26, 37)           # Deeper Eclipse Matte Navy
        self.COLOR_CARD_BG = RGBColor(35, 38, 55)      # Soft Glassmorphism Card Fill
        self.COLOR_TEXT_MAIN = RGBColor(248, 248, 242) # Pearl White Core
        self.COLOR_ACCENT = RGBColor(189, 147, 249)    # Neon Kawaii Purple
        self.COLOR_MUTED = RGBColor(139, 233, 253)     # Cyber Cyan Core Accent

    def transform_summary_to_slides(self, video_title: str, summary_text: str, target_slides: int, audience_level: str) -> dict:
        print(f"📊 [PPT Engine]: Transforming video intelligence summaries using structural payload bounds...")
        prompt = f"""
        You are an expert Enterprise AI Slide Architect. Parse the input text blocks and structure it into a clean JSON schema payload matching the exact shape.

        CRITICAL CONSTRAINTS:
        1. Create exactly {target_slides} individual items inside the 'slides' list block array.
        2. Set the 'total_slides' field integer value to exactly equal {target_slides}.
        3. Target Depth Profile: '{audience_level}'.
        4. Inside every slide object, the 'bullet_points' array MUST contain between 3 to 5 clear strings.

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
            print(f"✅ [PPT Engine]: LLM Structural Payload Arrays synced successfully.")
            return {"status": "success", "data": structured_data, "error": None}
        except Exception as e:
            return {"status": "failed", "data": None, "error": str(e)}

    def _apply_background(self, slide):
        left = top = Inches(0)
        width = Inches(10)
        height = Inches(7.5)
        bg_shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
        bg_shape.fill.solid()
        bg_shape.fill.fore_color.rgb = self.COLOR_BG
        bg_shape.line.fill.background()

    def _draw_content_card(self, slide, left, top, width, height):
        card = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = self.COLOR_CARD_BG
        card.line.fill.background()
        
        accent_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, Inches(0.08), height)
        accent_bar.fill.solid()
        accent_bar.fill.fore_color.rgb = self.COLOR_MUTED
        accent_bar.line.fill.background()

    def _compute_adaptive_font_size(self, text_string: str) -> int:
        """
        Day 18 Architectural Addition: Algorithmic Font Scaler Socket.
        Tracks character footprint density dynamically to compute optimal font sizes.
        """
        char_count = len(text_string)
        print(f"📐 [Font Scaler]: Analyzing string metric footprint -> Length: {char_count} chars.")
        
        if char_count <= 40:
            return 38  # Ultra Bold High Impact Heading
        elif char_count <= 75:
            return 26  # Medium Scaled Consolidated Heading
        else:
            return 20  # Dense Micro Compressed Heading (Overflow Shield)

    def generate_actual_pptx(self, structured_data: dict, output_filename: str = "presentation.pptx") -> str:
        print("🛠️ [Typography Engine]: Compiling spatial layouts with typography scaling hooks...")
        prs = Presentation()
        prs.slide_width = Inches(10)
        prs.slide_height = Inches(7.5)
        blank_layout = prs.slide_layouts[6]

        # ----------------------------------------------------------------------
        # TITLE SLIDE ARCHITECTURE (WITH AUTO-SCALING ALGORITHM)
        # ----------------------------------------------------------------------
        slide = prs.slides.add_slide(blank_layout)
        self._apply_background(slide)

        # Dynamic Extraction of Master Topic String
        master_topic = structured_data.get("topic", "Lumina OS Visual Core").upper()
        
        # Computing font size token programmatically matching the layout state
        dynamic_title_font_size = self._compute_adaptive_font_size(master_topic)

        txBox = slide.shapes.add_textbox(Inches(0.75), Inches(2.2), Inches(8.5), Inches(2.5))
        tf = txBox.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = master_topic
        p.font.name = 'Segoe UI'
        p.font.size = Pt(dynamic_title_font_size) # Dynamic Injected Pt Value
        p.font.bold = True
        p.font.color.rgb = self.COLOR_ACCENT

        p2 = tf.add_paragraph()
        p2.text = f"Asynchronous Typography Adaptation Interface Engine\nTotal Context Layout Nodes: {structured_data.get('total_slides', 0)} Content Grid Columns System"
        p2.font.name = 'Segoe UI'
        p2.font.size = Pt(13)
        p2.font.color.rgb = self.COLOR_MUTED
        p2.space_before = Pt(20)

        # ----------------------------------------------------------------------
        # DUAL-COLUMN SLIDES LOGIC WITH LOCAL TITLE MATRIX SCALE CHECK
        # ----------------------------------------------------------------------
        for slide_data in structured_data.get("slides", []):
            slide = prs.slides.add_slide(blank_layout)
            self._apply_background(slide)

            slide_title_text = f"{slide_data.get('slide_number')}. {slide_data.get('title')}"
            local_slide_font_size = self._compute_adaptive_font_size(slide_title_text)
            
            # Bound adjustments: Adjusting top offset if headings scale too small or too dense
            title_top_offset = Inches(0.6) if local_slide_font_size >= 26 else Inches(0.4)

            title_box = slide.shapes.add_textbox(Inches(0.75), title_top_offset, Inches(8.5), Inches(1.0))
            tf_title = title_box.text_frame
            tf_title.word_wrap = True
            p_title = tf_title.paragraphs[0]
            p_title.text = slide_title_text
            p_title.font.name = 'Segoe UI'
            p_title.font.size = Pt(min(local_slide_font_size, 26)) # Cap internal slide headers at 26 max
            p_title.font.bold = True
            p_title.font.color.rgb = self.COLOR_ACCENT

            points = slide_data.get("bullet_points", [])
            mid_index = (len(points) + 1) // 2
            left_points = points[:mid_index]
            right_points = points[mid_index:]

            col_width = Inches(4.1)
            card_height = Inches(4.8)
            content_top_offset = Inches(1.8)

            # --- COLUMN A: LEFT BLOCK POSITIONING ---
            col_left_start = Inches(0.75)
            self._draw_content_card(slide, col_left_start, content_top_offset, col_width, card_height)
            
            body_box_left = slide.shapes.add_textbox(col_left_start + Inches(0.2), content_top_offset + Inches(0.2), col_width - Inches(0.3), card_height - Inches(0.4))
            tf_left = body_box_left.text_frame
            tf_left.word_wrap = True

            for i, pt_text in enumerate(left_points):
                p_pt = tf_left.paragraphs[0] if i == 0 else tf_left.add_paragraph()
                p_pt.text = f"▪ {pt_text}"
                p_pt.font.name = 'Calibri'
                p_pt.font.size = Pt(14)
                p_pt.font.color.rgb = self.COLOR_TEXT_MAIN
                p_pt.space_after = Pt(14)

            # --- COLUMN B: RIGHT BLOCK POSITIONING ---
            col_right_start = Inches(5.15)
            self._draw_content_card(slide, col_right_start, content_top_offset, col_width, card_height)
            
            body_box_right = slide.shapes.add_textbox(col_right_start + Inches(0.2), content_top_offset + Inches(0.2), col_width - Inches(0.3), card_height - Inches(0.4))
            tf_right = body_box_right.text_frame
            tf_right.word_wrap = True

            for i, pt_text in enumerate(right_points):
                p_pt = tf_right.paragraphs[0] if i == 0 else tf_right.add_paragraph()
                p_pt.text = f"▪ {pt_text}"
                p_pt.font.name = 'Calibri'
                p_pt.font.size = Pt(14)
                p_pt.font.color.rgb = self.COLOR_TEXT_MAIN
                p_pt.space_after = Pt(14)

        output_dir = "output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        final_path = os.path.join(output_dir, output_filename)
        prs.save(final_path)
        print(f"💾 [Typography Engine]: Optimized auto-scaled file saved successfully at: {final_path}")
        return final_path