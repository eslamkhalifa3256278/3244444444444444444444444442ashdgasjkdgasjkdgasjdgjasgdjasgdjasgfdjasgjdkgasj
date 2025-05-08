import streamlit as st
import google.generativeai as genai
from datetime import datetime, date
import hashlib
import time
from dateutil.relativedelta import relativedelta
import re  # Added for email validation

# إعدادات التطبيق
LOGO_URL = "https://www2.0zz0.com/2025/05/01/22/992228290.png"
LOGIN_LOGO = "https://www2.0zz0.com/2025/05/01/22/314867624.png"

# تهيئة النموذج باستخدام مفتاح API من الـ secrets
try:
    genai.configure(api_key=st.secrets["API_KEY"])
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    st.error(f"فشل في تهيئة نموذج الذكاء الاصطناعي: {str(e)}")
    st.stop()

# قاعدة بيانات المستخدمين (مؤقتة)
if 'users_db' not in st.session_state:
    st.session_state.users_db = {}

# وظيفة للتحقق من صحة البريد الإلكتروني
def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

# إعداد واجهة المستخدم
def app():
    st.set_page_config(
        page_title="LEO Chat",
        page_icon=LOGIN_LOGO,
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Initialize session state variables
    if "uploaded_files" not in st.session_state:
        st.session_state.uploaded_files = 0
        st.session_state.max_files_per_day = 2
        st.session_state.last_upload_date = None
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "login"
    if 'show_info' not in st.session_state:
        st.session_state.show_info = False

    def create_account():
        st.markdown(f"""
            <div style='text-align:center; margin-bottom: 20px;'>
                <img src="{LOGIN_LOGO}" width="300">
                <h2 style='color:#4B4B4B;'>إنشاء حساب جديد</h2>
            </div>
            """, unsafe_allow_html=True)

        with st.form("إنشاء حساب جديد"):
            name = st.text_input("👤 الاسم الكامل", max_chars=50)
            email = st.text_input("📧 البريد الإلكتروني", max_chars=100)
            birth_date = st.date_input("🎂 تاريخ الميلاد", min_value=date(1900, 1, 1), max_value=date.today())
            password = st.text_input("🔒 كلمة المرور", type="password", min_chars=8)
            confirm_password = st.text_input("✅ تأكيد كلمة المرور", type="password")

            submitted = st.form_submit_button("إنشاء الحساب ✨")
            if submitted:
                if not name.strip():
                    st.error("❌ الرجاء إدخال اسم صحيح")
                elif not is_valid_email(email):
                    st.error("❌ البريد الإلكتروني غير صالح")
                else:
                    age = relativedelta(date.today(), birth_date).years
                    if age < 18:
                        st.error("❌ يجب أن يكون عمرك 18 عاماً أو أكثر")
                    elif len(password) < 8:
                        st.error("❌ كلمة المرور يجب أن تكون 8 أحرف على الأقل")
                    elif password != confirm_password:
                        st.error("❌ كلمة المرور غير متطابقة")
                    elif email in st.session_state.users_db:
                        st.error("❌ هذا البريد الإلكتروني مسجل بالفعل")
                    else:
                        st.session_state.users_db[email] = {
                            'name': name.strip(),
                            'password': hashlib.sha256(password.encode()).hexdigest(),
                            'birth_date': birth_date
                        }
                        st.success("✅ تم إنشاء الحساب بنجاح! يمكنك تسجيل الدخول الآن")
                        time.sleep(2)
                        st.session_state.current_page = "login"
                        st.rerun()

    def login_page():
        st.markdown(f"""
            <div style='text-align:center; margin-bottom: 20px;'>
                <img src="{LOGIN_LOGO}" width="300">
                <h2 style='color:#4B4B4B;'>تسجيل الدخول</h2>
            </div>
            """, unsafe_allow_html=True)

        with st.form("تسجيل الدخول"):
            email = st.text_input("📧 البريد الإلكتروني")
            password = st.text_input("🔒 كلمة المرور", type="password")

            submitted = st.form_submit_button("تسجيل الدخول ✅")
            if submitted:
                if not email or not password:
                    st.error("❌ الرجاء إدخال البريد الإلكتروني وكلمة المرور")
                elif email in st.session_state.users_db and \
                        hashlib.sha256(password.encode()).hexdigest() == st.session_state.users_db[email]['password']:
                    st.session_state.logged_in = True
                    st.session_state.current_user = {
                        'email': email,
                        'name': st.session_state.users_db[email]['name']
                    }
                    st.session_state.messages = []  # Reset chat history on new login
                    st.success("✅ تم تسجيل الدخول بنجاح!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ بيانات الدخول غير صحيحة")

    def info_page():
        st.title("معلومات عن التطبيق")
        st.markdown("""
        <div style="background-color:#f0f2f6;padding:20px;border-radius:10px">
            <h3>LEO Chat</h3>
            <p>تم تطوير هذا التطبيق بواسطة <strong>إسلام خليفة</strong></p>
            <p>الجنسية: مصري</p>
            <p>للتواصل: 01028799352</p>
            <p>الإصدار: 1.0</p>
        </div>
        """, unsafe_allow_html=True)

    # Main page routing
    if 'logged_in' in st.session_state and st.session_state.logged_in:
        with st.sidebar:
            st.image(LOGO_URL, width=200)
            st.markdown(f"### مرحباً، {st.session_state.current_user['name']}")
            st.markdown(f"**البريد:** {st.session_state.current_user['email']}")

            if st.button("🚪 تسجيل الخروج", type="primary", help="انقر لتسجيل الخروج"):
                for key in list(st.session_state.keys()):
                    if key not in ['users_db', 'current_page']:
                        del st.session_state[key]
                st.session_state.logged_in = False
                st.session_state.current_page = "login"
                st.rerun()

            st.markdown("---")
            if st.button("🔄 بدء محادثة جديدة"):
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
            if st.button("ℹ️ معلومات عن التطبيق"):
                st.session_state.show_info = True
                st.rerun()

        if st.session_state.show_info:
            info_page()
            if st.button("العودة للرئيسية"):
                st.session_state.show_info = False
                st.rerun()
        else:
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
                    st.success(
                        f"تم رفع الملف بنجاح! ({st.session_state.uploaded_files}/{st.session_state.max_files_per_day})")
                else:
                    st.warning("لقد تجاوزت الحد اليومي لرفع الملفات")

            if "messages" not in st.session_state:
                st.session_state.messages = []

            for message in st.session_state.messages:
                avatar = LOGIN_LOGO if message["role"] == "assistant" else "👤"
                with st.chat_message(message["role"], avatar=avatar):
                    st.markdown(message["content"])

            if prompt := st.chat_input("اكتب رسالتك هنا..."):
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.spinner("جارٍ إعداد الرد..."):
                    try:
                        response = model.generate_content(prompt)
                        if response.text:
                            st.session_state.messages.append({"role": "assistant", "content": response.text})
                        else:
                            st.error("لم يتم الحصول على رد من النموذج")
                        st.rerun()
                    except Exception as e:
                        st.error(f"حدث خطأ: {str(e)}")

            st.markdown("---")
            st.caption("""
            <div style="text-align: center; font-size: 14px;">
                تم التطوير بواسطة Eslam Khalifa | نموذج LEO AI 1.0
            </div>
            """, unsafe_allow_html=True)
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
