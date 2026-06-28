import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(CURRENT_DIR)
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

from backend.orchestrator import LuminaOrchestrator

def run_day4_diagnostics():
    print("🚀 Starting Day 4 System Integration Framework Diagnostics...")
    
    try:
        orchestrator = LuminaOrchestrator()
        
        # Testing query configuration
        test_query = "Summarize this framework layout video: https://www.youtube.com/watch?v=kqtD5dpn9C8"
        
        response = orchestrator.route_and_execute(test_query)
        
        print("\n📊 --- DIAGNOSTICS RESULTS ---")
        print(f"Video Title: {response['title']}")
        print(f"Extraction Status: {response['engine_status']}")
        
        if response['engine_status'] == "SUCCESS":
            print("\n✨ --- GENERATED MARKDOWN SUMMARY --- ✨")
            print(response['summary'])
            print("✨ ----------------------------------- ✨")
        else:
            print(f"❌ Error Message: {response['error']}")
            
    except Exception as e:
        print(f"💥 Framework Crash Detected: {str(e)}")
        
    print("\n✅ Day 4 System Diagnostics Executed!")

if __name__ == "__main__":
    run_day4_diagnostics()