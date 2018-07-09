import json
from watson_developer_cloud import ToneAnalyzerV3
from sensitive import give_watson_credentials


def authenticate():
    version, username, password = give_watson_credentials()

    tone_analyzer = ToneAnalyzerV3(
        version=version,
        username=username,
        password=password
    )

    return tone_analyzer


tone_analyzer = authenticate()

text = input('Enter text for Tone Analysis : ')
content_type = 'application/json'

tone = tone_analyzer.tone({"text": text}, content_type)

print(json.dumps(tone, indent=2))
