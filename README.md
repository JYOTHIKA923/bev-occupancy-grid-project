# bev-occupancy-grid-project
## 🚗 Bird’s Eye View (BEV) Occupancy Grid Mapping

## 📌 Project Overview
- This project converts a front-view road image into a Bird’s Eye View (BEV) and generates an Occupancy Grid Map.

- Front-view images suffer from perspective distortion, which makes navigation difficult.
This system transforms the input image into a top-down view and represents the environment in a structured grid format.

## 🎯 Applications

- Autonomous driving
- Robot navigation
- Path planning systems
- Computer Vision Systems 

## 🧠 Model Architecture

The system follows a computer vision pipeline:
- Input Image
- Perspective Transformation (BEV)
- Image Preprocessing (Grayscale + Blur)
- Thresholding (Segmentation)
- Morphological Operations (Noise Removal)
- Occupancy Map Generation
- Grid Conversion
- Output Visualization
This architecture converts raw image data into a structured spatial representation.

## 🎯 Key Features

- BEV (Top View) Transformation  
- Occupancy Map Generation  
- Grid-based Environment Representation  
- Colored Grid Visualization (Free vs Occupied)  
- Grid Overlay on BEV 
 
## 📂 Dataset Used

- Custom road image (road.jpeg)
- No training dataset required
- Rule-based computer vision approach
 

## 🧠 Workflow

- Input Image → BEV Transform → Image Processing → Occupancy Map → Grid Mapping

## 📊 Outputs
 
  - Bird's Eye View
  - Occupancy Map
  - Grid Map
  - BEV with Grid Overlay
  - Black and white grid
  - coloured grid
  - legend

## Visualization:

Displays original image, BEV, occupancy map, and grid map

 ## ⚙️ Technologies Used
 
 - Python
 - OpenCV
 - NumPy


## ▶️ How to Run

1. Install dependencies:
   pip install opencv-python numpy
2. Run the code:
   python main.py

 ## 📌 Future Improvements
 
  - Real-time video processing  
  - Object detection integration (YOLO)  
  - Path planning algorithms  

