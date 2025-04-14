# Instagram Post Generator

This application allows you to generate Instagram-style images based on sample company posts and custom prompts using Stable Diffusion.

## Features

- Upload sample Instagram posts for reference
- Generate new images based on custom prompts
- Adjust generation parameters (number of images, creativity level)
- Download generated images

## Setup

1. Clone this repository
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   streamlit run app.py
   ```

## Usage

1. Upload one or more sample Instagram posts that represent your desired style
2. Enter a detailed prompt describing what you want to generate
3. Adjust the number of images and guidance scale as needed
4. Click "Generate Images" to create new images
5. Download the generated images using the download buttons

## Requirements

- Python 3.8 or higher
- CUDA-capable GPU (recommended for faster generation)
- At least 8GB of RAM

## Notes

- The first run will download the Stable Diffusion model (about 4GB)
- Image generation may take 30-60 seconds per image depending on your hardware
- For best results, provide detailed prompts and high-quality sample images 