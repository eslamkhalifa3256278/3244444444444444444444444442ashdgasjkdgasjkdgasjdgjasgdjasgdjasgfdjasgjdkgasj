# LEO Chat - Mobile Friendly Version with Enhanced Features
import streamlit as st
import google.generativeai as genai
from datetime import datetime, date
import hashlib
import time
from dateutil.relativedelta import relativedelta
import base64

# إعدادات التطبيق
LOGO_URL = "https://www2.0zz0.com/2025/04/26/20/375098708.png"
API_KEY = st.secrets[""AIzaSyAIW5XnFdDZn3sZ6uwRN05hX-KmKy0OaW"]

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.0-vision-pro')

if 'users_db' not in st.session_state:
    st.session_state.users_db = {}

if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'current_page' not in st.session_state:
    st.session_state.current_page = "login"

def app():
    st.set_page_config(page_title="LEO Chat", layout="wide")

    with st.container():
        st.markdown("""
        <style>
        body, html, .main, .block-container {
            padding: 0;
            margin: 0;
        }
        .css-18e3th9 {
            padding-top: 1rem;
        }
        .chat-container {
            background-color: #f0f2f6;
            padding: 10px;
            border-radius: 10px;
        }
        .login-box {
            max-width: 400px;
            margin: auto;
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        }
        .login-title {
            text-align: center;
            margin-bottom: 1rem;
            font-size: 24px;
        }
        .download-btn {
            background-color: #2e8b57;
            color: white;
            padding: 5px 10px;
            border-radius: 5px;
            text-decoration: none;
            font-size: 13px;
        }
        </style>
        """, unsafe_allow_html=True)

    if 'logged_in' not in st.session_state:
        if st.session_state.current_page == "login":
            with st.container():
                with st.form("login", clear_on_submit=False):
                    st.markdown("""<div class="login-box">
                    <h2 class="login-title">تسجيل الدخول إلى LEO Chat</h2>""", unsafe_allow_html=True)
                    email = st.text_input("📧 البريد الإلكتروني")
                    password = st.text_input("🔒 كلمة المرور", type="password")
                    submitted = st.form_submit_button("تسجيل الدخول")
                    st.markdown("</div>", unsafe_allow_html=True)

                    if submitted:
                        if email in st.session_state.users_db and \
                                hashlib.sha256(password.encode()).hexdigest() == st.session_state.users_db[email]['password']:
                            st.session_state.logged_in = True
                            st.session_state.current_user = {'email': email, 'name': st.session_state.users_db[email]['name']}
                            st.success("تم تسجيل الدخول بنجاح!")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error("بيانات الدخول غير صحيحة")
            if st.button("إنشاء حساب جديد"):
                st.session_state.current_page = "create_account"
                st.rerun()

        elif st.session_state.current_page == "create_account":
            with st.form("signup"):
                st.markdown("""<div class="login-box">
                <h2 class="login-title">إنشاء حساب</h2>""", unsafe_allow_html=True)
                name = st.text_input("👤 الاسم الكامل")
                email = st.text_input("📧 البريد الإلكتروني")
                birth_date = st.date_input("🎂 تاريخ الميلاد")
                password = st.text_input("🔑 كلمة المرور", type="password")
                confirm_password = st.text_input("✅ تأكيد كلمة المرور", type="password")
                create = st.form_submit_button("إنشاء")
                st.markdown("</div>", unsafe_allow_html=True)

                if create:
                    if password != confirm_password:
                        st.error("كلمة المرور غير متطابقة")
                    elif email in st.session_state.users_db:
                        st.error("البريد الإلكتروني مستخدم بالفعل")
                    else:
                        st.session_state.users_db[email] = {
                            'name': name,
                            'password': hashlib.sha256(password.encode()).hexdigest(),
                            'birth_date': birth_date
                        }
                        st.success("تم إنشاء الحساب بنجاح!")
                        time.sleep(1)
                        st.session_state.current_page = "login"
                        st.rerun()
            if st.button("⬅️ العودة"):
                st.session_state.current_page = "login"
                st.rerun()

    else:
        with st.sidebar:
            st.image(LOGO_URL, width=150)
            st.markdown(f"### 👋 مرحباً، {st.session_state.current_user['name']}")
            if st.button("🚪 تسجيل الخروج"):
                st.session_state.logged_in = False
                st.session_state.current_page = "login"
                st.rerun()
            st.markdown("---")

        st.title("💬 LEO Chat - المحادثة الذكية")
        prompt = st.chat_input("اكتب هنا...")

        if prompt:
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.spinner("يتم المعالجة..."):
                try:
                    response = model.generate_content(prompt)
                    reply = response.text

                    # لو الرد فيه صورة
                    if hasattr(response, 'parts'):
                        for part in response.parts:
                            if hasattr(part, 'inline_data') and hasattr(part.inline_data, 'mime_type'):
                                b64_img = base64.b64encode(part.inline_data.data).decode()
                                reply = f'![تم إنشاء صورة](data:{part.inline_data.mime_type};base64,{b64_img})'
                                reply += f"\n\n[📥 تحميل الصورة](data:{part.inline_data.mime_type};base64,{b64_img})"

                    st.session_state.messages.append({"role": "assistant", "content": reply})
                    st.rerun()
                except Exception as e:
                    st.error("حدث خطأ: " + str(e))

        for message in st.session_state.messages:
            avatar = "https://www2.0zz0.com/2025/04/28/19/583882920.png" if message["role"] == "assistant" else "👤"
            with st.chat_message(message["role"], avatar=avatar):
                st.markdown(message["content"], unsafe_allow_html=True)

if __name__ == '__main__':
    app()
