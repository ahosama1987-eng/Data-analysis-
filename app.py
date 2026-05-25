import streamlit as st
import pandas as pd
import plotly.express as px

# 1. إعدادات صفحة الويب
st.set_page_config(page_title="Universal Data Analyzer", page_icon="📊", layout="wide")
st.title("📊 Universal Data Analyzer & Dashboard")
st.markdown("ارفع أي ملف CSV أو Excel، والأداة هتحلله وتطلعلك رسومات تفاعلية أوتوماتيك!")

# 2. رفع الملف
uploaded_file = st.file_uploader("اختار ملف البيانات (CSV or Excel)", type=["csv", "xlsx"])

if uploaded_file is not None:
    # 3. قراءة الملف بناءً على صيغته
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
            
        st.success("تم قراءة البيانات بنجاح! ✅")
        
        # 4. عرض نظرة عامة على البيانات
        st.subheader("🔍 نظرة سريعة على البيانات (Data Preview)")
        st.dataframe(df.head())
        
        # 5. عرض إحصائيات سريعة
        st.subheader("📈 إحصائيات عامة (Summary Statistics)")
        st.write(df.describe())
        
        # 6. بناء الـ Dashboard التفاعلية (زي Power BI)
        st.markdown("---")
        st.subheader("🎨 إنشاء الرسومات التفاعلية")
        
        # استخراج أسماء الأعمدة
        columns = df.columns.tolist()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            x_axis = st.selectbox("اختار محور السينات (X-axis)", options=columns)
        with col2:
            y_axis = st.selectbox("اختار محور الصادات (Y-axis)", options=columns)
        with col3:
            plot_type = st.selectbox("اختار نوع الرسمة", options=["Bar Chart", "Line Chart", "Scatter Plot"])
            
        # 7. رسم الـ Chart بناءً على اختيار المستخدم
        if st.button("رسم البيانات 🚀"):
            if plot_type == "Bar Chart":
                fig = px.bar(df, x=x_axis, y=y_axis, title=f"{y_axis} vs {x_axis}")
            elif plot_type == "Line Chart":
                fig = px.line(df, x=x_axis, y=y_axis, title=f"{y_axis} vs {x_axis}")
            else:
                fig = px.scatter(df, x=x_axis, y=y_axis, title=f"{y_axis} vs {x_axis}")
                
            # عرض الرسمة التفاعلية
            st.plotly_chart(fig, use_container_width=True)
            
    except Exception as e:
        st.error(f"حصلت مشكلة في قراءة الملف: {e}")
else:
    st.info("في انتظار رفع الملف للبدء في التحليل...")
