import os
import sys
import json

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(CURRENT_DIR)
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

from backend.orchestrator import LuminaOrchestrator

def run_day5_diagnostics():
    print("🚀 Starting Day 5 Presentation Layout Framework Diagnostics...")
    
    try:
        orchestrator = LuminaOrchestrator()
        test_query = "Summarize this framework layout video: https://www.youtube.com/watch?v=kqtD5dpn9C8"
        
        response = orchestrator.route_and_execute(test_query)
        
        print("\n📊 --- DIAGNOSTICS RESULTS ---")
        print(f"Video Title: {response['title']}")
        print(f"Engine Process Status: {response['engine_status']}")
        
        # Checking if presentation layout payload generated successfully
        if response['presentation_data']:
            print("\n✨ --- GENERATED STRUCTURED SLIDES PAYLOAD (JSON) --- ✨")
            print(json.dumps(response['presentation_data'], indent=4))
            print("✨ -------------------------------------------------- ✨")
        else:
            print(f"⚠️ Presentation JSON Generation skipped or failed. Error Context: {response['error']}")
            
    except Exception as e:
        print(f"💥 Framework Crash Detected: {str(e)}")
        
    print("\n✅ Day 5 System Diagnostics Executed!")

if __name__ == "__main__":
    run_day5_diagnostics()