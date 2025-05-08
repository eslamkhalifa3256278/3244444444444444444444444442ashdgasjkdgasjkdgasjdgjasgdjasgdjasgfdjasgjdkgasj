import streamlit as st
import google.generativeai as genai
from datetime import datetime, date
import hashlib
import time
from dateutil.relativedelta import relativedelta
import re

# إعدادات التطبيق
LOGO_URL = "https://www2.0zz0.com/2025/05/01/22/992228290.png"
LOGIN_LOGO = "https://www2.0zz0.com/2025/05/01/22/314867624.png"

# الألوان الرئيسية
PRIMARY_COLOR = "#4B6CB7"
SECONDARY_COLOR = "#182848"
BACKGROUND_COLOR = "#F5F7FA"
TEXT_COLOR = "#2D3748"
ACCENT_COLOR = "#FF6B6B"

# تهيئة النموذج
try:
    genai.configure(api_key=st.secrets["API_KEY"])
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    st.error(f"خطأ في تهيئة النموذج: {str(e)}")
    st.stop()

# وظيفة للتحقق من صحة البريد الإلكتروني
def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

# CSS مخصص
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# إعداد واجهة المستخدم
def main():
    st.set_page_config(
        page_title="LEO Chat",
        page_icon=LOGIN_LOGO,
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # تهيئة حالة الجلسة
    if 'users_db' not in st.session_state:
        st.session_state.users_db = {}
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "login"
    if 'show_info' not in st.session_state:
        st.session_state.show_info = False
    if 'uploaded_files' not in st.session_state:
        st.session_state.uploaded_files = 0
        st.session_state.max_files_per_day = 2
        st.session_state.last_upload_date = None
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # CSS مخصص
    st.markdown(f"""
    <style>
        /* التصميم العام */
        .stApp {{
            background-color: {BACKGROUND_COLOR};
        }}
        
        /* أزرار رئيسية */
        .stButton>button {{
            border: 2px solid {PRIMARY_COLOR};
            border-radius: 10px;
            color: white;
            background-color: {PRIMARY_COLOR};
            padding: 8px 16px;
            transition: all 0.3s;
        }}
        
        .stButton>button:hover {{
            background-color: {SECONDARY_COLOR};
            color: white;
            border-color: {SECONDARY_COLOR};
        }}
        
        /* مربعات النص */
        .stTextInput>div>div>input {{
            border-radius: 10px;
            border: 1px solid #ddd;
            padding: 10px;
        }}
        
        /* الشريط الجانبي */
        .css-1d391kg {{
            background-color: {SECONDARY_COLOR};
            color: white;
        }}
        
        /* بطاقات الرسائل */
        .message-card {{
            border-radius: 15px;
            padding: 15px;
            margin: 10px 0;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        
        .user-message {{
            background-color: {PRIMARY_COLOR};
            color: white;
            margin-left: 20%;
        }}
        
        .assistant-message {{
            background-color: #EDF2F7;
            color: {TEXT_COLOR};
            margin-right: 20%;
        }}
        
        /* رأس الصفحة */
        .header {{
            background: linear-gradient(135deg, {PRIMARY_COLOR}, {SECONDARY_COLOR});
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }}
        
        /* تأثيرات للبطاقات */
        .card {{
            transition: transform 0.3s;
        }}
        
        .card:hover {{
            transform: translateY(-5px);
        }}
    </style>
    """, unsafe_allow_html=True)

    def create_account():
        st.markdown(f"""
            <div class='header' style='text-align:center; margin-bottom: 30px;'>
                <img src="{LOGIN_LOGO}" width="200" style='margin-bottom: 20px;'>
                <h2 style='color:white;'>إنشاء حساب جديد</h2>
            </div>
            """, unsafe_allow_html=True)

        with st.form("create_account_form"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("👤 الاسم الكامل", max_chars=50, help="الرجاء إدخال اسمك الكامل")
                email = st.text_input("📧 البريد الإلكتروني", max_chars=100, help="example@example.com")
            with col2:
                birth_date = st.date_input("🎂 تاريخ الميلاد", min_value=date(1900, 1, 1), max_value=date.today())
                password = st.text_input("🔒 كلمة المرور", type="password", min_chars=8, help="8 أحرف على الأقل")
                confirm_password = st.text_input("✅ تأكيد كلمة المرور", type="password")

            st.markdown("---")
            submitted = st.form_submit_button("إنشاء الحساب ✨", 
                                           help="سيتم التحقق من البيانات قبل إنشاء الحساب")
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
                        with st.spinner("جاري إنشاء الحساب..."):
                            st.session_state.users_db[email] = {
                                'name': name.strip(),
                                'password': hashlib.sha256(password.encode()).hexdigest(),
                                'birth_date': birth_date
                            }
                            time.sleep(1.5)
                            st.success("✅ تم إنشاء الحساب بنجاح! يمكنك تسجيل الدخول الآن")
                            time.sleep(1.5)
                            st.session_state.current_page = "login"
                            st.experimental_rerun()

    def login_page():
        st.markdown(f"""
            <div class='header' style='text-align:center; margin-bottom: 30px;'>
                <img src="{LOGIN_LOGO}" width="200" style='margin-bottom: 20px;'>
                <h2 style='color:white;'>تسجيل الدخول</h2>
            </div>
            """, unsafe_allow_html=True)

        with st.form("login_form"):
            email = st.text_input("📧 البريد الإلكتروني", placeholder="أدخل بريدك الإلكتروني")
            password = st.text_input("🔒 كلمة المرور", type="password", placeholder="أدخل كلمة المرور")

            st.markdown("---")
            submitted = st.form_submit_button("تسجيل الدخول ✅", 
                                           help="الرجاء إدخال بيانات الاعتماد الخاصة بك")
            if submitted:
                if not email or not password:
                    st.error("❌ الرجاء إدخال البريد الإلكتروني وكلمة المرور")
                elif email in st.session_state.users_db and \
                        hashlib.sha256(password.encode()).hexdigest() == st.session_state.users_db[email]['password']:
                    with st.spinner("جاري تسجيل الدخول..."):
                        st.session_state.logged_in = True
                        st.session_state.current_user = {
                            'email': email,
                            'name': st.session_state.users_db[email]['name']
                        }
                        st.session_state.messages = []
                        time.sleep(1.5)
                        st.success("✅ تم تسجيل الدخول بنجاح!")
                        time.sleep(1)
                        st.experimental_rerun()
                else:
                    st.error("❌ بيانات الدخول غير صحيحة")

    def info_page():
        st.markdown(f"""
        <div class='header' style='margin-bottom: 30px;'>
            <h2 style='color:white;'>معلومات عن التطبيق</h2>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 3])
        with col1:
            st.image(LOGIN_LOGO, width=200)
        with col2:
            st.markdown(f"""
            <div style="background-color:white;padding:25px;border-radius:15px;box-shadow:0 4px 8px rgba(0,0,0,0.1)">
                <h3 style='color:{PRIMARY_COLOR};'>LEO Chat</h3>
                <p style='font-size:16px;'>تم تطوير هذا التطبيق بواسطة <strong style='color:{SECONDARY_COLOR};'>إسلام خليفة</strong></p>
                <p style='font-size:16px;'><span style='color:{SECONDARY_COLOR};'>الجنسية:</span> مصري</p>
                <p style='font-size:16px;'><span style='color:{SECONDARY_COLOR};'>للتواصل:</span> 01028799352</p>
                <p style='font-size:16px;'><span style='color:{SECONDARY_COLOR};'>الإصدار:</span> 1.0</p>
                <p style='font-size:16px; margin-top:20px;'>هذا التطبيق يستخدم نموذج Gemini Pro للذكاء الاصطناعي من Google</p>
            </div>
            """, unsafe_allow_html=True)

    # الصفحات الرئيسية
    if 'logged_in' in st.session_state and st.session_state.logged_in:
        # الشريط الجانبي
        with st.sidebar:
            st.image(LOGO_URL, width=150)
            st.markdown(f"<h3 style='color:white;'>مرحباً، {st.session_state.current_user['name']}</h3>", unsafe_allow_html=True)
            st.markdown(f"<p style='color:#ccc;'>البريد: {st.session_state.current_user['email']}</p>", unsafe_allow_html=True)

            st.markdown("---")
            
            if st.button("🚪 تسجيل الخروج", type="primary", key="logout_btn", 
                        help="سيتم إغلاق الجلسة الحالية"):
                keys_to_keep = ['users_db', 'current_page']
                for key in list(st.session_state.keys()):
                    if key not in keys_to_keep:
                        del st.session_state[key]
                st.session_state.logged_in = False
                st.session_state.current_page = "login"
                st.experimental_rerun()

            st.markdown("---")
            if st.button("🔄 بدء محادثة جديدة", key="new_chat_btn",
                        help="سيتم مسح سجل المحادثة الحالية"):
                st.session_state.messages = []
                st.experimental_rerun()

            st.markdown("---")
            st.markdown("<h4 style='color:white;'>آخر المحادثات</h4>", unsafe_allow_html=True)

            if not st.session_state.messages:
                st.markdown("<p style='color:#ccc;'>لا توجد محادثات سابقة</p>", unsafe_allow_html=True)
            else:
                for i, msg in enumerate(reversed(st.session_state.messages[-5:])):
                    if msg["role"] == "user":
                        with st.container():
                            st.markdown(f"""
                            <div style='background-color:rgba(255,255,255,0.1);padding:10px;border-radius:10px;margin-bottom:10px;'>
                                <p style='color:#ccc;font-size:12px;margin-bottom:5px;'>المحادثة {len(st.session_state.messages[-5:]) - i}</p>
                                <p style='color:white;'>{msg['content'][:30]}...</p>
                            </div>
                            """, unsafe_allow_html=True)

            st.markdown("---")
            if st.button("ℹ️ معلومات عن التطبيق", key="info_btn",
                       help="عرض معلومات حول التطبيق والمطور"):
                st.session_state.show_info = True
                st.experimental_rerun()

        # المحتوى الرئيسي
        if st.session_state.show_info:
            info_page()
            if st.button("← العودة للرئيسية", key="back_btn"):
                st.session_state.show_info = False
                st.experimental_rerun()
        else:
            # رأس الصفحة
            st.markdown(f"""
            <div style='display:flex;align-items:center;margin-bottom:30px;'>
                <img src='{LOGO_URL}' width='80' style='margin-right:20px;'>
                <div>
                    <h1 style='color:{PRIMARY_COLOR};margin-bottom:0;'>LEO Chat</h1>
                    <p style='color:{TEXT_COLOR};margin-top:0;'>مساعدك الذكي للدردشة والإجابة على الأسئلة</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # رفع الملفات
            with st.expander("📤 رفع ملف (حد أقصى 2 ملف يومياً)", expanded=False):
                uploaded_file = st.file_uploader(
                    "اختر ملف",
                    type=["pdf", "txt", "docx"],
                    accept_multiple_files=False,
                    key="file_uploader",
                    label_visibility="collapsed"
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

            # عرض محادثات الدردشة
            st.markdown("### المحادثة")
            for message in st.session_state.messages:
                if message["role"] == "user":
                    st.markdown(f"""
                    <div class='message-card user-message'>
                        <div style='display:flex;align-items:center;margin-bottom:5px;'>
                            <div style='background-color:white;width:30px;height:30px;border-radius:50%;display:flex;align-items:center;justify-content:center;margin-left:10px;'>
                                <span style='color:{PRIMARY_COLOR};font-weight:bold;'>أنت</span>
                            </div>
                        </div>
                        <div>{message["content"]}</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class='message-card assistant-message'>
                        <div style='display:flex;align-items:center;margin-bottom:5px;'>
                            <img src='{LOGIN_LOGO}' width='30' style='margin-right:10px;border-radius:50%;'>
                            <span style='font-weight:bold;color:{SECONDARY_COLOR};'>LEO</span>
                        </div>
                        <div>{message["content"]}</div>
                    </div>
                    """, unsafe_allow_html=True)

            # إدخال الرسائل
            if prompt := st.chat_input("اكتب رسالتك هنا...", key="chat_input"):
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.spinner("جارٍ إعداد الرد..."):
                    try:
                        response = model.generate_content(prompt)
                        if response.text:
                            st.session_state.messages.append({"role": "assistant", "content": response.text})
                        else:
                            st.error("لم يتم الحصول على رد من النموذج")
                        st.experimental_rerun()
                    except Exception as e:
                        st.error(f"حدث خطأ: {str(e)}")

            # تذييل الصفحة
            st.markdown("---")
            st.markdown(f"""
            <div style="text-align: center; font-size: 14px; color: {TEXT_COLOR};">
                تم التطوير بواسطة <strong style='color:{PRIMARY_COLOR};'>Eslam Khalifa</strong> | نموذج LEO AI 1.0
            </div>
            """, unsafe_allow_html=True)
    else:
        # صفحات تسجيل الدخول وإنشاء الحساب
        if st.session_state.current_page == "login":
            login_page()
            st.markdown("---")
            if st.button("إنشاء حساب جديد", key="create_account_btn",
                       help="إذا كنت مستخدم جديد، يمكنك إنشاء حساب من هنا"):
                st.session_state.current_page = "create_account"
                st.experimental_rerun()
        elif st.session_state.current_page == "create_account":
            create_account()
            st.markdown("---")
            if st.button("← العودة لتسجيل الدخول", key="back_to_login_btn"):
                st.session_state.current_page = "login"
                st.experimental_rerun()

if __name__ == "__main__":
    main()
