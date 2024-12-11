import speech_recognition as speech_recog

def speech_es():
    mic = speech_recog.Microphone()
    recog = speech_recog.Recognizer()
    
    with mic as audio_file:
        recog.adjust_for_ambient_noise(audio_file)  
        print("Escuchando...")
        audio = recog.listen(audio_file) 
        
    try:
        text = recog.recognize_google(audio, language="es-ES")  
        print("Texto reconocido:", text)
        return text
    except speech_recog.UnknownValueError:
        print("No se pudo entender lo que dijiste.")
        return None
    except speech_recog.RequestError:
        print("Error en la conexión con el servicio de Google.")
        return None
