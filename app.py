import streamlit as st
import torch
import cv2
import tempfile
import numpy as np
from weed_stage import get_weed_stage
from weed_control import weed_control_advice

st.markdown("""
<style>
    /* Main background with gradient */
    .stApp {
        background: linear-gradient(135deg, #e8f5e9 0%, #f1f8e9 100%);
    }

    /* Main content area spacing */
    .main .block-container {
        padding-top: 1rem;
        padding-left: 0.5rem;
        padding-right: 1rem;
        max-width: 1200px;
    }

    /* Reduce gap between sidebar and main content */
    .css-1d391kg {
        padding-left: 0.2rem !important;
    }

    .css-1lcbmhc {
        padding-left: 0.2rem !important;
    }

    /* Further reduce main content padding */
    .stApp > div {
        padding-left: 0.5rem !important;
    }

    /* Title styling */
    h1 {
        color: #2e7d32;
        text-align: center;
        font-size: 3.5rem !important;
        font-weight: 700 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        padding: 1rem 0;
        margin-bottom: 1rem;
        white-space: nowrap;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.8rem;
    }

    /* Subheader styling */
    h2, h3 {
        color: #388e3c;
        font-weight: 600 !important;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2e7d32 0%, #388e3c 100%);
    }

    [data-testid="stSidebar"] * {
        color: white !important;
    }

    /* =============================== */
    /* 🎯 CONFIDENCE LEVEL SLIDER STYLE */
    /* =============================== */

    /* Confidence Level heading text */
    [data-testid="stSidebar"] .stSlider label {
        color: #a5d6a7 !important;   /* Light green */
        font-weight: 700;
        font-size: 1rem;
    }

    /* Slider container box */
    [data-testid="stSidebar"] .stSlider {
        background: rgba(255, 255, 255, 0.12);
        padding: 1rem;
        border-radius: 12px;
    }

    /* Slider track */
    [data-testid="stSidebar"] div[role="slider"] {
        background-color: rgba(255, 255, 255, 0.3) !important;
    }

    /* Filled slider portion */
    [data-testid="stSidebar"] div[role="slider"] > div {
        background-color: #a5d6a7 !important;
    }

    /* Slider thumb (circle) */
    [data-testid="stSidebar"] div[role="slider"] span {
        background-color: #66bb6a !important;
        border: 2px solid white !important;
    }

    /* Feature Card Styling */
    .feature-card {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease-in-out;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: center;
        border: 1px solid rgba(76, 175, 80, 0.2);
    }

    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
        border-color: rgba(76, 175, 80, 0.4);
    }

    .feature-card h3 {
        color: #2e7d32 !important;
        margin-top: 1rem;
        margin-bottom: 0.8rem;
        font-size: 1.4rem;
        font-weight: 600;
    }

    .feature-card p {
        color: #388e3c;
        font-size: 1rem;
        line-height: 1.6;
        margin: 0;
    }

    .feature-card div[style*="font-size: 4rem"] {
        color: #4caf50;
        margin-bottom: 1rem;
        transition: transform 0.3s ease;
    }

    .feature-card:hover div[style*="font-size: 4rem"] {
        transform: scale(1.1);
    }

    /* Section Header Styling */
    .section-header {
        color: #2e7d32;
        text-align: center;
        font-size: 2.5rem;
        font-weight: 700;
        margin-top: 3rem;
        margin-bottom: 2rem;
        position: relative;
    }

    .section-header::after {
        content: '';
        position: absolute;
        left: 50%;
        bottom: -10px;
        transform: translateX(-50%);
        width: 80px;
        height: 4px;
        background-color: #66bb6a;
        border-radius: 2px;
    }

    /* How It Works Card Styling */
    .how-it-works-card {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease-in-out;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: center;
        border: 1px solid rgba(76, 175, 80, 0.2);
    }

    .how-it-works-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
        border-color: rgba(76, 175, 80, 0.4);
    }

    .how-it-works-card h4 {
        color: #2e7d32 !important;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
        font-size: 1.2rem;
        font-weight: 600;
    }

    .how-it-works-card p {
        color: #558b2f;
        font-size: 0.95rem;
        line-height: 1.5;
        margin: 0;
    }

    .how-it-works-card div[style*="font-size: 3rem"] {
        color: #4caf50;
        margin-bottom: 0.8rem;
        transition: transform 0.3s ease;
    }

    .how-it-works-card:hover div[style*="font-size: 3rem"] {
        transform: scale(1.1);
    }

</style>
""", unsafe_allow_html=True)
 
