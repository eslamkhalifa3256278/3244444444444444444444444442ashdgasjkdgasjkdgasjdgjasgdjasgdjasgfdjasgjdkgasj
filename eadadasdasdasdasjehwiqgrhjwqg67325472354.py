from flask import Flask, render_template_string
import datetime
import time

app = Flask(__name__)

# تاريخ ووقت انتهاء الصيانة (اضبطه حسب احتياجك)
MAINTENANCE_END = datetime.datetime(2023, 12, 31, 23, 59, 59)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>الموقع تحت الصيانة</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Tajawal', sans-serif;
        }
        
        body {
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: #fff;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            padding: 20px;
            overflow-x: hidden;
        }
        
        .maintenance-container {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 40px;
            max-width: 800px;
            width: 100%;
            box-shadow: 0 15px 30px rgba(0, 0, 0, 0.3);
            animation: fadeIn 1.5s ease-in-out;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        h1 {
            font-size: 2.5rem;
            margin-bottom: 20px;
            color: #fff;
            text-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
        }
        
        p {
            font-size: 1.2rem;
            margin-bottom: 30px;
            line-height: 1.6;
        }
        
        .countdown {
            display: flex;
            justify-content: center;
            gap: 15px;
            margin: 30px 0;
            flex-wrap: wrap;
        }
        
        .countdown-box {
            background: rgba(0, 0, 0, 0.3);
            border-radius: 10px;
            padding: 20px;
            min-width: 100px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
            position: relative;
            overflow: hidden;
            transition: all 0.3s ease;
        }
        
        .countdown-box:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
        }
        
        .countdown-box::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.1), transparent);
            transform: translateX(-100%);
            animation: shine 3s infinite;
        }
        
        .countdown-value {
            font-size: 3rem;
            font-weight: bold;
            display: block;
            margin-bottom: 5px;
        }
        
        .countdown-label {
            font-size: 1rem;
            opacity: 0.8;
        }
        
        .social-icons {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-top: 30px;
        }
        
        .social-icon {
            color: #fff;
            font-size: 1.5rem;
            transition: all 0.3s ease;
        }
        
        .social-icon:hover {
            transform: scale(1.2);
            color: #4fc3f7;
        }
        
        .progress-container {
            width: 100%;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 10px;
            margin: 30px 0;
            overflow: hidden;
        }
        
        .progress-bar {
            height: 10px;
            background: linear-gradient(90deg, #4fc3f7, #00e676);
            width: 0%;
            border-radius: 10px;
            transition: width 0.5s ease;
            animation: progressAnimation 2s infinite alternate;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes shine {
            100% { transform: translateX(100%); }
        }
        
        @keyframes progressAnimation {
            0% { background-position: 0% 50%; }
            100% { background-position: 100% 50%; }
        }
        
        .gear {
            font-size: 3rem;
            margin-bottom: 20px;
            animation: spin 5s linear infinite;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        @media (max-width: 768px) {
            .maintenance-container {
                padding: 30px 20px;
            }
            
            h1 {
                font-size: 2rem;
            }
            
            p {
                font-size: 1rem;
            }
            
            .countdown-box {
                min-width: 80px;
                padding: 15px;
            }
            
            .countdown-value {
                font-size: 2rem;
            }
        }
    </style>
</head>
<body>
    <div class="maintenance-container">
        <div class="gear">
            <i class="fas fa-cog"></i>
            <i class="fas fa-cog" style="margin-right: 15px; animation-direction: reverse;"></i>
            <i class="fas fa-cog"></i>
        </div>
        
        <h1>الموقع تحت الصيانة</h1>
        <p>نقوم حاليًا بإجراء بعض التحديثات والتطويرات على الموقع لتحسين تجربتك. نعتذر للإزعاج وسنعود قريبًا!</p>
        
        <div class="progress-container">
            <div class="progress-bar" id="progressBar"></div>
        </div>
        
        <div class="countdown">
            <div class="countdown-box">
                <span class="countdown-value" id="days">00</span>
                <span class="countdown-label">أيام</span>
            </div>
            <div class="countdown-box">
                <span class="countdown-value" id="hours">00</span>
                <span class="countdown-label">ساعات</span>
            </div>
            <div class="countdown-box">
                <span class="countdown-value" id="minutes">00</span>
                <span class="countdown-label">دقائق</span>
            </div>
            <div class="countdown-box">
                <span class="countdown-value" id="seconds">00</span>
                <span class="countdown-label">ثواني</span>
            </div>
        </div>
        
        <p>يمكنك متابعتنا على وسائل التواصل الاجتماعي للاطلاع على آخر التحديثات</p>
        
        <div class="social-icons">
            <a href="#" class="social-icon"><i class="fab fa-facebook"></i></a>
            <a href="#" class="social-icon"><i class="fab fa-twitter"></i></a>
            <a href="#" class="social-icon"><i class="fab fa-instagram"></i></a>
            <a href="#" class="social-icon"><i class="fab fa-linkedin"></i></a>
        </div>
    </div>

    <script>
        // تاريخ ووقت انتهاء الصيانة (يجب أن يتطابق مع الوقت في السيرفر)
        const endDate = new Date("{{ end_date }}").getTime();
        
        function updateCountdown() {
            const now = new Date().getTime();
            const distance = endDate - now;
            
            // حساب الوقت المتبقي
            const days = Math.floor(distance / (1000 * 60 * 60 * 24));
            const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((distance % (1000 * 60)) / 1000);
            
            // عرض النتائج
            document.getElementById("days").innerHTML = days.toString().padStart(2, "0");
            document.getElementById("hours").innerHTML = hours.toString().padStart(2, "0");
            document.getElementById("minutes").innerHTML = minutes.toString().padStart(2, "0");
            document.getElementById("seconds").innerHTML = seconds.toString().padStart(2, "0");
            
            // حساب نسبة الإكمال
            const totalDuration = endDate - new Date("{{ start_date }}").getTime();
            const progress = ((totalDuration - distance) / totalDuration) * 100;
            document.getElementById("progressBar").style.width = `${Math.min(progress, 100)}%`;
            
            // إذا انتهى الوقت
            if (distance < 0) {
                clearInterval(countdownTimer);
                document.querySelector(".countdown").innerHTML = "<h2>الصيانة انتهت! نعود قريبًا...</h2>";
                document.getElementById("progressBar").style.width = "100%";
            }
        }
        
        // تحديث العداد كل ثانية
        const countdownTimer = setInterval(updateCountdown, 1000);
        updateCountdown(); // التشغيل الأولي
    </script>
</body>
</html>
"""

@app.route('/')
def maintenance_page():
    # حساب الوقت المتبقي
    now = datetime.datetime.now()
    time_remaining = MAINTENANCE_END - now
    
    # إذا انتهى وقت الصيانة، يمكنك توجيه المستخدم للصفحة الرئيسية
    if time_remaining.total_seconds() <= 0:
        return "الصيانة انتهت! نعود قريبًا..."
    
    # تقديم صفحة الصيانة مع البيانات المطلوبة
    return render_template_string(HTML_TEMPLATE, 
                               end_date=MAINTENANCE_END.strftime("%Y-%m-%dT%H:%M:%S"),
                               start_date=now.strftime("%Y-%m-%dT%H:%M:%S"))

if __name__ == '__main__':
    app.run(debug=True)
