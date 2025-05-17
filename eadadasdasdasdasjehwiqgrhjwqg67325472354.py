import streamlit as st
import google.generativeai as genai
from datetime import datetime, date
import hashlib
import time
from dateutil.relativedelta import relativedelta
import base64
import json
import random
import uuid
import os

# إعدادات التطبيق
LOGO_URL = "https://www2.0zz0.com/2025/05/01/22/992228290.png"
LOGIN_LOGO = "https://www2.0zz0.com/2025/05/01/22/314867624.png"

# API Gemini
genai.configure(api_key=st.secrets["API_KEY"])
model = genai.GenerativeModel('gemini-2.0-flash')

# إعداد API توليد الصور
IMAGE_API_KEY = "66f5ddc8-6842-452a-9f6a-189b1f4ce2f2"
IMAGE_API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2"

# قاعدة بيانات المستخدمين
if 'users_db' not in st.session_state:
    st.session_state.users_db = {}

if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

st.set_page_config(page_title="LEO Chat", page_icon=LOGIN_LOGO, layout="wide")

# CSS للوضع الليلي
if st.session_state.dark_mode:
    st.markdown("""
        <style>
            body { background-color: #1E1E1E; color: white; }
            .stButton>button { background-color: #444; color: white; }
        </style>
    """, unsafe_allow_html=True)

# حفظ المحادثة
def save_conversation():
    if 'messages' in st.session_state and st.session_state.messages:
        filename = f"conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(st.session_state.messages, f, ensure_ascii=False, indent=2)
        with open(filename, 'rb') as f:
            b64 = base64.b64encode(f.read()).decode()
            href = f'<a href="data:file/json;base64,{b64}" download="{filename}">📥 تحميل المحادثة</a>'
            st.markdown(href, unsafe_allow_html=True)

def show_confetti():
    st.balloons()
    st.snow()

