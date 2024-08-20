from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import speech_recognition as sr
import threading
from diffusers import StableDiffusionPipeline
import torch
from django.conf import settings
from googleapiclient.discovery import build
import pyttsx3
import os
from django.contrib import messages as flash

# Create your views here.

my_api_key = "AIzaSyDApriqN0cJUSHf05rWzdPhgPXO0bvl7NQ"
my_cse_id = "f7db93df0a43d4b66"

model = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
device = 'cuda' if torch.cuda.is_available() else 'cpu'
model.to(device)

engine = pyttsx3.init()

class SpeechEngine:
    def __init__(self, engine):
        self.engine = engine

    def speak(self, text):
        def speak_text():
            if not self.engine._inLoop:
                self.engine.say(text)
                self.engine.runAndWait()
            else:
            	self.engine.endLoop()
            	self.engine.say(text)
            	self.engine.runAndWait()

        threading.Thread(target=speak_text).start()



class talkAndDo:
    def recognize_speech_mic(self):
        recognizer = sr.Recognizer()
        mic = sr.Microphone()

        with mic as source:
            print('Now talk...?')
            audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio)
            print('You said: ' + text)
            return text
        except sr.UnknownValueError:
            print("Could not understand the audio")
            return None
        except sr.RequestError:
            print("Could not request results; check your network connection")
            return None

    def image_generator(self):
        prompt = self.recognize_speech_mic()
        if prompt:
            print(f'Generating you an image of {prompt}...')
            with torch.no_grad():
               
                image = model(prompt, torch_dtype=torch.float32).images[0]
            
            directory = os.path.join('media', 'generated_images')
            if not os.path.exists(directory):
                os.makedirs(directory)
            
            image_path = os.path.join(directory, 'result.png')
            image.save(image_path)
            return image_path

    def google_search(self, search_term, api_key, cse_id, **kwargs):
        service = build("customsearch", "v1", developerKey=api_key)
        res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
        return res['items']


def home(request):


	return render(request, 'home.html')

@login_required
def miniG(request):


	return render(request, 'minigoogle.html')

@login_required
def imageG(request):


	return render(request, 'image.html')



def minigoogle(request):
	
	reply = []
	query = talkAndDo().recognize_speech_mic()
	results = talkAndDo().google_search(query, my_api_key, my_cse_id, num=10)
	print(results[0]['snippet'])
	reply.append(results[0]['snippet'])
	
	try:
		speech_engine = SpeechEngine(engine)
		speech_engine.speak('According to Google, ' + results[0]['snippet'])
	except Exception as e:
		print(e)
		



	return JsonResponse(reply, safe=False)



def image_generator(request):
    talk_and_do = talkAndDo()
    image_path = talk_and_do.image_generator()
    if image_path:
        
        image_url = request.build_absolute_uri(settings.MEDIA_URL + 'generated_images/result.png')
        return JsonResponse({'image_url': image_url})
    else:
        return JsonResponse({'error': 'Image generation failed'}, status=500)
