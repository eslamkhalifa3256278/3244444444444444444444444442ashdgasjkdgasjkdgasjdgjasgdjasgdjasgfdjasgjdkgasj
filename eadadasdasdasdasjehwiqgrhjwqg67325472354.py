# صفحة تسجيل الدخول
def login_page():
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(LOGO_URL, width=300)
    
    with col2:
        st.markdown("""
        <div style="background-color:#f0f2f6;padding:30px;border-radius:15px;box-shadow:0 4px 8px rgba(0,0,0,0.1)">
            <h2 style="color:#2c3e50;text-align:center;margin-bottom:30px">تسجيل الدخول</h2>
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
                    st.success("تم تسجيل الدخول بنجاح!")
                    time.sleep(1)
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

# صفحة إنشاء حساب
def create_account():
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(LOGO_URL, width=300)
    
    with col2:
        st.markdown("""
        <div style="background-color:#f0f2f6;padding:30px;border-radius:15px;box-shadow:0 4px 8px rgba(0,0,0,0.1)">
            <h2 style="color:#2c3e50;text-align:center;margin-bottom:30px">إنشاء حساب جديد</h2>
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
        
        st.markdown("""
        </div>
        <div style="text-align:center;margin-top:20px">
            <p style="color:#7f8c8d">لديك حساب بالفعل؟</p>
        """, unsafe_allow_html=True)
        
        if st.button("العودة لتسجيل الدخول", key="go_to_login"):
            st.session_state.current_page = "login"
            st.rerun()
