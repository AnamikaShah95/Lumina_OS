import os
import sys

# System runtime mapping setup
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(CURRENT_DIR)
if PARENT_DIR not in sys.path:
    sys.path.append(PARENT_DIR)

from backend.router import route_user_intent
from backend.video_engine import fetch_video_data, VideoDataPayload
from pydantic import BaseModel
from typing import Optional

class OrchestratorOutput(BaseModel):
    intent: str
    confidence_score: float
    video_payload: Optional[VideoDataPayload] = None
    raw_query: str

def process_lumina_request(user_query: str) -> OrchestratorOutput:
    print(f"⚡ [Orchestrator]: Analyzing incoming network request stream...")
    
    # 1. Day 2 Intent Router Engine trigger karein
    route_result = route_user_intent(user_query)
    print(f"🧠 [Router]: Detected Intent -> '{route_result.intent}' (Confidence: {route_result.confidence_score})")

    # 2. Dynamic Payload Syncing Matrix
    video_payload = None
    if route_result.intent == "summarize" and route_result.extracted_entities.video_url:
        print(f"🎬 [Orchestrator]: Triggering Video Processing Engine for URL: {route_result.extracted_entities.video_url}")
        video_payload = fetch_video_data(route_result.extracted_entities.video_url)
    
    return OrchestratorOutput(
        intent=route_result.intent,
        confidence_score=route_result.confidence_score,
        video_payload=video_payload,
        raw_query=user_query
    )