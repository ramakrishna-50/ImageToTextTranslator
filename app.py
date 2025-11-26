import streamlit as st
from PIL import Image
import pytesseract
from pytesseract import TesseractNotFoundError
from deep_translator import GoogleTranslator
import fitz  # PyMuPDF


LANG_CHOICES = {
    "Telugu": "te",
    "Hindi": "hi",
    "English": "en",
    "Tamil": "ta",
}


def translate_text(text: str, target: str) -> str:
    text = text.strip()
    if not text:
        return ""
    try:
        return GoogleTranslator(source="auto", target=target).translate(text)
    except Exception as e:
        return f"Translation error: {e}"


def extract_image_text(uploaded_file):
    try:
        img = Image.open(uploaded_file)
        return pytesseract.image_to_string(img)
    except TesseractNotFoundError:
        return None
    except Exception as e:
        return f"OCR error: {e}"


def extract_pdf_text(uploaded_file):
    try:
        file_bytes = uploaded_file.read()
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        return f"PDF extract error: {e}"


def main():
    st.set_page_config(
        page_title="Image / PDF to Text Translation System",
        page_icon="🌍",
        layout="centered",
    )

    st.title("🖼️ Image / 📄 PDF ➜ 🔤 Text ➜ 🌍 Translation System")
    st.write(
        "Upload an Image, PDF or enter Plain Text, then choose the target language to translate."
    )

    input_type = st.radio(
        "Select input type:",
        ["Image", "PDF", "Plain Text"],
        horizontal=True,
    )

    target_lang = st.selectbox("Translate to:", list(LANG_CHOICES.keys()))
    target_lang_code = LANG_CHOICES[target_lang]

    st.markdown("---")

    # IMAGE
    if input_type == "Image":
        file = st.file_uploader("Upload image", type=["jpg", "jpeg", "png"])

        if file is not None and st.button("Translate"):
            extracted = extract_image_text(file)

            if extracted is None:   # Tesseract missing on cloud
                st.error(
                    "Image OCR is not available on this online version because Tesseract is not installed.\n"
                    "You can use PDF / Plain Text on the cloud, or run the app locally for full OCR."
                )
                return

            st.subheader("Extracted Text")
            st.text_area("Extracted", extracted, height=200)

            translated = translate_text(extracted, target_lang_code)

            st.subheader(f"Translated Text ({target_lang})")
            st.text_area("Translated", translated, height=200)

            st.download_button(
                "Download Result",
                data=translated,
                file_name=f"output_{target_lang_code}.txt",
                mime="text/plain",
            )

    # PDF
    elif input_type == "PDF":
        file = st.file_uploader("Upload PDF", type=["pdf"])

        if file is not None and st.button("Translate"):
            extracted = extract_pdf_text(file)

            st.subheader("Extracted Text from PDF")
            st.text_area("Extracted", extracted, height=250)

            translated = translate_text(extracted, target_lang_code)

            st.subheader(f"Translated Text ({target_lang})")
            st.text_area("Translated", translated, height=250)

            st.download_button(
                "Download Result",
                data=translated,
                file_name=f"output_{target_lang_code}.txt",
                mime="text/plain",
            )

    # PLAIN TEXT
    else:
        text = st.text_area("Enter text here:", height=200)

        if st.button("Translate"):
            translated = translate_text(text, target_lang_code)

            st.subheader(f"Translated Text ({target_lang})")
            st.text_area("Translated", translated, height=250)

            st.download_button(
                "Download Result",
                data=translated,
                file_name=f"output_{target_lang_code}.txt",
                mime="text/plain",
            )


if __name__ == "__main__":
    main()
