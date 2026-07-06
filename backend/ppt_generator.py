import json
import os
import time
from google import genai
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
#  CLEAN OPENXML NAMESPACE (Removed duplicate broken line 9)
from pptx.oxml.xmlchemy import OxmlElement
from pptx.oxml.ns import qn
from config.settings import GEMINI_API_KEY
from backend.presentation_engine import PresentationPayload

class LuminaPPTGenerator:
    def __init__(self):
        if not GEMINI_API_KEY:
            raise ValueError("❌ Critical Error: GEMINI_API_KEY is missing in environment.")
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.model_name = 'gemini-2.5-flash'

        # Premium Corporate Design Tokens Palette
        self.COLOR_BG = RGBColor(24, 26, 37)           # Eclipse Matte Navy
        self.COLOR_CARD_BG = RGBColor(35, 38, 55)      # Glassmorphism Card Fill
        self.COLOR_TEXT_MAIN = RGBColor(248, 248, 242) # Pearl White Core
        self.COLOR_ACCENT = RGBColor(189, 147, 249)    # Neon Kawaii Purple
        self.COLOR_MUTED = RGBColor(139, 233, 253)     # Cyber Cyan Core Accent

    def transform_summary_to_slides(self, video_title: str, summary_text: str, target_slides: int, audience_level: str) -> dict:
        print(f"📊 [PPT Engine]: Instructing structural payload transformations via Gemini schemas...")
        prompt = f"""
        You are an expert Enterprise AI Slide Architect. Parse the input summary segments and structure it into a clean JSON schema payload matching the exact shape.

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
            print(f"✅ [PPT Engine]: LLM Structural Payload Arrays locked successfully.")
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
        char_count = len(text_string)
        if char_count <= 40:
            return 38
        elif char_count <= 75:
            return 26
        else:
            return 20

    def _generate_mock_visual_placeholder(self, slide, left, top, width, height, placeholder_text: str):
        img_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        img_box.fill.solid()
        img_box.fill.fore_color.rgb = RGBColor(43, 47, 68)
        img_box.line.color.rgb = self.COLOR_MUTED
        img_box.line.width = Pt(1)
        
        tx_box = slide.shapes.add_textbox(left, top + (height / 2) - Inches(0.4), width, Inches(0.8))
        tf = tx_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = f"⚙️ [ VISUAL NODE CONTEXT ]\n{placeholder_text.upper()}"
        p.font.name = 'Segoe UI Semibold'
        p.font.size = Pt(10)
        p.font.color.rgb = self.COLOR_MUTED
        p.alignment = PP_ALIGN.CENTER

    def _inject_fade_transition(self, slide):
        slide_element = slide.element
        transition_node = OxmlElement('p:transition')
        transition_node.set('spd', 'fast')
        fade_node = OxmlElement('p:fade')
        transition_node.append(fade_node)
        slide_element.append(transition_node)

    def _format_rich_bullet_point(self, paragraph, text: str, font_size_pt: int = 13):
        """
        Day 22 Core Addition: Rich Typography Paragraph Formatter.
        Applies precise line-spacing multipliers, whitespace rules, and
        injects distinct typography runs for clean structural layout density.
        """
        paragraph.text = "" # Clearing default text allocations
        
        # 1. Injecting exact line spacing parameters configuration
        paragraph.line_spacing = 1.3               # Line Spacing Multiplier (Clean corporate layout standard)
        paragraph.space_before = Pt(4)             # Padding cushion atop paragraph boundaries
        paragraph.space_after = Pt(12)             # Structural spacing breakdown between text list rows
        
        # 2. Separating bullet marker run block for premium aesthetic alignment
        marker_run = paragraph.add_run()
        marker_run.text = "▪  "
        marker_run.font.name = 'Segoe UI'
        marker_run.font.size = Pt(font_size_pt - 1)
        marker_run.font.bold = True
        marker_run.font.color.rgb = self.COLOR_MUTED # Giving cyan highlights to checkboxes markers
        
        # 3. Main Text Core Body Run block
        body_run = paragraph.add_run()
        body_run.text = text
        body_run.font.name = 'Calibri'
        body_run.font.size = Pt(font_size_pt)
        body_run.font.color.rgb = self.COLOR_TEXT_MAIN

    def generate_actual_pptx(self, structured_data: dict, output_filename: str = "presentation.pptx") -> str:
        print("🛠️ [Typography Architect]: Compiling rich paragraph templates with custom runs...")
        prs = Presentation()
        prs.slide_width = Inches(10)
        prs.slide_height = Inches(7.5)
        blank_layout = prs.slide_layouts[6]

        # ----------------------------------------------------------------------
        # TITLE SLIDE ARCHITECTURE
        # ----------------------------------------------------------------------
        slide = prs.slides.add_slide(blank_layout)
        self._apply_background(slide)
        self._inject_fade_transition(slide)

        master_topic = structured_data.get("topic", "Lumina OS Visual Core").upper()
        dynamic_title_font_size = self._compute_adaptive_font_size(master_topic)

        txBox = slide.shapes.add_textbox(Inches(0.75), Inches(2.2), Inches(8.5), Inches(2.5))
        tf = txBox.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = master_topic
        p.font.name = 'Segoe UI'
        p.font.size = Pt(dynamic_title_font_size)
        p.font.bold = True
        p.font.color.rgb = self.COLOR_ACCENT

        p2 = tf.add_paragraph()
        p2.text = f"Rich Text Run Component Processing Subsystem\nLine Spacing Multiplier: 1.3 Tracker Grid | Total Processed Nodes: {structured_data.get('total_slides', 0)}"
        p2.font.name = 'Segoe UI'
        p2.font.size = Pt(13)
        p2.font.color.rgb = self.COLOR_MUTED
        p2.space_before = Pt(20)

        # ----------------------------------------------------------------------
        # THREE-ZONE INFOGRAPHIC SLIDES GENERATION LOOP
        # ----------------------------------------------------------------------
        for slide_data in structured_data.get("slides", []):
            slide = prs.slides.add_slide(blank_layout)
            self._apply_background(slide)
            self._inject_fade_transition(slide)

            slide_title_text = f"{slide_data.get('slide_number')}. {slide_data.get('title')}"
            local_slide_font_size = self._compute_adaptive_font_size(slide_title_text)
            title_top_offset = Inches(0.5)

            title_box = slide.shapes.add_textbox(Inches(0.75), title_top_offset, Inches(8.5), Inches(1.0))
            tf_title = title_box.text_frame
            tf_title.word_wrap = True
            p_title = tf_title.paragraphs[0]
            p_title.text = slide_title_text
            p_title.font.name = 'Segoe UI'
            p_title.font.size = Pt(min(local_slide_font_size, 26))
            p_title.font.bold = True
            p_title.font.color.rgb = self.COLOR_ACCENT

            points = slide_data.get("bullet_points", [])
            mid_index = (len(points) + 1) // 2
            left_points = points[:mid_index]
            right_points = points[mid_index:]

            col_width = Inches(2.7)
            img_width = Inches(2.6)
            card_height = Inches(4.8)
            content_top_offset = Inches(1.8)

            # ZONE 1: Context Graphic Placeholder
            img_left_start = Inches(0.75)
            self._generate_mock_visual_placeholder(
                slide=slide, left=img_left_start, top=content_top_offset, width=img_width, height=card_height, 
                placeholder_text=slide_data.get('title', 'Analytics Data Core')
            )

            # ZONE 2: TEXT CONTENT COLUMN A (Middle Position with Rich Formatting)
            col_left_start = Inches(3.6)
            self._draw_content_card(slide, col_left_start, content_top_offset, col_width, card_height)
            
            body_box_left = slide.shapes.add_textbox(col_left_start + Inches(0.15), content_top_offset + Inches(0.2), col_width - Inches(0.2), card_height - Inches(0.4))
            tf_left = body_box_left.text_frame
            tf_left.word_wrap = True

            for i, pt_text in enumerate(left_points):
                p_pt = tf_left.paragraphs[0] if i == 0 else tf_left.add_paragraph()
                self._format_rich_bullet_point(p_pt, pt_text, font_size_pt=13)

            # ZONE 3: TEXT CONTENT COLUMN B (Right Position with Rich Formatting)
            col_right_start = Inches(6.55)
            self._draw_content_card(slide, col_right_start, content_top_offset, col_width, card_height)
            
            body_box_right = slide.shapes.add_textbox(col_right_start + Inches(0.15), content_top_offset + Inches(0.2), col_width - Inches(0.2), card_height - Inches(0.4))
            tf_right = body_box_right.text_frame
            tf_right.word_wrap = True

            for i, pt_text in enumerate(right_points):
                p_pt = tf_right.paragraphs[0] if i == 0 else tf_right.add_paragraph()
                self._format_rich_bullet_point(p_pt, pt_text, font_size_pt=13)

        output_dir = "output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        final_path = os.path.join(output_dir, output_filename)
        prs.save(final_path)
        print(f"💾 [Typography Architect]: Rich paragraph style presentation saved safely at: {final_path}")
        return final_path