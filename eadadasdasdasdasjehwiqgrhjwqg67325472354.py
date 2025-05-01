import streamlit as st
import google.generativeai as genai
from datetime import datetime, date
import hashlib
import time
from dateutil.relativedelta import relativedelta

# إعدادات التطبيق
LOGO_URL = "https://www2.0zz0.com/2025/04/26/20/375098708.png"

# تهيئة النموذج
genai.configure(api_key=st.secrets["API_KEY"])
model = genai.GenerativeModel('gemini-2.0-flash')

# قاعدة بيانات المستخدمين
if 'users_db' not in st.session_state:
    st.session_state.users_db = {}

# CSS مخصص للتصميم الهادئ
st.markdown("""
<style>
    :root {
        --primary: #2D3748;
        --secondary: #4A5568;
        --accent: #4299E1;
        --light: #F7FAFC;
        --border: #E2E8F0;
    }
    
    .main {
        background-color: #F8F9FA;
    }
    
    .auth-container {
        max-width: 480px;
        margin: 2rem auto;
        padding: 2.5rem;
        background: white;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
        border: 1px solid var(--border);
    }
    
    .logo-container {
        text-align: center;
        margin-bottom: 1.5rem;
    }
    
    .logo-img {
        width: 80px;
        height: auto;
        opacity: 0.9;
    }
    
    .auth-header {
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .auth-header h2 {
        color: var(--primary);
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .auth-header p {
        color: var(--secondary);
        font-size: 0.95rem;
    }
    
    .stTextInput>div>div>input, 
    .stPassword>div>div>input,
    .stDateInput>div>div>input {
        border-radius: 8px;
        border: 1px solid var(--border);
        padding: 10px 12px;
    }
    
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        padding: 12px;
        background-color: var(--primary);
        transition: all 0.2s;
    }
    
    .stButton>button:hover {
        background-color: var(--secondary);
        transform: none;
    }
    
    .auth-footer {
        text-align: center;
        margin-top: 1.5rem;
        color: var(--secondary);
        font-size: 0.9rem;
    }
    
    .auth-footer a {
        color: var(--accent);
        text-decoration: none;
        font-weight: 500;
    }
    
    .error-message {
        color: #E53E3E;
        font-size: 0.9rem;
        margin-top: 0.5rem;
        text-align: center;
    }
    
    .success-message {
        color: #38A169;
        font-size: 0.9rem;
        margin-top: 0.5rem;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

def create_account():
    with st.container():
        st.markdown("""
        <div class="auth-container">
            <div class="logo-container">
                <img src="https://www2.0zz0.com/2025/04/28/19/583882920.png" class="logo-img">
            </div>
            <div class="auth-header">
                <h2>إنشاء حساب جديد</h2>
                <p>ابدأ رحلتك مع LEO Chat</p>
            </div>
        """, unsafe_allow_html=True)
        
        with st.form("register_form"):
            name = st.text_input("الاسم الكامل", placeholder="الاسم الثلاثي")
            email = st.text_input("البريد الإلكتروني", placeholder="example@example.com")
            birth_date = st.date_input("تاريخ الميلاد", min_value=date(1900, 1, 1))
            password = st.text_input("كلمة المرور", type="password", placeholder="8 أحرف على الأقل")
            confirm_password = st.text_input("تأكيد كلمة المرور", type="password", placeholder="أعد إدخال كلمة المرور")
            
            submitted = st.form_submit_button("إنشاء الحساب")
            
            if submitted:
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
                    st.markdown('<p class="success-message">تم إنشاء الحساب بنجاح</p>', unsafe_allow_html=True)
                    time.sleep(1.5)
                    st.session_state.current_page = "login"
                    st.rerun()
        
        st.markdown("""
            <div class="auth-footer">
                لديك حساب بالفعل؟ <a href="#" onclick="window.streamlitApi.setComponentValue('go_to_login')">تسجيل الدخول</a>
            </div>
        </div>
        """, unsafe_allow_html=True)

def login_page():
    with st.container():
        st.markdown("""
        <div class="auth-container">
            <div class="logo-container">
                <img src="https://www2.0zz0.com/2025/04/28/19/583882920.png" class="logo-img">
            </div>
            <div class="auth-header">
                <h2>تسجيل الدخول</h2>
                <p>مرحبًا بعودتك إلى LEO Chat</p>
            </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            email = st.text_input("البريد الإلكتروني", placeholder="example@example.com")
            password = st.text_input("كلمة المرور", type="password", placeholder="أدخل كلمة المرور")
            
            submitted = st.form_submit_button("تسجيل الدخول")
            
            if submitted:
                if email in st.session_state.users_db and \
                        hashlib.sha256(password.encode()).hexdigest() == st.session_state.users_db[email]['password']:
                    st.session_state.logged_in = True
                    st.session_state.current_user = {
                        'email': email,
                        'name': st.session_state.users_db[email]['name']
                    }
                    st.markdown('<p class="success-message">جاري تحويلك...</p>', unsafe_allow_html=True)
                    time.sleep(1)
                    st.rerun()
                else:
                    st.markdown('<p class="error-message">بيانات الدخول غير صحيحة</p>', unsafe_allow_html=True)
        
        st.markdown("""
            <div class="auth-footer">
                ليس لديك حساب؟ <a href="#" onclick="window.streamlitApi.setComponentValue('go_to_register')">إنشاء حساب جديد</a>
            </div>
        </div>
        """, unsafe_allow_html=True)

# باقي الكود كما هو (الجزء الخاص بالداشبورد بعد التسجيل)
# ... [يتبع باقي الكود الأصلي دون تغيير]

if __name__ == "__main__":
    app()
