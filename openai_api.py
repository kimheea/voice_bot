from encodings.base64_codec import base64_encode

from dotenv import load_dotenv
from openai import OpenAI
import os
import base64

load_dotenv()

client = OpenAI() # api_key = OPEN_API_KEY

def stt(audio):
    filename = 'temp.mp3' # 임시파일
    audio.export(filename, format='mp3')


    with open(filename, 'rb') as f:
        transcription = client.audio.transcriptions.create(
            model='whisper-1',
            file=f
        )
    # 임시파일삭제
    os.remove(filename)
    return transcription.text


def ask_gpt(messages, model):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=1, # 사용자에게 선택하라고 할 수 있음
        max_tokens=4096,
        top_p=1
    )
    return response.choices[0].message.content

def tts(text):
    filename = 'output.mp3'
    with client.audio.speech.with_streaming_response.create(
        model = 'tts-1',
        voice = 'alloy',
        input = text
    ) as response:
        response.stream_to_file(filename)

    # 음원 문자열 BASE64로 인코딩

    with open(filename, 'rb') as f:
        data = f.read()
        base64_encoded = base64.b64encode(data).decode()
        audio_tag = f"""
        <audio autoplay="true">
            <source src = "data:audio/mp3;base64, {base64_encoded}" type="audio/mp3" />
        </audio>

        """
    # 임시파일 삭제
    os.remove(filename)

    return audio_tag
