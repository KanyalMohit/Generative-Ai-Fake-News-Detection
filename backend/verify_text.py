import requests
import json
import time

URL = "http://127.0.0.1:8001/analyze/text"

payload = {
    "content": "The moon is made of green cheese and NASA is hiding it.",
    "is_url": False
}

print(f"Sending request to {URL}...")
try:
    start_time = time.time()
    response = requests.post(URL, json=payload, timeout=120)
    end_time = time.time()
    
    print(f"Status Code: {response.status_code}")
    print(f"Time Taken: {end_time - start_time:.2f}s")
    
    if response.status_code == 200:
        data = response.json()
        print("\n--- Response Keys ---")
        print(data.keys())
        
        print("\n--- Label ---")
        print(data.get("label"))
        
        print("\n--- Summary ---")
        print(data.get("summary"))
        
        print("\n--- Verify JSON Structure ---")
        if "credibility_analysis" in data and "key_facts" in data:
            print("SUCCESS: JSON structure refined by Gemini.")
        else:
            print("FAILURE: Missing Gemini fields.")
    else:
        print("Error:", response.text)

except Exception as e:
    print(f"Request failed: {e}")
