import os
from google import genai
from config.settings import GEMINI_API_KEY

class LuminaSummarizer:
    def __init__(self):
        if not GEMINI_API_KEY:
            raise ValueError("❌ Critical Error: GEMINI_API_KEY matrix is missing in environment.")
        # Initializing the new Google GenAI SDK client architecture
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.model_name = 'gemini-2.5-flash'

    def generate_summary(self, video_title: str, transcript_text: str) -> str:
        """
        Processes transcript payloads and structures them into systemic, beautiful Markdown summaries.
        """
        if not transcript_text or len(transcript_text.strip()) == 0:
            return "⚠️ No valid transcript payload found to summarize."

        # Structured Prompt Matrix optimization
        prompt = f"""
        You are Lumina Video Architect, an expert technical summarizer.
        Analyze the following YouTube video transcript and generate a highly structured, clean Markdown summary.
        
        Video Title: {video_title}
        Transcript: {transcript_text}
        
        Please format your output exactly as follows:
        # 🎬 Executive Overview
        [Provide a concise 2-3 sentence strategic summary of the entire video context]
        
        ## 🧠 Core Structural Pillars & Key Takeaways
        - **[Key Concept Name]**: Detailed technical explanation or contextual point.
        - **[Key Concept Name]**: Focus areas, actionable insights, or development highlights.
        
        ## 💡 Actionable Summary & Conclusion
        [A quick wrap-up statement summarizing the ultimate value of the content]
        """

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            return response.text
        except Exception as e:
            return f"❌ LLM Processing Layer Failed: {str(e)}"