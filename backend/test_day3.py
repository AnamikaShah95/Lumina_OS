import sys
import os

# Root directory ko path mein add karein taaki absolute imports chal sakein
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(CURRENT_DIR)
if PARENT_DIR not in sys.path:
    sys.path.append(PARENT_DIR)

# Ab import bina kisi error ke chalega!
from backend.orchestrator import process_lumina_request

def run_day3_diagnostics():
    print("🚀 Starting Day 3 Diagnostics: Core Video Pipeline & Payload Handler...\n")
    
    # Standard Python programming guide clip for testing text layer stream mapping
    # Real tutorial snippet with guaranteed clean english transcript matrix
    # Real short working tutorial clip for absolute transcript verification matrix
    test_query = "Summarize this framework layout video: https://www.youtube.com/watch?v=kqtD5dpn9C8"
    
    output = process_lumina_request(test_query)
    
    print("\n📊 --- DIAGNOSTICS RESULTS ---")
    print(f"User Query: {output.raw_query}")
    print(f"Final Scheduled Intent: {output.intent}")
    
    if output.video_payload:
        print(f"Video Extraction Status: {output.video_payload.status.upper()}")
        print(f"Extracted Video Title: {output.video_payload.title}")
        if output.video_payload.transcript:
            print(f"Transcript Snippet: {output.video_payload.transcript[:150]}...")
        else:
            print(f"❌ Error Message: {output.video_payload.error_message}")
            
    print("\n✅ Day 3 Diagnostics Pipeline Executed!")

if __name__ == "__main__":
    run_day3_diagnostics()