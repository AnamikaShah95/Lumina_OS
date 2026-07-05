from pydantic import BaseModel, Field
from typing import List

class SlideContent(BaseModel):
    slide_number: int = Field(
        ..., 
        description="The strictly sequential numerical index identifier tracking the position layout framework of the current slide, starting from 1."
    )
    title: str = Field(
        ..., 
        description="A highly concise, professional title header mapping the main structural theme context of this specific slide block."
    )
    bullet_points: List[str] = Field(
        ..., 
        description="A bounded collection array containing exactly 3 to 5 highly structured, clear engineering talking points explaining the target subject matter."
    )

class PresentationPayload(BaseModel):
    topic: str = Field(
        ..., 
        description="The master overriding presentation deck metadata title extracted or synthesized cleanly from the video title stream logic."
    )
    total_slides: int = Field(
        ..., 
        description="The absolute total count integer tracking the exact number of core content slide array blocks rendered inside this payload configuration grid."
    )
    slides: List[SlideContent] = Field(
        ..., 
        description="The primary sequential structural array node block containing the individual structured data layout entries for each slide context frame."
    )