import requests
import json
import speech_recognition as sr
from gtts import gTTS
import os
r = sr.Recognizer()

def generate_gemini_content(api_key, prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"

    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    response = requests.post(url, headers=headers, data=json.dumps(data), verify=False) 
    if response.status_code == 200:
        return response.text  
    else:
        return f"Error: {response.status_code}, {response.text}"



api_key = "API_KEY"  
# print(" click 1 for text or 2 for speaking")
print("Enter 1 for text input or 2 for speaking or enter q to exit")
option = (input())
while option!='q' or option!= 'Q':
    if option == '1':
            prompt = input("Enter your query:")
    else:
            with sr.Microphone() as source:
                print("Talk")
                audio_text = r.listen(source)
                print("Recording Done!")

                try:
                    print("Text: "+r.recognize_google(audio_text))
                    prompt = r.recognize_google(audio_text)
                except:
                    print("Sorry, I did not get that")
    gemini_response = generate_gemini_content(api_key, prompt)
    try:
        parsed_response = json.loads(gemini_response)
        print("Gemini : ")
        overall = " "
        if 'candidates' in parsed_response and parsed_response['candidates']:
            for candidate in parsed_response['candidates']:
                for part in candidate.get('content', {}).get('parts', []):
                    if 'text' in part:
                        print(part['text'])
                        overall += part['text'].replace('*',"") +" "
            language = 'en'
            myobj = gTTS(text=overall, lang=language, slow=False)
            myobj.save("welcome.mp3")
            os.system("start welcome.mp3")                    
        else:
            print("Unexpected JSON structure.  Raw response:")
            print(gemini_response)  
    except json.JSONDecodeError:
        print("Invalid JSON response:")
        print(gemini_response) 
    print("Enter 1 for text input or 2 for speaking or enter q to exit")
    option = int(input())
