import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- Streamlit Page Setup ---
st.set_page_config(page_title="🥗 Calories Advisor App")
st.title("🥗 Calories Advisor App")

# --- Sidebar: API Key Input ---
st.sidebar.title("🔑 API Key Configuration")
api_key = st.sidebar.text_input("Enter your Google API Key", type="password")

# --- API Key Check ---
if not api_key:
    st.warning("Please enter your Google API key in the sidebar to continue.")
    st.stop()
else:
    genai.configure(api_key=api_key)

# --- Gemini Response Function ---
def get_gemini_response(input_prompt, image):
    model = genai.GenerativeModel('models/gemini-1.5-flash')
    response = model.generate_content([input_prompt, image[0]])
    return response.text

# --- Image Processing Function ---
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# --- User Upload Image ---
uploaded_file = st.file_uploader("📷 Upload your food image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="🍽️ Uploaded Image", use_container_width=True)

# --- Prompt for Gemini ---
input_prompt = """
You are an expert nutritionist. Analyze the food items visible in the image and:
1. List each item with its estimated calorie count.
2. Indicate if the overall meal is healthy or not.
3. Provide a nutritional breakdown in percentage for:
   - Carbohydrates
   - Fats
   - Fibers
   - Sugars
   - Other relevant nutrients
Use the format:

1. Item A - X calories  
2. Item B - Y calories  
...  
Conclusion: [Healthy/Unhealthy]  
Nutrition Split: Carbs X%, Fats Y%, Fibers Z%, Sugars A%, etc.
"""

# --- Button to Trigger Response ---
submit = st.button("📊 Analyze Calories")

if submit:
    if uploaded_file:
        image_data = input_image_setup(uploaded_file)
        response = get_gemini_response(input_prompt, image_data)
        st.subheader("📝 Calorie & Nutrition Analysis")
        st.write(response)
    else:
        st.warning("⚠️ Please upload an image first.")
