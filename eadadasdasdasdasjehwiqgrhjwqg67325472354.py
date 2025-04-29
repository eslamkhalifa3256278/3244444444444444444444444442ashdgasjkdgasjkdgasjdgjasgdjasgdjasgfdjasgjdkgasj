mport streamlit as st
import google.generativeai as genai
from datetime import datetime, date
import hashlib
import time
from dateutil.relativedelta import relativedelta
import base64
from PIL import Image
import io

# إعدادات التطبيق
LOGO_URL = "https://www2.0zz0.com/2025/04/26/20/375098708.png"
API_KEY = "AIzaSyAIW5XnFdDZn3sZ6uwRN05hX-KmKy0OaWw"

# تهيئة النموذج
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')
vision_model = genai.GenerativeModel('gemini-pro-vision')

# قاعدة بيانات المستخدمين
if 'users_db' not in st.session_state:
    st.session_state.users_db = {}

# إعداد واجهة المستخدم
def app():
    st.set_page_config(
        page_title="LEO Chat",
        page_icon="https://www2.0zz0.com/2025/04/28/19/583882920.png",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # تحسينات للهاتف المحمول
    st.markdown("""
    <style>
        @media (max-width: 768px) {
            .sidebar .sidebar-content {
                width: 80px !important;
            }
            .main .block-container {
                padding: 1rem;
            }
            .stChatInput {
                bottom: 0;
                position: fixed;
                width: 100%;
                left: 0;
                padding: 0.5rem;
                background: white;
                z-index: 100;
            }
            .stChatMessage {
                max-width: 85%;
            }
        }
        
        /* تحسينات عامة */
        .stTextInput input, .stTextArea textarea, .stPassword input {
            border-radius: 10px !important;
            padding: 10px !important;
        }
        .stButton button {
            border-radius: 10px !important;
            padding: 8px 16px !important;
        }
        .stChatMessage {
            border-radius: 15px !important;
            padding: 12px !important;
            margin: 8px 0 !important;
        }
        .sidebar .sidebar-content {
            background: linear-gradient(180deg, #f8f9fa, #e9ecef);
        }
    </style>
    """, unsafe_allow_html=True)

    # إدارة الملفات
    if "uploaded_files" not in st.session_state:
        st.session_state.uploaded_files = 0
        st.session_state.max_files_per_day = 2
        st.session_state.last_upload_date = None

    # صفحة إنشاء حساب
    def create_account():
        st.markdown("""
        <style>
            .auth-container {
                max-width: 500px;
                margin: 0 auto;
                padding: 2rem;
                border-radius: 15px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                background-color: white;
            }
            .auth-title {
                text-align: center;
                color: #2c3e50;
                margin-bottom: 1.5rem;
            }
        </style>
        """, unsafe_allow_html=True)
        
        with st.container():
            st.markdown('<div class="auth-container">', unsafe_allow_html=True)
            st.markdown('<h2 class="auth-title">إنشاء حساب جديد</h2>', unsafe_allow_html=True)
            
            with st.form("إنشاء حساب جديد"):
                name = st.text_input("الاسم الكامل", placeholder="أدخل اسمك الكامل")
                email = st.text_input("البريد الإلكتروني", placeholder="example@example.com")
                birth_date = st.date_input("تاريخ الميلاد", min_value=date(1900, 1, 1))
                password = st.text_input("كلمة المرور", type="password", placeholder="كلمة مرور قوية")
                confirm_password = st.text_input("تأكيد كلمة المرور", type="password", placeholder="أعد إدخال كلمة المرور")

                if st.form_submit_button("إنشاء الحساب", use_container_width=True):
                    age = relativedelta(date.today(), birth_date).years
                    if age < 18:
                        st.error("يجب أن يكون عمرك 18 عاماً أو أكثر")
                    elif password != confirm_password:
                        st.error("كلمة المرور غير متطابقة")
                    elif email in st.session_state.users_db:
                        st.error("هذا البريد الإلكتروني مسجل بالفعل")
                    else:
                        st.session_state.users_db[email] = {
                            'name': name,
                            'password': hashlib.sha256(password.encode()).hexdigest(),
                            'birth_date': birth_date
                        }
                        st.success("تم إنشاء الحساب بنجاح! يمكنك تسجيل الدخول الآن")
                        time.sleep(2)
                        st.session_state.current_page = "login"
                        st.rerun()
            
            if st.button("العودة لتسجيل الدخول", use_container_width=True):
                st.session_state.current_page = "login"
                st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)

    # صفحة تسجيل الدخول
    def login_page():
        st.markdown("""
        <style>
            .auth-container {
                max-width: 500px;
                margin: 0 auto;
                padding: 2rem;
                border-radius: 15px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                background-color: white;
            }
            .auth-title {
                text-align: center;
                color: #2c3e50;
                margin-bottom: 1.5rem;
            }
            .logo-container {
                text-align: center;
                margin-bottom: 1.5rem;
            }
        </style>
        """, unsafe_allow_html=True)
        
        with st.container():
            st.markdown('<div class="auth-container">', unsafe_allow_html=True)
            st.markdown('<div class="logo-container"><img src="{}" width="150"></div>'.format(LOGO_URL), unsafe_allow_html=True)
            st.markdown('<h2 class="auth-title">تسجيل الدخول</h2>', unsafe_allow_html=True)
            
            with st.form("تسجيل الدخول"):
                email = st.text_input("البريد الإلكتروني", placeholder="أدخل بريدك الإلكتروني")
                password = st.text_input("كلمة المرور", type="password", placeholder="أدخل كلمة المرور")

                if st.form_submit_button("تسجيل الدخول", use_container_width=True):
                    if email in st.session_state.users_db and \
                            hashlib.sha256(password.encode()).hexdigest() == st.session_state.users_db[email]['password']:
                        st.session_state.logged_in = True
                        st.session_state.current_user = {
                            'email': email,
                            'name': st.session_state.users_db[email]['name']
                        }
                        st.success("تم تسجيل الدخول بنجاح!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("بيانات الدخول غير صحيحة")
            
            if st.button("إنشاء حساب جديد", use_container_width=True):
                st.session_state.current_page = "create_account"
                st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)

    # صفحة المعلومات
    def info_page():
        st.title("معلومات عن التطبيق")
        st.markdown("""
        <div style="background-color:#f0f2f6;padding:20px;border-radius:10px;margin-bottom:20px">
            <h3>LEO Chat</h3>
            <p>تم تطوير هذا التطبيق بواسطة <strong>إسلام خليفة</strong></p>
            <p>الجنسية: مصري</p>
            <p>للتواصل: 01028799352</p>
            <p>الإصدار: 1.0</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("العودة للرئيسية", use_container_width=True):
            st.session_state.show_info = False
            st.rerun()

    # دالة لتنزيل الصور
    def get_image_download_link(img_data, filename="image.png"):
        buffered = io.BytesIO()
        img_data.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        href = f'<a href="data:file/png;base64,{img_str}" download="{filename}">تنزيل الصورة</a>'
        return href

    # إدارة الصفحات
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "login" if not st.session_state.users_db else "login"

    # الشريط الجانبي للمستخدم المسجل
    if 'logged_in' in st.session_state and st.session_state.logged_in:
        with st.sidebar:
            st.image(LOGO_URL, width=120)
            st.markdown(f"### مرحباً، {st.session_state.current_user['name']}")
            st.markdown(f"**البريد:** {st.session_state.current_user['email']}")
            
            if st.button("🚪 تسجيل الخروج", type="primary", use_container_width=True):
                st.session_state.logged_in = False
                st.rerun()

            st.markdown("---")

            if st.button("🔄 بدء محادثة جديدة", use_container_width=True):
                st.session_state.messages = []
                st.rerun()

            st.markdown("---")
            st.subheader("آخر المحادثات")

            if "messages" not in st.session_state:
                st.session_state.messages = []

            if not st.session_state.messages:
                st.caption("لا توجد محادثات سابقة")
            else:
                for i, msg in enumerate(reversed(st.session_state.messages[-5:])):
                    if msg["role"] == "user":
                        with st.container(border=True):
                            st.caption(f"المحادثة {len(st.session_state.messages[-5:]) - i}")
                            st.markdown(f"**{msg['content'][:30]}...**")

            st.markdown("---")
            if st.button("ℹ️ معلومات عن التطبيق", use_container_width=True):
                st.session_state.show_info = True
                st.rerun()

    # الصفحة الرئيسية
    if 'logged_in' not in st.session_state or not st.session_state.logged_in:
        if st.session_state.current_page == "login":
            login_page()
        elif st.session_state.current_page == "create_account":
            create_account()
    else:
        if 'show_info' in st.session_state and st.session_state.show_info:
            info_page()
        else:
            # المنطقة الرئيسية
            col1, col2 = st.columns([0.1, 0.9])
            with col1:
                st.image(LOGO_URL, width=60)
            with col2:
                st.title("LEO Chat")

            # تحميل الملفات مع إرسال الرسالة
            if "logged_in" in st.session_state and st.session_state.logged_in:
                uploaded_file = st.file_uploader(
                    "📤 رفع ملف (حد أقصى 2 ملف يومياً)",
                    type=["pdf", "txt", "docx", "png", "jpg", "jpeg"],
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
                        st.success(
                            f"تم رفع الملف بنجاح! ({st.session_state.uploaded_files}/{st.session_state.max_files_per_day})")
                    else:
                        st.warning("لقد تجاوزت الحد اليومي لرفع الملفات")

            # عرض المحادثة
            if "messages" not in st.session_state:
                st.session_state.messages = []

            for message in st.session_state.messages:
                avatar = "https://www2.0zz0.com/2025/04/28/19/583882920.png" if message["role"] == "assistant" else "👤"
                with st.chat_message(message["role"], avatar=avatar):
                    if message["type"] == "text":
                        st.markdown(message["content"])
                    elif message["type"] == "image":
                        st.image(message["content"])
                        if "download_link" in message:
                            st.markdown(message["download_link"], unsafe_allow_html=True)

            # إدخال الرسائل مع إرسال بالضغط على Enter
            if prompt := st.chat_input("اكتب رسالتك هنا..."):
                if "logged_in" not in st.session_state or not st.session_state.logged_in:
                    st.warning("الرجاء تسجيل الدخول لإرسال الرسائل")
                else:
                    # إضافة رسالة المستخدم
                    st.session_state.messages.append({"role": "user", "content": prompt, "type": "text"})

                    # توليد الرد
                    with st.spinner("جارٍ إعداد الرد..."):
                        try:
                            if "اصنع صورة" in prompt or "أنشئ صورة" in prompt or "ارسم صورة" in prompt:
                                response = model.generate_content(prompt + " (أرجو إنشاء صورة)")
                                if hasattr(response, 'images'):
                                    img = response.images[0]
                                    img_bytes = io.BytesIO()
                                    img.save(img_bytes, format='PNG')
                                    img_data = Image.open(io.BytesIO(img_bytes.getvalue()))
                                    
                                    download_link = get_image_download_link(img_data)
                                    st.session_state.messages.append({
                                        "role": "assistant", 
                                        "content": img_data, 
                                        "type": "image",
                                        "download_link": download_link
                                    })
                                else:
                                    reply = response.text
                                    st.session_state.messages.append({"role": "assistant", "content": reply, "type": "text"})
                            else:
                                response = model.generate_content(prompt)
                                reply = response.text
                                st.session_state.messages.append({"role": "assistant", "content": reply, "type": "text"})
                            st.rerun()
                        except Exception as e:
                            st.error(f"حدث خطأ: {str(e)}")

            # تذييل الصفحة
            st.markdown("---")
            st.caption("""
            <div style="text-align: center; font-size: 14px;">
                تم التطوير بواسطة Eslam Khalifa | نموذج LEO AI 1.0
            </div>
            """, unsafe_allow_html=True)


if __name__ == "__main__":
    app()   
