import os
from google import genai
from google.genai import types

def verify_key():
    api_key = "AIzaSyCTWJnEwGsG-tWvM1-xzV3s8YMXtjlvY_A"
    print(f"Verifying API Key: {api_key[:8]}...{api_key[-4:]}")
    
    try:
        client = genai.Client(api_key=api_key)
        # Try a simple list models call
        models = list(client.models.list())
        print(f"Success! Found {len(models)} models.")
        
        gemini_3_models = [m for m in models if "gemini-3" in m.name.lower()]
        
        if gemini_3_models:
            print(f"\nFound Gemini 3 models:")
            for model in gemini_3_models:
                print(f" - {model.name}")
        else:
            print("\nNo Gemini 3 models found in your available models list.")
            print("Latest Gemini models available:")
            flash_models = [m for m in models if "flash" in m.name.lower()]
            for model in sorted(flash_models, reverse=True)[:5]:
                print(f" - {model.name}")
        return True
    except Exception as e:
        print(f"\nVerification failed!")
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    verify_key()
