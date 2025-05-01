import streamlit as st
from datetime import datetime
import time

def maintenance_page():
    st.set_page_config(
        page_title="LEO Chat -  تحت الصيانة ",
        page_icon="🔧",
        layout="centered"
    )
    
    # CSS مخصص لصفحة الصيانة
    st.markdown("""
    <style>
        .maintenance-container {
            max-width: 800px;
            margin: 0 auto;
            padding: 3rem;
            text-align: center;
            border-radius: 20px;
            background: linear-gradient(135deg, #f5f7fa 0%, #e4e8f0 100%);
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        .maintenance-header {
            margin-bottom: 2rem;
        }
        .maintenance-header h1 {
            color: #2c3e50;
            font-size: 2.5rem;
            margin-bottom: 1rem;
        }
        .maintenance-icon {
            font-size: 5rem;
            margin-bottom: 1.5rem;
            color: #e74c3c;
        }
        .maintenance-content {
            margin-bottom: 2rem;
            line-height: 1.8;
            color: #34495e;
        }
        .progress-container {
            height: 20px;
            background: #ecf0f1;
            border-radius: 10px;
            margin: 2rem 0;
            overflow: hidden;
        }
        .progress-bar {
            height: 100%;
            background: linear-gradient(90deg, #3498db, #2ecc71);
            width: 0;
            transition: width 1s ease-in-out;
            border-radius: 10px;
        }
        .countdown {
            font-size: 1.5rem;
            font-weight: bold;
            color: #e74c3c;
            margin: 1rem 0;
        }
        .social-links {
            display: flex;
            justify-content: center;
            gap: 1rem;
            margin-top: 2rem;
        }
        .social-link {
            padding: 0.5rem 1rem;
            background: #3498db;
            color: white;
            border-radius: 5px;
            text-decoration: none;
            transition: all 0.3s;
        }
        .social-link:hover {
            background: #2980b9;
            transform: translateY(-2px);
        }
        .contact-info {
            margin-top: 2rem;
            padding: 1rem;
            background: rgba(255,255,255,0.7);
            border-radius: 10px;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # تاريخ ووقت الصيانة
    maintenance_start = datetime(2025, 5, 15, 10, 0)  # تاريخ بدء الصيانة
    maintenance_end = datetime(2025, 5, 15, 16, 0)   # تاريخ انتهاء الصيانة
    now = datetime.now()
    
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
        time_left = None
        progress = 100
    
    # واجهة صفحة الصيانة
    with st.container():
        st.markdown("""
        <div class="maintenance-container">
            <div class="maintenance-header">
                <div class="maintenance-icon">🔧</div>
                <h1>التطبيق قيد الصيانة</h1>
            </div>
            
            <div class="maintenance-content">
                <p>نقوم حاليًا بإجراء بعض التحديثات والتطويرات على النظام لتحسين تجربتك.</p>
                <p>نعتذر عن أي إزعاج وسنعود قريبًا بإصدار أفضل!</p>
            </div>
            
            <div style="margin: 2rem 0;">
                <h3>حالة الصيانة: <strong>{}</strong></h3>
                <div class="progress-container">
                    <div class="progress-bar" style="width: {}%;"></div>
                </div>
            </div>
        """.format(status, progress), unsafe_allow_html=True)
        
        if time_left:
            hours, remainder = divmod(time_left.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            st.markdown(f"""
            <div class="countdown">
                الوقت المتبقي: {hours} ساعة {minutes} دقيقة {seconds} ثانية
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
            <div class="contact-info">
                <h4>للتواصل خلال فترة الصيانة:</h4>
                <p>📧 البريد الإلكتروني: support@leochat.com</p>
                <p>📞 الهاتف: 01028799352</p>
            </div>
            
            <div class="social-links">
                <a href="#" class="social-link">تويتر</a>
                <a href="#" class="social-link">فيسبوك</a>
                <a href="#" class="social-link">إنستجرام</a>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # تأثيرات حركية للشريط التقدمي
    if st.session_state.get('progress', 0) < progress:
        for i in range(int(st.session_state.get('progress', 0)), int(progress) + 1):
            st.session_state.progress = i
            time.sleep(0.02)
            st.rerun()

if __name__ == "__main__":
    maintenance_page() 
