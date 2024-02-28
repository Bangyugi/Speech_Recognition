import requests
from api_secrets import API_KEY_ASSEMBLYAI
import sys
import time
from api_communication import *

filename = "D:\My storage\Desktop\Speech_Recognition\output.wav"


audio_url = upload(filename)
save_transcript(audio_url, filename)
