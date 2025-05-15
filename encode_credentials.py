#!/usr/bin/env python3
"""
Utility script to encode the service account JSON file as a base64 string
for deployment to platforms like Render.

Usage:
    python encode_credentials.py

This will read the service account JSON file from the path specified in the
.env file and print the base64-encoded string to the console.
"""

import os
import base64
from dotenv import load_dotenv

def encode_service_account():
    """Encode the service account JSON file as a base64 string."""
    # Load environment variables
    load_dotenv()
    
    # Get the service account path
    service_account_path = os.getenv("SERVICE_ACCOUNT_PATH")
    if not service_account_path:
        print("ERROR: SERVICE_ACCOUNT_PATH environment variable not found in .env file")
        return
    
    # Check if the file exists
    if not os.path.exists(service_account_path):
        print(f"ERROR: Service account file not found at {service_account_path}")
        return
    
    # Read the file
    try:
        with open(service_account_path, 'rb') as f:
            file_content = f.read()
        
        # Encode as base64
        encoded = base64.b64encode(file_content).decode('utf-8')
        
        print("\n=== SERVICE_ACCOUNT_JSON_BASE64 ===")
        print(encoded)
        print("\n=== END OF ENCODED STRING ===")
        print("\nCopy this string and set it as the SERVICE_ACCOUNT_JSON_BASE64 environment variable in Render.")
        
    except Exception as e:
        print(f"ERROR: Failed to encode service account file: {e}")

if __name__ == "__main__":
    encode_service_account()
