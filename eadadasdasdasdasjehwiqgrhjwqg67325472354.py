import streamlit as st
from datetime import datetime, timedelta
import time
import pytz
from streamlit.components.v1 import html

def maintenance_page():
    # إعدادات الصفحة الأساسية
    st.set_page_config(
        page_title="LEO Chat - الصيانة",
        page_icon="🔧",
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    
    # CSS مخصص متطور
    st.markdown("""
    <style>
        :root {
            --primary-color: #3498db;
            --secondary-color: #2ecc71;
            --error-color: #e74c3c;
            --text-color: #2c3e50;
            --light-bg: #f5f7fa;
            --dark-bg: #34495e;
            --gradient: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        }
        
        .maintenance-container {
            max-width: 900px;
            margin: 2rem auto;
            padding: 3rem 2rem;
            text-align: center;
            border-radius: 20px;
            background: linear-gradient(135deg, #f5f7fa 0%, #e4e8f0 100%);
            box-shadow: 0 15px 35px rgba(0,0,0,0.1);
            position: relative;
            overflow: hidden;
            border: 1px solid rgba(255,255,255,0.3);
        }
        
        .maintenance-container::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.8) 0%, rgba(255,255,255,0) 70%);
            animation: pulse 8s infinite linear;
            z-index: 0;
        }
        
        @keyframes pulse {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .maintenance-header {
            margin-bottom: 2.5rem;
            position: relative;
            z-index: 1;
        }
        
        .maintenance-header h1 {
            color: var(--text-color);
            font-size: 2.8rem;
            margin-bottom: 1.5rem;
            font-weight: 700;
            text-shadow: 1px 1px 3px rgba(0,0,0,0.1);
        }
        
        .maintenance-icon {
            font-size: 6rem;
            margin-bottom: 2rem;
            color: var(--error-color);
            animation: bounce 2s infinite;
        }
        
        @keyframes bounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-20px); }
        }
        
        .maintenance-content {
            margin-bottom: 3rem;
            line-height: 1.8;
            color: var(--text-color);
            font-size: 1.1rem;
            position: relative;
            z-index: 1;
        }
        
        .progress-container {
            height: 25px;
            background: #ecf0f1;
            border-radius: 12px;
            margin: 3rem 0;
            overflow: hidden;
            box-shadow: inset 0 2px 5px rgba(0,0,0,0.1);
            position: relative;
            z-index: 1;
        }
        
        .progress-bar {
            height: 100%;
            background: var(--gradient);
            width: 0;
            transition: width 0.5s ease-in-out;
            border-radius: 12px;
            position: relative;
            overflow: hidden;
        }
        
        .progress-bar::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(90deg, 
                rgba(255,255,255,0) 0%, 
                rgba(255,255,255,0.3) 50%, 
                rgba(255,255,255,0) 100%);
            animation: shine 2s infinite;
        }
        
        @keyframes shine {
            0% { transform: translateX(-100%); }
            100% { transform: translateX(100%); }
        }
        
        .countdown {
            font-size: 1.8rem;
            font-weight: bold;
            color: var(--error-color);
            margin: 2rem 0;
            display: flex;
            justify-content: center;
            gap: 1rem;
            flex-wrap: wrap;
            position: relative;
            z-index: 1;
        }
        
        .countdown-item {
            background: rgba(255,255,255,0.8);
            padding: 0.8rem 1.5rem;
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            min-width: 80px;
        }
        
        .countdown-value {
            font-size: 2.2rem;
            display: block;
            color: var(--primary-color);
        }
        
        .countdown-label {
            font-size: 0.9rem;
            color: var(--text-color);
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .social-links {
            display: flex;
            justify-content: center;
            gap: 1.5rem;
            margin: 3rem 0 2rem;
            flex-wrap: wrap;
            position: relative;
            z-index: 1;
        }
        
        .social-link {
            padding: 0.8rem 1.8rem;
            background: var(--primary-color);
            color: white;
            border-radius: 50px;
            text-decoration: none;
            transition: all 0.3s;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-weight: 500;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        .social-link:hover {
            background: #2980b9;
            transform: translateY(-3px);
            box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        }
        
        .contact-info {
            margin-top: 3rem;
            padding: 1.5rem;
            background: rgba(255,255,255,0.8);
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.05);
            position: relative;
            z-index: 1;
        }
        
        .contact-info h4 {
            margin-bottom: 1rem;
            color: var(--text-color);
            font-size: 1.3rem;
        }
        
        .contact-method {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.8rem;
            margin: 1rem 0;
            font-size: 1.1rem;
        }
        
        .updates-container {
            background: rgba(255,255,255,0.9);
            border-radius: 15px;
            padding: 1.5rem;
            margin: 2rem 0;
            text-align: right;
            box-shadow: 0 5px 15px rgba(0,0,0,0.05);
            position: relative;
            z-index: 1;
        }
        
        .update-item {
            padding: 1rem;
            margin: 1rem 0;
            border-right: 4px solid var(--primary-color);
            background: rgba(240, 240, 240, 0.7);
            border-radius: 8px;
        }
        
        .update-time {
            font-size: 0.8rem;
            color: #7f8c8d;
            margin-bottom: 0.5rem;
        }
        
        .language-switcher {
            position: absolute;
            top: 20px;
            left: 20px;
            z-index: 10;
        }
        
        .language-btn {
            background: rgba(255,255,255,0.8);
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            cursor: pointer;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            transition: all 0.3s;
        }
        
        .language-btn:hover {
            background: white;
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        }
        
        @media (max-width: 768px) {
            .maintenance-container {
                padding: 2rem 1rem;
                margin: 1rem;
            }
            
            .maintenance-header h1 {
                font-size: 2rem;
            }
            
            .countdown {
                flex-direction: column;
                gap: 0.5rem;
            }
            
            .countdown-item {
                padding: 0.5rem 1rem;
                min-width: auto;
            }
            
            .countdown-value {
                font-size: 1.8rem;
            }
        }
    </style>
    """, unsafe_allow_html=True)
    
    # JavaScript للعد التنازلي الدقيق
    countdown_js = """
    <script>
    function updateCountdown() {
        const now = new Date();
        const maintenanceEnd = new Date("%s");
        const diff = maintenanceEnd - now;
        
        if (diff <= 0) {
            document.getElementById("countdown").innerHTML = "تم الانتهاء من الصيانة!";
            return;
        }
        
        const days = Math.floor(diff / (1000 * 60 * 60 * 24));
        const hours = Math.floor((diff %% (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((diff %% (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((diff %% (1000 * 60)) / 1000);
        
        document.getElementById("countdown-days").innerText = days;
        document.getElementById("countdown-hours").innerText = hours;
        document.getElementById("countdown-minutes").innerText = minutes;
        document.getElementById("countdown-seconds").innerText = seconds;
    }
    
    setInterval(updateCountdown, 1000);
    updateCountdown();
    </script>
    """
    
    # إعدادات الصيانة
    timezone = pytz.timezone('Africa/Cairo')  # توقيت القاهرة
    maintenance_start = timezone.localize(datetime(2025, 5, 15, 10, 0))  # تاريخ بدء الصيانة
    maintenance_end = timezone.localize(datetime(2025, 5, 15, 16, 0))   # تاريخ انتهاء الصيانة
    now = datetime.now(timezone)
    
    # حساب وقت الصيانة المتبقي
    if now < maintenance_start:
        status = "قيد الإعداد"
        time_left = maintenance_start - now
        progress = 0
    elif now < maintenance_end:
        status = "جارية"
        time_left = maintenance_end - now
        total_seconds = (maintenance_end - maintenance_start).total_seconds()
        elapsed_seconds = (now - maintenance_start).total_seconds()
        progress = min(100, (elapsed_seconds / total_seconds) * 100)
    else:
        status = "تم الانتهاء"
        time_left = timedelta(0)
        progress = 100
    
    # تحديثات الصيانة
    updates = [
        {
            "time": "10:00 ص",
            "date": "15 مايو 2025",
            "title": "بدء أعمال الصيانة",
            "content": "تم بدء عملية التحديثات المخطط لها على الخوادم الرئيسية."
        },
        {
            "time": "12:30 م",
            "date": "15 مايو 2025",
            "title": "تحديث قاعدة البيانات",
            "content": "جاري الآن تحديث هياكل البيانات وتحسين أداء الاستعلامات."
        },
        {
            "time": "14:00 م",
            "date": "15 مايو 2025",
            "title": "نشر الميزات الجديدة",
            "content": "تم بنجاح نشر وحدات الدردشة المحسنة مع تحسينات الأمان."
        }
    ]
    
    # واجهة صفحة الصيانة
    with st.container():
        st.markdown("""
        <div class="maintenance-container">
            <div class="language-switcher">
                <button class="language-btn">English</button>
            </div>
            
            <div class="maintenance-header">
                <div class="maintenance-icon">🔧</div>
                <h1>التطبيق قيد الصيانة</h1>
            </div>
            
            <div class="maintenance-content">
                <p>نقوم حاليًا بإجراء بعض التحديثات والتطويرات الأساسية على النظام لتحسين تجربتك.</p>
                <p>هذه التحديثات ستجلب ميزات جديدة، تحسينات في الأداء، وتعزيزات أمنية مهمة.</p>
                <p>نعتذر عن أي إزعاج وسنعود قريبًا بإصدار أفضل وأسرع!</p>
            </div>
            
            <div style="margin: 3rem 0;">
                <h3>حالة الصيانة: <strong style="color: var(--primary-color);">{}</strong></h3>
                <div class="progress-container">
                    <div class="progress-bar" style="width: {}%;"></div>
                </div>
                <div style="display: flex; justify-content: space-between; margin-top: 0.5rem;">
                    <span>بداية الصيانة: 10:00 ص</span>
                    <span>نهاية الصيانة: 4:00 م</span>
                </div>
            </div>
        """.format(status, progress), unsafe_allow_html=True)
        
        # قسم العد التنازلي
        st.markdown("""
        <div class="countdown" id="countdown">
            <div class="countdown-item">
                <span class="countdown-value" id="countdown-days">0</span>
                <span class="countdown-label">أيام</span>
            </div>
            <div class="countdown-item">
                <span class="countdown-value" id="countdown-hours">0</span>
                <span class="countdown-label">ساعات</span>
            </div>
            <div class="countdown-item">
                <span class="countdown-value" id="countdown-minutes">0</span>
                <span class="countdown-label">دقائق</span>
            </div>
            <div class="countdown-item">
                <span class="countdown-value" id="countdown-seconds">0</span>
                <span class="countdown-label">ثواني</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # حقن JavaScript للعد التنازلي
        html(countdown_js % maintenance_end.strftime("%Y-%m-%dT%H:%M:%S%z"))
        
        # قسم التحديثات
        st.markdown("""
        <div class="updates-container">
            <h3 style="text-align: center; margin-bottom: 1.5rem;">تحديثات الصيانة</h3>
        """, unsafe_allow_html=True)
        
        for update in updates:
            st.markdown(f"""
            <div class="update-item">
                <div class="update-time">{update['time']} - {update['date']}</div>
                <h4 style="margin: 0.5rem 0; color: var(--primary-color);">{update['title']}</h4>
                <p style="margin: 0;">{update['content']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # قسم التواصل
        st.markdown("""
        <div class="contact-info">
            <h4>للتواصل خلال فترة الصيانة</h4>
            
            <div class="contact-method">
                <span>📧</span>
                <a href="mailto:support@leochat.com" style="color: var(--primary-color); text-decoration: none;">support@leochat.com</a>
            </div>
            
            <div class="contact-method">
                <span>📞</span>
                <a href="tel:+201028799352" style="color: var(--primary-color); text-decoration: none;">01028799352</a>
            </div>
            
            <div class="contact-method">
                <span>📍</span>
                <span>القاهرة، مصر</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # روابط التواصل الاجتماعي
        st.markdown("""
        <div class="social-links">
            <a href="https://twitter.com/leochat" class="social-link">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                    <path d="M5.026 15c6.038 0 9.341-5.003 9.341-9.334 0-.14 0-.282-.006-.422A6.685 6.685 0 0 0 16 3.542a6.658 6.658 0 0 1-1.889.518 3.301 3.301 0 0 0 1.447-1.817 6.533 6.533 0 0 1-2.087.793A3.286 3.286 0 0 0 7.875 6.03a9.325 9.325 0 0 1-6.767-3.429 3.289 3.289 0 0 0 1.018 4.382A3.323 3.323 0 0 1 .64 6.575v.045a3.288 3.288 0 0 0 2.632 3.218 3.203 3.203 0 0 1-.865.115 3.23 3.23 0 0 1-.614-.057 3.283 3.283 0 0 0 3.067 2.277A6.588 6.588 0 0 1 .78 13.58a6.32 6.32 0 0 1-.78-.045A9.344 9.344 0 0 0 5.026 15z"/>
                </svg>
                تويتر
            </a>
            <a href="https://facebook.com/leochat" class="social-link">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                    <path d="M16 8.049c0-4.446-3.582-8.05-8-8.05C3.58 0-.002 3.603-.002 8.05c0 4.017 2.926 7.347 6.75 7.951v-5.625h-2.03V8.05H6.75V6.275c0-2.017 1.195-3.131 3.022-3.131.876 0 1.791.157 1.791.157v1.98h-1.009c-.993 0-1.303.621-1.303 1.258v1.51h2.218l-.354 2.326H9.25V16c3.824-.604 6.75-3.934 6.75-7.951z"/>
                </svg>
                فيسبوك
            </a>
            <a href="https://instagram.com/leochat" class="social-link">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                    <path d="M8 0C5.829 0 5.556.01 4.703.048 3.85.088 3.269.222 2.76.42a3.917 3.917 0 0 0-1.417.923A3.927 3.927 0 0 0 .42 2.76C.222 3.268.087 3.85.048 4.7.01 5.555 0 5.827 0 8.001c0 2.172.01 2.444.048 3.297.04.852.174 1.433.372 1.942.205.526.478.972.923 1.417.444.445.89.719 1.416.923.51.198 1.09.333 1.942.372C5.555 15.99 5.827 16 8 16s2.444-.01 3.298-.048c.851-.04 1.434-.174 1.943-.372a3.916 3.916 0 0 0 1.416-.923c.445-.445.718-.891.923-1.417.197-.509.332-1.09.372-1.942C15.99 10.445 16 10.173 16 8s-.01-2.445-.048-3.299c-.04-.851-.175-1.433-.372-1.941a3.926 3.926 0 0 0-.923-1.417A3.911 3.911 0 0 0 13.24.42c-.51-.198-1.092-.333-1.943-.372C10.443.01 10.172 0 7.998 0h.003zm-.717 1.442h.718c2.136 0 2.389.007 3.232.046.78.035 1.204.166 1.486.275.373.145.64.319.92.599.28.28.453.546.598.92.11.281.24.705.275 1.485.039.843.047 1.096.047 3.231s-.008 2.389-.047 3.232c-.035.78-.166 1.203-.275 1.485a2.47 2.47 0 0 1-.599.919c-.28.28-.546.453-.92.598-.28.11-.704.24-1.485.276-.843.038-1.096.047-3.232.047s-2.39-.009-3.233-.047c-.78-.036-1.203-.166-1.485-.276a2.478 2.478 0 0 1-.92-.598 2.48 2.48 0 0 1-.6-.92c-.109-.281-.24-.705-.275-1.485-.038-.843-.046-1.096-.046-3.233 0-2.136.008-2.388.046-3.231.036-.78.166-1.204.276-1.486.145-.373.319-.64.599-.92.28-.28.546-.453.92-.598.282-.11.705-.24 1.485-.276.738-.034 1.024-.044 2.515-.045v.002zm4.988 1.328a.96.96 0 1 0 0 1.92.96.96 0 0 0 0-1.92zm-4.27 1.122a4.109 4.109 0 1 0 0 8.217 4.109 4.109 0 0 0 0-8.217zm0 1.441a2.667 2.667 0 1 1 0 5.334 2.667 2.667 0 0 1 0-5.334z"/>
                </svg>
                إنستجرام
            </a>
        </div>
        
        <div style="text-align: center; margin-top: 2rem; color: #7f8c8d; font-size: 0.9rem; position: relative; z-index: 1;">
            © 2025 LEO Chat. جميع الحقوق محفوظة.
        </div>
        </div>
        """, unsafe_allow_html=True)
    
    # تأثيرات حركية للشريط التقدمي
    if 'progress' not in st.session_state:
        st.session_state.progress = 0
    
    if st.session_state.progress < progress:
        increment = max(0.5, (progress - st.session_state.progress) / 20)
        st.session_state.progress += increment
        if st.session_state.progress < progress:
            time.sleep(0.03)
            st.rerun()

if __name__ == "__main__":
    maintenance_page()