# ------------------------------- 
# Sidebar Navigation & Info
# ------------------------------- 
with st.sidebar:
    st.markdown("# 🌾 Dashboard")
    st.markdown("---")
    
    st.markdown("### 📍 Navigation")
    st.markdown("""
    - 🏠 **Home**
    - 📊 **Analytics**
    - ⚙️ **Settings**
    - 📖 **Guide**
    """)
    
    st.markdown("---")
    
    st.markdown("### ⚙️ Detection Settings")
    confidence_threshold = st.slider(
        "🎯 Confidence Level",
        min_value=0.1,
        max_value=1.0,
        value=0.4,
        step=0.05,
        help="Adjust the sensitivity of weed detection"
    )
    
    st.markdown("---")
    
    st.markdown("### 📋 System Status")
    st.markdown("""
    **🤖 Model:** YOLOv5 Custom
    
    **📦 Version:** 1.0.0
    
    **🎯 Classes:** 2
    - 🌽 Maize
    - 🌿 Weeds
    """)
    
    st.markdown("---")
    
    st.markdown("### 💡 Quick Tips")
    st.markdown("""
    ✅ Use high-quality images
    
    ✅ Ensure good lighting
    
    ✅ Capture full plant view
    
    ✅ Avoid blurry images
    """)
    
    st.markdown("---")
    
    st.markdown("### 📞 Support")
    st.markdown("""
    📧 support@agritech.com
    
    🌐 www.agritech.com
    """)

# ------------------------------- 
# Load YOLOv5 Model
# ------------------------------- 
@st.cache_resource
def load_model():
    model_path = r"C:\Users\Akhila\HNC\weed_detection_using_single crop\yolov5\runs\train\maize_weed_v1\weights\best.pt"
    model = torch.hub.load(
        'ultralytics/yolov5',
        'custom',
        path=model_path,
        force_reload=True
    )
    return model

try:
    model = load_model()
except Exception as e:
    st.error(f"❌ Model Loading Failed: {e}")
    st.stop()

