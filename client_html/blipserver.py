from flask import Flask, request, render_template
import os
import cv2
import base64
import time
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image

app = Flask(__name__)
save_folder = "received_images"
os.makedirs(save_folder, exist_ok=True)

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

i = 0

@app.route('/', methods=['GET', 'POST'])
def upload_image():
    global i
    if request.method == 'POST':
        file = request.files['image']
        if not file:
            return "No file uploaded", 400

        i += 1
        file_path = os.path.join(save_folder, f'received_image{i}.jpg')
        file.save(file_path)

        image = cv2.imread(file_path)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(image_rgb)

        inputs = processor(pil_image, return_tensors="pt")
        start_time = time.time()
        outputs = model.generate(**inputs)
        processing_time = time.time() - start_time
        caption = processor.decode(outputs[0], skip_special_tokens=True)

        _, buffer = cv2.imencode('.jpg', image)
        image_encoded = base64.b64encode(buffer).decode('utf-8')

        return render_template('index.html', image_data=image_encoded, caption=caption, processing_time= processing_time)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
