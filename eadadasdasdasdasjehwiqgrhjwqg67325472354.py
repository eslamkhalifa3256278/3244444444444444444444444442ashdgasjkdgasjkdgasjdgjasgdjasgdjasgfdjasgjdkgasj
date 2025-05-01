import streamlit as st
import google.generativeai as genai
from datetime import datetime, date
import hashlib
import time
from dateutil.relativedelta import relativedelta

# إعدادات التطبيق
LOGO_URL = "https://www2.0zz0.com/2025/04/26/20/375098708.png"
BG_IMAGE = "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?q=80&w=2070&auto=format&fit=crop"

# تهيئة النموذج باستخدام مفتاح API من الـ secrets
genai.configure(api_key=st.secrets["API_KEY"])
model = genai.GenerativeModel('gemini-2.0-flash')

# قاعدة بيانات المستخدمين (مؤقتة)
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

    # CSS مخصص للواجهة
    st.markdown(f"""
    <style>
        .main {{
            background-image: url("{BG_IMAGE}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        .auth-container {{
            background-color: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 2rem;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            margin: auto;
            max-width: 500px;
            backdrop-filter: blur(5px);
        }}
        .stButton>button {{
            width: 100%;
            border: none;
            background-color: #4f46e5;
            color: white;
            padding: 0.75rem;
            border-radius: 8px;
            font-weight: 600;
            transition: all 0.3s;
        }}
        .stButton>button:hover {{
            background-color: #4338ca;
            transform: translateY(-2px);
        }}
        .stTextInput>div>div>input, .stPassword>div>div>input, .stDateInput>div>div>input {{
            border-radius: 8px !important;
            padding: 10px !important;
        }}
        .logo-container {{
            text-align: center;
            margin-bottom: 2rem;
        }}
        .logo-img {{
            width: 120px;
            height: auto;
            border-radius: 50%;
            border: 3px solid #4f46e5;
            padding: 5px;
        }}
        .toggle-auth {{
            text-align: center;
            margin-top: 1.5rem;
            color: #6b7280;
        }}
        .toggle-auth a {{
            color: #4f46e5;
            text-decoration: none;
            font-weight: 600;
            cursor: pointer;
        }}
        .header-text {{
            text-align: center;
            margin-bottom: 1.5rem;
            color: #111827;
        }}
        .error-message {{
            color: #ef4444;
            text-align: center;
            margin-top: 1rem;
        }}
        .success-message {{
            color: #10b981;
            text-align: center;
            margin-top: 1rem;
        }}
        [data-testid="stForm"] {{
            border: none !important;
            padding: 0 !important;
        }}
    </style>
    """, unsafe_allow_html=True)

    if "uploaded_files" not in st.session_state:
        st.session_state.uploaded_files = 0
        st.session_state.max_files_per_day = 2
        st.session_state.last_upload_date = None

    def create_account():
        with st.container():
            with st.form("إنشاء حساب جديد"):
                st.markdown("""
                <div class="logo-container">
                    <img src="https://www2.0zz0.com/2025/04/28/19/583882920.png" class="logo-img">
                </div>
                <div class="header-text">
                    <h2>إنشاء حساب جديد</h2>
                    <p>انضم إلى مجتمع LEO Chat اليوم</p>
                </div>
                """, unsafe_allow_html=True)
                
                name = st.text_input("الاسم الكامل", placeholder="أدخل اسمك الكامل")
                email = st.text_input("البريد الإلكتروني", placeholder="أدخل بريدك الإلكتروني")
                birth_date = st.date_input("تاريخ الميلاد", min_value=date(1900, 1, 1))
                password = st.text_input("كلمة المرور", type="password", placeholder="أدخل كلمة المرور")
                confirm_password = st.text_input("تأكيد كلمة المرور", type="password", placeholder="أعد إدخال كلمة المرور")

                submit_button = st.form_submit_button("إنشاء الحساب")
                
                if submit_button:
                    age = relativedelta(date.today(), birth_date).years
                    if age < 18:
                        st.markdown('<p class="error-message">يجب أن يكون عمرك 18 عاماً أو أكثر</p>', unsafe_allow_html=True)
                    elif password != confirm_password:
                        st.markdown('<p class="error-message">كلمة المرور غير متطابقة</p>', unsafe_allow_html=True)
                    elif email in st.session_state.users_db:
                        st.markdown('<p class="error-message">هذا البريد الإلكتروني مسجل بالفعل</p>', unsafe_allow_html=True)
                    else:
                        st.session_state.users_db[email] = {
                            'name': name,
                            'password': hashlib.sha256(password.encode()).hexdigest(),
                            'birth_date': birth_date
                        }
                        st.markdown('<p class="success-message">تم إنشاء الحساب بنجاح! يمكنك تسجيل الدخول الآن</p>', unsafe_allow_html=True)
                        time.sleep(2)
                        st.session_state.current_page = "login"
                        st.rerun()

            st.markdown("""
            <div class="toggle-auth">
                لديك حساب بالفعل؟ <a onclick="window.streamlitApi.setComponentValue('toggle_to_login')">تسجيل الدخول</a>
            </div>
            """, unsafe_allow_html=True)

    def login_page():
        with st.container():
            with st.form("تسجيل الدخول"):
                st.markdown("""
                <div class="logo-container">
                    <img src="https://www2.0zz0.com/2025/04/28/19/583882920.png" class="logo-img">
                </div>
                <div class="header-text">
                    <h2>تسجيل الدخول</h2>
                    <p>مرحبًا بعودتك إلى LEO Chat</p>
                </div>
                """, unsafe_allow_html=True)
                
                email = st.text_input("البريد الإلكتروني", placeholder="أدخل بريدك الإلكتروني")
                password = st.text_input("كلمة المرور", type="password", placeholder="أدخل كلمة المرور")
                
                submit_button = st.form_submit_button("تسجيل الدخول")
                
                if submit_button:
                    if email in st.session_state.users_db and \
                            hashlib.sha256(password.encode()).hexdigest() == st.session_state.users_db[email]['password']:
                        st.session_state.logged_in = True
                        st.session_state.current_user = {
                            'email': email,
                            'name': st.session_state.users_db[email]['name']
                        }
                        st.markdown('<p class="success-message">تم تسجيل الدخول بنجاح!</p>', unsafe_allow_html=True)
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.markdown('<p class="error-message">بيانات الدخول غير صحيحة</p>', unsafe_allow_html=True)

            st.markdown("""
            <div class="toggle-auth">
                ليس لديك حساب؟ <a onclick="window.streamlitApi.setComponentValue('toggle_to_register')">إنشاء حساب جديد</a>
            </div>
            """, unsafe_allow_html=True)

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

    if 'current_page' not in st.session_state:
        st.session_state.current_page = "login"

    if 'logged_in' in st.session_state and st.session_state.logged_in:
        with st.sidebar:
            st.image(LOGO_URL, width=200)
            st.markdown(f"### مرحباً، {st.session_state.current_user['name']}")
            st.markdown(f"**البريد:** {st.session_state.current_user['email']}")

            if st.button("🚪 تسجيل الخروج", type="primary", help="انقر لتسجيل الخروج"):
                st.session_state.logged_in = False
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

    if 'logged_in' not in st.session_state or not st.session_state.logged_in:
        # وضع الصفحة في منتصف الشاشة
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            with st.container():
                st.markdown('<div class="auth-container">', unsafe_allow_html=True)
                
                if st.session_state.current_page == "login":
                    login_page()
                elif st.session_state.current_page == "create_account":
                    create_account()
                
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        if 'show_info' in st.session_state and st.session_state.show_info:
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
                avatar = "https://www2.0zz0.com/2025/04/28/19/583882920.png" if message["role"] == "assistant" else "👤"
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
            st.caption("""
            <div style="text-align: center; font-size: 14px;">
                تم التطوير بواسطة Eslam Khalifa | نموذج LEO AI 1.0
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    app()
