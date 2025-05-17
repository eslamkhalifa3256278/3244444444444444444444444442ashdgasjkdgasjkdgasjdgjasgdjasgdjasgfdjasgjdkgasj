# Create the final full code as a .py file including the latest image generation chat feature
final_code = """
import streamlit as st
import google.generativeai as genai
from datetime import datetime, date
import hashlib
import time
from dateutil.relativedelta import relativedelta
import base64
import json
import random

# إعدادات التطبيق
LOGO_URL = "https://www2.0zz0.com/2025/05/01/22/992228290.png"
LOGIN_LOGO = "https://www2.0zz0.com/2025/05/01/22/314867624.png"

# تهيئة النموذج باستخدام مفتاح API
genai.configure(api_key="66f5ddc8-6842-452a-9f6a-189b1f4ce2f2")
model = genai.GenerativeModel('gemini-2.0-flash')

if 'users_db' not in st.session_state:
    st.session_state.users_db = {}

if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

if 'image_generation' not in st.session_state:
    st.session_state.image_generation = False

st.set_page_config(
    page_title="LEO Chat",
    page_icon=LOGIN_LOGO,
    layout="wide"
)

if st.session_state.dark_mode:
    st.markdown(\"""
        <style>
            body {
                background-color: #1E1E1E;
                color: white;
            }
            .stButton>button {
                background-color: #444;
                color: white;
            }
        </style>
    \""", unsafe_allow_html=True)

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

def image_generation_page():
    st.title("🎨 إنشاء صورة باستخدام الذكاء الاصطناعي")
    prompt = st.chat_input("🖼️ اكتب وصف الصورة اللي عايز تولدها:")

    if prompt:
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            with st.spinner("⏳ جاري توليد الصورة..."):
                try:
                    image_url = f"https://image.pollinations.ai/prompt/{prompt.replace(' ', '%20')}"
                    st.image(image_url, caption="📷 الصورة اللي تم توليدها")

                    btn = f"""
                        <a href="{image_url}" download="generated_image.png">
                            <button style="background-color:#4CAF50;color:white;padding:10px 20px;border:none;border-radius:5px;cursor:pointer;margin-top:10px;">
                                ⬇️ تحميل الصورة
                            </button>
                        </a>
                    """
                    st.markdown(btn, unsafe_allow_html=True)

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": f"📷 تم إنشاء صورة بناءً على وصفك: **{prompt}**\\n\\n![Generated Image]({image_url})",
                        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                except Exception as e:
                    st.error(f"❌ حصل خطأ أثناء توليد الصورة: {str(e)}")

def app():
    if "uploaded_files" not in st.session_state:
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
                    st.success("✅ تم إنشاء الحساب بنجاح! يمكنك تسجيل الدخول الآن")
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

    def info_page():
        st.title("معلومات عن التطبيق")
        st.markdown(\"""
            <div style="background-color:#f0f2f6;padding:20px;border-radius:10px">
                <h3>LEO Chat</h3>
                <p>تم تطوير هذا التطبيق بواسطة <strong>إسلام خليفة</strong></p>
                <p>الجنسية: مصري</p>
                <p>للتواصل: 01028799352</p>
                <p>الإصدار: 1.0</p>
            </div>
        \""", unsafe_allow_html=True)

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
            if st.button("🔄 بدء محادثة جديدة"):
                st.session_state.messages = []
                st.rerun()

            if st.button("🗑️ حذف المحادثة"):
                st.session_state.messages = []
                st.success("✅ تم حذف المحادثة")
                st.rerun()

            if st.button("💾 حفظ المحادثة"):
                save_conversation()

            if st.button("🌗 تبديل الوضع الليلي"):
                st.session_state.dark_mode = not st.session_state.dark_mode
                st.rerun()

            if st.button("🖼️ إنشاء صور"):
                st.session_state.image_generation = True
                st.rerun()

            if st.button("ℹ️ معلومات عن التطبيق"):
                st.session_state.show_info = True
                st.rerun()

            st.subheader("📊 إحصائيات")
            st.markdown(f"- عدد الرسائل: {len(st.session_state.get('messages', []))}")
            st.markdown(f"- عدد الملفات المرفوعة: {st.session_state.uploaded_files}/{st.session_state.max_files_per_day}")

        if st.session_state.image_generation:
            image_generation_page()
        else:
            today = datetime.now().date()
            if 'last_welcome_date' not in st.session_state or st.session_state.last_welcome_date != today:
                st.info(f"👋 صباح الخير يا {st.session_state.current_user['name']}! أتمنى لك يوم سعيد ومثمر 😄")
                st.session_state.last_welcome_date = today

            col1, col2 = st.columns([0.1, 0.9])
            with col1:
                st.image(LOGO_URL, width=80)
            with col2:
                st.title("LEO Chat")

            uploaded_file = st.file_uploader(
                "📤 رفع ملف (حد أقصى 2 ملف يومياً)",
                type=["pdf", "txt", "docx"],
                accept_multiple_files=False,
                key="file_uploader"
            )

            if uploaded_file:
                current_date = datetime.now().date()
                if st.session_state.last_upload_date != current_date:
                    st.session_state.uploaded_files = 0
                    st.session_state.last_upload_date = current_date

                if st.session_state.uploaded_files < st.session_state.max_files_per_day:
                    st.session_state.uploaded_files += 1
                    st.success(f"تم رفع الملف بنجاح! ({st.session_state.uploaded_files}/{st.session_state.max_files_per_day})")
                else:
                    st.warning("لقد تجاوزت الحد اليومي لرفع الملفات")

            if "messages" not in st.session_state:
                st.session_state.messages = []

            for message in st.session_state.messages:
                avatar = LOGIN_LOGO if message["role"] == "assistant" else "👤"
                with st.chat_message(message["role"], avatar=avatar):
                    st.markdown(message["content"])
                    if "time" in message:
                        st.caption(f"🕒 {message['time']}")

            if prompt := st.chat_input("اكتب رسالتك هنا..."):
                if "logged_in" not in st.session_state or not st.session_state.logged_in:
                    st.warning("الرجاء تسجيل الدخول لإرسال الرسائل")
                else:
                    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    st.session_state.messages.append({"role": "user", "content": prompt, "time": now})
                    with st.spinner("🤖 بيكتبلك الرد..."):
                        try:
                            response = model.generate_content(prompt)
                            reply = response.text
                            time.sleep(random.uniform(1, 2))
                            st.session_state.messages.append({"role": "assistant", "content": reply, "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
                            st.rerun()
                        except Exception as e:
                            st.error(f"حدث خطأ: {str(e)}")

            st.markdown("---")
            st.caption("تم التطوير بواسطة Eslam Khalifa | نموذج LEO AI 1.0", unsafe_allow_html=True)

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
        elif 'show_info' in st.session_state and st.session_state.show_info:
            info_page()
            if st.button("العودة للرئيسية"):
                st.session_state.show_info = False
                st.rerun()

if __name__ == "__main__":
    app()
"""

# Save code to a file
with open("/mnt/data/leo_chat_final.py", "w", encoding="utf-8") as f:
    f.write(final_code)

"/mnt/data/leo_chat_final.py"

