from PIL import Image
from transformers import Blip2Processor, Blip2ForConditionalGeneration
import torch

device = torch.device("mps")

processor = Blip2Processor.from_pretrained("Salesforce/blip2-opt-2.7b")
model = Blip2ForConditionalGeneration.from_pretrained(
    "Salesforce/blip2-opt-2.7b", device_map='mps', torch_dtype=torch.float16
) 
model.to(device)
# url = "http://images.cocodataset.org/val2017/000000039769.jpg"
# image = Image.open(requests.get(url, stream=True).raw)
image = Image.open('salad.png')

inputs = processor(images=image, return_tensors="pt").to(device, torch.float16)

# generated_ids = model.generate(**inputs)
# generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0].strip()
# print(generated_text)

prompt = "Question: What vegetable is in the image? Answer:"
inputs = processor(images=image, text=prompt, return_tensors="pt").to(device, dtype=torch.float16)

generated_ids = model.generate(**inputs)
generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0].strip()
print(generated_text)
# engine = pyttsx3.init()
# engine.say(generated_text)
# engine.runAndWait()