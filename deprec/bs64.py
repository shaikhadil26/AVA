import base64
output_file = "image_base64.txt"

with open("dataset-cover.jpg", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

with open(output_file, "w") as file:
    file.write(encoded_string)