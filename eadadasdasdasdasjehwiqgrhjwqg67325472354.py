import streamlit as st
import google.generativeai as genai
from datetime import datetime, date
import hashlib
import time
from dateutil.relativedelta import relativedelta

# إعدادات التطبيق
LOGO_URL = "https://www2.0zz0.com/2025/04/26/20/375098708.png"
API_KEY = "AIzaSyAIW5XnFdDZn3sZ6uwRN05hX-KmKy0OaWw"

# تهيئة النموذج
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

# قاعدة بيانات المستخدمين (في الواقع يجب أن تكون قاعدة بيانات حقيقية)
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

    # إدارة الملفات
    if "uploaded_files" not in st.session_state:
        st.session_state.uploaded_files = 0
        st.session_state.max_files_per_day = 2
        st.session_state.last_upload_date = None

    # صفحة إنشاء حساب (التصميم الجديد)
    def create_account():
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image(LOGO_URL, width=300)
        
        with col2:
            st.markdown("""
            <div style="background-color:#4169E1;padding:30px;border-radius:15px;box-shadow:0 4px 8px rgba(0,0,0,0.1)">
                <h2 style="color:#FFFFFF;text-align:center;margin-bottom:30px">إنشاء حساب جديد</h2>
            """, unsafe_allow_html=True)
            
            with st.form("إنشاء حساب جديد"):
                name = st.text_input("الاسم الكامل", placeholder="أدخل اسمك الكامل")
                email = st.text_input("البريد الإلكتروني", placeholder="أدخل بريدك الإلكتروني")
                birth_date = st.date_input("تاريخ الميلاد", min_value=date(1900, 1, 1))
                password = st.text_input("كلمة المرور", type="password", placeholder="أدخل كلمة مرور قوية")
                confirm_password = st.text_input("تأكيد كلمة المرور", type="password", placeholder="أعد إدخال كلمة المرور")
                
                submit_button = st.form_submit_button("إنشاء الحساب", type="primary")
                
                if submit_button:
                    age = relativedelta(date.today(), birth_date).years
                    if age < 18:
                        st.error("🥺يجب أن يكون عمرك 18 عاماً أو أكثر")
                    elif password != confirm_password:
                        st.error("🤦‍♂️كلمة المرور غير متطابقة")
                    elif email in st.session_state.users_db:
                        st.error("🤦‍♂️هذا البريد الإلكتروني مسجل بالفعل")
                    else:
                        st.session_state.users_db[email] = {
                            'name': name,
                            'password': hashlib.sha256(password.encode()).hexdigest(),
                            'birth_date': birth_date
                        }
                        st.success("☺️تم إنشاء الحساب بنجاح! يمكنك تسجيل الدخول الآن")
                        time.sleep(2)
                        st.session_state.current_page = "login"
                        st.rerun()
            
            st.markdown("""
            </div>
            <div style="text-align:center;margin-top:20px">
                <p style="color:#7f8c8d">لديك حساب بالفعل؟</p>
            """, unsafe_allow_html=True)
            
            if st.button("العودة لتسجيل الدخول", key="go_to_login"):
                st.session_state.current_page = "login"
                st.rerun()

    # صفحة تسجيل الدخول (التصميم الجديد)
    def login_page():
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image(LOGO_URL, width=500)
        
        with col2:
            st.markdown("""
            <div style="background-color:#4169E1;padding:30px;border-radius:15px;box-shadow:0 4px 8px rgba(0,0,0,0.1)">
                <h2 style="color:#FFFFFF;text-align:center;margin-bottom:30px">تسجيل الدخول</h2>
            """, unsafe_allow_html=True)
            
            with st.form("تسجيل الدخول"):
                email = st.text_input("البريد الإلكتروني", placeholder="أدخل بريدك الإلكتروني")
                password = st.text_input("كلمة المرور", type="password", placeholder="أدخل كلمة المرور")
                
                submit_button = st.form_submit_button("تسجيل الدخول", type="primary")
                
                if submit_button:
                    if email in st.session_state.users_db and \
                            hashlib.sha256(password.encode()).hexdigest() == st.session_state.users_db[email]['password']:
                        st.session_state.logged_in = True
                        st.session_state.current_user = {
                            'email': email,
                            'name': st.session_state.users_db[email]['name']
                        }
                        st.success("تم تسجيل الدخول بنجاح!☺️")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("بيانات الدخول غير صحيحة")
            
            st.markdown("""
            </div>
            <div style="text-align:center;margin-top:20px">
                <p style="color:#7f8c8d">ليس لديك حساب يا صديقي/ة!!</p>
            """, unsafe_allow_html=True)
            
            if st.button("إنشاء حساب جديد", key="go_to_register"):
                st.session_state.current_page = "create_account"
                st.rerun()

    # صفحة المعلومات
    def info_page():
        st.title("معلومات عن التطبيق")
        st.markdown("""
        <div style="background-color:#000000;padding:20px;border-radius:10px">
            <h3>LEO Chat</h3>
            <p>تم تطوير هذا التطبيق بواسطة <strong>إسلام خليفة</strong></p>
            <p>الجنسية: مصري</p>
            <p>للتواصل: 01028799352</p>
            <p>الإصدار: 1.0</p>
        </div>
        """, unsafe_allow_html=True)

    # إدارة الصفحات
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "login" if not st.session_state.users_db else "login"

    # الشريط الجانبي للمستخدم المسجل
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

    # الصفحة الرئيسية
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
            # المنطقة الرئيسية
            col1, col2 = st.columns([0.1, 0.9])
            with col1:
                st.image(LOGO_URL, width=80)
            with col2:
                st.title("LEO Chat")

            # تحميل الملفات مع إرسال الرسالة
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
                        st.warning("لقد تجاوزت الحد اليومي لرفع الملفات للأسف")

            # عرض المحادثة
            if "messages" not in st.session_state:
                st.session_state.messages = []

            for message in st.session_state.messages:
                avatar = "https://www2.0zz0.com/2025/04/28/19/583882920.png" if message["role"] == "assistant" else "👤"
                with st.chat_message(message["role"], avatar=avatar):
                    st.markdown(message["content"])

            # إدخال الرسائل مع إرسال بالضغط على Enter
            if prompt := st.chat_input("اكتب رسالتك هنا..."):
                if "logged_in" not in st.session_state or not st.session_state.logged_in:
                    st.warning("الرجاء تسجيل الدخول لإرسال الرسائل")
                else:
                    # إضافة رسالة المستخدم
                    st.session_state.messages.append({"role": "user", "content": prompt})

                    # توليد الرد
                    with st.spinner("جارٍ إعداد الرد..."):
                        try:
                            response = model.generate_content(prompt)
                            reply = response.text
                            st.session_state.messages.append({"role": "assistant", "content": reply})
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
