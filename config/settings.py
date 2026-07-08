import os
import re
import sys
from dotenv import load_dotenv

# Locating local environment boundary states safely
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

class LuminaSecuritySandbox:
    """
    Day 29 Core Addition: Secure Stream Interceptor & Token Masking Sandbox.
    Intercepts standard output buffers dynamically via regex patterns to enforce
    runtime logging compliance and protect sensitive credential signatures.
    """
    def __init__(self, target_stream):
        self.orig_stream = target_stream
        # Pattern matching standard credential hashes (Hex arrays, alpha-numeric keys, or system boundaries tokens)
        self.sensitive_regex = re.compile(r'(AIzaSy[A-Za-z0-9_\-]{31})|([a-zA-Z0-9]{32,})')

    def write(self, data_buffer):
        if not data_buffer:
            self.orig_stream.write(data_buffer)
            return

        # Scanning the stream buffer for potential leak footprints
        masked_data = data_buffer
        matches = self.sensitive_regex.findall(data_buffer)
        
        if matches:
            for match in matches:
                full_token = match[0] if match[0] else match[1]
                if GEMINI_API_KEY and full_token in GEMINI_API_KEY and len(full_token) > 8:
                    # Leaving only the first 6 signature bytes exposed for developer telemetry audits
                    safe_mask = f"{full_token[:6]}...[SECURE_MASK_LOCKED]...*"
                    masked_data = masked_data.replace(full_token, safe_mask)

        self.orig_stream.write(masked_data)

    def flush(self):
        self.orig_stream.flush()

    def isatty(self):
        """
        Day 29 Structural Fix: Pass-through for terminal interactive checks.
        Prevents Uvicorn color formatter configuration crashes.
        """
        return hasattr(self.orig_stream, "isatty") and self.orig_stream.isatty()

    def __getattr__(self, name):
        """
        Fallback attribute router to ensure all other native sys.stdout properties
        (like encoding, errors, etc.) dissolve seamlessly into the original stream.
        """
        return getattr(self.orig_stream, name)

# Injecting the dynamic log masking sandbox directly over the active system stdout stream frames
sys.stdout = LuminaSecuritySandbox(sys.stdout)

def verify_sandbox_clearance():
    print("🔒 [Security Sandbox]: Dynamic log masking interceptor initialization stream hooked successfully.")
    if GEMINI_API_KEY:
        # Slicing safely to show only first few characters before layout verification test prints
        print(f"📡 [Security Sandbox]: Validating masking proxy logic raw variable telemetry check -> {GEMINI_API_KEY}")
    else:
        print("⚠️ [Security Sandbox Warning]: Core token empty. Skipping environment masking evaluation tests.")

# Auto executing structural safeguard validation check upon import configuration loads
verify_sandbox_clearance()