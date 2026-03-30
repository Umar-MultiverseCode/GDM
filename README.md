# 🧬 GDM AI: Clinical Decision Support System

[![Streamlit App](https://static.streamlit.io/badge_streamlit.svg)](https://share.streamlit.io/)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An advanced, AI-powered diagnostic portal designed for early detection of **Gestational Diabetes Mellitus (GDM)**. This system leverages ensemble learning (Random Forest) to provide clinicians with sub-second risk assessments based on a set of 8 clinical parameters.

---

## 🚀 Key Features

-   **🧠 Predictive Intelligence**: Utilizes a trained Random Forest classifier with 75%+ accuracy for risk identification.
-   **📊 Dynamic Clinical Analytics**: Interactive 3D vector space and sunburst charts to visualize patient distributions.
-   **🧬 Real-time Risk Engine**: Dynamic radar charts that compare individual patient profiles against general averages.
-   **👨‍⚕️ AI Doctor Consultation**: Simulated clinical insight engine that provides automated medical recommendations.
-   **📈 Model Transparency (XAI)**: Detailed feature importance breakdown (SHAP approximation) to understand the "Why" behind every prediction.
-   **📑 Clinical Report Export**: Generate and download structured patient risk reports instantly.

---

## 🛠️ Technology Stack

-   **Core**: Python 3.10+
-   **Framework**: [Streamlit](https://streamlit.io/) (Premium Dark Mode UI)
-   **Machine Learning**: Scikit-learn (Random Forest)
-   **Visualizations**: Plotly Express & Graph Objects
-   **Aesthetics**: Glassmorphism CSS, Lucide Icons, Lottie Animations

---

## 💻 Installation & Setup

Follow these simple steps to get the clinical portal running on your local machine:

### 1. Clone the Repository
```bash
git clone https://github.com/Umar-MultiverseCode/GDM.git
cd GDM
```

### 2. Set Up Virtual Environment (Recommended)
```bash
# Create venv
python -m venv venv

# Activate venv (Windows)
.\venv\Scripts\activate

# Activate venv (Mac/Linux)
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Train the AI Model
```bash
python train_model.py
```

### 5. Launch the Portal
```bash
streamlit run app.py
```

---

## 🏛️ System Architecture

The GDM Clinical System follows a decoupled architecture ensuring data integrity and model reliability:

| Component | Responsibility | Technology |
| :--- | :--- | :--- |
| **Ingestion Engine** | Stochastic data augmentation & normalization | `Pandas`, `NumPy` |
| **Intelligence Core** | Ensemble learning (Random Forest) classification | `Scikit-learn` |
| **UX Layer** | Interactive clinical dashboard | `Streamlit` |
| **Telemetry** | Real-time logging & performance diagnostics | `Python Logging` |

---

## 🔬 Clinical Parameters Used

The model analyzes the following features to determine GDM susceptibility:
1.  **Pregnancies**: Number of times pregnant.
2.  **Glucose**: Plasma glucose concentration.
3.  **Blood Pressure**: Diastolic blood pressure (mm Hg).
4.  **Skin Thickness**: Triceps skin fold thickness (mm).
5.  **Insulin**: 2-Hour serum insulin (mu U/ml).
6.  **BMI**: Body mass index (weight in kg/(height in m)^2).
7.  **Diabetes Pedigree Function**: Family history impact score.
8.  **Age**: Patient age in years.

---

## 🚀 Future Roadmap

- [ ] **HL7 FHIR Integration**: Seamless connectivity with Hospital Information Systems.
- [ ] **CNN-based Analysis**: Incorporating ultrasound imaging data.
- [ ] **Multi-language Support**: Expanding clinical accessibility globally.
- [ ] **Mobile Clinical Companion**: Native iOS/Android app for bedside diagnostics.

---

## 🤝 Contribution & License

Contributions are welcome! Feel free to open a PR or report a bug.
Distributed under the MIT License. See `LICENSE` for more information.

---
**Developed with ❤️ for Medical Clinical Intelligence | Umar-MultiverseCode**

## Clinical Compliance
Designed with medical assessment guidelines in mind.

---
*Audit Log: Security & Privacy Compliant | Version 3.1*
