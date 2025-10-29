from flask import Flask, request, jsonify
from flask_cors import CORS
import speech_recognition as sr
import pyttsx3
import threading
import queue
from TranslationBNR32 import translation as tr

app = Flask(__name__)
CORS(app)
recording = False
audio_queue = queue.Queue()
current_language_pair = None
target = None
recognizer = sr.Recognizer()
translator = tr.TranslationBNR32(None, None)
engine = pyttsx3.init()
voices = engine.getProperty('voices')
voicemap = {
    "en": voices[0].id,
    "hi": voices[1].id,
    "de": voices[2].id,
    "fr": voices[5].id,
}

def recognize_speech(language):
    """
    Obtain the speech from the microphone and convert it to text.

    Parameters
    ----------
    language : str
        the language of the speech provided in the microphone input
        ['en', 'de', 'fr', 'hi']

    Returns
    -------
    text: str
        the recognized speech from the microphone input
    None
        When no recognition was performed or no proper sentences could be formed

    """
    with sr.Microphone() as source:
        print(f"Listening for {language}...")
        audio = recognizer.listen(source, timeout=(float("inf")))
        try:
            text = recognizer.recognize_google(audio, language=language)
            print(f"Recognized: {text}")
            return text
        except Exception as e:
            print(f"error while recording {e}")
            return None


def translate_text(text, source_lang, target_lang):
    """
    Translate the text from source language to target language

    Parameters
    ----------
    source_lang : str
        formated string of the source language
        ['en', 'de', 'fr', 'hi']
    target_lang : str
        formatted string of the target language
        ['en', 'de', 'fr', 'hi'] and != lang1

    Returns
    -------
    translated_text: str
        the translated text from source language to target language
    """
    try:
        translator.lang1 = source_lang
        translator.lang2 = target_lang
        translation = translator.translate(text)
        print(f"Translated: {translation}")
        return translation
    except Exception as e:
        print(f"Translation error: {e}")
        return None


def text_to_speech(text, language):
    """
    Convertt the text to speech output and plays the audio generated

    Parameters
    ----------
    text : str
        The text to be played as audio
    language : str
        formatted string of the language the text belongs to
        ['en', 'de', 'fr', 'hi'] and != lang1

    """
    engine = pyttsx3.init()
    if engine._inLoop:
        engine.endLoop()
    engine.setProperty("rate", 220)
    engine.setProperty("volume", 2)
    engine.setProperty("voice", voicemap[language])
    engine.say(text)
    engine.runAndWait()

def process_audio_stream():
    """
    Initializes all the required settings and starts the text to speech
    once the translation is done

    """
    global recording, current_language_pair, target
    while recording:
        try:
            source_lang = current_language_pair[target[0]]
            target_lang = current_language_pair[target[1]]
            recognized_text = recognize_speech(source_lang)
            if recognized_text:
                translated_text = translate_text(
                    recognized_text,
                    source_lang,
                    target_lang
                )
                if translated_text:
                    text_to_speech(translated_text, target_lang)
        except Exception as e:
            print(f"Error in audio processing: {str(e)}")


@app.route('/api/start-recording', methods=['POST'])
def start_recording():
    """
        Gets called when the front end sends a request to start recording
        when the user presses the language button

    """
    global recording, current_language_pair, target
    try:
        data = request.json
        current_language_pair = data.get('languagePair')
        speaker = current_language_pair[data.get('speaker')]
        if speaker == current_language_pair["target"]:
            target = ["target", "source"]
        else:
            target = ["source", "target"]

        if not recording:
            recording = True
            threading.Thread(target=process_audio_stream, daemon=True).start()

        return jsonify({
            'status': 'success',
            'message': f'Started recording for {speaker} in {current_language_pair["source"]} to {current_language_pair["target"]}'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/stop-recording', methods=['POST'])
def stop_recording():
    """
    Gets called when the front end sends a request to stop recording
    when the user presses the stop recording button

    """
    global recording
    try:
        recording = False
        return jsonify({
            'status': 'success',
            'message': 'Recording stopped'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

app.run(debug=True, port=5000)