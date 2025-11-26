import streamlit as st
from PIL import Image
import pytesseract
from deep_translator import GoogleTranslator
import fitz

# Tesseract OCR path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

LANG_CODES = {
    "Telugu": "te",
    "Hindi": "hi",
    "English": "en",
    "Tamil": "ta",
}

def extract_image(uploaded):
    img = Image.open(uploaded)
    return pytesseract.image_to_string(img)

def extract_pdf(uploaded):
    doc = fitz.open(stream=uploaded.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def translate_text(text, lang):
    return GoogleTranslator(source="auto", target=LANG_CODES[lang]).translate(text)

st.title("🖼️ Image / 📄 PDF → 🔤 Text → 🌍 Translation System")
st.write("Upload Image or PDF, choose language, and translate the extracted text.")

choice = st.radio("Select Input Type:", ["Image", "PDF", "Plain Text"])
file = None
text = ""

if choice in ("Image", "PDF"):
    file = st.file_uploader("Upload file", type=["jpg", "jpeg", "png", "pdf"])
else:
    text = st.text_area("Enter text manually")

lang = st.selectbox("Translate to:", list(LANG_CODES.keys()))

if st.button("Translate"):
    if choice in ("Image", "PDF") and not file:
        st.error("⚠ Please upload a file")
    else:
        if choice == "Image":
            text = extract_image(file)
        elif choice == "PDF":
            text = extract_pdf(file)

        st.subheader("📌 Extracted Text")
        st.text_area("Extracted", text, height=200)

        translated = translate_text(text, lang)

        st.subheader(f"🌍 Translated Text ({lang})")
        st.text_area("Translated", translated, height=200)

        st.download_button("⬇ Download Result", translated,
                           file_name=f"translation_{LANG_CODES[lang]}.txt")
