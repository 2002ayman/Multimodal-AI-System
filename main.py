import streamlit as st
from PIL import Image
import io
import json
import hashlib
import numpy as np
from multimodal_module import MultimodalHandler
from ocr import OCRHandler
import database

st.set_page_config(page_title="Multimodal AI System", layout="wide")


@st.cache_resource
def load_handler():
    return MultimodalHandler()

@st.cache_resource
def load_ocr():
    return OCRHandler(languages=['ar', 'en'])

handler = load_handler()
ocr_handler = load_ocr()


database.create_table()


page = st.sidebar.selectbox("اختر الصفحة", [" رفع صورة", " البحث وعرض البيانات"])


if page == " رفع صورة":
    st.title(" رفع صورة ومعالجتها")

    if "last_uploaded" not in st.session_state:
        st.session_state.last_uploaded = None

    uploaded_files = st.file_uploader(
        "Upload multiple images",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True
    )

    if uploaded_files:
        for uploaded_file in uploaded_files:
            image = Image.open(uploaded_file).convert("RGB")
            st.image(image, caption=f"Uploaded: {uploaded_file.name}", width=300)


            caption = handler.generate_caption(image)
            st.write("Caption:", caption)


            features = handler.extract_features(image)
            features_json = json.dumps(features.tolist())

            ocr_results = ocr_handler.extract_text(image)
            extracted_texts = [item['text'] for item in ocr_results] if ocr_results else []
            ocr_text_combined = " ".join(extracted_texts)
            st.write("OCR:", ocr_text_combined if extracted_texts else "No text detected")

            img_bytes_io = io.BytesIO()
            image.save(img_bytes_io, format="PNG")
            img_bytes = img_bytes_io.getvalue()

            file_hash = hashlib.md5(uploaded_file.getvalue()).hexdigest()


            if st.session_state.get("last_uploaded") != file_hash:
                database.insert_data(
                    image_name=uploaded_file.name,
                    image_data=img_bytes,
                    caption=caption,
                    ocr_text=ocr_text_combined,
                    features=features_json
                )
                st.success(f"✅ {uploaded_file.name} saved to database!")
                st.session_state.last_uploaded = file_hash


elif page == " البحث وعرض البيانات":
    st.title(" البحث وعرض البيانات")

    query = st.text_input("أدخل كلمة البحث")

    if query.strip():
        results = database.search_data(query)
    else:

        results = database.get_all_data()

    if results:
        for row in results:
            img_data, caption, ocr_text = row
            img = Image.open(io.BytesIO(img_data))
            st.image(img, width=200)
            st.write("Caption:", caption)
            st.write("OCR:", ocr_text)
            st.markdown("---")
    else:
        st.warning("لا توجد بيانات مخزنة")