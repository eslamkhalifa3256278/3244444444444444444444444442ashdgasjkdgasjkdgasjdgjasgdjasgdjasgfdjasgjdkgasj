import streamlit as st
import google.generativeai as genai
from datetime import datetime, date
import hashlib
import time
from dateutil.relativedelta import relativedelta

# إعدادات التطبيق
LOGO_URL = "https://www2.0zz0.com/2025/05/01/22/992228290.png"
LOGIN_LOGO = "https://www2.0zz0.com/2025/05/01/22/314867624.png"

# تهيئة النموذج باستخدام مفتاح API من الـ secrets
genai.configure(api_key=st.secrets["API_KEY"])
model = genai.GenerativeModel('gemini-2.0-flash')

# قاعدة بيانات المستخدمين (مؤقتة)
if 'users_db' not in st.session_state:
    st.session_state.users_db = {}

# CSS مخصص للتصميم الجديد
def load_css():
    st.markdown("""
    <style>
        /* التصميم العام */
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f5f5f5;
            direction: rtl;
        }
        
        /* تصميم حقول الإدخال */
        .stTextInput>div>div>input, 
        .stPassword>div>div>input,
        .stDateInput>div>div>input {
            text-align: right;
            padding: 12px;
            border-radius: 8px;
            border: 1px solid #ddd;
        }
        
        /* تصميم الأزرار */
        .stButton>button {
            width: 100%;
            border-radius: 8px;
            padding: 10px;
            font-weight: bold;
            background-color: #4285F4;
            color: white;
            border: none;
        }
        
        /* تصميم البطاقات */
        .stMarkdown {
            border-radius: 12px;
            padding: 15px;
            background-color: white;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        /* تصميم الشريط الجانبي */
        [data-testid="stSidebar"] {
            background-color: white;
            padding: 20px;
            box-shadow: 2px 0 10px rgba(0,0,0,0.1);
        }
        
        /* تصميم المحادثة */
        [data-testid="chatMessage"] {
            border-radius: 12px;
            padding: 12px;
            margin: 8px 0;
        }
        
        /* تصميم العناوين */
        h1, h2, h3 {
            color: #333;
            text-align: right;
        }
        
        /* تصميم الروابط */
        a {
            color: #4285F4;
            text-decoration: none;
        }
    </style>
    """, unsafe_allow_html=True)

