from typing import List, Optional
from pydantic import BaseModel, Field

# 1. Individual Slide ka Content Blueprint
class SlideContent(BaseModel):
    slide_number: int = Field(description="The sequential number of the slide starting from 1")
    title: str = Field(description="A short, catchy and clear heading for the slide")
    bullet_points: List[str] = Field(description="3 to 5 clear, high-impact technical bullet points for the slide body")
    visual_suggestion: Optional[str] = Field(default=None, description="A layout or visual idea for this specific slide")

# 2. Complete Presentation Object Blueprint
class PresentationPayload(BaseModel):
    topic: str = Field(description="The main topic or title of the video/presentation")
    total_slides: int = Field(description="Total number of slides generated")
    slides: List[SlideContent] = Field(description="List of all structured slides")