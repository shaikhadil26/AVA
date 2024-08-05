from flask import Flask, request, jsonify
import os
import cv2
import numpy as np
import base64

app = Flask(__name__)
save_folder = "received_images"
os.makedirs(save_folder, exist_ok=True)

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

        if image is None:
            raise ValueError("Failed to decode image")
        
        i+=1
        file_path = os.path.join(save_folder, f'received_image{i}.jpg')
        cv2.imwrite(file_path, image)

        return jsonify({'message': 'Image received and saved successfully'})
    
    except Exception as e:
        print(f"Error processing image: {e}")
        return jsonify({'error': 'Failed to process image'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
