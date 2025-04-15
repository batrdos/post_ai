import streamlit as st
import torch
# from diffusers import StableDiffusionPipeline
from PIL import Image
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(
    page_title="Instagram Post Generator",
    page_icon="📸",
    layout="wide"
)

# # Initialize the Stable Diffusion pipeline
# @st.cache_resource
# def load_model():
#     model_id = "stable-diffusion-v1-5/stable-diffusion-v1-5"
#     pipe = StableDiffusionPipeline.from_pretrained(
#         model_id,
#         torch_dtype=torch.float32,
#         use_safetensors=True
#     )
#     if torch.cuda.is_available():
#         pipe = pipe.to("cuda")
#     return pipe

def main():
    st.title("📸 Instagram Post Generator")
    st.write("Upload a sample Instagram post and generate similar images with your custom prompts!")

    # Initialize session state for uploaded images
    if 'uploaded_images' not in st.session_state:
        st.session_state.uploaded_images = []

    # File uploader for sample images
    uploaded_files = st.file_uploader(
        "Upload sample Instagram posts",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True
    )

    if uploaded_files:
        st.session_state.uploaded_images = uploaded_files
        st.write(f"Uploaded {len(uploaded_files)} images")

        # Display uploaded images
        cols = st.columns(min(4, len(uploaded_files)))
        for idx, img in enumerate(uploaded_files):
            with cols[idx % len(cols)]:
                st.image(img, use_column_width=True)

    # User input for prompt
    prompt = st.text_area(
        "Enter your prompt for image generation",
        placeholder="A professional Instagram post showing..."
    )

    # Additional parameters
    col1, col2 = st.columns(2)
    with col1:
        num_images = st.slider("Number of images to generate", 1, 4, 1)
    with col2:
        guidance_scale = st.slider("Guidance scale (creativity vs. prompt adherence)", 7.0, 15.0, 7.5)

    # Generate button
    if st.button("Generate Images") and prompt:
        with st.spinner("Generating images..."):
            try:
                pipe = load_model()
                generated_images = []
                
                for _ in range(num_images):
                    image = pipe(
                        prompt,
                        guidance_scale=guidance_scale,
                        num_inference_steps=50
                    ).images[0]
                    generated_images.append(image)

                # Display generated images
                cols = st.columns(min(4, len(generated_images)))
                for idx, img in enumerate(generated_images):
                    with cols[idx % len(cols)]:
                        st.image(img, use_column_width=True)
                        st.download_button(
                            f"Download Image {idx + 1}",
                            img,
                            file_name=f"generated_image_{idx + 1}.png",
                            mime="image/png"
                        )

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main() 