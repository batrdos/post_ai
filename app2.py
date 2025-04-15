import streamlit as st
import replicate
import urllib.request
import os
import tempfile
from PIL import Image
import io

# Set page configuration
st.set_page_config(
    page_title="Replicate AI Generator",
    page_icon="🧠",
    layout="wide"
)

# Add title and description
st.title("AI Text & Image Generator")
st.markdown("Generate text using Llama 2 and images using Flux Schnell through Replicate's API")

# Check for API token
if "REPLICATE_API_TOKEN" not in os.environ:
    api_key = st.text_input("Enter your Replicate API Token:", type="password")
    if api_key:
        os.environ["REPLICATE_API_TOKEN"] = api_key
        st.success("API token set successfully!")
    else:
        st.warning("Please enter your Replicate API token to continue.")
        st.stop()

# Create tabs for the different generators
text_tab, image_tab = st.tabs(["Text Generation", "Image Generation"])

# Text Generation Tab
with text_tab:
    st.header("Llama 2 Text Generation")
    
    text_prompt = st.text_area(
        "Enter your text prompt:",
        value="Once upon a time a llama explored",
        height=100
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        temperature = st.slider("Temperature:", min_value=0.1, max_value=1.0, value=0.75, step=0.05)
        top_p = st.slider("Top P:", min_value=0.1, max_value=1.0, value=0.9, step=0.05)
    
    with col2:
        top_k = st.slider("Top K:", min_value=10, max_value=100, value=50, step=5)
        max_tokens = st.slider("Max New Tokens:", min_value=32, max_value=512, value=128, step=32)
    
    if st.button("Generate Text", key="generate_text"):
        with st.spinner("Generating text..."):
            text_input = {
                "prompt": text_prompt,
                "temperature": temperature,
                "top_p": top_p,
                "top_k": top_k,
                "max_new_tokens": max_tokens,
                "min_new_tokens": -1
            }
            
            try:
                # Create a placeholder for streaming output
                text_output = st.empty()
                full_text = ""
                
                # Stream the output
                for event in replicate.stream(
                    "anthropic/claude-3.5-haiku",
                    input=text_input
                ):
                    full_text += event.data
                    text_output.markdown(f"**Output:**\n\n{full_text}")
                
                # Display final output
                st.success("Text generation completed!")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

# Image Generation Tab
with image_tab:
    st.header("Flux Schnell Image Generation")
    
    image_prompt = st.text_area(
        "Enter your image prompt:",
        value="black forest gateau cake spelling out the words \"FLUX SCHNELL\", tasty, food photography, dynamic shot",
        height=100
    )
    
    if st.button("Generate Image", key="generate_image"):
        with st.spinner("Generating image (this may take a minute or two)..."):
            image_input = {
                "prompt": image_prompt
            }
            
            try:
                # Run the model
                output = replicate.run(
                    "black-forest-labs/flux-schnell",
                    input=image_input
                )
                
                # Ensure output is treated as a list
                if isinstance(output, str):
                    output = [output]
                
                # Display images
                st.success(f"Generated {len(output)} image(s)!")
                
                for index, url in enumerate(output):
                    st.markdown(f"**Image {index+1}:**")
                    
                    # Create columns for each image
                    img_col, dl_col = st.columns([4, 1])
                    
                    with img_col:
                        st.image(url, use_column_width=True)
                    
                    with dl_col:
                        # Add download button
                        try:
                            response = urllib.request.urlopen(url)
                            image_data = response.read()
                            
                            st.download_button(
                                label="Download",
                                data=image_data,
                                file_name=f"flux_schnell_{index}.webp",
                                mime="image/webp"
                            )
                        except Exception as e:
                            st.error(f"Failed to prepare download: {e}")
                            
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

# Add footer with instructions
st.markdown("---")
st.markdown("""
### How to use this app:
1. Make sure you have a valid [Replicate API token](https://replicate.com/)
2. Enter your prompt in the respective tab
3. Adjust parameters as needed
4. Click the generate button and wait for results
5. For images, you can download them using the download button
""")