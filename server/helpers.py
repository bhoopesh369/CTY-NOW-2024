import speech_recognition as sr
from os import path
from pydub import AudioSegment




def convertAudioToText(audio_file: str, lang: str = None):       
# transcribe audio file                                                         
# AUDIO_FILE = "/home/mani1911/Documents/Pragyan-Hack/CTY-NOW-2024/uploads/sriman.wav"
# use the audio file as the audio source                                        
    r = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
            audio = r.record(source)  # read the entire audio file    
            #     try:
      # using google speech recognition
            if lang is None or lang == "english":
                text = r.recognize_google(audio)
            elif lang == "hindi":
                text = r.recognize_google(audio, language='hi-IN')
            elif lang == "tamil":
                text = r.recognize_google(audio, language='ta-IN')              
            return r.recognize_google(audio)
    return None

# print(convertAudioToText("/home/mani1911/Documents/Pragyan-Hack/CTY-NOW-2024/uploads/sriman.wav"))