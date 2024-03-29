import time
import datetime
import sounddevice as sd
import pyttsx3
import threading
import numpy as np
SAMPLE_RATE = 44100
DURATION = 1 
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def generate_beep(duration=1000, frequency=1000):
    t = np.linspace(0, duration / 1000, int(SAMPLE_RATE * duration / 1000), False)
    beep_signal = np.sin(2 * np.pi * frequency * t)
    sd.play(beep_signal, samplerate=SAMPLE_RATE)
    sd.wait()

def generate_time_signal():
    spoken_midnight = False 
    spoken_at_the_tone = False

    while True:
        current_time = datetime.datetime.now()
        current_hour = current_time.hour
        current_minute = current_time.minute
        current_second = current_time.second

        
        generate_beep(frequency=200, duration=50)

        if current_second == 45 and not spoken_at_the_tone:
            next_minute = (current_minute + 1) % 60
            next_hour = current_hour + (1 if next_minute == 0 else 0)

            speak(f"At the tone, {next_hour} hours, {next_minute} minutes, universal time")
            spoken_at_the_tone = True

        if current_second == 0:
            if current_minute == 0 and current_hour == 0 and not spoken_midnight:
                speak("National time management, this is radio station CALLSIGN")
                spoken_midnight = True
            else:
                generate_beep() 

                spoken_at_the_tone = False

        time.sleep(1)

if __name__ == "__main__":
    signal_thread = threading.Thread(target=generate_time_signal)
    signal_thread.daemon = True
    signal_thread.start()

    while True:
        user_input = input("Press 'q' to quit: ")
        if user_input.lower() == 'q':
            break

