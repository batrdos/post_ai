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
st.markdown("Generate text using Claude Sonnet 3.5 and images using custom Flux through Replicate's API")

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
# text_tab, image_tab = st.tabs(["Text Generation", "Image Generation"])

# Text Generation Tab
# with text_tab:
st.header("Text Generation")

text_prompt = st.text_area(
    "Enter your text prompt:",
    value="Только на этой неделе: скидка 5% на готовые проекты!",
    height=100
)

# col1, col2 = st.columns(2)

# with col1:
#     temperature = st.slider("Temperature:", min_value=0.1, max_value=1.0, value=0.75, step=0.05)
#     top_p = st.slider("Top P:", min_value=0.1, max_value=1.0, value=0.9, step=0.05)

# with col2:
#     top_k = st.slider("Top K:", min_value=10, max_value=100, value=50, step=5)
#     max_tokens = st.slider("Max New Tokens:", min_value=32, max_value=512, value=128, step=32)

if st.button("Generate Text", key="generate_text"):
    with st.spinner("Generating text..."):
        text_input = {
            "prompt": text_prompt,
            "max_tokens": 8192,
            "system_prompt": f"""You are an expert Instagram caption writer for appartment building company. Create an engaging caption for an Instagram post.

                            Write a caption that is:
                            1. Engaging and authentic
                            2. In Russian
                            3. Resonates with potential home buyers
                            4. No hashtags

                            Примеры:
                                1. 'Золотое летнее утро. Вы выходите на личную террасу с чашкой кофе, садитесь в любимое кресло. И наслаждаетесь свежим воздухом и прекрасным видом.

Мы запланировали в PRIVILEGIA просторные террасы. К примеру, у этих 3-комнатных апартаментов будет терраса площадью почти 24,5 метра. Можно разместить на ней уютную лаунж-зону с диванами и гамаками.

Самое приятное в том, что будущие жители PRIVILEGIA оплачивают только 1/3 от площади террасы. Остальное идёт в подарок.

Персональная терраса придаёт очарование загородного дома. Всегда можно устроить семейный завтрак на свежем воздухе.

Выбирайте апартаменты в комплексе элитных клубных домов.'
                                2. 'Элитный комплекс клубных домов располагается в одной из лучших алматинских локаций. С одной стороны — рядом горы, с другой — можно за минуту выехать на Аль-Фараби.

В PRIVILEGIA чистый воздух и прекрасный вид сочетаются с идеальной транспортной доступностью. До MEGA Alma-Ata 5 минут, до Esentai Mall — 10 минут на авто.

Присоединяйтесь к PRIVILEGIA! Выбирайте комфорт и безопасность элитного комплекса клубных домов.'
                                3. 'Команда PRIVILEGIA идёт чётко по графику. На стройплощадке кипит работа. Здесь армируют стены, монтируют опалубку для плит перекрытия и заливают бетон.

Строительство движется в правильном ритме, все процессы начинаются и завершаются в срок. Одно из самых приятных ощущений в нашей работе — видеть, что проект растёт и развивается так, как было задумано.

Наш комплекс клубных домов сейчас в процессе строительства. При этом половина резиденций уже продана. PRIVILEGIA — по-настоящему уникальный и качественный проект в престижном районе.

Смотрите видео о том, как продвигаются работы на стройплощадке. В ленте вы найдёте статусы, которые мы снимали ранее. По ним будет проще отследить прогресс.'


                            Format the response as a clean caption without any explanations."""

        }
        
        try:
            # Create a placeholder for streaming output
            text_output = st.empty()
            full_text = ""
            
            # Stream the output
            for event in replicate.stream(
                "anthropic/claude-3.5-sonnet",
                input=text_input
            ):
                full_text += event.data
                text_output.markdown(f"**Output:**\n\n{full_text}")
            
            # Display final output
            st.success("Text generation completed!")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")


# Add a separator
st.markdown("---")


# Image Generation Tab
# with image_tab:
st.header("Image Generation")

image_prompt = st.text_area(
    "Enter your image prompt:",
    value="PRIVILEGIA — это уникальный комплекс клубных домов, созданный в соответствии с высокими стандартами элитной недвижимости. Только на этой неделе: скидка 5% на готовые проекты!",
    height=100
)

if st.button("Generate Image", key="generate_image"):
    with st.spinner("Generating image ..."):
        image_input = {
            "model": "dev",
            "prompt": image_prompt,
            "go_fast": False,
            "lora_scale": 1,
            "megapixels": "1",
            "num_outputs": 1,
            "aspect_ratio": "1:1",
            "output_format": "webp",
            "guidance_scale": 3,
            "output_quality": 80,
            "prompt_strength": 0.8,
            "extra_lora_scale": 1,
            "num_inference_steps": 28
        }
        
        try:
            # Run the model
            output = replicate.run(
                "batrdos/post-ai:4f78c1cf551024e30c7cb1f03ed48f20ab27e255095ef1e67a8af484fb8fd301",
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
1. Enter your prompt in the respective tabs
2. Click the generate button and wait for results
3. For images, you can download them using the download button or post them directly to Instagram account
""")