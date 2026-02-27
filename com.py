import streamlit as st
import cv2
import numpy as np
import easyocr
from PIL import Image

# --- 1. การตั้งค่าหน้าตาเว็บ (Minimal & Rounded) ---
st.set_page_config(page_title="Thai LPR Minimal", layout="centered")

st.markdown("""
    <style>
    /* ปรับพื้นหลังให้ดูสะอาด */
    .main {
        background-color: #f8fafc;
        font-family: 'Prompt', sans-serif;
    }
    
    /* ตกแต่ง Container ให้ขอบมนและมีเงา */
    div.stButton > button {
        width: 100%;
        border-radius: 12px;
        height: 3.5em;
        background-color: #2563eb;
        color: white;
        border: none;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    div.stButton > button:hover {
        background-color: #1d4ed8;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
    }

    /* ตกแต่งกล่องอัปโหลดไฟล์ */
    .stFileUploader {
        border-radius: 16px;
        padding: 10px;
    }

    /* ตกแต่งรูปภาพที่แสดงผลให้ขอบมน */
    img {
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    }

    /* ส่วนแสดงผลลัพธ์แบบ Minimal Card */
    .result-card {
        background-color: white;
        padding: 24px;
        border-radius: 20px;
        text-align: center;
        border: 1px solid #e2e8f0;
        margin-top: 24px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
    }
    </style>
    """, unsafe_allow_html=True) # แก้ไขจาก unsafe_allow_stdio เป็น unsafe_allow_html

# --- 2. ส่วนของ Logic ประมวลผลภาพ ---
@st.cache_resource
def load_model():
    # โหลด EasyOCR ภาษาไทยและอังกฤษ
    return easyocr.Reader(['th', 'en'])

reader = load_model()

def process_image(image):
    # แปลงรูปภาพเป็น numpy array
    img_array = np.array(image)
    # ใช้ EasyOCR อ่านข้อความในภาพ
    results = reader.readtext(img_array)
    return results

# --- 3. ส่วนประกอบหน้าเว็บ (Frontend) ---
st.title("ระบบอ่านป้ายทะเบียน")
st.write("อัปโหลดรูปภาพเพื่อวิเคราะห์ข้อมูล")

uploaded_file = st.file_uploader("เลือกไฟล์รูปภาพ...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # แสดงรูปตัวอย่างก่อนประมวลผล
    image = Image.open(uploaded_file)
    st.image(image, caption="รูปภาพที่อัปโหลด", use_container_width=True)
    
    # ปุ่มกดที่ขอบมนตามดีไซน์
    if st.button("วิเคราะห์ป้ายทะเบียน"):
        with st.spinner('กำลังประมวลผลด้วย AI...'):
            results = process_image(image)
            
            if results:
                # รวมข้อความที่อ่านได้ทั้งหมด
                full_text = " ".join([res[1] for res in results])
                
                st.markdown(f"""
                    <div class="result-card">
                        <p style="color: #64748b; font-size: 0.875rem; margin-bottom: 8px;">ผลการตรวจจับ</p>
                        <h1 style="color: #1e293b; margin: 0; font-size: 2rem;">{full_text}</h1>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.error("ไม่พบข้อความในภาพ กรุณาลองใหม่อีกครั้ง")

else:
    st.info("คำแนะนำ: เลือกภาพที่เห็นทะเบียนชัดเจน")