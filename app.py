import streamlit as st
import fitz
import requests
import json

st.set_page_config(page_title="PDF / Text Translator", page_icon="🌍")

LANG_CODES = {
    "Telugu": "te",
    "Hindi": "hi",
    "Tamil": "ta",
    "English": "en"
}

# PDF extraction
def extract_pdf(uploaded_file):
    text = ""
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

# Hugging Face API (no token required)
def translate(text, target_lang):
    url = "https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-en-" + target_lang
    payload = {"inputs": text}
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    result = response.json()
    try:
        return result[0]['translation_text']
    except:
        return "⚠ Translation failed. Try shorter text."

st.title("📄 PDF / 📝 Text ➜ 🌍 Multi-Language Translator")

mode = st.radio("Select Input Type:", ["PDF", "Plain Text"])
file = None

if mode == "PDF":
    file = st.file_uploader("Upload PDF", type=["pdf"])
elif mode == "Plain Text":
    file = st.text_area("Enter text here:")

target = st.selectbox("Translate To:", list(LANG_CODES.keys()))

if st.button("Translate"):
    if not file:
        st.error("Upload or enter text first!")
    else:
        if mode == "PDF":
            text = extract_pdf(file)
        else:
            text = file

        result = translate(text, LANG_CODES[target])
        st.subheader("Translated Text:")
        st.write(result)

        st.download_button("⬇ Download Translation", result)
