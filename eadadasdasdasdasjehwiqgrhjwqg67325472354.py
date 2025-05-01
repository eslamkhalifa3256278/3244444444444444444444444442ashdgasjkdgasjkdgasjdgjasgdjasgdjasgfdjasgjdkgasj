import streamlit as st
import google.generativeai as genai
from datetime import datetime, date
import hashlib
import os
import re
from dateutil.relativedelta import relativedelta
import bcrypt
import sqlite3
from PIL import Image
from io import BytesIO

# Load environment variables (create a .env file for local development)
from dotenv import load_dotenv
load_dotenv()

# App settings
LOGO_URL = "https://www2.0zz0.com/2025/04/26/20/375098708.png"
API_KEY = os.getenv("API_KEY") or "YOUR_API_KEY"  # Replace with your actual API key or use .env

# Initialize the model
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-pro')

# Database setup
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    
    # Create users table
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (email TEXT PRIMARY KEY, 
                  name TEXT NOT NULL, 
                  password_hash TEXT NOT NULL,
                  birth_date TEXT NOT NULL,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    # Create uploaded_files table
    c.execute('''CREATE TABLE IF NOT EXISTS uploaded_files
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_email TEXT NOT NULL,
                  file_name TEXT NOT NULL,
                  file_type TEXT NOT NULL,
                  upload_date TEXT NOT NULL,
                  FOREIGN KEY(user_email) REFERENCES users(email))''')
    
    conn.commit()
    conn.close()

init_db()

# Helper functions
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def get_user_files_count(email, date):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM uploaded_files WHERE user_email = ? AND upload_date = ?", 
              (email, date))
    count = c.fetchone()[0]
    conn.close()
    return count

def save_uploaded_file(email, file):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("INSERT INTO uploaded_files (user_email, file_name, file_type, upload_date) VALUES (?, ?, ?, ?)",
              (email, file.name, file.type, datetime.now().date().isoformat()))
    conn.commit()
    conn.close()

def get_user_files(email, limit=2):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT file_name, file_type FROM uploaded_files WHERE user_email = ? ORDER BY id DESC LIMIT ?", 
              (email, limit))
    files = c.fetchall()
    conn.close()
    return files

