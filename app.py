import streamlit as st
import pandas as pd
import plotly.express as px

# 1. إعدادات الصفحة الاحترافية (Power BI Style)
st.set_page_config(page_title="Universal BI Pro", page_icon="⚡", layout="wide")

# 2. إضافة لمسة جمالية بالكود (CSS) لتغيير شكل الكروت والخلفية
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    [data-testid="stMetric"] {
        background-color: #1f2937;
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #deff9a; /* لون أخضر فسفوري مميز */
        box-shadow: 2px 2px 10px rgba(0,0,0,0.5);
    }
    </style>
    """, unsafe_allow_html=True)

# 3. القائمة الجانبية للفلاتر والرفع
with st.sidebar:
    st.title("⚙️ الإعدادات")
    st.info("ارفع ملفك هنا لتبدأ التحليل")
    uploaded_file = st.file_uploader("Upload Data", type=["csv", "xlsx"])

if uploaded_file:
    # قراءة الداتا
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
    numeric_cols = df.select_dtypes(include=['number']).columns
    
    # 4. قسم كروت المؤشرات (KPIs) - أهم حتة في الداشبورد
    st.subheader("📌 المؤشرات الرئيسية (Key Metrics)")
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    
    kpi1.metric("إجمالي السجلات", f"{len(df):,}")
    kpi2.metric("عدد الأعمدة", f"{len(df.columns)}")
    
    if len(numeric_cols) > 0:
        kpi3.metric("المتوسط العام", f"{df[numeric_cols[0]].mean():.2f}")
        kpi4.metric("أعلى قيمة", f"{df[numeric_cols[0]].max():,}")

    st.markdown("---")
    
    # 5. قسم الرسومات البيانية (جنب بعض زي الباور بي آي)
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.write("📊 تحليل التوزيع")
        x_axis = st.selectbox("اختار محور X", df.columns)
        y_axis = st.selectbox("اختار محور Y", numeric_cols if len(numeric_cols)>0 else df.columns)
        fig_bar = px.bar(df, x=x_axis, y=y_axis, template="plotly_dark", color_discrete_sequence=['#deff9a'])
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_chart2:
        st.write("📈 تحليل العلاقات")
        fig_scatter = px.scatter(df, x=x_axis, y=y_axis, template="plotly_dark", color_discrete_sequence=['#10b981'])
        st.plotly_chart(fig_scatter, use_container_width=True)

    # 6. عرض جدول البيانات في الأسفل
    with st.expander("👀 عرض البيانات الكاملة"):
        st.dataframe(df, use_container_width=True)
else:
    st.warning("👈 من فضلك ارفع ملف من القائمة الجانبية للبدء.")
        
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
