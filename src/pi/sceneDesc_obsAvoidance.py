import socket
import cv2
import sys
import time
import pyttsx3
import requests

engine = pyttsx3.init()
engine.setProperty('rate', 200)
engine.setProperty('volume', 0.5)

resolution = (320, 240)
frame_rate = 12

NGROK_URL = "https://83b2-34-73-16-30.ngrok-free.app"

def send_image(file_path):
	with open(file_path, 'rb') as img:
		response = requests.post(NGROK_URL, files={'file': img})
	return response

def main(server_ip, port):
	i = 0
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((server_ip, port))
	print(f"[+] Connected to server {server_ip}:{port}")

	cap = cv2.VideoCapture(0)
	cap.set(cv2.CAP_PROP_FRAME_WIDTH, resolution[0])
	cap.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution[1])
	cap.set(cv2.CAP_PROP_FPS, frame_rate)

	while cap.isOpened():
		ret, frame = cap.read()
		if not ret:
			print("[-] Failed to capture frame.")
			break

		ret, buffer = cv2.imencode('.jpeg', frame)
		if not ret:
			print("[-] Failed to encode frame.")
			continue

		if i%20 == 0:
			file_path = "/tmp/frame.jpeg"
			with open(file_path, 'wb') as f:
				f.write(buffer)

			response = send_image(file_path)
			print(f"[+] Response from server: {response.text}") # Use tts model 

		try:
			sock.sendall(buffer.tobytes())
			response = sock.recv(1024)
			print(response.decode('utf-8'))
			i += 1
			if i % 10 == 0:
				engine.say(response.decode('utf-8'))
				engine.runAndWait()

			time.sleep(0.05)
		   
		except socket.error as se:
			print(f"[-] Socket error: {se}")
			break
	   
	cap.release()
	sock.close()
	print("[+] Connection closed.")

if __name__ == "__main__":
	if len(sys.argv) != 3:
		print("Usage: python client.py <server_ip> <port>")
		sys.exit(1)
	main(sys.argv[1], int(sys.argv[2]))
