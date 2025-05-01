import streamlit as st
import google.generativeai as genai
from datetime import datetime, date
import hashlib
import time
from dateutil.relativedelta import relativedelta
import firebase_admin
from firebase_admin import credentials, firestore, auth
from firebase_admin.exceptions import FirebaseError
import re
import smtplib
from email.mime.text import MIMEText
import random
import string

# إعدادات التطبيق
LOGO_URL = "https://www2.0zz0.com/2025/04/26/20/375098708.png"
API_KEY = "AIzaSyAIW5XnFdDZn3sZ6uwRN05hX-KmKy0OaWw"

# إعدادات البريد الإلكتروني (لإعادة تعيين كلمة المرور)
EMAIL_CONFIG = {
    'sender': 'your_email@example.com',
    'password': 'your_email_password',
    'smtp_server': 'smtp.example.com',
    'smtp_port': 587
}

# تهيئة النموذج
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

# تهيئة Firebase
FIREBASE_CONFIG = {
    "apiKey": "AIzaSyBFYADCyytqgbSenbgIfOHxvP_4fV_Qais",
    "authDomain": "leoai-924b5.firebaseapp.com",
    "projectId": "leoai-924b5",
    "storageBucket": "leoai-924b5.firebasestorage.app",
    "messagingSenderId": "997032037109",
    "appId": "1:997032037109:web:25a701d30dffe9f8d2d3bc"
}

# إنشاء بيانات الاعتبارات من التكوين
firebase_creds = {
    "type": "service_account",
    "project_id": FIREBASE_CONFIG["projectId"],
    "private_key_id": "YOUR_PRIVATE_KEY_ID",
    "private_key": "-----BEGIN PRIVATE KEY-----\nYOUR_PRIVATE_KEY\n-----END PRIVATE KEY-----\n",
    "client_email": f"firebase-adminsdk-abcdef@{FIREBASE_CONFIG['projectId']}.iam.gserviceaccount.com",
    "client_id": "123456789012345678901",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": f"https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-abcdef%40{FIREBASE_CONFIG['projectId']}.iam.gserviceaccount.com"
}

try:
    if not firebase_admin._apps:
        cred = credentials.Certificate(firebase_creds)
        firebase_admin.initialize_app(cred)
    db = firestore.client()
    auth = auth
except Exception as e:
    st.error(f"فشل في تهيئة Firebase: {str(e)}")

# وظيفة التحقق من صحة البريد الإلكتروني
def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# وظيفة إرسال بريد إلكتروني لإعادة تعيين كلمة المرور
def send_password_reset_email(email, reset_token):
    try:
        reset_link = f"http://your-app-url.com/reset-password?token={reset_token}"
        message = f"""
        مرحباً،
        
        لقد طلبت إعادة تعيين كلمة المرور لحسابك في LEO Chat.
        الرجاء النقر على الرابط التالي لإعادة تعيين كلمة المرور:
        
        {reset_link}
        
        إذا لم تطلب هذا التغيير، يمكنك تجاهل هذا البريد الإلكتروني.
        
        مع تحيات،
        فريق LEO Chat
        """
        
        msg = MIMEText(message)
        msg['Subject'] = 'إعادة تعيين كلمة المرور - LEO Chat'
        msg['From'] = EMAIL_CONFIG['sender']
        msg['To'] = email
        
        with smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port']) as server:
            server.starttls()
            server.login(EMAIL_CONFIG['sender'], EMAIL_CONFIG['password'])
            server.sendmail(EMAIL_CONFIG['sender'], [email], msg.as_string())
        
        return True
    except Exception as e:
        st.error(f"فشل في إرسال البريد الإلكتروني: {str(e)}")
        return False

# وظيفة إنشاء رمز إعادة تعيين
def generate_reset_token():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=32))

