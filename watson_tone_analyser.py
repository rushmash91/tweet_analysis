import json
from watson_developer_cloud import ToneAnalyzerV3


def sentiment(text):
    tone_analyzer = ToneAnalyzerV3(
        version ='2017-09-21',
        username ='e89947b2-8f33-4811-aad2-b8cafcf48f8d',
        password ='6KooqVkkA57L'
    )

    content_type = 'application/json'

    tone = tone_analyzer.tone({"text": text},content_type)
    tone = json.dumps(tone)
    return tone


def main():
    print(sentiment(input('Enter the text : ')))


if __name__ == '__main__':
    main()