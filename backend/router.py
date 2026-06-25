import os
import sys

# Framework engine path setting
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(CURRENT_DIR)
if PARENT_DIR not in sys.path:
    sys.path.append(PARENT_DIR)

from config.settings import GEMINI_API_KEY
from pydantic import BaseModel, Field
from typing import Literal, Optional
from google import genai
from google.genai import types
from config.settings import GEMINI_API_KEY

# 1. Base Structure for Entities (Bina kisi extra config dict ke)
class ExtractedEntities(BaseModel):
    video_url: Optional[str] = Field(default=None, description="The URL of the YouTube video if provided.")
    topic: Optional[str] = Field(default=None, description="The main topic or subject of presentation/query.")
    tone: Optional[str] = Field(default=None, description="The requested tone (e.g., professional, casual).")

# 2. Main Response Schema
class IntentRoutingResponse(BaseModel):
    intent: Literal["summarize", "generate_ppt", "general_query"] = Field(
        description="The detected intent of the user query."
    )
    confidence_score: float = Field(
        description="Confidence score of the intent classification between 0.0 and 1.0"
    )
    extracted_entities: ExtractedEntities = Field(
        description="Structured entities extracted from the query."
    )

def route_user_intent(user_query: str) -> IntentRoutingResponse:
    """
    Analyzes the user query and routes it strictly into structured JSON.
    """
    if not GEMINI_API_KEY:
        raise ValueError("Critical Error: GEMINI_API_KEY missing in router context.")

    client = genai.Client(api_key=GEMINI_API_KEY)

    system_instruction = (
        "You are the Core Intent Router of Lumina OS. Your job is to classify user queries "
        "into one of three intents: 'summarize', 'generate_ppt', or 'general_query'. "
        "Extract fields like video_url, topic, or tone if present inside the extracted_entities structure."
    )

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_query,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json",
                response_schema=IntentRoutingResponse,
                temperature=0.1
            ),
        )
        
        return IntentRoutingResponse.model_validate_json(response.text)

    except Exception as e:
        print(f"❌ Router Engine Exception: {str(e)}")
        return IntentRoutingResponse(
            intent="general_query", 
            confidence_score=0.0, 
            extracted_entities=ExtractedEntities()
        )