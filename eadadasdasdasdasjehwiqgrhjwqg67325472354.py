import streamlit as st
from datetime import datetime, timedelta
import time

def maintenance_page():
    st.set_page_config(
        page_title="Yap STS - الصيانة",
        page_icon="🔧",
        layout="centered"
    )
    
    # إعداد تواريخ الصيانة
    maintenance_date = datetime.now().replace(hour=13, minute=0, second=0)  # 1 مساءً
    maintenance_end = maintenance_date + timedelta(hours=4)  # 5 مساءً
    
    # CSS مخصص لصفحة الصيانة
    st.markdown("""
    <style>
        :root {
            --primary-color: #4a6bff;
            --secondary-color: #ff6b6b;
        }
        
        .maintenance-container {
            max-width: 600px;
            margin: 0 auto;
            padding: 2rem;
            text-align: center;
            border-radius: 16px;
            background: white;
            box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        }
        
        .maintenance-header {
            margin-bottom: 1.5rem;
        }
        
        .maintenance-header h1 {
            color: var(--primary-color);
            font-size: 2.2rem;
            margin-bottom: 0.5rem;
        }
        
        .maintenance-header h2 {
            color: #555;
            font-size: 1.3rem;
            font-weight: normal;
        }
        
        .maintenance-divider {
            height: 3px;
            background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
            margin: 1.5rem 0;
            border-radius: 3px;
        }
        
        .maintenance-schedule {
            background: #f8f9fa;
            padding: 1rem;
            border-radius: 10px;
            margin: 1.5rem 0;
        }
        
        .maintenance-schedule h3 {
            color: var(--secondary-color);
            margin-bottom: 0.5rem;
        }
        
        .maintenance-schedule p {
            font-size: 1.1rem;
            margin: 0;
        }
        
        .countdown {
            font-size: 1.8rem;
            font-weight: bold;
            color: var(--primary-color);
            margin: 1.5rem 0;
        }
        
        .logo {
            font-size: 2.5rem;
            font-weight: bold;
            color: var(--primary-color);
            margin-bottom: 1rem;
        }
        
        .progress-container {
            height: 8px;
            background: #e9ecef;
            border-radius: 4px;
            margin: 1.5rem 0;
        }
        
        .progress-bar {
            height: 100%;
            background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
            width: 0%;
            border-radius: 4px;
            transition: width 0.5s ease;
        }
        
        .emoji {
            font-size: 3rem;
            margin: 1rem 0;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # حساب وقت الصيانة المتبقي
    now = datetime.now()
    if now < maintenance_date:
        status = "قيد الإعداد"
        time_left = maintenance_date - now
        progress = 0
    elif now < maintenance_end:
        status = "جارية"
        time_left = maintenance_end - now
        total_duration = (maintenance_end - maintenance_date).total_seconds()
        elapsed = (now - maintenance_date).total_seconds()
        progress = min(100, (elapsed / total_duration) * 100)
    else:
        status = "تم الانتهاء"
        time_left = None
        progress = 100
    
    # واجهة صفحة الصيانة
    with st.container():
        st.markdown("""
        <div class="maintenance-container">
            <div class="logo">Yap STS</div>
            <div class="emoji">🔧</div>
            
            <div class="maintenance-header">
                <h1>موقعنا تحت الصيانة</h1>
                <h2>شوي بين وراجعين...</h2>
            </div>
            
            <div class="maintenance-divider"></div>
            
            <div class="maintenance-schedule">
                <h3>12 أغسطس</h3>
                <p>من 1 - 5 مساءً</p>
            </div>
            
            <div class="progress-container">
                <div class="progress-bar" style="width: {}%"></div>
            </div>
            
            <p>تطبيق <strong>Yap STS</strong> راح يكون تحت الصيانة كم ساعة بين وراجعين.</p>
        """.format(progress), unsafe_allow_html=True)
        
        if time_left:
            hours, remainder = divmod(time_left.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            st.markdown(f"""
            <div class="countdown">
                {hours} ساعة {minutes} دقيقة {seconds} ثانية
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
            <div class="maintenance-divider"></div>
            
            <p style="font-size: 1.2rem; margin-top: 1.5rem;">
                نشكركم على صبركم وسنعود أقوى من قبل!
            </p>
            
            <div style="margin-top: 2rem;">
                <strong>فريق Yap STS</strong>
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
