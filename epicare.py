import os
import base64
import requests
from dotenv import load_dotenv

load_dotenv()

# OpenAI API Key
api_key = os.getenv('API_KEY')

# Function to encode the image
def encode_image(file_path):
    with open(file_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Function to upload the image and get base64 string
def upload_image_and_get_base64(file_path):
    base64_image = encode_image(file_path)
    return base64_image

# Path to your image
# image_path = "path_to_your_image.jpg"

    

if __name__ == "__main__":
    import os
    from flask import Flask, request, render_template, redirect

    app = Flask(__name__)
        

    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/submit', methods=['POST'])
    def submit():
        file = request.files["user_input"]
        if file.filename != "":
                file_path = os.path.join("uploads", file.filename)
                file.save(file_path)
        response = send_request_to_openai(file_path)
        os.remove(file_path)  # Remove the uploaded file after use
        choices = response["choices"]
        mssg = choices[0]
        message_value = mssg["message"]
        output = message_value["content"]
        return redirect(f'/result?output={output}')
    def send_request_to_openai(file_path):
        base64_image = upload_image_and_get_base64(file_path)

        headers = {
          "Content-Type": "application/json",
          "Authorization": f"Bearer {api_key}"
        }

        payload = {
          "model": "gpt-4-turbo",
          "messages": [
            {
              "role": "user",
              "content": [
                {
                  "type": "text",
                  "text": "What’s in this image?, explain in 2 words"
                },
                {
                  "type": "image_url",
                  "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                  }
                }
              ]
            }
          ],
          "max_tokens": 150
        }

        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        end = response.json()
        return end
    @app.route('/result')
    def result():
        otput = request.args.get('output')
        return render_template('result.html', output=otput)
    if __name__ == "__main__":
        app.run(debug=True, port="8080")