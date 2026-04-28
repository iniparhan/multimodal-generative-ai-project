import streamlit as st
import requests
import os
from dotenv import load_dotenv
from groq import Groq
from gtts import gTTS
import urllib.parse

# ======================
# CONFIG
# ======================
st.set_page_config(page_title="AI Story Generator", layout="wide")

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ======================
# STATE
# ======================
if "history" not in st.session_state:
    st.session_state.history = []

# ======================
# BACKEND FUNCTIONS
# ======================
def generate_story(prompt):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": f"Buat cerita anak dari ide berikut:\n{prompt}\n\nGunakan bahasa sederhana, singkat, dan menarik."
            }
        ],
        temperature=0.7
    )
    return response.choices[0].message.content


def generate_image(prompt):
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"

    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.content
        return None
    except:
        return None


def text_to_speech(text):
    tts = gTTS(text)
    file_path = "story.mp3"
    tts.save(file_path)
    return file_path

# ======================
# HEADER
# ======================
st.title("AI Story Generator")
st.caption("Generate cerita anak lengkap dengan ilustrasi dan audio")

# ======================
# INPUT SECTION
# ======================
with st.container():
    col1, col2 = st.columns([3, 1])

    with col1:
        user_input = st.text_input(
            "Masukkan ide cerita",
            placeholder="Contoh: Kucing petualang di luar angkasa"
        )

    with col2:
        generate_btn = st.button("Generate", use_container_width=True)

# ======================
# MAIN PROCESS
# ======================
if generate_btn:

    if user_input.strip() == "":
        st.warning("Input tidak boleh kosong")
    else:
        with st.spinner("Sedang membuat cerita dan ilustrasi..."):

            story = generate_story(user_input)

            image_prompt = f"cute cartoon {user_input}, happy family, children's book illustration, colorful, friendly, 2D animation"
            image = generate_image(image_prompt)

            audio = text_to_speech(story)

            # Save ke history
            st.session_state.history.append({
                "prompt": user_input,
                "story": story
            })

        # ======================
        # OUTPUT DISPLAY (TABS)
        # ======================
        tab1, tab2, tab3 = st.tabs(["Cerita", "Ilustrasi", "Audio"])

        with tab1:
            st.subheader("Hasil Cerita")
            st.write(story)

        with tab2:
            st.subheader("Ilustrasi")
            if image:
                st.image(image, width="stretch")
            else:
                st.error("Gagal membuat gambar")

        with tab3:
            st.subheader("Audio Cerita")
            st.audio(audio)

# ======================
# HISTORY SECTION
# ======================
st.divider()
st.subheader("Riwayat Cerita")

if len(st.session_state.history) == 0:
    st.caption("Belum ada cerita yang dibuat")
else:
    for i, item in enumerate(reversed(st.session_state.history)):
        with st.expander(f"Story #{i+1}: {item['prompt']}"):
            st.write(item["story"])