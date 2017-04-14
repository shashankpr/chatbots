import audiotranscode
import requests

at = audiotranscode.AudioTranscode()

def get_audio_file(audio_url):
    r = requests.get(audio_url)
    with open('audio.mp3', 'wb') as f:
        f.write(r.content)

def aac_to_mp3(audio_file = 'audio.wav', output_file = 'audio.mp3'):
    conversion = at.transcode(audio_file, output_file)

    return conversion


url = 'https://cdn.fbsbx.com/v/t59.3654-21/17695304_10211588381840935_4291541419631312896_n.aac/audioclip-1491740374478-3932.aac?oh=ba0c59a8c4f0b45bdb7c0a1ba43fdddd&oe=58EC35CC'
aac_to_mp3()