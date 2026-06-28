import json
from google import genai
from config.settings import GEMINI_API_KEY
from backend.presentation_engine import PresentationPayload

class LuminaPPTGenerator:
    def __init__(self):
        if not GEMINI_API_KEY:
            raise ValueError("❌ Critical Error: GEMINI_API_KEY is missing in environment.")
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.model_name = 'gemini-2.5-flash'

    def transform_summary_to_slides(self, video_title: str, summary_text: str) -> dict:
        """
        Converts Markdown summaries into structured Presentation JSON structures safely.
        """
        print("🎨 [PPT Generator]: Structuring markdown summary into dynamic slide layout blocks...")
        
        prompt = f"""
        You are a Master Presentation Designer. Convert the following technical video summary into a clean, slide-by-slide presentation structure.
        The presentation should be highly structured, engaging, and perfect for engineering students.
        
        Video Title: {video_title}
        Source Summary Text:
        {summary_text}
        """

        try:
            # Using Gemini Structured Outputs to strictly enforce our Pydantic Schema
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config={
                    'response_mime_type': 'application/json',
                    'response_schema': PresentationPayload,
                }
            )
            
            # Parsing the verified structured JSON text output
            structured_data = json.loads(response.text)
            return {
                "status": "success",
                "data": structured_data,
                "error": None
            }
        except Exception as e:
            return {
                "status": "failed",
                "data": None,
                "error": f"Presentation Layer Structuring Failed: {str(e)}"
            }