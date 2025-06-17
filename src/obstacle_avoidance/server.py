import socket
import numpy as np
import cv2
import argparse
import cv2
import torch
import numpy as np


moving_average_frames = 5 
depth_buffer = []  

midas = torch.hub.load('intel-isl/MiDaS', 'MiDaS_small')
device = torch.device('cpu')
midas.to(device)
midas.eval()

transforms = torch.hub.load('intel-isl/MiDaS', 'transforms')
transform = transforms.small_transform


frames = []

def depth_mp(frame):
	global frames
	global depth_buffer

	img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
	imgbatch = transform(img).to(device)

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

		output_filtered = cv2.medianBlur(output_normalized, 5)
		depth_buffer.append(output_filtered)

		averaged_depth = np.mean(depth_buffer[-moving_average_frames:], axis=0)
		averaged_depth = np.uint8(averaged_depth)

		frames.append(averaged_depth)

		if len(frames) < moving_average_frames:
			return [0,0,0]
		
		height, width = averaged_depth.shape
		part_width = width // 3
		prev_output = frames[-1]
		if prev_output is not None:
			left_depth = averaged_depth[:, :part_width]
			middle_depth = averaged_depth[:, part_width:2 * part_width]
			right_depth = averaged_depth[:, 2 * part_width:]

			depth_coverage_threshold = 150  
			coverage_percentage_threshold = 80  

			left_depth_coverage = np.mean(left_depth > depth_coverage_threshold) * 100
			middle_depth_coverage = np.mean(middle_depth > depth_coverage_threshold) * 100
			right_depth_coverage = np.mean(right_depth > depth_coverage_threshold) * 100

			pane = [0,0,0]  

			if left_depth_coverage > coverage_percentage_threshold:
				pane[0] = 1

			if middle_depth_coverage > coverage_percentage_threshold:
				pane[1] = 1

			if right_depth_coverage > coverage_percentage_threshold:
				pane[2] = 1

			if 1 in pane:
				return pane

			flow = cv2.calcOpticalFlowFarneback(prev_output, averaged_depth, None, 
												0.5, 3, 15, 3, 5, 1.2, 0)
			mag, _ = cv2.cartToPolar(flow[..., 0], flow[..., 1])
			motion_map = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)
			motion_map = np.uint8(motion_map)

			

			left_motion = motion_map[:, :part_width]
			middle_motion = motion_map[:, part_width:2 * part_width]
			right_motion = motion_map[:, 2 * part_width:]

			left_motion_intensity = np.mean(left_motion)
			middle_motion_intensity = np.mean(middle_motion)
			right_motion_intensity = np.mean(right_motion)


			motion_avg = np.mean([left_motion_intensity, middle_motion_intensity, right_motion_intensity])
			motion_std = np.std([left_motion_intensity, middle_motion_intensity, right_motion_intensity])
			dynamic_threshold = motion_avg + motion_std * 0.5  # Adjust factor as needed


			if left_motion_intensity > dynamic_threshold:
				pane[0] = 1

			if middle_motion_intensity > dynamic_threshold:
				pane[1] = 1

			if right_motion_intensity > dynamic_threshold:
				pane[2] = 1
			return pane




def display_image(bytes, cli_sock):
	frame = cv2.imdecode(np.fromstring(bytes, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
	l, m, r = depth_mp(frame)
	
	cli_sock.sendall((f'{"left" if l== 1 else ""},  {"middle" if m == 1 else ""},  {"right" if r == 1 else ""}\n').encode())

	# cli_sock.sendall(('left\n').encode())
	cv2.imshow("Present frame", frame)
	cv2.waitKey(1)

def main(server, port):
	try:
		server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server_socket.bind((server, port))
		print(f'[+] streamera server created at {server}:{port}')
	except:
		print(f'[!] Could not create streamera server at {server}:{port}')
		return -1
    
    
	server_socket.listen(5)

	cli_sock, ret = server_socket.accept()
	print(f"[+] CLIENT JOINED: {cli_sock}")
    
	SIZE = 1500
	str_buf = b''
    
	while True:
		
		try:
			msg = cli_sock.recv(SIZE)
		except:
			print('[-] Client disconnected.\n[-] Terminating server.')
			break

		if(msg):
			str_buf += msg

			# if string contains ffd9 (it means end of image)
			pos = str_buf.find(b'\xff\xd9')
			if pos >= 0:
				display_image(str_buf[:pos+2], cli_sock)
				str_buf = str_buf[pos+2:]

	server_socket.close()

if __name__ == "__main__":

	argparser = argparse.ArgumentParser()
	argparser.add_argument("server", type=str, help="IP Address")
	argparser.add_argument("port", type=int, help="Port")
	args = argparser.parse_args()

	main(args.server, args.port)