import time
from openai_chat import OpenAiManager
from eleven_labs import ElevenLabsManager
from azure_speech_to_text import SpeechToTextManager
from audioplayer import AudioManager
import sys
import asyncio
import subprocess
from flask import Flask, redirect

 
elevenlabs_manager = ElevenLabsManager()
openai_manager = OpenAiManager()
speechtotext_manager = SpeechToTextManager()
audio_manager = AudioManager()


character = sys.argv[1].strip().lower()
ELEVENLABS_VOICE = "Sarah"
FIRST_SYSTEM_MESSAGE = {"role": "system", "content": '''
Generate a story according to the following strict guidelines:
1) Use maximum of 150 words to generate the story.
2) Give the story a proper ending
3) Keep the story child-friendly and simple to understand.
4) Divide the story into no more than 5 paragraphs.
5) Keep each paragraph short and keep only two events in each paragraph.
6) Keep the transition to each paragraph smooth to understand.
7) Do not ever exceed 150 words limit in total when generating the story
8) This is the user prompt : 
'''}

if character == "peter":
    ELEVENLABS_VOICE = "peter"
    
elif character == "RDJ":
    ELEVENLABS_VOICE = "RDJ"

elif character == "SteveJobs":
    ELEVENLABS_VOICE = "SteveJobs"
    
print("[Starting the loop, press a to begin")
# while True:
    # Wait until user presses "a" key
# if keyboard.read_key() != "a":
#     time.sleep(0.1)
    # continue

print("[green]User pressed a key! Now listening to your microphone:")

# Get question from mic
final_mic_result = FIRST_SYSTEM_MESSAGE["content"] + sys.argv[2]
# Send question to OpenAi
openai_result = openai_manager.generate_story(final_mic_result)

prompt_list = openai_result.split("\n")

async def generate_images(prompt_list):
    for idx, prompt in enumerate(prompt_list):
        if len(prompt) != 0:
            # Construct the command to generate an image using Stability Diffusion AI
            command = [
                "python", "-m", "stability_sdk", "generate",
                "-W", "1024", "-H", "1024",  # Width and height of the image
                prompt 
            ]
            subprocess.run(command)
            print(f"Generated image for prompt {idx + 1}")


async def main():

    # Start generating images asynchronously
    generate_task = asyncio.create_task(generate_images(prompt_list))
    
    # Perform the API call using elevenlabs_manager.text_to_audio()
    elevenlabs_output = elevenlabs_manager.text_to_audio(openai_result, ELEVENLABS_VOICE, False)
    
    # Wait for image generation to complete
    await generate_task

    print("Image generation completed.")
    audio_manager.play_audio(elevenlabs_output, True, True, True)

    # Make a GET request
    # response = requests.get('http://127.0.0.1:5000/generate')

    # # Check if the request was successful
    # if response.status_code == 200:
    #     # Print the JSON content of the response
    #     data = response.json()
    #     print(data)
    # else:
    #     print('An error has occurred.')
    
asyncio.run(main())

    