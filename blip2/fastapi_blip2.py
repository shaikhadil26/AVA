from fastapi import FastAPI, File, Form, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os
import cv2
import base64
import time
from transformers import Blip2Processor, Blip2ForConditionalGeneration
from PIL import Image
import torch
from starlette.staticfiles import StaticFiles
from typing import Optional

app = FastAPI()

# Setting up template directory
templates = Jinja2Templates(directory="blip2/templates")

# Folder for saving received images
save_folder = "received_images"
os.makedirs(save_folder, exist_ok=True)

# Setting up device for model
device = torch.device("mps")

# Loading model and processor
processor = Blip2Processor.from_pretrained("Salesforce/blip2-opt-2.7b")
model = Blip2ForConditionalGeneration.from_pretrained(
    "Salesforce/blip2-opt-2.7b", device_map='mps', torch_dtype=torch.float16
)
model.to(device)

i = 0

@app.post("/", response_class=HTMLResponse)
async def upload_image(
    request: Request, 
    file: UploadFile = File(...), 
    prompt: Optional[str] = Form("")
):
    global i
    i += 1

    # Save uploaded image
    file_path = os.path.join(save_folder, f'received_image{i}.jpg')
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # Load and process the image using OpenCV and PIL
    image = cv2.imread(file_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(image_rgb)

    # Handle the prompt (if any)
    if prompt:
        prompt_text = f"Question: {prompt} Answer:"
    else:
        prompt_text = " "

    # Prepare inputs for the BLIP2 model
    inputs = processor(images=pil_image, text=prompt_text, return_tensors="pt").to(device, torch.float16)

    # Generate caption from the model
    start_time = time.time()
    outputs = model.generate(**inputs)
    processing_time = time.time() - start_time
    caption = processor.batch_decode(outputs, skip_special_tokens=True)[0].strip()

    # Encode the image to base64
    _, buffer = cv2.imencode('.jpg', image)
    image_encoded = base64.b64encode(buffer).decode('utf-8')

    # Render the HTML page with the image and caption
    return templates.TemplateResponse("index.html", {
        "request": request,
        "image_data": image_encoded,
        "caption": caption,
        "processing_time": processing_time
    })

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    # Render the HTML page for uploading images
    return templates.TemplateResponse("index.html", {"request": request})


# Mount static files if necessary
# app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