# إعداد واجهة المستخدم
def app():
    st.set_page_config(
        page_title="LEO Chat",
        page_icon="https://www2.0zz0.com/2025/04/28/19/583882920.png",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # تحميل حالة "تذكرني" من الجلسة
    if 'remember_me' not in st.session_state:
        st.session_state.remember_me = False

    # إدارة الملفات
    if "uploaded_files" not in st.session_state:
        st.session_state.uploaded_files = 0
        st.session_state.max_files_per_day = 2
        st.session_state.last_upload_date = None
        st.session_state.uploaded_files_list = []

    # صفحة إعادة تعيين كلمة المرور
    def reset_password_page():
        st.title("إعادة تعيين كلمة المرور")
        
        with st.form("reset_password_form"):
            email = st.text_input("البريد الإلكتروني", placeholder="أدخل بريدك الإلكتروني المسجل")
            submit_button = st.form_submit_button("إرسال رابط إعادة التعيين")
            
            if submit_button:
                if not is_valid_email(email):
                    st.error("البريد الإلكتروني غير صحيح")
                else:
                    try:
                        user_ref = db.collection('users').document(email)
                        user_data = user_ref.get()
                        
                        if user_data.exists:
                            reset_token = generate_reset_token()
                            # حفظ الرمز في قاعدة البيانات مع تاريخ انتهاء الصلاحية
                            user_ref.update({
                                'reset_token': reset_token,
                                'reset_token_expiry': datetime.now().timestamp() + 3600  # صلاحية ساعة واحدة
                            })
                            
                            if send_password_reset_email(email, reset_token):
                                st.success("تم إرسال رابط إعادة تعيين كلمة المرور إلى بريدك الإلكتروني")
                                time.sleep(2)
                                st.session_state.current_page = "login"
                                st.rerun()
                        else:
                            st.error("البريد الإلكتروني غير مسجل")
                    except Exception as e:
                        st.error(f"حدث خطأ: {str(e)}")
        
        if st.button("العودة لتسجيل الدخول"):
            st.session_state.current_page = "login"
            st.rerun()

    # صفحة إنشاء حساب (التصميم الجديد)
    def create_account():
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image(LOGO_URL, width=500)
        
        with col2:
            st.markdown("""
            <div style="background-color:#4169E1;padding:30px;border-radius:15px;box-shadow:0 4px 8px rgba(0,0,0,0.1)">
                <h2 style="color:#FFFFFF;text-align:center;margin-bottom:30px">إنشاء حساب جديد</h2>
            """, unsafe_allow_html=True)
            
            with st.form("😎إنشاء حساب جديد"):
                name = st.text_input("الاسم الكامل", placeholder="أدخل اسمك الكامل")
                email = st.text_input("البريد الإلكتروني", placeholder="أدخل بريدك الإلكتروني")
                birth_date = st.date_input("تاريخ الميلاد", min_value=date(1900, 1, 1))
                password = st.text_input("كلمة المرور", type="password", placeholder="أدخل كلمة مرور قوية (5 أحرف على الأقل)")
                confirm_password = st.text_input("تأكيد كلمة المرور", type="password", placeholder="أعد إدخال كلمة المرور")
                
                submit_button = st.form_submit_button("إنشاء الحساب", type="primary")
                
                if submit_button:
                    age = relativedelta(date.today(), birth_date).years
                    if age < 18:
                        st.error("🥺يجب أن يكون عمرك 18 عاماً أو أكثر")
                    elif len(password) < 5:
                        st.error("كلمة المرور يجب أن تحتوي على الأقل على 5 أحرف")
                    elif password != confirm_password:
                        st.error("🤦‍♂️كلمة المرور غير متطابقة")
                    elif not is_valid_email(email):
                        st.error("البريد الإلكتروني غير صحيح")
                    else:
                        try:
                            user_ref = db.collection('users').document(email)
                            if user_ref.get().exists:
                                st.error("🤦‍♂️هذا البريد الإلكتروني مسجل بالفعل")
                            else:
                                user_data = {
                                    'name': name,
                                    'password': hashlib.sha256(password.encode()).hexdigest(),
                                    'birth_date': birth_date.strftime('%Y-%m-%d'),
                                    'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                }
                                user_ref.set(user_data)
                                st.success("☺️تم إنشاء الحساب بنجاح! يمكنك تسجيل الدخول الآن")
                                time.sleep(2)
                                st.session_state.current_page = "login"
                                st.rerun()
                        except Exception as e:
                            st.error(f"حدث خطأ: {str(e)}")
            
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
            
            with st.form("😉تسجيل الدخول"):
                email = st.text_input("البريد الإلكتروني", placeholder="أدخل بريدك الإلكتروني")
                password = st.text_input("كلمة المرور", type="password", placeholder="أدخل كلمة المرور")
                remember_me = st.checkbox("تذكرني", value=st.session_state.remember_me)
                
                submit_button = st.form_submit_button("تسجيل الدخول", type="primary")
                
                if submit_button:
                    if not is_valid_email(email):
                        st.error("البريد الإلكتروني غير صحيح")
                    else:
                        try:
                            user_ref = db.collection('users').document(email)
                            user_data = user_ref.get()
                            
                            if user_data.exists and \
                                    hashlib.sha256(password.encode()).hexdigest() == user_data.to_dict().get('password'):
                                st.session_state.logged_in = True
                                st.session_state.current_user = {
                                    'email': email,
                                    'name': user_data.to_dict().get('name')
                                }
                                st.session_state.remember_me = remember_me
                                st.success("تم تسجيل الدخول بنجاح!☺️")
                                time.sleep(1)
                                st.rerun()
                            else:
                                st.error("بيانات الدخول غير صحيحة")
                        except Exception as e:
                            st.error(f"حدث خطأ: {str(e)}")
            
            st.markdown("""
            </div>
            <div style="text-align:center;margin-top:20px">
                <p style="color:#7f8c8d">ليس لديك حساب يا صديقي/ة!!</p>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("إنشاء حساب جديد", key="go_to_register"):
                    st.session_state.current_page = "create_account"
                    st.rerun()
            with col2:
                if st.button("نسيت كلمة المرور؟", key="forgot_password"):
                    st.session_state.current_page = "reset_password"
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
        st.session_state.current_page = "login"

    # الشريط الجانبي للمستخدم المسجل
    if 'logged_in' in st.session_state and st.session_state.logged_in:
        with st.sidebar:
            st.image(LOGO_URL, width=200)
            st.markdown(f"### مرحباً، {st.session_state.current_user['name']}")
            st.markdown(f"**البريد:** {st.session_state.current_user['email']}")

            if st.button("🚪 تسجيل الخروج", type="primary", help="انقر لتسجيل الخروج"):
                st.session_state.logged_in = False
                st.session_state.remember_me = False
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
        elif st.session_state.current_page == "reset_password":
            reset_password_page()
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

            # تحميل الملفات مع إرسال الرسالة - التصميم الجديد
            if "logged_in" in st.session_state and st.session_state.logged_in:
                # إضافة تنسيقات CSS مخصصة
                st.markdown("""
                <style>
                    .file-upload-container {
                        display: flex;
                        align-items: center;
                        gap: 10px;
                        margin-bottom: 15px;
                    }
                    .file-upload-icon {
                        font-size: 28px;
                        color: #4169E1;
                    }
                    .file-preview-container {
                        display: flex;
                        gap: 8px;
                        margin-top: 5px;
                    }
                    .file-preview-item {
                        width: 32px;
                        height: 32px;
                        border-radius: 4px;
                        background-color: #f0f2f6;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-size: 16px;
                    }
                    .upload-btn {
                        flex-grow: 1;
                    }
                    .footer {
                        position: fixed;
                        bottom: 0;
                        width: 100%;
                        background-color: #f0f2f6;
                        padding: 10px;
                        text-align: center;
                        border-top: 1px solid #ddd;
                    }
                </style>
                """, unsafe_allow_html=True)

                # صف لتحميل الملفات
                st.markdown('<div class="file-upload-container">', unsafe_allow_html=True)
                
                # أيقونة الملفات
                st.markdown('<div class="file-upload-icon">📁</div>', unsafe_allow_html=True)
                
                # زر رفع الملفات
                uploaded_file = st.file_uploader(
                    "رفع ملف (حد أقصى 2 ملف يومياً)",
                    type=["pdf", "txt", "docx", "png", "jpg", "jpeg"],
                    accept_multiple_files=False,
                    key="file_uploader",
                    label_visibility="collapsed"
                )
                
                st.markdown('</div>', unsafe_allow_html=True)

                # عرض معاينة الملفات المرفوعة
                if st.session_state.uploaded_files_list:
                    st.markdown('<div class="file-preview-container">', unsafe_allow_html=True)
                    for file in st.session_state.uploaded_files_list[-2:]:  # عرض آخر ملفين فقط
                        if file.type.startswith('image/'):
                            st.image(file, width=32)
                        else:
                            file_icon = "📄" if file.type == "application/pdf" else \
                                        "📝" if file.type == "text/plain" else \
                                        "📎" if file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document" else "📁"
                            st.markdown(f'<div class="file-preview-item">{file_icon}</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                if uploaded_file:
                    current_date = datetime.now().date()
                    if st.session_state.last_upload_date != current_date:
                        st.session_state.uploaded_files = 0
                        st.session_state.last_upload_date = current_date
                        st.session_state.uploaded_files_list = []

                    if st.session_state.uploaded_files < st.session_state.max_files_per_day:
                        st.session_state.uploaded_files += 1
                        st.session_state.uploaded_files_list.append(uploaded_file)
                        
                        # عرض رسالة نجاح مع أيقونة
                        file_icon = "📄" if uploaded_file.type == "application/pdf" else \
                                    "📝" if uploaded_file.type == "text/plain" else \
                                    "🖼️" if uploaded_file.type.startswith("image/") else "📎"
                        
                        st.success(f"""
                        {file_icon} تم رفع الملف بنجاح: **{uploaded_file.name}**  
                        ({st.session_state.uploaded_files}/{st.session_state.max_files_per_day} - الحد اليومي)
                        """)
                    else:
                        st.warning("""
                        ⚠️ لقد وصلت للحد الأقصى اليومي لرفع الملفات  
                        (2 ملف يومياً في النسخة المجانية)
                        """)

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

            # تذييل الصفحة في الأسفل
            st.markdown("""
            <div style="margin-top: 50px; padding: 15px; background-color: #f0f2f6; border-radius: 8px; text-align: center;">
                <p style="margin: 0; font-size: 14px; color: #555;">
                    تم التطوير بواسطة <strong>إسلام خليفة</strong> | نموذج <strong>Gemini</strong> 1.0
                </p>
            </div>
            """, unsafe_allow_html=True)


if __name__ == "__main__":
    app()
