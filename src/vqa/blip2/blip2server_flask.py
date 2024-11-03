from flask import Flask, request, render_template
import os
import cv2
import base64
import time
from transformers import Blip2Processor, Blip2ForConditionalGeneration
from PIL import Image
import torch

app = Flask(__name__)
save_folder = "received_images"
os.makedirs(save_folder, exist_ok=True)

device = torch.device("mps")

processor = Blip2Processor.from_pretrained("Salesforce/blip2-opt-2.7b")
model = Blip2ForConditionalGeneration.from_pretrained(
    "Salesforce/blip2-opt-2.7b", device_map='mps', torch_dtype=torch.float16
) 
model.to(device)

i = 0

@app.route('/', methods=['GET', 'POST'])
def upload_image():
    global i
    if request.method == 'POST':
        file = request.files['image']
        prompt = request.form.get('prompt', '')

        if not file:
            return "No file uploaded", 400

        i += 1
        file_path = os.path.join(save_folder, f'received_image{i}.jpg')
        file.save(file_path)

        image = cv2.imread(file_path)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(image_rgb)

        if prompt:
            prompt_text = f"Question: {prompt} Answer:"
        else:
            prompt_text = " "

        inputs = processor(images=pil_image, text=prompt_text, return_tensors="pt").to(device, torch.float16)

        start_time = time.time()
        outputs = model.generate(**inputs)
        processing_time = time.time() - start_time
        caption = processor.batch_decode(outputs, skip_special_tokens=True)[0].strip()

        _, buffer = cv2.imencode('.jpg', image)
        image_encoded = base64.b64encode(buffer).decode('utf-8')

        return render_template('index.html', image_data=image_encoded, caption=caption, processing_time=processing_time)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