# App UI
def app():
    st.set_page_config(
        page_title="LEO Chat",
        page_icon="https://www2.0zz0.com/2025/04/28/19/583882920.png",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Custom CSS
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
            padding: 10px;
            text-align: center;
            border-top: 1px solid #ddd;
        }
        @media (max-width: 768px) {
            .responsive-column {
                flex-direction: column;
            }
        }
    </style>
    """, unsafe_allow_html=True)

    # Page management
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "login"

    # Create account page
    def create_account():
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image(LOGO_URL, width=500)
        
        with col2:
            st.markdown("""
            <div style="background-color:#4169E1;padding:30px;border-radius:15px;box-shadow:0 4px 8px rgba(0,0,0,0.1)">
                <h2 style="color:#FFFFFF;text-align:center;margin-bottom:30px">إنشاء حساب جديد</h2>
            """, unsafe_allow_html=True)
            
            with st.form("create_account_form"):
                name = st.text_input("الاسم الكامل", placeholder="أدخل اسمك الكامل")
                email = st.text_input("البريد الإلكتروني", placeholder="أدخل بريدك الإلكتروني")
                birth_date = st.date_input("تاريخ الميلاد", min_value=date(1900, 1, 1), max_value=date.today())
                password = st.text_input("كلمة المرور", type="password", placeholder="أدخل كلمة مرور قوية (8 أحرف على الأقل)")
                confirm_password = st.text_input("تأكيد كلمة المرور", type="password", placeholder="أعد إدخال كلمة المرور")
                
                submit_button = st.form_submit_button("إنشاء الحساب", type="primary")
                
                if submit_button:
                    # Validation
                    errors = []
                    if len(name.strip()) < 3:
                        errors.append("الاسم يجب أن يكون على الأقل 3 أحرف")
                    if not is_valid_email(email):
                        errors.append("البريد الإلكتروني غير صالح")
                    if len(password) < 8:
                        errors.append("كلمة المرور يجب أن تكون 8 أحرف على الأقل")
                    if password != confirm_password:
                        errors.append("كلمة المرور غير متطابقة")
                    
                    age = relativedelta(date.today(), birth_date).years
                    if age < 18:
                        errors.append("يجب أن يكون عمرك 18 عاماً أو أكثر")
                    
                    # Check if email exists
                    conn = sqlite3.connect('users.db')
                    c = conn.cursor()
                    c.execute("SELECT email FROM users WHERE email = ?", (email,))
                    if c.fetchone():
                        errors.append("هذا البريد الإلكتروني مسجل بالفعل")
                    conn.close()
                    
                    if errors:
                        for error in errors:
                            st.error(error)
                    else:
                        # Save to database
                        conn = sqlite3.connect('users.db')
                        c = conn.cursor()
                        c.execute("INSERT INTO users (email, name, password_hash, birth_date) VALUES (?, ?, ?, ?)",
                                  (email, name.strip(), hash_password(password), birth_date.isoformat()))
                        conn.commit()
                        conn.close()
                        
                        st.success("تم إنشاء الحساب بنجاح! يمكنك تسجيل الدخول الآن")
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

    # Login page
    def login_page():
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image(LOGO_URL, width=500)
        
        with col2:
            st.markdown("""
            <div style="background-color:#4169E1;padding:30px;border-radius:15px;box-shadow:0 4px 8px rgba(0,0,0,0.1)">
                <h2 style="color:#FFFFFF;text-align:center;margin-bottom:30px">تسجيل الدخول</h2>
            """, unsafe_allow_html=True)
            
            with st.form("login_form"):
                email = st.text_input("البريد الإلكتروني", placeholder="أدخل بريدك الإلكتروني")
                password = st.text_input("كلمة المرور", type="password", placeholder="أدخل كلمة المرور")
                
                submit_button = st.form_submit_button("تسجيل الدخول", type="primary")
                
                if submit_button:
                    conn = sqlite3.connect('users.db')
                    c = conn.cursor()
                    c.execute("SELECT email, name, password_hash FROM users WHERE email = ?", (email,))
                    user = c.fetchone()
                    conn.close()
                    
                    if user and verify_password(password, user[2]):
                        st.session_state.logged_in = True
                        st.session_state.current_user = {
                            'email': user[0],
                            'name': user[1]
                        }
                        st.session_state.messages = []
                        st.success("تم تسجيل الدخول بنجاح!")
                        st.rerun()
                    else:
                        st.error("بيانات الدخول غير صحيحة")
            
            st.markdown("""
            </div>
            <div style="text-align:center;margin-top:20px">
                <p style="color:#7f8c8d">ليس لديك حساب؟</p>
            """, unsafe_allow_html=True)
            
            if st.button("إنشاء حساب جديد", key="go_to_register"):
                st.session_state.current_page = "create_account"
                st.rerun()

            # Forgot password link
            st.markdown("""
            <div style="text-align:center;margin-top:10px">
                <a href="#" onclick="alert('سيتم إرسال رابط إعادة تعيين كلمة المرور إلى بريدك الإلكتروني')" style="color:#7f8c8d;text-decoration:none">نسيت كلمة المرور؟</a>
            </div>
            """, unsafe_allow_html=True)

    # Info page
    def info_page():
        st.title("معلومات عن التطبيق")
        st.markdown("""
        <div style="background-color:#f8f9fa;padding:20px;border-radius:10px">
            <h3>LEO Chat</h3>
            <p>تم تطوير هذا التطبيق بواسطة <strong>إسلام خليفة</strong></p>
            <p>الجنسية: مصري</p>
            <p>للتواصل: example@email.com</p>
            <p>الإصدار: 2.0</p>
            <p>تاريخ الإصدار: ١ يناير ٢٠٢٤</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("العودة للرئيسية"):
            st.session_state.show_info = False
            st.rerun()

    # Main chat page
    def chat_page():
        # Header
        col1, col2 = st.columns([0.1, 0.9])
        with col1:
            st.image(LOGO_URL, width=80)
        with col2:
            st.title("LEO Chat")

        # File upload section
        MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
        MAX_FILES_PER_DAY = 2
        
        uploaded_file = st.file_uploader(
            "رفع ملف (PDF, نص, صور) - حد أقصى 2 ملف يومياً بحجم 5MB",
            type=["pdf", "txt", "docx", "png", "jpg", "jpeg"],
            accept_multiple_files=False,
            key="file_uploader"
        )

        # File handling
        if uploaded_file:
            current_date = datetime.now().date().isoformat()
            files_count = get_user_files_count(st.session_state.current_user['email'], current_date)
            
            if files_count >= MAX_FILES_PER_DAY:
                st.warning("""
                ⚠️ لقد وصلت للحد الأقصى اليومي لرفع الملفات  
                (2 ملف يومياً في النسخة المجانية)
                """)
            elif uploaded_file.size > MAX_FILE_SIZE:
                st.warning("حجم الملف كبير جداً (الحد الأقصى 5MB)")
            else:
                save_uploaded_file(st.session_state.current_user['email'], uploaded_file)
                st.toast(f"تم رفع الملف بنجاح: {uploaded_file.name}", icon="✅")

        # Show uploaded files preview
        user_files = get_user_files(st.session_state.current_user['email'])
        if user_files:
            st.markdown('<div class="file-preview-container">', unsafe_allow_html=True)
            for file in user_files:
                file_icon = "📄" if file[1].startswith('application/pdf') else \
                            "📝" if file[1] == "text/plain" else \
                            "🖼️" if file[1].startswith("image/") else "📎"
                st.markdown(f'<div class="file-preview-item" title="{file[0]}">{file_icon}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # Chat messages
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            avatar = "https://www2.0zz0.com/2025/04/28/19/583882920.png" if message["role"] == "assistant" else "👤"
            with st.chat_message(message["role"], avatar=avatar):
                st.markdown(message["content"])

        # Chat input
        if prompt := st.chat_input("اكتب رسالتك هنا..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Generate response
            with st.spinner("جارٍ إعداد الرد..."):
                try:
                    response = model.generate_content(prompt)
                    reply = response.text
                    st.session_state.messages.append({"role": "assistant", "content": reply})
                    st.rerun()
                except Exception as e:
                    st.error(f"حدث خطأ أثناء توليد الرد: {str(e)}")

        # Footer
        st.markdown("""
        <div class="footer">
            <p style="margin: 0; font-size: 14px; color: #555;">
                تم التطوير بواسطة <strong>إسلام خليفة</strong> | نموذج <strong>Gemini 1.5</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Sidebar for logged in users
    if 'logged_in' in st.session_state and st.session_state.logged_in:
        with st.sidebar:
            st.image(LOGO_URL, width=200)
            st.markdown(f"### مرحباً، {st.session_state.current_user['name']}")
            st.markdown(f"**البريد:** {st.session_state.current_user['email']}")

            if st.button("🚪 تسجيل الخروج", type="primary"):
                st.session_state.logged_in = False
                st.session_state.current_user = None
                st.session_state.messages = []
                st.rerun()

            st.markdown("---")

            if st.button("🔄 بدء محادثة جديدة"):
                st.session_state.messages = []
                st.rerun()

            st.markdown("---")
            st.subheader("آخر المحادثات")

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

    # Page routing
    if 'logged_in' not in st.session_state or not st.session_state.logged_in:
        if st.session_state.current_page == "login":
            login_page()
        elif st.session_state.current_page == "create_account":
            create_account()
    else:
        if 'show_info' in st.session_state and st.session_state.show_info:
            info_page()
        else:
            chat_page()

if __name__ == "__main__":
    app()
