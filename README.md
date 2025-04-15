# Instagram Post Generator

This application generates professional Instagram posts by combining Flux 1.1 Pro for high-quality image generation and Claude 3.5 Sonnet for engaging caption writing.

## Features

- Generate stunning images using Flux 1.1 Pro AI
- Create engaging captions with Claude 3.5 Sonnet
- Upload reference images for style inspiration
- Customize caption tone and target audience
- Adjust image generation parameters
- Download ready-to-post images and captions

## Setup

1. Clone this repository
2. Create a `.env` file in the root directory with your Replicate API token:
   ```
   REPLICATE_API_TOKEN=your_token_here
   ```
   Get your API token from [Replicate](https://replicate.com/account)
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   streamlit run app.py
   ```

## Usage

1. (Optional) Upload reference Instagram posts for style inspiration
2. Enter a detailed prompt describing your desired image
3. Select your preferred caption tone and target audience
4. Adjust the image creativity level if needed
5. Click "Generate Posts" to create your content
6. Download the generated images and captions

## Requirements

- Python 3.8 or higher
- Internet connection
- Replicate API token

## Models Used

- **Image Generation**: Flux 1.1 Pro
  - High-resolution output (1024x1024)
  - Professional-grade image quality
  - Advanced prompt understanding
  - Built-in negative prompting for better results

- **Caption Generation**: Claude 3.5 Sonnet
  - Engaging and authentic writing style
  - Context-aware captions
  - Targeted audience customization
  - Automatic hashtag generation
  - Character-optimized for Instagram

## Notes

- Image generation typically takes 20-30 seconds per image
- Captions are optimized for Instagram's character limits
- For best results, provide detailed prompts and clear audience targeting
- All generated content is ready to post without additional editing 