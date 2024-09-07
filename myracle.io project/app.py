from flask import Flask, request, jsonify
import os
import requests  # For making HTTP requests to Olama API
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configure folder to store uploaded files
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Olama API details (replace these with actual Olama API details)
OLAMA_API_URL = 'https://cloud.llamaindex.ai/api-key'  # Replace with actual endpoint
OLAMA_API_KEY = 'insert your api key'  # Replace with your actual Olama API key

def call_olama_api(images, context):
    # Prepare files for the request
    files = [('images', (image, open(image, 'rb'), 'image/jpeg')) for image in images]
    
    # Prepare headers and payload
    headers = {
        'Authorization': f'Bearer {OLAMA_API_KEY}',
    }

    data = {
        'context': context if context else "No context provided"
    }

    # Make the API request to Olama
    response = requests.post(OLAMA_API_URL, headers=headers, data=data, files=files)

    # Check if the request was successful
    if response.status_code == 200:
        return response.json().get('instructions', 'No instructions generated.')
    else:
        return f"Error: {response.status_code} - {response.text}"

@app.route('/generate-instructions', methods=['POST'])
def generate_instructions():
    # Get optional context
    context = request.form.get('context')
    
    # Save uploaded screenshots
    screenshots = request.files.getlist('screenshots')
    saved_screenshots = []
    
    for screenshot in screenshots:
        filename = secure_filename(screenshot.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        screenshot.save(filepath)
        saved_screenshots.append(filepath)
    
    # Call Olama API with screenshots and context
    instructions = call_olama_api(saved_screenshots, context)
    # Return the generated instructions
    return jsonify({'instructions': instructions})

if __name__ == '__main__':
    app.run(debug=True)
