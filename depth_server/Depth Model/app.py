from flask import Flask, render_template, Response
import cv2
import torch
import numpy as np

app = Flask(__name__)

# Downloading the MiDaS model
midas = torch.hub.load('intel-isl/MiDaS', 'MiDaS_small')
midas.to('cuda')
midas.eval()

transforms = torch.hub.load('intel-isl/MiDaS', 'transforms')
transform = transforms.small_transform

def generate_frames():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Transforming the image
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        imgbatch = transform(img).to('cuda')

        with torch.no_grad():
            prediction = midas(imgbatch)
            
            prediction = torch.nn.functional.interpolate(
                prediction.unsqueeze(1),
                size=img.shape[:2],
                mode='bicubic',
                align_corners=False
            ).squeeze()
            
            output = prediction.cpu().numpy()
            output_normalized = cv2.normalize(output, None, 0, 255, cv2.NORM_MINMAX)
            output_normalized = np.uint8(output_normalized)
            
            # Apply a colormap to the normalized output
            output_colormap = cv2.applyColorMap(output_normalized, cv2.COLORMAP_JET)
            
            # Concatenate original frame and depth map
            combined_frame = np.hstack((frame, output_colormap))

            ret, buffer = cv2.imencode('.jpg', combined_frame)
            combined_frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + combined_frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)
