# Assistive Device for the Visually Impaired

This project aims to create an affordable and effective assistive device with minimal hardware requirements for visually impaired individuals. The device uses advanced deep learning and computer vision techniques to provide three core functionalities:
- **Obstacle Avoidance**: Alerts the user to nearby obstacles, helping them navigate safely.
- **Scene Description**: Provides descriptive summaries of the scene in front of the user.
- **Visual Question Answering (VQA)**: Allows users to ask questions about their surroundings.



By integrating these capabilities, this project seeks to improve accessibility and independence for visually impaired individuals.

---

## Table of Contents
1. [Project Overview](#project-overview)
2. [Core Functionalities](#core-functionalities)
   - [Obstacle Avoidance](#obstacle-avoidance)
   - [Scene Description](#scene-description)
   - [Visual Question Answering (VQA)](#visual-question-answering-vqa)
3. [Technology Stack](#technology-stack)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Datasets](#datasets)
7. [Future Work](#future-work)


---

## Project Overview

The assistive device leverages cutting-edge computer vision and AI models to interpret and respond to a user’s environment in real-time. Designed to be both effective and cost-efficient, this device delivers valuable information to visually impaired users, assisting with obstacle detection, environment understanding, and interactive questioning.

---

## Core Functionalities

### 1. Obstacle Avoidance

To enable obstacle avoidance, we use:
- **Monocular Depth Estimation**: Implemented with the [MiDaS v2 model](https://github.com/isl-org/MiDaS), which estimates depth from a single camera view.
- **Optical Flow Analysis**: Using the **Gunnar Farneback Dense Optical Flow** technique, we track object motion and calculate the direction and speed of moving obstacles.

The combination of these methods allows us to:
- **Localize Obstacles in the Field of View (FOV)**: The FOV is divided into three sections—Left, Middle, and Right—to provide specific feedback on obstacle location.
- **Alert the User**: Based on obstacle proximity in each pane, the device informs the user of the nearest obstacles, aiding them in safe navigation.

### 2. Scene Description

For scene description, we employ a fine-tuned version of **BLIP2-OPT2.7B** with [PEFT: LoRA](https://github.com/microsoft/LoRA). Our custom fine-tuning process used:
- **Datasets**: [sezenkarakus/image-description-dataset](https://huggingface.co/datasets/sezenkarakus/image-description-dataset), [sezenkarakus/image-description-dataset-v2](https://huggingface.co/datasets/sezenkarakus/image-description-dataset-v2)
- **Hardware**: Fine-tuned on NVIDIA H100 GPUs.
- **Training**: The model was trained over **n epochs** to optimize performance on scene description tasks.

This model can generate comprehensive descriptions of the user’s surroundings, providing valuable context and enhancing spatial awareness.

### 3. Visual Question Answering (VQA)

To enable interactive question-answering about the environment, we integrate the **BLIP2-OPT2.7B VQA model**. The model allows users to ask specific questions about their surroundings and receive relevant responses. Currently, we are testing this model and may replace it with **Molmo-7B-D-0924** for enhanced performance.

VQA enables users to:
- **Interact with the Scene**: They can inquire about specific objects, colors, actions, or other contextual details within the environment.
- **Receive Real-time Responses**: Answers are generated promptly, providing a smooth user experience.

---

## Technology Stack

- **Monocular Depth Estimation**: MiDaS v2
- **Optical Flow**: Gunnar Farneback Dense Optical Flow
- **Scene Description Model**: BLIP2-OPT2.7B fine-tuned with PEFT: LoRA
- **Visual Question Answering**: BLIP2-OPT2.7B VQA model (tentatively), Molmo-7B-D-0924 as a potential alternative
- **API Framework**: FastAPI for handling VQA and scene description requests

---

## Installation

### Prerequisites
- Python 3.9+
- [CUDA Toolkit](https://developer.nvidia.com/cuda-toolkit) (if using a GPU)

### Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/shaikhadil26/AVA.git
   cd AVA

2. **Install Dependancies**
   ```bash
   pip install -r requirements.txt 


## Usage

### Obstacle Avoidance
- Start the camera feed with depth estimation and optical flow modules enabled.
- The system divides the FOV into left, middle, and right panes, providing alerts based on obstacle proximity.

### Scene Description
- Capture an image from the camera feed.
- The system generates a descriptive summary, accessible via the FastAPI endpoint.

### Visual Question Answering
- Send a question via the FastAPI VQA endpoint.
- The model analyzes the scene and returns an answer based on the user’s query.

---

## Datasets

- [sezenkarakus/image-description-dataset](https://huggingface.co/datasets/sezenkarakus/image-description-dataset) - Dataset used for scene description fine-tuning.
- [sezenkarakus/image-description-dataset-v2](https://huggingface.co/datasets/sezenkarakus/image-description-dataset-v2) - Additional dataset used to enhance description quality.

These datasets were instrumental in training the Scene Description Model to describe complex scenes with accuracy.

---

## Future Work

- **Enhanced VQA Model**: Evaluate and potentially integrate **Molmo-7B-D-0924** for improved VQA performance.

- **Edge Computing**: Optimize obstacle detection to run more efficiently on edge devices.

- **Relativity of Monocular Depth Estimation**: To overcome the relativity problem in MiDaS, which leads to false positives, by possibilty integrating mono depth models like [apple/DepthPro](https://huggingface.co/apple/DepthPro)

