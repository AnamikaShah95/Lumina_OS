import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.router import route_user_intent

def run_router_diagnostics():
    print("🚀 Starting Day 2 Diagnostics: Intent Router & Strict JSON Parser...\n")
    
    # Test Case 1: Video Summarization Intent
    query_1 = "Can you summarize this YouTube video for me? https://youtube.com/watch?v=12345"
    print(f"📥 Test Case 1 Input: '{query_1}'")
    res_1 = route_user_intent(query_1)
    print(f"📡 Parsed JSON Output:\n{res_1.model_dump_json(indent=2)}\n")
    
    # Test Case 2: PPT Generation Intent
    query_2 = "Create a presentation on Quantum Computing with a professional tone."
    print(f"📥 Test Case 2 Input: '{query_2}'")
    res_2 = route_user_intent(query_2)
    print(f"📡 Parsed JSON Output:\n{res_2.model_dump_json(indent=2)}\n")
    
    print("✅ Day 2 Diagnostics Completed Successfully!")

if __name__ == "__main__":
    run_router_diagnostics()