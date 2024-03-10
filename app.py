from flask import Flask, render_template, request, jsonify

from azure_speech_to_text import SpeechToTextManager
import threading  # Add this line to import the threading module
import subprocess  # Add this line to import subprocess module
import os



app = Flask(__name__)

speechtotext_manager = SpeechToTextManager()

def takecommand():
    return speechtotext_manager.speechtotext_from_mic_continuous()

listening_thread = None  # Define listening_thread globally

@app.route('/')
def index():
    return render_template('index.html')



character = ""
@app.route('/set_character', methods=['POST'])
def set_character():
    global character
    character = request.json['character']
    # Optionally, you can store the character name in a global variable or session for later use
    return jsonify({'status': 'success'})



def takecommand_and_process():
    global mic_result
    mic_result = takecommand()
    # Assuming you have a way to determine the character's name, let's say it's stored in a variable called 'character'
    character_ = character  # Implement this function to determine the character's name
    # Call chatgpt_character.py passing the character's name and mic_result


    subprocess.run(['python', 'chatgpt_char.py', character_, mic_result])


@app.route('/start_listening', methods=['POST'])
def start_listening():
    global listening_thread
    listening_thread = threading.Thread(target=takecommand_and_process)
    listening_thread.start()
    return jsonify({'status': 'success'})


@app.route('/stop_listening', methods=['POST'])
def stop_listening():
    speechtotext_manager.stop_listening()  # Signal the SpeechToTextManager to stop listening
    global listening_thread
    if listening_thread:
        listening_thread.join()  # Wait for the thread to complete
    return jsonify({'status': 'success'})


@app.route('/generate', methods=['GET', 'POST'])
def show_images():
    image_folder = os.path.join('static', '')
    images = [os.path.join(image_folder, file) for file in os.listdir(image_folder) if file.endswith((".png"))]
    return render_template('gallery.html', images=images)

if __name__ == '__main__':
    app.run(debug=True)

