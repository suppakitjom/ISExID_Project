import azure.cognitiveservices.speech as speechsdk
import simpleaudio as sa

speech_config = speechsdk.SpeechConfig(
    subscription='44d7d58744334bea8b7c72de640ed3e3', region='southeastasia')
audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)


def speakText(text):
    speech_config.speech_synthesis_voice_name = "fr-FR-JeromeNeura"
    speech_synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=audio_config)
    sa.WaveObject.from_wave_file("./tts/ring.wav").play().wait_done()
    speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()


def speakTextSSML(text):  #change voice and style in tts_voice_config.xml
    '''
    Speak text using configurations in the tts_voice_config.xml file
    can be used to change the voice and style of the speaker
    '''
    # names:
    # "en-GB-RyanNeural" : default, cheerful, chat
    # "en-US-DavisNeural" : default, chat, angry, cheerful, excited, friendly, hopeful, sad, shouting, terrified, unfriendly, whispering
    # "en-US-GuyNeural" : default, newscast, angry, cheerful, sad, excited, friendly, terrified, shouting, unfriendly, whispering, hopeful
    # "en-US-JasonNeural" : default, angry, cheerful, excited, friendly, hopeful, sad, shouting, terrified, unfriendly, whispering
    # "en-US-TonyNeural" : default, angry, cheerful, excited, friendly, hopeful, sad, shouting, terrified, unfriendly, whispering
    # "en-US-AriaNeural" : default, chat, customerservice, narration-professional, newscast-casual, newscast-formal, cheerful, empathetic, angry, sad, excited, friendly, terrified, shouting, unfriendly, whispering, hopeful
    # "en-US-JennyNeural" : default, assistant, chat, customerservice, newscast, angry, cheerful, sad, excited, friendly, terrified, shouting, unfriendly, whispering, hopeful

    style = 'angry'
    voice = 'en-US-DavisNeural'
    if not text:
        return
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config,
                                              audio_config=audio_config)
    ssml_string = open("./tts/tts_voice_config.xml", "r").read()
    ssml_string = ssml_string.replace('TEXT', text)
    ssml_string = ssml_string.replace('STYLE', repr(style))
    ssml_string = ssml_string.replace('VOICE', repr(voice))
    # sa.WaveObject.from_wave_file("./tts/ring.wav").play().wait_done()
    # sa.WaveObject.from_wave_file("./tts/ring.wav").play()
    result = synthesizer.speak_ssml_async(ssml_string).get()


if __name__ == "__main__":
    speakTextSSML()
    pass