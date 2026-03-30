# Clinical AI Diagnostic System - Application Entry Point
# Version: 3.1.0-clinical
# Authorized clinician use only.

import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.express as px
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestClassifier
from streamlit_lottie import st_lottie
import requests

# Page configuration
st.set_page_config(
    page_title="GDM Predictor | Clinical AI",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Clinical AI Diagnostic System - Application Entry Point

def load_lottieurl(url: str):
    """
    Fetches a Lottie animation JSON from a remote URL.
    
    Args:
        url (str): The asset URL for the Lottie animation.
        
    Returns:
        dict: The JSON animation data or None if the request fails.
    """
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except Exception:
        return None

lottie_medical = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_5njp3v67.json")
lottie_scanning = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_6p8pS8.json")

def apply_custom_styles():
    """
    Injects professional CSS into the Streamlit application to ensure a premium UI/UX.
    """
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
        
        .stApp {
            background-color: #0d1117;
            color: #c9d1d9;
            font-family: 'Outfit', sans-serif;
        }
        
        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #161b22;
            border-right: 1px solid #30363d;
        }
        
        /* Center the main container */
        .block-container {
            padding-top: 2rem;
            max-width: 1200px;
        }
        
        /* Section Grouping */
        .section-container {
            padding: 1rem 0;
            margin-bottom: 2.5rem;
        }
        
        /* Header Gradient */
        .main-title {
            background: linear-gradient(90deg, #58a6ff, #bc8cf2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 3rem;
            font-weight: 800;
            margin-bottom: 0.5rem;
        }
        
        /* Metric Styling */
        [data-testid="stMetricValue"] {
            color: #58a6ff;
            font-weight: 600;
        }
        
        /* Button Styling */
        .stButton>button {
            background: linear-gradient(90deg, #238636, #2ea043);
            border: none;
            color: white;
            padding: 0.8rem 2rem;
            font-weight: 600;
            border-radius: 8px;
            width: 100%;
            margin-top: 1rem;
        }
        
        /* Inputs Styling */
        .stNumberInput input {
            background-color: #0d1117;
            color: white;
            border: 1px solid #30363d;
        }
        </style>
        """, unsafe_allow_html=True)

# Initialize Design System
apply_custom_styles()

@st.cache_resource
def load_trained_model():
    """
    Loads the serialized Random Forest classifier from the local filesystem.
    
    Returns:
        sklearn.ensemble.RandomForestClassifier: The trained model instance.
    """
    try:
        with open('gdm_model.pkl', 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        st.error("Model binary not found. Please run individual training first.")
        st.stop()

# Load Model Instance
model = load_trained_model()

df = pd.read_csv('diabetesGDM (1).csv')

# --- SIDEBAR ---
with st.sidebar:
    if lottie_medical:
        st_lottie(lottie_medical, height=150, key="sidebar_heart")
    else:
        st.markdown("<h1 style='text-align: center;'>🧬</h1>", unsafe_allow_html=True)
    
    st.markdown("<h2 style='text-align: center; color: #58a6ff;'>GDM Portal</h2>", unsafe_allow_html=True)
    st.markdown("---")
    menu = st.radio("MAIN MENU", ["🏠 Dashboard", "📊 Analytics", "🧪 Predict Risk", "🧠 AI Insights"], index=0)
    st.markdown("---")
    st.caption("Developed by Clinical AI Dept")

# --- DASHBOARD ---
if menu == "🏠 Dashboard":
    st.markdown("<h1 class='main-title'>Clinical Overview</h1>", unsafe_allow_html=True)
    st.write("Real-time monitoring of Gestational Diabetes risk factors.")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("Total Patients", len(df))
    with col2: st.metric("Diabetic Cases", len(df[df['Outcome']==1]))
    with col3: st.metric("Normal Range", len(df[df['Outcome']==0]))
    with col4: st.metric("Model Acc", "75.3%")
    
    st.markdown("<div class='section-container'>", unsafe_allow_html=True)
    st.subheader("Recent Patient Trends")
    fig = px.line(df.groupby('Age')['Glucose'].mean().reset_index(), x='Age', y='Glucose', 
                  title="Average Glucose by Age Group", template="plotly_dark", color_discrete_sequence=['#58a6ff'])
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- ANALYTICS ---
elif menu == "📊 Analytics":
    st.markdown("<h1 class='main-title'>Data Analytics</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='section-container'>", unsafe_allow_html=True)
        fig = px.histogram(df, x="BMI", color="Outcome", barmode="overlay", template="plotly_dark", title="BMI vs Outcome")
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='section-container'>", unsafe_allow_html=True)
        fig = px.scatter(df, x="Glucose", y="Insulin", color="Outcome", template="plotly_dark", title="Glucose-Insulin Correlation")
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# --- PREDICTION ---
elif menu == "🧪 Predict Risk":
    st.markdown("<h1 class='main-title'>Risk Predictor</h1>", unsafe_allow_html=True)
    
    col_input, col_res = st.columns([1, 1], gap="large")
    
    with col_input:
        st.markdown("<div class='section-container'>", unsafe_allow_html=True)
        st.subheader("🧬 Clinical Inputs")
        
        c1, c2 = st.columns(2)
        with c1:
            preg = st.number_input("Pregnancies", 0, 20, 3)
            glu = st.number_input("Glucose Level", 0, 400, 120)
            bp = st.number_input("Blood Pressure", 0, 150, 70)
            skin = st.number_input("Skin Thickness", 0, 100, 20)
        with c2:
            ins = st.number_input("Insulin Level", 0, 900, 79)
            bmi = st.number_input("BMI Index", 0.0, 70.0, 32.0)
            dpf = st.number_input("Diabetes Func", 0.0, 3.0, 0.47)
            age = st.number_input("Age", 0, 100, 31)
            
        predict_btn = st.button("RUN AI ANALYSYS")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_res:
        if predict_btn:
            input_data = pd.DataFrame([[preg, glu, bp, skin, ins, bmi, dpf, age]], 
                                    columns=['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age'])
            prob = model.predict_proba(input_data)[0][1] * 100
            
            st.markdown("<div class='section-container'>", unsafe_allow_html=True)
            st.subheader("🎯 Result")
            
            fig = go.Figure(go.Indicator(
                mode = "gauge+number", value = prob,
                gauge = {'axis': {'range': [None, 100]}, 'bar': {'color': "#58a6ff"}},
                title = {'text': "GDM Risk Probability", 'font': {'size': 18}}
            ))
            fig.update_layout(height=250, paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"}, margin=dict(l=20,r=20,t=50,b=20))
            st.plotly_chart(fig, use_container_width=True)
            
            if prob > 50:
                st.error("🚨 HIGH RISK ALERT")
                st.info("The AI suggests clinical monitoring is necessary.")
            else:
                st.success("✅ LOW RISK")
                st.write("Patient is within early safety parameters.")
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            if lottie_scanning:
                st_lottie(lottie_scanning, height=350)
            else:
                st.info("Please fill clinical data and click Analysis.")

# --- AI INSIGHTS ---
elif menu == "🧠 AI Insights":
    st.markdown("<h1 class='main-title'>Model Intelligence</h1>", unsafe_allow_html=True)
    
    st.markdown("<div class='section-container'>", unsafe_allow_html=True)
    st.subheader("Feature Importance")
    importances = model.feature_importances_
    feats = df.drop('Outcome', axis=1).columns
    f_df = pd.DataFrame({'Feature': feats, 'Weight': importances}).sort_values('Weight', ascending=True)
    fig = px.bar(f_df, x='Weight', y='Feature', orientation='h', template="plotly_dark", color_discrete_sequence=['#58a6ff'])
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# FOOTER
st.markdown("---")
st.markdown("<center><p style='color: #8b949e;'>GDM AI Clinical Decision System v3.0 | 2026</p></center>", unsafe_allow_html=True)