# توليد صورة من وصف
def generate_image(prompt):
    import requests
    headers = {"Authorization": f"Bearer {IMAGE_API_KEY}"}
    payload = {"inputs": prompt}
    response = requests.post(IMAGE_API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        image_id = str(uuid.uuid4()) + ".png"
        with open(image_id, "wb") as f:
            f.write(response.content)
        return image_id
    else:
        return None

# واجهة الدردشة الخاصة بالصور
def image_chat_interface():
    st.title("🎨 توليد صورة باستخدام الذكاء الاصطناعي")
    prompt = st.text_input("🖌️ اكتب وصف للصورة اللي عايز تولدها:")
    if st.button("🚀 توليد الصورة"):
        if prompt:
            with st.spinner("⏳ جاري إنشاء الصورة..."):
                image_path = generate_image(prompt)
                if image_path:
                    st.image(image_path, caption="✅ تم توليد الصورة")
                    with open(image_path, "rb") as f:
                        b64 = base64.b64encode(f.read()).decode()
                        st.markdown(f"""
                            <a href="data:image/png;base64,{b64}" download="generated_image.png" style="display:inline-block;margin-top:10px;padding:10px 20px;background-color:#4CAF50;color:white;text-decoration:none;border-radius:5px;">
                                ⬇️ تحميل الصورة
                            </a>
                        """, unsafe_allow_html=True)
                else:
                    st.error("❌ يتم تطويرها عزيزي")

# التطبيق الرئيسي
def app():
    if 'uploaded_files' not in st.session_state:
        st.session_state.uploaded_files = 0
        st.session_state.max_files_per_day = 2
        st.session_state.last_upload_date = None

    def create_account():
        st.image(LOGIN_LOGO, width=300)
        st.header("إنشاء حساب جديد")
        with st.form("إنشاء حساب جديد"):
            name = st.text_input("👤 الاسم الكامل")
            email = st.text_input("📧 البريد الإلكتروني")
            birth_date = st.date_input("🎂 تاريخ الميلاد", min_value=date(1900, 1, 1))
            password = st.text_input("🔒 كلمة المرور", type="password")
            confirm_password = st.text_input("✅ تأكيد كلمة المرور", type="password")
            submitted = st.form_submit_button("إنشاء الحساب ✨")
            if submitted:
                age = relativedelta(date.today(), birth_date).years
                if age < 18:
                    st.error("❌ يجب أن يكون عمرك 18 عاماً أو أكثر")
                elif password != confirm_password:
                    st.error("❌ كلمة المرور غير متطابقة")
                elif email in st.session_state.users_db:
                    st.error("❌ هذا البريد الإلكتروني مسجل بالفعل")
                else:
                    st.session_state.users_db[email] = {
                        'name': name,
                        'password': hashlib.sha256(password.encode()).hexdigest(),
                        'birth_date': birth_date
                    }
                    st.success("✅ تم إنشاء الحساب بنجاح!")
                    show_confetti()
                    time.sleep(2)
                    st.session_state.current_page = "login"
                    st.rerun()

    def login_page():
        st.image(LOGIN_LOGO, width=300)
        st.header("تسجيل الدخول")
        with st.form("تسجيل الدخول"):
            email = st.text_input("📧 البريد الإلكتروني")
            password = st.text_input("🔒 كلمة المرور", type="password")
            submitted = st.form_submit_button("تسجيل الدخول ✅")
            if submitted:
                if email in st.session_state.users_db and \
                        hashlib.sha256(password.encode()).hexdigest() == st.session_state.users_db[email]['password']:
                    st.session_state.logged_in = True
                    st.session_state.current_user = {
                        'email': email,
                        'name': st.session_state.users_db[email]['name']
                    }
                    st.success("✅ تم تسجيل الدخول بنجاح!")
                    show_confetti()
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ بيانات الدخول غير صحيحة")

    if 'current_page' not in st.session_state:
        st.session_state.current_page = "login"

    if 'logged_in' in st.session_state and st.session_state.logged_in:
        with st.sidebar:
            st.image(LOGO_URL, width=200)
            st.markdown(f"### مرحباً، {st.session_state.current_user['name']}")
            st.markdown(f"**البريد:** {st.session_state.current_user['email']}")
            if st.button("🚪 تسجيل الخروج"):
                st.session_state.logged_in = False
                st.rerun()
            st.markdown("---")
            if st.button("💬 دردشة نصية"):
                st.session_state.chat_mode = "text"
                st.rerun()
            if st.button("🖼️ توليد صورة"):
                st.session_state.chat_mode = "image"
                st.rerun()
            st.markdown("---")
            st.button("🌗 تبديل الوضع الليلي", on_click=lambda: st.session_state.update({"dark_mode": not st.session_state.dark_mode}))
            st.markdown("---")

        if 'chat_mode' not in st.session_state:
            st.session_state.chat_mode = "text"

        if st.session_state.chat_mode == "image":
            image_chat_interface()
        else:
            st.title("LEO Chat")
            if "messages" not in st.session_state:
                st.session_state.messages = []
            for message in st.session_state.messages:
                avatar = LOGIN_LOGO if message["role"] == "assistant" else "👤"
                with st.chat_message(message["role"], avatar=avatar):
                    st.markdown(message["content"])
            if prompt := st.chat_input("اكتب رسالتك هنا..."):
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                st.session_state.messages.append({"role": "user", "content": prompt, "time": now})
                with st.spinner("🤖جارى الرد ..."):
                    try:
                        response = model.generate_content(prompt)
                        reply = response.text
                        time.sleep(random.uniform(1, 2))
                        st.session_state.messages.append({"role": "assistant", "content": reply, "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
                        st.rerun()
                    except Exception as e:
                        st.error(f"حدث خطأ: {str(e)}")
    else:
        if st.session_state.current_page == "login":
            login_page()
            if st.button("إنشاء حساب جديد"):
                st.session_state.current_page = "create_account"
                st.rerun()
        elif st.session_state.current_page == "create_account":
            create_account()
            if st.button("العودة لتسجيل الدخول"):
                st.session_state.current_page = "login"
                st.rerun()

if __name__ == "__main__":
    app()
