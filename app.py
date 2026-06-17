
import pickle
import streamlit as st
from streamlit_option_menu import option_menu
import os
from PIL import Image

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="Heart Disease Prediction System",
    page_icon="❤️",
    layout="wide"
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------
st.markdown("""
<style>

/* Main Background */
.stApp {
    background-color: #FFF0F5;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #8B0000;
}

[data-testid="stSidebar"] * {
    color: white;
}

/* Buttons */
.stButton > button {
    background-color: #DC143C;
    color: white;
    border-radius: 10px;
    height: 3em;
    width: 100%;
    font-size: 18px;
    font-weight: bold;
    border: none;
}

.stButton > button:hover {
    background-color: #B22222;
    color: white;
}

/* Text Inputs */
.stTextInput input {
    border: 2px solid #DC143C;
    border-radius: 8px;
}

/* Footer */
.footer {
    text-align: center;
    color: #8B0000;
    font-size: 16px;
    margin-top: 40px;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# LOAD MODEL
# --------------------------------------------------
working_dir = os.path.dirname(os.path.abspath(__file__))

heart_disease_model = pickle.load(
    open(f'{working_dir}/saved_models/heart_disease_model.sav', 'rb')
)

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
with st.sidebar:
    selected = option_menu(
        "Disease Prediction System",
        ["Heart Disease Prediction"],
        menu_icon="hospital-fill",
        icons=["heart"],
        default_index=0
    )

# --------------------------------------------------
# HEART DISEASE PAGE
# --------------------------------------------------
if selected == "Heart Disease Prediction":

    # Dashboard Header
    st.markdown("""
    <div style="
    background-color:#DC143C;
    padding:20px;
    border-radius:15px;
    text-align:center;
    margin-bottom:20px;">

    <h1 style="color:white;">
    ❤️ Heart Disease Prediction System
    </h1>

    <p style="color:white;font-size:18px;">
    Machine Learning Based Cardiovascular Risk Assessment
    </p>

    </div>
    """, unsafe_allow_html=True)

    # Optional Header Image
    try:
        header_image_path = "images/header_image.png"

        if os.path.exists(header_image_path):
            st.image(
                header_image_path,
                use_container_width=True
            )

    except Exception:
        pass

    st.info(
        "Enter the patient's medical information below and click the prediction button."
    )

    # --------------------------------------------------
    # INPUT FIELDS
    # --------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:
        age = st.text_input("Age")

    with col2:
        sex_option = st.selectbox(
            "Sex",
            ["Male", "Female"]
        )
        sex_val = 1 if sex_option == "Male" else 0

    with col3:
        cp_val = st.selectbox(
            "Chest Pain Type",
            [0, 1, 2, 3]
        )

    with col1:
        trestbps = st.text_input(
            "Resting Blood Pressure"
        )

    with col2:
        chol = st.text_input(
            "Serum Cholesterol (mg/dl)"
        )

    with col3:
        fbs_val = st.selectbox(
            "Fasting Blood Sugar > 120 mg/dl",
            [0, 1]
        )

    with col1:
        restecg_val = st.selectbox(
            "Resting ECG Results",
            [0, 1, 2]
        )

    with col2:
        thalach = st.text_input(
            "Maximum Heart Rate Achieved"
        )

    with col3:
        exang_val = st.selectbox(
            "Exercise Induced Angina",
            [0, 1]
        )

    with col1:
        oldpeak = st.text_input(
            "ST Depression (Oldpeak)"
        )

    with col2:
        slope_val = st.selectbox(
            "Slope of Peak Exercise ST Segment",
            [0, 1, 2]
        )

    with col3:
        ca_val = st.selectbox(
            "Major Vessels Colored by Fluoroscopy",
            [0, 1, 2, 3, 4]
        )

    with col1:
        thal_val = st.selectbox(
            "Thal",
            [0, 1, 2, 3]
        )

    # --------------------------------------------------
    # PREDICTION
    # --------------------------------------------------

    if st.button("🔍 Predict Heart Disease"):

        text_inputs_to_check = [
            age,
            trestbps,
            chol,
            thalach,
            oldpeak
        ]

        if any(val == "" for val in text_inputs_to_check):
            st.warning(
                "Please fill in all numerical input fields."
            )

        else:

            try:

                input_data = [
                    float(age),
                    sex_val,
                    cp_val,
                    float(trestbps),
                    float(chol),
                    fbs_val,
                    restecg_val,
                    float(thalach),
                    exang_val,
                    float(oldpeak),
                    slope_val,
                    ca_val,
                    thal_val
                ]

                prediction = heart_disease_model.predict(
                    [input_data]
                )

                if prediction[0] == 1:

                    st.error("""
                    ⚠️ High Risk Detected

                    The model predicts that the patient may have heart disease.

                    Please consult a healthcare professional for further medical evaluation.
                    """)

                else:

                    st.success("""
                    ✅ Low Risk Detected

                    The model predicts that the patient is unlikely to have heart disease.
                    """)

            except ValueError:

                st.error(
                    "Please enter valid numerical values."
                )

    # --------------------------------------------------
    # FOOTER
    # --------------------------------------------------

    st.markdown("""
    <div class="footer">

    ❤️ Heart Disease Prediction System

    Developed by Catherine Abimiku

    📧 your_email@abimikucatherine4@gmail.com

    </div>
    """, unsafe_allow_html=True)
