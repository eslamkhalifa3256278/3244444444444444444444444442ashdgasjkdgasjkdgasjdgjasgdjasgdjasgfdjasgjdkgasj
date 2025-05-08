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

# إعداد واجهة المستخدم
def app():
    st.set_page_config(
        page_title="LEO Chat",
        page_icon=LOGIN_LOGO,
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # إعداد الجلسات الأولية
    if "theme" not in st.session_state:
        st.session_state.theme = "light"

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "uploaded_files" not in st.session_state:
        st.session_state.uploaded_files = 0
        st.session_state.max_files_per_day = 2
        st.session_state.last_upload_date = None

    if "current_page" not in st.session_state:
        st.session_state.current_page = "login"

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if "show_info" not in st.session_state:
        st.session_state.show_info = False

    def create_account():
        st.markdown(f"""
            <div style='text-align:center; margin-bottom: 20px;'>
                <img src="{LOGIN_LOGO}" width="300">
                <h2 style='color:#4B4B4B;'>إنشاء حساب جديد</h2>
            </div>
            """, unsafe_allow_html=True)

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
                if email in st.session_state.users_db and \
                        hashlib.sha256(password.encode()).hexdigest() == st.session_state.users_db[email]['password']:
                    st.session_state.logged_in = True
                    st.session_state.current_user = {
                        'email': email,
                        'name': st.session_state.users_db[email]['name']
                    }
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

    if not st.session_state.logged_in:
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
    else:
        # الوضع الليلي / النهاري
        theme_option = st.sidebar.selectbox("🎨 اختر الوضع", ["light", "dark"])
        st.session_state.theme = theme_option

        bg_color = "#0e1117" if theme_option == "dark" else "#FFFFFF"
        text_color = "#FAFAFA" if theme_option == "dark" else "#000000"

        with st.sidebar:
            st.image(LOGO_URL, width=200)
            st.markdown(f"### مرحباً، {st.session_state.current_user['name']}")
            st.markdown(f"**📧 البريد:** {st.session_state.current_user['email']}")
            st.markdown(f"**📁 عدد الملفات المرفوعة اليوم:** {st.session_state.uploaded_files}/2")
            st.markdown(f"**💬 عدد الرسائل:** {len(st.session_state.messages)}")
            if st.button("🚪 تسجيل الخروج"):
                st.session_state.logged_in = False
                st.rerun()
            if st.button("🧹 مسح المحادثة"):
                st.session_state.messages = []
                st.success("✅ تم مسح المحادثة")
                time.sleep(1)
                st.rerun()
            if st.button("ℹ️ معلومات عن التطبيق"):
                st.session_state.show_info = True
                st.rerun()

        if st.session_state.show_info:
            info_page()
            if st.button("⬅️ العودة"):
                st.session_state.show_info = False
                st.rerun()
        else:
            st.markdown(f"""
            <div style='background-color:{bg_color}; color:{text_color}; padding: 15px; border-radius: 10px;'>
                <h2 style='margin:0;'>LEO Chat 🤖</h2>
            </div>
            """, unsafe_allow_html=True)

            uploaded_file = st.file_uploader(
                "📤 رفع ملف (حد أقصى 2 ملف يومياً)",
                type=["pdf", "txt", "docx"],
                accept_multiple_files=False
            )
            if uploaded_file:
                current_date = datetime.now().date()
                if st.session_state.last_upload_date != current_date:
                    st.session_state.uploaded_files = 0
                    st.session_state.last_upload_date = current_date

                if st.session_state.uploaded_files < st.session_state.max_files_per_day:
                    st.session_state.uploaded_files += 1
                    st.success("✅ تم رفع الملف بنجاح")
                else:
                    st.warning("⚠️ لقد تجاوزت الحد اليومي لرفع الملفات")

            for message in st.session_state.messages:
                avatar = LOGIN_LOGO if message["role"] == "assistant" else "👤"
                with st.chat_message(message["role"], avatar=avatar):
                    st.markdown(message["content"])

            prompt = st.chat_input("اكتب رسالتك هنا...")
            if prompt:
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.spinner("جاري تجهيز الرد..."):
                    try:
                        response = model.generate_content(prompt)
                        reply = response.text
                        st.session_state.messages.append({"role": "assistant", "content": reply})
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ حدث خطأ: {e}")

            st.markdown("""
            <hr style='border-top: 1px solid #ccc;'>
            <div style="text-align: center; font-size: 14px;">
                تم التطوير بواسطة Eslam Khalifa | نموذج LEO AI 1.0
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    app()
