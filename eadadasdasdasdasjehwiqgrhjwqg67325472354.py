def maintenance_page():
    st.set_page_config(page_title="🚧 التطبيق تحت الصيانة", layout="centered")
    
    st.markdown(
        """
        <div style="text-align: center; padding: 50px;">
            <img src="https://cdn-icons-png.flaticon.com/512/565/565547.png" width="120">
            <h2 style="color:#FF4B4B;">🚧 التطبيق تحت الصيانة حالياً</h2>
            <p style="font-size:18px;">نعمل حالياً على تحسين تجربتك معنا.</p>
            <p style="font-size:16px;">نرجو المحاولة لاحقاً.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
