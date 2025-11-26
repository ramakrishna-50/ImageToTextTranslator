import streamlit as st
from googletrans import Translator
from PIL import Image
import fitz

st.set_page_config(page_title="Translator", page_icon="🌍")

LANG_MAP = {
    "Telugu": "te",
    "Hindi": "hi",
    "Tamil": "ta",
    "English": "en"
}

translator = Translator()

def extract_pdf(uploaded_file):
    text = ""
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    for page in doc:
        text += page.get_text()
    return text

st.title("📸 Image / 📄 PDF ➜ 🌍 Text Translation System")

choice = st.radio("Select input type:", ["Image", "PDF", "Plain Text"])

uploaded_file = st.file_uploader("Upload file", type=["jpg", "jpeg", "png", "pdf", "txt"])
target_lang = st.selectbox("Translate to:", list(LANG_MAP.keys()))

if st.button("Translate"):
    if not uploaded_file:
        st.error("Upload a file first.")
    else:
        if choice == "PDF":
            text = extract_pdf(uploaded_file)

        elif choice == "Plain Text":
            text = uploaded_file.read().decode("utf-8")

        elif choice == "Image":
            st.error("⚠ Image OCR unsupported on cloud. Use PDF/Text.")
            st.stop()

        translated = translator.translate(text, dest=LANG_MAP[target_lang]).text
        st.subheader("Translated Text")
        st.write(translated)

        st.download_button("⬇ Download Result", translated)

