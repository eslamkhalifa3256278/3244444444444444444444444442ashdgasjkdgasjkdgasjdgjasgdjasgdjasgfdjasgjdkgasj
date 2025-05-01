import streamlit as st
import hashlib
from datetime import date
from dateutil.relativedelta import relativedelta

# CSS مخصص للتصميم البسيط
st.markdown("""
<style>
    .auth-container {
        max-width: 400px;
        margin: 50px auto;
        padding: 30px;
        border-radius: 8px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        background: white;
    }
    .auth-title {
        text-align: center;
        color: #4F46E5;
        margin-bottom: 25px;
        font-size: 24px;
    }
    .stTextInput>div>div>input,
    .stPassword>div>div>input,
    .stDateInput>div>div>input {
        border-radius: 6px;
        padding: 10px;
    }
    .stButton>button {
        width: 100%;
        background-color: #4F46E5;
        color: white;
        border: none;
        padding: 12px;
        border-radius: 6px;
        font-weight: 500;
    }
    .auth-toggle {
        text-align: center;
        margin-top: 20px;
        color: #666;
    }
    .auth-toggle a {
        color: #4F46E5;
        text-decoration: none;
        font-weight: 500;
    }
    .error-msg {
        color: #EF4444;
        text-align: center;
        margin-top: 10px;
    }
    .success-msg {
        color: #10B981;
        text-align: center;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# قاعدة بيانات مؤقتة
if 'users_db' not in st.session_state:
    st.session_state.users_db = {}

def show_auth_form():
    """عرض نموذج المصادقة"""
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="auth-container">', unsafe_allow_html=True)
        
        if st.session_state.get('show_register', False):
            # نموذج إنشاء حساب
            st.markdown('<div class="auth-title">إنشاء حساب جديد</div>', unsafe_allow_html=True)
            
            with st.form("register_form"):
                name = st.text_input("الاسم الكامل")
                email = st.text_input("البريد الإلكتروني")
                birth_date = st.date_input("تاريخ الميلاد", min_value=date(1900, 1, 1))
                password = st.text_input("كلمة المرور", type="password")
                confirm_password = st.text_input("تأكيد كلمة المرور", type="password")
                
                if st.form_submit_button("إنشاء الحساب"):
                    age = relativedelta(date.today(), birth_date).years
                    if age < 18:
                        st.markdown('<div class="error-msg">يجب أن يكون عمرك 18 عاماً أو أكثر</div>', unsafe_allow_html=True)
                    elif password != confirm_password:
                        st.markdown('<div class="error-msg">كلمة المرور غير متطابقة</div>', unsafe_allow_html=True)
                    elif email in st.session_state.users_db:
                        st.markdown('<div class="error-msg">هذا البريد الإلكتروني مسجل بالفعل</div>', unsafe_allow_html=True)
                    else:
                        st.session_state.users_db[email] = {
                            'name': name,
                            'password': hashlib.sha256(password.encode()).hexdigest(),
                            'birth_date': birth_date
                        }
                        st.markdown('<div class="success-msg">تم إنشاء الحساب بنجاح</div>', unsafe_allow_html=True)
                        st.session_state.show_register = False
                        st.rerun()
            
            st.markdown("""
            <div class="auth-toggle">
                لديك حساب بالفعل؟ <a href="#" onclick="window.streamlitApi.setComponentValue('show_login')">تسجيل الدخول</a>
            </div>
            """, unsafe_allow_html=True)
        
        else:
            # نموذج تسجيل الدخول
            st.markdown('<div class="auth-title">تسجيل الدخول</div>', unsafe_allow_html=True)
            
            with st.form("login_form"):
                email = st.text_input("البريد الإلكتروني")
                password = st.text_input("كلمة المرور", type="password")
                
                if st.form_submit_button("تسجيل الدخول"):
                    if email in st.session_state.users_db and \
                            hashlib.sha256(password.encode()).hexdigest() == st.session_state.users_db[email]['password']:
                        st.session_state.logged_in = True
                        st.session_state.user = st.session_state.users_db[email]
                        st.markdown('<div class="success-msg">جاري تحويلك...</div>', unsafe_allow_html=True)
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.markdown('<div class="error-msg">بيانات الدخول غير صحيحة</div>', unsafe_allow_html=True)
            
            st.markdown("""
            <div class="auth-toggle">
                ليس لديك حساب؟ <a href="#" onclick="window.streamlitApi.setComponentValue('show_register')">إنشاء حساب جديد</a>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# إعداد الصفحة الرئيسية
def main():
    st.set_page_config(page_title="تسجيل الدخول", layout="wide")
    
    if not st.session_state.get('logged_in', False):
        show_auth_form()
    else:
        # صفحة المستخدم بعد التسجيل
        st.success(f"مرحباً بك، {st.session_state.user['name']}!")
        if st.button("تسجيل الخروج"):
            st.session_state.logged_in = False
            st.rerun()

if __name__ == "__main__":
    main()