# إعداد واجهة المستخدم
def app():
    st.set_page_config(
        page_title="LEO Chat",
        page_icon=LOGIN_LOGO,
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    load_css()  # تحميل CSS المخصص

    if "uploaded_files" not in st.session_state:
        st.session_state.uploaded_files = 0
        st.session_state.max_files_per_day = 2
        st.session_state.last_upload_date = None

    def create_account():
        st.markdown(f"""
            <div style='text-align:center; margin-bottom: 20px;'>
                <img src="{LOGIN_LOGO}" width="200">
                <h1 style='color:#333;'>LEO.AI</h1>
            </div>
            """, unsafe_allow_html=True)

        with st.form("إنشاء حساب جديد", clear_on_submit=True):
            st.markdown("### إنشاء حساب جديد")
            name = st.text_input("👤 الاسم الكامل")
            email = st.text_input("📧 البريد الإلكتروني")
            birth_date = st.date_input("🎂 تاريخ الميلاد", min_value=date(1900, 1, 1))
            password = st.text_input("🔒 كلمة المرور", type="password")
            confirm_password = st.text_input("✅ تأكيد كلمة المرور", type="password")

            submitted = st.form_submit_button("إنشاء الحساب")
            if submitted:
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

        st.markdown("---")
        st.markdown("أو")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("تسجيل الدخول عبر Google", use_container_width=True):
                st.info("هذه الميزة قيد التطوير")
        with col2:
            if st.button("تسجيل الدخول عبر Microsoft", use_container_width=True):
                st.info("هذه الميزة قيد التطوير")
        st.markdown("---")
        if st.button("لديك حساب بالفعل؟ تسجيل الدخول"):
            st.session_state.current_page = "login"
            st.rerun()

    def login_page():
        st.markdown(f"""
            <div style='text-align:center; margin-bottom: 20px;'>
                <img src="{LOGIN_LOGO}" width="200">
                <h1 style='color:#333;'>LEO.AI</h1>
            </div>
            """, unsafe_allow_html=True)

        with st.form("تسجيل الدخول", clear_on_submit=True):
            email = st.text_input("البريد الإلكتروني")
            password = st.text_input("كلمة المرور", type="password")

            submitted = st.form_submit_button("تسجيل الدخول")
            if submitted:
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

        st.markdown("---")
        st.markdown("أو")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("تسجيل الدخول عبر Google", use_container_width=True):
                st.info("هذه الميزة قيد التطوير")
        with col2:
            if st.button("تسجيل الدخول عبر Microsoft", use_container_width=True):
                st.info("هذه الميزة قيد التطوير")
        st.markdown("---")
        if st.button("ليس لديك حساب؟ إنشاء حساب جديد"):
            st.session_state.current_page = "create_account"
            st.rerun()

    def info_page():
        st.markdown(f"""
            <div style='text-align:center; margin-bottom: 20px;'>
                <img src="{LOGIN_LOGO}" width="200">
                <h1 style='color:#333;'>LEO.AI</h1>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("""
        <div style="background-color:#f0f2f6;padding:20px;border-radius:10px">
            <h3>معلومات عن التطبيق</h3>
            <p>تم تطوير هذا التطبيق بواسطة <strong>إسلام خليفة</strong></p>
            <p>الجنسية: مصري</p>
            <p>للتواصل: 01028799352</p>
            <p>الإصدار: 1.0</p>
        </div>
        """, unsafe_allow_html=True)

    if 'current_page' not in st.session_state:
        st.session_state.current_page = "login"

    if 'logged_in' in st.session_state and st.session_state.logged_in:
        with st.sidebar:
            st.image(LOGO_URL, width=150)
            st.markdown(f"### مرحباً، {st.session_state.current_user['name']}")
            st.markdown(f"**البريد:** {st.session_state.current_user['email']}")

            if st.button("تسجيل الخروج", use_container_width=True):
                st.session_state.logged_in = False
                st.rerun()

            st.markdown("---")
            st.markdown("**المحادثات**")
            
            if st.button("بدء محادثة جديدة", use_container_width=True):
                st.session_state.messages = []
                st.rerun()

            st.markdown("---")
            st.markdown("**آخر المحادثات**")

            if "messages" not in st.session_state:
                st.session_state.messages = []

            if not st.session_state.messages:
                st.markdown("لا توجد محادثات سابقة")
            else:
                for i, msg in enumerate(reversed(st.session_state.messages[-5:])):
                    if msg["role"] == "user":
                        with st.container(border=True):
                            st.markdown(f"**المحادثة {len(st.session_state.messages[-5:]) - i}**")
                            st.markdown(f"{msg['content'][:30]}...")

            st.markdown("---")
            if st.button("معلومات عن التطبيق", use_container_width=True):
                st.session_state.show_info = True
                st.rerun()

    if 'logged_in' not in st.session_state or not st.session_state.logged_in:
        if st.session_state.current_page == "login":
            login_page()
        elif st.session_state.current_page == "create_account":
            create_account()
    else:
        if 'show_info' in st.session_state and st.session_state.show_info:
            info_page()
            if st.button("العودة للرئيسية"):
                st.session_state.show_info = False
                st.rerun()
        else:
            st.markdown(f"""
                <div style='text-align:center; margin-bottom: 20px;'>
                    <img src="{LOGO_URL}" width="100">
                    <h1 style='color:#333;'>LEOAI</h1>
                </div>
                """, unsafe_allow_html=True)

            if "logged_in" in st.session_state and st.session_state.logged_in:
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
                if "logged_in" not in st.session_state or not st.session_state.logged_in:
                    st.warning("الرجاء تسجيل الدخول لإرسال الرسائل")
                else:
                    st.session_state.messages.append({"role": "user", "content": prompt})
                    with st.spinner("جارٍ إعداد الرد..."):
                        try:
                            response = model.generate_content(prompt)
                            reply = response.text
                            st.session_state.messages.append({"role": "assistant", "content": reply})
                            st.rerun()
                        except Exception as e:
                            st.error(f"حدث خطأ: {str(e)}")

            st.markdown("---")
            st.markdown("""
            <div style="text-align: center; font-size: 14px;">
                تم التطوير بواسطة Eslam Khalifa | نموذج LEO AI 1.0
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    app()
