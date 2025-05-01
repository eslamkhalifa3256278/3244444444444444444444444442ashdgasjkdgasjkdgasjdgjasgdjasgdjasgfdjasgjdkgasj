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

# CSS مخصص للتصميم
st.markdown("""
<style>
    :root {
        --primary-light: #6366F1;
        --primary-dark: #4F46E5;
        --secondary-light: #A5B4FC;
        --secondary-dark: #818CF8;
        --text-dark: #1F2937;
        --text-light: #6B7280;
        --bg-light: #F9FAFB;
        --border-light: #E5E7EB;
    }
    
    .main {
        background-color: var(--bg-light);
    }
    
    .auth-container {
        max-width: 420px;
        margin: 3rem auto;
        padding: 2rem;
        background: white;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        border: 1px solid var(--border-light);
    }
    
    .logo-header {
        text-align: center;
        margin-bottom: 1.5rem;
    }
    
    .logo-img {
        width: 70px;
        height: auto;
        opacity: 0.95;
    }
    
    .auth-title {
        text-align: center;
        margin-bottom: 1.5rem;
        background: linear-gradient(135deg, var(--primary-light), var(--primary-dark));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 600;
        font-size: 1.8rem;
    }
    
    .auth-subtitle {
        text-align: center;
        color: var(--text-light);
        font-size: 0.95rem;
        margin-bottom: 1.5rem;
    }
    
    .stTextInput>div>div>input, 
    .stPassword>div>div>input,
    .stDateInput>div>div>input {
        border-radius: 8px;
        border: 1px solid var(--border-light);
        padding: 10px 12px;
    }
    
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        padding: 0.75rem;
        background: linear-gradient(135deg, var(--primary-light), var(--primary-dark));
        color: white;
        font-weight: 500;
        border: none;
        transition: all 0.2s;
    }
    
    .stButton>button:hover {
        opacity: 0.9;
        transform: translateY(-1px);
    }
    
    .auth-toggle {
        text-align: center;
        margin-top: 1.5rem;
        color: var(--text-light);
        font-size: 0.9rem;
    }
    
    .auth-toggle a {
        color: var(--primary-dark);
        font-weight: 500;
        text-decoration: none;
        cursor: pointer;
    }
    
    .error-msg {
        color: #EF4444;
        font-size: 0.85rem;
        text-align: center;
        margin-top: 0.5rem;
    }
    
    .success-msg {
        color: #10B981;
        font-size: 0.85rem;
        text-align: center;
        margin-top: 0.5rem;
    }
    
    [data-testid="stForm"] {
        border: none !important;
        padding: 0 !important;
    }
</style>
""", unsafe_allow_html=True)

def auth_section():
    """جزء المصادقة في صفحة واحدة"""
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="auth-container">', unsafe_allow_html=True)
        
        # شعار التطبيق
        st.markdown("""
        <div class="logo-header">
            <img src="https://www2.0zz0.com/2025/04/28/19/583882920.png" class="logo-img">
        </div>
        """, unsafe_allow_html=True)
        
        # التحويل بين تسجيل الدخول وإنشاء حساب
        if st.session_state.get('show_register', False):
            # نموذج إنشاء حساب
            st.markdown('<h2 class="auth-title">إنشاء حساب جديد</h2>', unsafe_allow_html=True)
            st.markdown('<p class="auth-subtitle">املأ البيانات لإنشاء حسابك</p>', unsafe_allow_html=True)
            
            with st.form("register_form"):
                name = st.text_input("الاسم الكامل", placeholder="أدخل اسمك الكامل")
                email = st.text_input("البريد الإلكتروني", placeholder="example@example.com")
                birth_date = st.date_input("تاريخ الميلاد", min_value=date(1900, 1, 1))
                password = st.text_input("كلمة المرور", type="password", placeholder="8 أحرف على الأقل")
                confirm_password = st.text_input("تأكيد كلمة المرور", type="password", placeholder="أعد إدخال كلمة المرور")
                
                submitted = st.form_submit_button("إنشاء الحساب")
                
                if submitted:
                    age = relativedelta(date.today(), birth_date).years
                    if age < 18:
                        st.markdown('<p class="error-msg">يجب أن يكون عمرك 18 عاماً أو أكثر</p>', unsafe_allow_html=True)
                    elif password != confirm_password:
                        st.markdown('<p class="error-msg">كلمة المرور غير متطابقة</p>', unsafe_allow_html=True)
                    elif email in st.session_state.users_db:
                        st.markdown('<p class="error-msg">هذا البريد الإلكتروني مسجل بالفعل</p>', unsafe_allow_html=True)
                    else:
                        st.session_state.users_db[email] = {
                            'name': name,
                            'password': hashlib.sha256(password.encode()).hexdigest(),
                            'birth_date': birth_date
                        }
                        st.markdown('<p class="success-msg">تم إنشاء الحساب بنجاح</p>', unsafe_allow_html=True)
                        st.session_state.show_register = False
                        st.rerun()
            
            st.markdown("""
            <div class="auth-toggle">
                لديك حساب بالفعل؟ <a onclick="window.streamlitApi.setComponentValue('toggle_login')">تسجيل الدخول</a>
            </div>
            """, unsafe_allow_html=True)
        
        else:
            # نموذج تسجيل الدخول
            st.markdown('<h2 class="auth-title">تسجيل الدخول</h2>', unsafe_allow_html=True)
            st.markdown('<p class="auth-subtitle">أدخل بياناتك للوصول إلى حسابك</p>', unsafe_allow_html=True)
            
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
                        st.markdown('<p class="success-msg">جاري تحويلك...</p>', unsafe_allow_html=True)
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.markdown('<p class="error-msg">بيانات الدخول غير صحيحة</p>', unsafe_allow_html=True)
            
            st.markdown("""
            <div class="auth-toggle">
                ليس لديك حساب؟ <a onclick="window.streamlitApi.setComponentValue('toggle_register')">إنشاء حساب جديد</a>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# باقي الكود (الجزء الخاص بالداشبورد بعد التسجيل)
# ... [يتبع باقي الكود الأصلي مع التعديلات اللازمة]

if __name__ == "__main__":
    app()