# ------------------------------- 
# Helper: Detect Objects
# ------------------------------- 
def detect_objects(image):
    results = model(image)
    detections = results.xyxy[0].cpu().numpy()
    
    weed_boxes = []
    crop_boxes = []
    
    for det in detections:
        x1, y1, x2, y2, conf, cls = det
        
        if conf < confidence_threshold:
            continue
            
        if int(cls) == 1:  # Weeds
            weed_boxes.append([x1, y1, x2, y2])
            color = (0, 0, 255)
            label = f"Weed {conf:.2f}"
        elif int(cls) == 0:  # Maize
            crop_boxes.append([x1, y1, x2, y2])
            color = (0, 255, 0)
            label = f"Maize {conf:.2f}"
        
        # Draw bounding box
        cv2.rectangle(
            image,
            (int(x1), int(y1)),
            (int(x2), int(y2)),
            color,
            3
        )
        
        # Background for label
        (w, h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
        cv2.rectangle(
            image,
            (int(x1), int(y1) - h - 10),
            (int(x1) + w, int(y1)),
            color,
            -1
        )
        
        # Label text
        cv2.putText(
            image,
            label,
            (int(x1), int(y1) - 5),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2
        )
    
    return image, weed_boxes, crop_boxes

# ===============================
# MAIN LAYOUT - HERO SECTION
# ===============================
st.markdown("""
<div style="display: flex; align-items: center; justify-content: center; gap: 1rem; margin-bottom: 1rem;">
    <h1 style="color: #2e7d32; font-size: 3.5rem !important; font-weight: 700 !important; text-shadow: 2px 2px 4px rgba(0,0,0,0.1); margin: 0; display: flex; align-items: center; gap: 0.5rem;">
        🌽 Maize Weed Detection & Control System
    </h1>
</div>
<div style="text-align: center; margin-bottom: 2rem;">
    <p style="color: #1b5e20; font-size: 1.2rem; font-weight: 500; margin: 0;">
        Intelligent Agricultural Monitoring Powered by Advanced AI Technology
    </p>
</div>
""", unsafe_allow_html=True)

# Hero Image/Icon Section
st.markdown("""
<div class="hero-section" style="text-align: center; margin-bottom: 3rem;">
    <h2 style="color: #2e7d32; margin-bottom: 1rem; display: flex; align-items: center; justify-content: center; gap: 0.8rem;">
        <span style="font-size: 2.5rem;">🌱</span> Transform Your Farm with AI-Powered Weed Detection
    </h2>
    <p style="font-size: 1.1rem; color: #558b2f; max-width: 800px; margin: 0 auto; line-height: 1.8;">
        Our cutting-edge system uses advanced machine learning to identify weeds in your maize fields, 
        providing real-time analysis and actionable recommendations to optimize your crop yield.
    </p>
</div>
""", unsafe_allow_html=True)

# ===============================
# FEATURES SECTION
# ===============================
st.markdown('<h2 class="section-header">✨ Key Features</h2>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div style="font-size: 4rem; margin-bottom: 1rem;">🎯</div>
        <h3 style="color: #388e3c; margin-bottom: 1rem;">Accurate Detection</h3>
        <p style="color: #558b2f; line-height: 1.6;">
            AI-powered weed and crop identification with high precision using state-of-the-art YOLOv5 technology.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div style="font-size: 4rem; margin-bottom: 1rem;">📊</div>
        <h3 style="color: #388e3c; margin-bottom: 1rem;">Real-time Analysis</h3>
        <p style="color: #558b2f; line-height: 1.6;">
            Instant statistics and weed infestation metrics to help you make informed decisions quickly.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div style="font-size: 4rem; margin-bottom: 1rem;">🛠️</div>
        <h3 style="color: #388e3c; margin-bottom: 1rem;">Smart Recommendations</h3>
        <p style="color: #558b2f; line-height: 1.6;">
            Tailored weed control strategies based on growth stage and infestation level for optimal results.
        </p>
    </div>
    """, unsafe_allow_html=True)

# Additional Features Row
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div style="font-size: 4rem; margin-bottom: 1rem;">🎥</div>
        <h3 style="color: #388e3c; margin-bottom: 1rem;">Video Support</h3>
        <p style="color: #558b2f; line-height: 1.6;">
            Process entire videos for comprehensive field analysis and monitoring over time.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div style="font-size: 4rem; margin-bottom: 1rem;">⚡</div>
        <h3 style="color: #388e3c; margin-bottom: 1rem;">Fast Processing</h3>
        <p style="color: #558b2f; line-height: 1.6;">
            Get results in seconds with our optimized detection pipeline and cloud infrastructure.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div style="font-size: 4rem; margin-bottom: 1rem;">📈</div>
        <h3 style="color: #388e3c; margin-bottom: 1rem;">Detailed Reports</h3>
        <p style="color: #558b2f; line-height: 1.6;">
            Comprehensive analytics including weed count, infestation rate, and growth stage classification.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ===============================
# HOW IT WORKS SECTION
# ===============================
st.markdown('<h2 class="section-header">🔄 How It Works</h2>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="how-it-works-card">
        <div style="font-size: 3rem; margin-bottom: 0.8rem;">1️⃣</div>
        <h4>Upload</h4>
        <p>Upload your field image or video</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="how-it-works-card">
        <div style="font-size: 3rem; margin-bottom: 0.8rem;">2️⃣</div>
        <h4>Analyze</h4>
        <p>AI detects weeds and crops</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="how-it-works-card">
        <div style="font-size: 3rem; margin-bottom: 0.8rem;">3️⃣</div>
        <h4>Review</h4>
        <p>Get detailed statistics</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="how-it-works-card">
        <div style="font-size: 3rem; margin-bottom: 0.8rem;">4️⃣</div>
        <h4>Act</h4>
        <p>Apply recommendations</p>
    </div>
    """, unsafe_allow_html=True)

# UPLOAD SECTION
# ===============================
st.markdown('<h2 class="section-header">📤 Upload Your Field Data</h2>', unsafe_allow_html=True)

st.markdown("""
<div class="upload-section feature-card">
    <div style="text-align: center; margin-bottom: 2rem;">
        <div style="font-size: 4rem; margin-bottom: 1rem;">📁</div>
        <h3 style="color: #2e7d32; margin-bottom: 0.5rem;">Ready to Analyze Your Field?</h3>
        <p style="color: #558b2f; font-size: 1.1rem;">
            Upload an image or video of your maize field to get started. 
            Supported formats: JPG, PNG, MP4, AVI
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Choose a file",
    type=["jpg", "jpeg", "png", "mp4", "avi"],
    help="Upload an image or video file for weed detection analysis"
)

st.markdown("---")

# ===============================
# IMAGE PROCESSING
# ===============================
if uploaded_file and uploaded_file.type.startswith("image"):
    with st.spinner("🔍 Analyzing your field image... Please wait."):
        image = cv2.imdecode(
            np.frombuffer(uploaded_file.read(), np.uint8),
            cv2.IMREAD_COLOR
        )
        
        processed_image, weed_boxes, crop_boxes = detect_objects(image)
    
    st.success("✅ Analysis Complete!")
    st.markdown('<h2 class="section-header">📊 Detection Results</h2>', unsafe_allow_html=True)
    
    # Display results
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📸 Annotated Image")
        st.image(processed_image, channels="BGR", use_column_width=True)

    with col2:
        st.markdown("### 📈 Field Statistics")
        
        st.metric(
            label="🌾 Maize Plants Detected",
            value=len(crop_boxes),
            delta="Healthy Crop Count"
        )
        
        st.metric(
            label="🌿 Weeds Detected",
            value=len(weed_boxes),
            delta="Requires Attention" if len(weed_boxes) > 0 else "Clean Field",
            delta_color="inverse" if len(weed_boxes) > 0 else "normal"
        )
        
        if len(crop_boxes) + len(weed_boxes) > 0:
            infestation = (len(weed_boxes) / (len(crop_boxes) + len(weed_boxes))) * 100
            st.metric(
                label="⚠️ Infestation Rate",
                value=f"{infestation:.1f}%",
                delta="Critical" if infestation > 30 else "Moderate" if infestation > 10 else "Low",
                delta_color="inverse" if infestation > 10 else "normal"
            )
    
    st.markdown("---")
    
    # Weed Analysis
    weed_stage = get_weed_stage(weed_boxes)
    control = weed_control_advice(weed_stage)
    
    st.markdown('<h2 class="section-header">🌿 Weed Management Plan</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="info-card">
            <h3 style="color: #388e3c; margin-top: 0;">🔬 Weed Growth Stage</h3>
            <p style="font-size: 1.5rem; font-weight: 700; color: #2e7d32; margin: 1.5rem 0;">
                {weed_stage}
            </p>
            <p style="color: #558b2f; font-size: 0.95rem;">
                Classification based on detected weed count and distribution pattern
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if isinstance(control, dict):
            st.markdown(f"""
            <div class="info-card">
                <h3 style="color: #388e3c; margin-top: 0;">🛠️ Recommended Action</h3>
                <p style="font-size: 1.3rem; font-weight: 700; color: #2e7d32; margin: 1rem 0;">
                    {control['method']}
                </p>
                <p style="color: #558b2f; margin: 0.8rem 0;">
                    <strong>📋 Reason:</strong> {control['reason']}
                </p>
                <p style="color: #558b2f; margin: 0.8rem 0;">
                    <strong>💊 Treatment:</strong> {control['chemical']}
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="info-card">
                <h3 style="color: #388e3c; margin-top: 0;">🛠️ Recommendation</h3>
                <p style="color: #558b2f; font-size: 1.1rem; line-height: 1.6;">{control}</p>
            </div>
            """, unsafe_allow_html=True)

# ===============================
# VIDEO PROCESSING
# ===============================
elif uploaded_file and uploaded_file.type.startswith("video"):
    st.markdown('<h2 class="section-header">🎥 Video Analysis in Progress</h2>', unsafe_allow_html=True)
    
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())
    
    cap = cv2.VideoCapture(tfile.name)
    stframe = st.empty()
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    all_weed_boxes = []
    all_crop_boxes = []
    frame_count = 0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        processed_frame, weed_boxes, crop_boxes = detect_objects(frame)
        all_weed_boxes.extend(weed_boxes)
        all_crop_boxes.extend(crop_boxes)
        
        stframe.image(processed_frame, channels="BGR", use_container_width=True)
        
        frame_count += 1
        progress = frame_count / total_frames
        progress_bar.progress(progress)
        status_text.text(f"🎬 Processing: Frame {frame_count}/{total_frames}")
    
    cap.release()
    progress_bar.empty()
    status_text.empty()
    
    st.success("✅ Video Analysis Complete!")
    st.markdown("---")
    
    # Video Results
    st.markdown('<h2 class="section-header">📊 Video Analysis Results</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("🌾 Total Maize Detected", len(all_crop_boxes))
    
    with col2:
        st.metric("🌿 Total Weeds Detected", len(all_weed_boxes))
    
    with col3:
        if len(all_crop_boxes) + len(all_weed_boxes) > 0:
            infestation = (len(all_weed_boxes) / (len(all_crop_boxes) + len(all_weed_boxes))) * 100
            st.metric("⚠️ Infestation Rate", f"{infestation:.1f}%")
    
    st.markdown("---")
    
    # Weed Analysis
    weed_stage = get_weed_stage(all_weed_boxes)
    control = weed_control_advice(weed_stage)
    
    st.markdown('<h2 class="section-header">🌿 Weed Management Plan</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="info-card">
            <h3 style="color: #388e3c; margin-top: 0;">🔬 Weed Growth Stage</h3>
            <p style="font-size: 1.5rem; font-weight: 700; color: #2e7d32; margin: 1.5rem 0;">
                {weed_stage}
            </p>
            <p style="color: #558b2f; font-size: 0.95rem;">
                Analysis based on {frame_count} frames processed
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if isinstance(control, dict):
            st.markdown(f"""
            <div class="info-card">
                <h3 style="color: #388e3c; margin-top: 0;">🛠️ Recommended Action</h3>
                <p style="font-size: 1.3rem; font-weight: 700; color: #2e7d32; margin: 1rem 0;">
                    {control['method']}
                </p>
                <p style="color: #558b2f; margin: 0.8rem 0;">
                    <strong>📋 Reason:</strong> {control['reason']}
                </p>
                <p style="color: #558b2f; margin: 0.8rem 0;">
                    <strong>💊 Treatment:</strong> {control['chemical']}
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="info-card">
                <h3 style="color: #388e3c; margin-top: 0;">🛠️ Recommendation</h3>
                <p style="color: #558b2f; font-size: 1.1rem; line-height: 1.6;">{control}</p>
            </div>
            """, unsafe_allow_html=True)

# ===============================
# FOOTER
# ===============================
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem 1rem; background: linear-gradient(135deg, rgba(255,255,255,0.9) 0%, rgba(245,245,245,0.9) 100%); border-radius: 15px; margin-top: 3rem;">
    <h3 style="color: #2e7d32; margin-bottom: 1rem;">🌾 Powered by Advanced AI Technology 🌾</h3>
    <p style="color: #558b2f; margin-top: 1rem;">
         Agricultural AI Solutions | Making Farming Smarter
    </p>
</div>
""", unsafe_allow_html=True)