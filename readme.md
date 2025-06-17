# AVA: AI-powered Vision Assistant

This project aims to create an affordable, effective assistive device for visually impaired individuals, using advanced deep learning and computer vision. The device provides three core functionalities:
- **Obstacle Avoidance**: Alerts users to nearby obstacles for safe navigation.
- **Scene Description**: Generates descriptive summaries of the user's environment.
- **Visual Question Answering (VQA)**: Allows users to ask questions about their surroundings and receive answers.

By integrating these capabilities, AVA improves accessibility and independence for visually impaired users.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Core Functionalities](#core-functionalities)
   - [Obstacle Avoidance](#obstacle-avoidance)
   - [Scene Description](#scene-description)
   - [Visual Question Answering (VQA)](#visual-question-answering-vqa)
   - [Raspberry Pi Integration](#raspberry-pi-integration)`
3. [Technology Stack](#technology-stack)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Datasets](#datasets)
7. [Future Work](#future-work)

---

## Project Overview

AVA leverages cutting-edge computer vision and AI models to interpret and respond to a user's environment in real-time. Designed for cost-efficiency and effectiveness, AVA delivers valuable information to visually impaired users, assisting with obstacle detection, environment understanding, and interactive questioning.

---

## Core Functionalities

### 1. Obstacle Avoidance

- **Monocular Depth Estimation**: Uses the MiDaS v2 model to estimate depth from a single camera.
- **Optical Flow Analysis**: Employs Gunnar Farneback Dense Optical Flow to track object motion and detect moving obstacles.
- **Field of View (FOV) Segmentation**: The FOV is divided into Left, Middle, and Right panes, providing specific feedback on obstacle location.
- **User Alerts**: The system informs the user of the nearest obstacles in each pane, aiding safe navigation.

**Implementation Details:**
- The server (`src/obstacle_avoidance/server.py`) receives image frames from the Raspberry Pi client over a TCP socket.
- Each frame is processed for depth and motion, and the server sends back pane-specific obstacle alerts.
- The Pi client uses text-to-speech to relay these alerts to the user.

### 2. Scene Description

- **Model**: [shaikhadil26/blip2-opt-2.7b-image-description-v2](https://huggingface.co/shaikhadil26/blip2-opt-2.7b-image-description-v2), Fine-tuned [BLIP2-OPT2.7B](https://huggingface.co/Salesforce/blip2-opt-2.7b) using [PEFT: LoRA](https://github.com/microsoft/LoRA)}.
- **Datasets**: Trained on [sezenkarakus/image-description-dataset](https://huggingface.co/datasets/sezenkarakus/image-description-dataset) and [sezenkarakus/image-description-dataset-v2](https://huggingface.co/datasets/sezenkarakus/image-description-dataset-v2).
- **API**: A FastAPI server (see `src/apis/scene_description.ipynb`) exposes an endpoint for image uploads. The server returns a generated scene description.

**How it works:**
- The Pi client captures an image and sends it via HTTP POST to the FastAPI endpoint.
- The server processes the image and returns a descriptive caption.
- The Pi client can use text-to-speech to read the description aloud.

### 3. Visual Question Answering (VQA)

- **Model**: BLIP2-OPT2.7B VQA model (with plans to evaluate Molmo-7B-D-0924).
- **API**: A FastAPI server (see `src/apis/vqa.ipynb`) exposes an endpoint for image and question uploads. The server returns an answer to the user's question.

**How it works:**
- The Pi client captures an image and sends it, along with a user question, via HTTP POST to the FastAPI endpoint.
- The server processes the image and question, returning an answer.
- The Pi client can use text-to-speech to relay the answer.

---

## Raspberry Pi Integration

The `src/pi` folder contains Python scripts for running AVA on a Raspberry Pi:

- **obsAvoidance.py**: 
  - Captures video frames from the Pi camera.
  - Sends frames to the obstacle avoidance server via TCP socket.
  - Receives pane-specific obstacle alerts and uses text-to-speech to inform the user.

- **sceneDesc_obsAvoidance.py**:
  - Extends obstacle avoidance with scene description.
  - Periodically captures frames and sends them to the FastAPI scene description endpoint.
  - Receives and reads out both obstacle alerts and scene descriptions.

**Key Features:**
- Real-time video capture and processing.
- Socket-based communication for low-latency obstacle alerts.
- HTTP-based communication for scene description and VQA.
- Text-to-speech feedback for all functionalities.

---

## Technology Stack

- **Monocular Depth Estimation**: MiDaS v2
- **Optical Flow**: Gunnar Farneback Dense Optical Flow
- **Scene Description Model**: BLIP2-OPT2.7B fine-tuned with PEFT: LoRA
- **Visual Question Answering**: BLIP2-OPT2.7B VQA model (tentative), Molmo-7B-D-0924 as a potential alternative
- **API Framework**: FastAPI for scene description and VQA. Obstacle avoidance uses socket-based streaming for real-time feedback.
- **Raspberry Pi 5B**: Python scripts for camera capture, communication, and TTS

---

## Installation

### Prerequisites

- Python 3.9+
- [CUDA Toolkit](https://developer.nvidia.com/cuda-toolkit) (if using a GPU)
- Raspberry Pi with camera module (for client-side scripts)

### Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/shaikhadil26/AVA.git
   cd AVA
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

### Obstacle Avoidance

- **Server**: Run `src/obstacle_avoidance/server.py` on your main machine.
- **Client (Raspberry Pi)**: Run `src/pi/obsAvoidance.py` with the server's IP and port.
- The Pi will send frames to the server and receive obstacle alerts, which are read aloud.

### Scene Description

- **API Server**: Run the FastAPI server in `src/apis/scene_description.ipynb` (or convert to `.py` for production).
- **Client (Raspberry Pi)**: Run `src/pi/sceneDesc_obsAvoidance.py` with the server's IP and port.
- The Pi will periodically send images to the FastAPI endpoint and read out the returned scene description.

### Visual Question Answering

- **API Server**: Run the FastAPI server in `src/apis/vqa.ipynb`.
- **Client**: Send an image and a question to the VQA endpoint; the server will return an answer.

---

## Datasets

- [sezenkarakus/image-description-dataset](https://huggingface.co/datasets/sezenkarakus/image-description-dataset) - Dataset used for scene description fine-tuning.
- [sezenkarakus/image-description-dataset-v2](https://huggingface.co/datasets/sezenkarakus/image-description-dataset-v2) - Additional dataset used to enhance description quality.

These datasets were instrumental in training the Scene Description Model to describe complex scenes with accuracy.

---

## Future Work

- **Enhanced VQA Model**: Evaluate and potentially integrate Molmo-7B-D-0924 for improved VQA performance.
- **Edge Computing**: Optimize obstacle detection to run more efficiently on edge devices.
- **Relativity of Monocular Depth Estimation**: To overcome the relativity problem in MiDaS, which leads to false positives, by possibilty integrating mono depth models like [apple/DepthPro](https://huggingface.co/apple/DepthPro)

