from flask import Flask, request, jsonify
import os
import cv2
import numpy as np
import base64
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image

app = Flask(__name__)
save_folder = "received_images"
os.makedirs(save_folder, exist_ok=True)

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

i = 0

@app.route('/process', methods=['POST'])
def process_data():
    data = request.json
    global i
    if 'image' not in data:
        return jsonify({'error': 'No image data provided'}), 400

    image_data = data['image']
    try:
        image_data = base64.b64decode(image_data)
        np_arr = np.frombuffer(image_data, np.uint8)
        image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        i += 1
        file_path = os.path.join(save_folder, f'received_image{i}.jpg')
        cv2.imwrite(file_path, image)
        if image is None:
            raise ValueError("Failed to decode image")

        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(image_rgb)
        inputs = processor(pil_image, return_tensors="pt")
        outputs = model.generate(**inputs)
        caption = processor.decode(outputs[0], skip_special_tokens=True)

        return jsonify({'message': 'Image processed successfully', 'caption': caption})

    except Exception as e:
        print(f"Error processing image: {e}")
        return jsonify({'error': 'Failed to process image'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
