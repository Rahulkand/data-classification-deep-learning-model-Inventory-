import requests
import json

class LanguageDetector():

    def language_processor_model(self,user_text):
        headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiY2Y4NDJiZjItMWZkMS00OTI0LWEyM2ItOWU3YzE5YzU4MTQ4IiwidHlwZSI6ImFwaV90b2tlbiJ9.hmOF7zU_bEQ-oQBenuyUZfxN1RWtpg9ldr-hhRLSQKY"}

        url ="https://api.edenai.run/v2/translation/language_detection"
        payload={
                "providers": "openai",
                "text": user_text,
                "fallback_providers": ""
        }

        response = requests.post(url, json=payload, headers=headers)

        result = json.loads(response.text)
        return f"lang: {result['openai']['items'][0]['language']}" +"\n"+ f"display name: {result['openai']['items'][0]['display_name']}"
