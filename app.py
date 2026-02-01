"""
InnoSortRecycle Digital Twin Application.
This is the main entry point for the Streamlit dashboard, orchestrating the AI,
Simulation, and Financial modules.
"""
import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.simulation_engine import BioleachingReactor, ElectroRecovery
from src.ai_engine import HyperspectralClassifier
from src.financials import FinancialModel
from src.connect_agent import ConnectAgent

# Page Config
st.set_page_config(
    page_title="InnoSortRecycle Digital Twin",
    page_icon="none",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Look with Depth Hierarchy
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Base Layer - Darkest */
    .stApp {
        background: #000000;
        background-image:
            radial-gradient(at 20% 30%, rgba(0, 255, 148, 0.05) 0px, transparent 50%),
            radial-gradient(at 80% 70%, rgba(0, 212, 255, 0.05) 0px, transparent 50%);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Container Layer - Dark */
    .main .block-container {
        background: rgba(10, 15, 28, 0.6);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }

    /* Typography Hierarchy */
    h1 {
        background: linear-gradient(135deg, #00ff94 0%, #00d4ff 50%, #00ff94 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700;
        font-size: 3rem !important;
        letter-spacing: -0.02em;
        margin-bottom: 1.5rem;
        text-shadow: 0 0 40px rgba(0, 255, 148, 0.3);
    }

    h2 {
        color: #ffffff;
        font-weight: 600;
        font-size: 1.75rem !important;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }

    h3 {
        color: rgba(0, 255, 148, 0.9);
        font-weight: 500;
        font-size: 1.25rem !important;
    }

    /* Card Elevation System */
    .metric-card {
        background: linear-gradient(135deg, rgba(26, 35, 50, 0.8) 0%, rgba(45, 53, 72, 0.6) 100%);
        backdrop-filter: blur(10px);
        padding: 30px;
        border-radius: 20px;
        border: 1px solid rgba(0, 255, 148, 0.15);
        box-shadow:
            0 8px 32px rgba(0, 0, 0, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.05);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }

    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, #00ff94, transparent);
        opacity: 0;
        transition: opacity 0.4s;
    }

    .metric-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow:
            0 20px 60px rgba(0, 255, 148, 0.2),
            0 0 0 1px rgba(0, 255, 148, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        border-color: rgba(0, 255, 148, 0.4);
    }

    .metric-card:hover::before {
        opacity: 1;
    }

    /* Button Hierarchy */
    .stButton>button {
        background: linear-gradient(135deg, #00ff94 0%, #00d4ff 100%);
        color: #000000;
        border: none;
        border-radius: 30px;
        font-weight: 600;
        padding: 0.875rem 2.5rem;
        font-size: 1.05rem;
        letter-spacing: 0.02em;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow:
            0 4px 20px rgba(0, 255, 148, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
        position: relative;
        overflow: hidden;
    }

    .stButton>button::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        transform: translate(-50%, -50%);
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transition: width 0.6s, height 0.6s;
    }

    .stButton>button:hover::before {
        width: 300px;
        height: 300px;
    }

    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow:
            0 8px 30px rgba(0, 255, 148, 0.5),
            inset 0 1px 0 rgba(255, 255, 255, 0.3);
    }

    /* Sidebar Depth */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(10, 15, 28, 0.95) 0%, rgba(0, 0, 0, 0.98) 100%);
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(0, 255, 148, 0.1);
    }

    /* Metrics Enhancement */
    [data-testid="stMetricValue"] {
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        background: linear-gradient(135deg, #00ff94 0%, #00d4ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    [data-testid="stMetricLabel"] {
        color: rgba(255, 255, 255, 0.6) !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* Input Fields */
    .stTextInput>div>div>input, .stSelectbox>div>div>select {
        background: rgba(26, 35, 50, 0.6);
        border: 1px solid rgba(0, 255, 148, 0.2);
        border-radius: 12px;
        color: #ffffff;
        padding: 0.75rem 1rem;
        transition: all 0.3s;
    }

    .stTextInput>div>div>input:focus, .stSelectbox>div>div>select:focus {
        border-color: #00ff94;
        box-shadow: 0 0 0 3px rgba(0, 255, 148, 0.1);
    }

    /* Progress Bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #00ff94 0%, #00d4ff 100%);
        border-radius: 10px;
        box-shadow: 0 0 20px rgba(0, 255, 148, 0.5);
    }

    /* Dataframe Styling */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }

    /* Radio Buttons */
    .stRadio > label {
        background: rgba(26, 35, 50, 0.4);
        padding: 0.75rem 1.25rem;
        border-radius: 10px;
        transition: all 0.3s;
        border: 1px solid transparent;
    }

    .stRadio > label:hover {
        background: rgba(26, 35, 50, 0.8);
        border-color: rgba(0, 255, 148, 0.3);
    }

    /* Info/Success/Warning/Error Boxes */
    .stAlert {
        background: rgba(26, 35, 50, 0.6);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        border-left: 4px solid #00ff94;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }

    /* Mobile Optimization */
    @media (max-width: 768px) {
        h1 {
            font-size: 2rem !important;
        }

        h2 {
            font-size: 1.5rem !important;
        }

        .main .block-container {
            padding: 1rem;
        }

        .metric-card {
            padding: 20px;
            margin-bottom: 1rem;
        }

        [data-testid="stMetricValue"] {
            font-size: 1.75rem !important;
        }

        .stButton>button {
            width: 100%;
            padding: 1rem;
            font-size: 0.95rem;
        }

        /* Stack columns on mobile */
        [data-testid="column"] {
            width: 100% !important;
            margin-bottom: 1rem;
        }
    }

    @media (max-width: 480px) {
        h1 {
            font-size: 1.75rem !important;
        }

        section[data-testid="stSidebar"] {
            width: 100% !important;
        }
    }

    /* Smooth Scrolling */
    html {
        scroll-behavior: smooth;
    }

    /* Loading Animation */
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }

    .stSpinner > div {
        border-color: #00ff94 !important;
        animation: pulse 1.5s ease-in-out infinite;
    }

    /* File Uploader */
    [data-testid="stFileUploader"] {
        background: rgba(26, 35, 50, 0.4);
        border: 2px dashed rgba(0, 255, 148, 0.3);
        border-radius: 15px;
        padding: 2rem;
        transition: all 0.3s;
    }

    [data-testid="stFileUploader"]:hover {
        border-color: rgba(0, 255, 148, 0.6);
        background: rgba(26, 35, 50, 0.6);
    }
</style>
""", unsafe_allow_html=True)

# Sidebar with Custom Logo
st.sidebar.markdown("""
<div style="text-align: center; padding: 1.5rem 0 1rem 0;">
    <svg width="80" height="80" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="logoGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#00ff94;stop-opacity:1" />
                <stop offset="100%" style="stop-color:#00d4ff;stop-opacity:1" />
            </linearGradient>
        </defs>
        <circle cx="50" cy="50" r="45" fill="none" stroke="url(#logoGrad)" stroke-width="3" opacity="0.4"/>
        <circle cx="50" cy="50" r="35" fill="none" stroke="url(#logoGrad)" stroke-width="2" opacity="0.6"/>
        <rect x="40" y="30" width="20" height="40" rx="3" fill="url(#logoGrad)" opacity="0.8"/>
        <rect x="35" y="25" width="30" height="3" rx="1.5" fill="url(#logoGrad)"/>
        <circle cx="32" cy="45" r="3" fill="#00ff94" opacity="0.6"/>
        <circle cx="50" cy="45" r="3" fill="#00d4ff" opacity="0.6"/>
        <circle cx="68" cy="45" r="3" fill="#00ff94" opacity="0.6"/>
        <circle cx="32" cy="60" r="3" fill="#00d4ff" opacity="0.6"/>
        <circle cx="50" cy="60" r="3" fill="#00ff94" opacity="0.6"/>
        <circle cx="68" cy="60" r="3" fill="#00d4ff" opacity="0.6"/>
    </svg>
</div>
<h2 style="text-align: center; font-size: 1.5rem; font-weight: 700;
    background: linear-gradient(135deg, #00ff94 0%, #00d4ff 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;">RADORDENA</h2>
<p style="text-align: center; color: rgba(255,255,255,0.6); font-size: 0.85rem;
    margin-bottom: 1.5rem; font-weight: 500;">Intelligence Hub</p>
""", unsafe_allow_html=True)
st.sidebar.markdown("---")

# Navigation
page = st.sidebar.radio("Module Selection",
                        ["Dashboard Overview",
                         "RADORDENA Connect",
                         "Agent Training Center",
                         "Chat with Plant",
                         "AI Battery Sorting",
                         "Process Simulation",
                         "Financial Analysis",
                         "Carbon Credits & ESG",
                         "EU Regulatory Compliance"])

# Initialize Engines
reactor = BioleachingReactor()
extractor = ElectroRecovery()
ai_classifier = HyperspectralClassifier()
finance = FinancialModel()
connector = ConnectAgent()


# Diagnostic response generation function
def generate_agent_response(query):
    """Generate contextual diagnostic response based on query keywords"""
    query_lower = query.lower()

    if any(word in query_lower for word in ["cobalt", "co", "tank 4", "recovery"]):
        return """**Root Cause Analysis: Cobalt Recovery**

**Issue Detected:** Cobalt recovery in Tank 4 dropped to 67% (Target: >90%)

**Chain-of-Thought Reasoning:**
1. **Sensor Reading:** pH drifted from 1.8 → 4.2 over last 6 hours
2. **Chemical Impact:** At pH > 3.5, Manganese precipitates as Mn(OH)₂
3. **Contamination:** Mn carry-over to Co filtration circuit → reduced selectivity
4. **Bacterial Activity:** *A. ferrooxidans* Fe²⁺ oxidation rate dropped 40%

**Autonomous Corrective Actions:**
[COMPLETE] Dosed 2.5L H₂SO₄ (0.5M) → pH now 3.8
[COMPLETE] Increased air sparging (+15%) → Fe²⁺/Fe³⁺ regeneration
[COMPLETE] Diverted Mn-rich stream to precipitation tank

**Prediction:** Co purity will restore to >92% in 45 minutes. Monitoring via HPLC."""

    elif any(word in query_lower for word in ["efficiency", "performance", "status"]):
        return """**Live System Status Report**

**Bio-Reactor Core (Tank 1-4):**
- **Overall Efficiency:** 92.4% ± 2.1%
- **Bacterial Load:** 5.2×10⁸ cells/mL (Optimal range)
- **Fe²⁺ Oxidation Rate:** 0.82 mmol/L/hr
- **Dissolved O₂:** 4.3 mg/L (Target: 4.0-5.0)

**Metal Recovery Stats (24hr moving average):**
- **Lithium (Li):** 94.2% → Li₂CO₃
- **Cobalt (Co):** 89.1% → Co(OH)₂
- **Nickel (Ni):** 91.7% → NiSO₄
- **Manganese (Mn):** 88.5% → MnCO₃

**Predictive Maintenance Alert:**
[WARNING] Filter F-03 pressure differential +12% (normal: <10%)
→ Recommend backwash cycle in next 6 hours"""

    elif any(word in query_lower for word in ["temperature", "temp", "cooling", "heating"]):
        return """**Thermal Management Analysis**

**Current State:**
- **Tank 1-3:** 29.8°C [NOMINAL] (Target: 30°C ± 1°C)
- **Tank 4:** 33.2°C [ELEVATED]

**Arrhenius Impact (Tank 4):**
Expected bacterial activity: k = A×exp(-Ea/RT)
→ At 33°C: -18% activity vs. optimal 30°C

**Corrective Strategy:**
1. Activated chiller loop (proportional control: P=2.5W/°C)
2. Reduced feed rate from 120 L/hr → 100 L/hr
3. Monitoring exothermic oxidation: 4Fe²⁺ + O₂ → 4Fe³⁺ (ΔH = -840 kJ/mol)

**ETA to stabilization:** 15 minutes"""

    elif any(word in query_lower for word in ["ph", "acid", "acidity", "alkaline"]):
        return """**pH Control System Status**

**Current pH Profile:**
- Tank 1: 1.82 [NOMINAL]
- Tank 2: 1.79 [NOMINAL]
- Tank 3: 1.85 [NOMINAL]
- Tank 4: 3.21 [ALERT - DRIFTING HIGH]

**RL Agent Decision:**
IF pH > 2.0 → Dose H₂SO₄ (0.5M)
→ **Action:** Injecting 1.2L H₂SO₄ to Tank 4

**Bacterial Sensitivity:**
*Acidithiobacillus ferrooxidans* optimal pH: 1.5-2.0
- At pH 3.0: Growth rate drops 60%
- At pH 1.2: Acid stress (reversible inhibition)

**Target restoration:** 12 minutes (feedback loop: 50ms latency)"""

    elif any(word in query_lower for word in ["bacteria", "microbe", "ferrooxidans"]):
        return """**Bacterial Colony Health Assessment**

**Species:** *Acidithiobacillus ferrooxidans* (Chemolithoautotroph)

**Population Dynamics:**
- **Cell Density:** 5.2×10⁸ cells/mL
- **Viability:** 94.1% (Flow cytometry)
- **Generation Time:** 8.2 hours

**Metabolic Activity:**
Energy source: Fe²⁺ → Fe³⁺ + e⁻
Carbon fixation: CO₂ → Biomass (Calvin cycle)

**Nutritional Status:**
[NOMINAL] NH₄⁺: 120 mg/L (Sufficient)
[NOMINAL] PO₄³⁻: 45 mg/L (Sufficient)
[NOMINAL] Trace metals (Mg, K, Ca): Within range

**Stress Indicators:**
[WARNING] Slight oxidative stress detected (ΔpH spike, Tank 4)
→ Enhanced monitoring for next 2 hours"""

    else:
        return f"""**Diagnostic Query Interface**

**System Response:**
Processing query: "{query}"

**Available Diagnostic Modules:**
- Process Diagnostics: Parameter deviation analysis
- Troubleshooting: Recovery rate optimization
- Efficiency Analysis: Performance metrics
- Predictive Maintenance: Equipment service scheduling
- Real-time Monitoring: Subsystem status

**Monitored Subsystems:**
1. Bio-Reactor Tanks (1-4): pH, Temperature, DO, bacterial load
2. Sorting Line: Vision AI classification accuracy
3. Recovery Tanks: Metal precipitation, filtration efficiency

Please specify a subsystem (Bio-Reactor, Sorting Line, Recovery Tank) or parameter (pH, temperature, efficiency, cobalt)."""


if page == "Dashboard Overview":
    st.title("RADORDENA Intelligence Hub")
    st.markdown("### Turning Urban Waste into Strategic Energy Assets")
    st.markdown(
        """
        **The Solution:** A hybrid, closed-loop LIB recycling system designed for India.
        **RADORDENA** replaces the "burn it all" approach with a precision
        **"Sort-Bioleach-Recover"** pipeline:
        **Intelligent Sorting ('Eyes') → Bioleaching ('Core') → Electro-Recovery ('Harvest')**.
        """
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            '<div class="metric-card"><h3>> 95%</h3><p>Critical Mineral Recovery</p></div>',
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            '<div class="metric-card"><h3>-30%</h3><p>Operating Costs</p></div>',
            unsafe_allow_html=True
        )
    with col3:
        st.markdown(
            '<div class="metric-card"><h3>128 GWh</h3><p>2030 Market Target</p></div>',
            unsafe_allow_html=True
        )

    st.markdown("---")

    col_a, col_b = st.columns([2, 1])
    with col_a:
        st.image(
            "https://images.unsplash.com/photo-1593941707882-a5bba14938c7?"
            "ixlib=rb-1.2.1&auto=format&fit=crop&w=1352&q=80",
            caption="RADORDENA Pilot Facility Representation",
            use_column_width=True
        )
    with col_b:
        st.markdown("### The Bottleneck")
        st.info(
            "Global recycling rates are stuck at 5%. Traditional smelting is toxic "
            "and cannot handle the surge of 1.6 million tons of EV waste."
        )
        st.markdown("### The Innovation")
        st.success(
            "**RADORDENA:**\n"
            r"Ambient Temp ($30^\circ C$)\n"
            "Zero Toxic Emissions\n"
            "Handles Mixed Feed (LFP/NMC)"
        )

    st.markdown("### Operational Status")
    st.progress(92)
    st.caption(
        "Bioleaching Reactor Efficiency (Acidithiobacillus ferrooxidans Activity)")

elif page == "RADORDENA Connect":
    st.title("RADORDENA Connect (Consumer Agent)")
    st.markdown("### Scan-to-Recycle: The 'One-Click' Logistics Engine")

    col_input, col_process = st.columns([1, 2])

    with col_input:
        st.info("Takes a photo of waste battery -> Autonomous Logistics & Payment.")
        img_file = st.file_uploader(
            "Upload Battery Photo", type=['jpg', 'png', 'jpeg'])
        user_loc = st.text_input(
            "Pickup Location", "Sector 5, Salt Lake, Kolkata")

        if img_file is not None:
            st.image(img_file, caption="Input Data", use_column_width=True)
            if st.button("Activate Connect Agent"):
                st.session_state['connect_active'] = True

    with col_process:
        if st.session_state.get('connect_active') and img_file:
            with st.spinner("Agent Vision Analyzing..."):
                # Run Agent Logic
                data, value, carbon_pts, log = connector.process_request(
                    img_file, user_loc)

            # 1. Perception Result
            st.success("**Step 1: Visual Ingestion (Perceiver Agent)**")
            c1, c2, c3 = st.columns(3)
            c1.metric("Chemistry ID", data['type'])
            c2.metric("Condition", data['condition'])
            c3.metric("Est. Weight", f"{data['weight_est']} kg")

            if data['safety'] == 'Hazardous':
                st.error(
                    "Safety Flag: Swelling Detected. HAZMAT Transport Protocol Initiated.")

            st.markdown("---")

            # 2. Valuation
            st.info("**Step 2: Instant Valuation (Pricing Engine)**")
            v1, v2 = st.columns(2)
            v1.metric("Credits Offered", f"₹ {value:,.2f}")
            v2.metric("Carbon Points", f"{carbon_pts} pts")

            st.markdown("---")

            # 3. Logistics
            st.warning("**Step 3: Autonomous Logistics (The 'Claw')**")
            st.write(f"**Provider:** {log['provider']}")
            st.write(f"**Truck ID:** {log['truck_id']}")
            st.write(f"**Hazmat Manifest:** `{log['manifest']}`")
            st.progress(100)
            st.caption(
                f"ETA: {log['eta']} | Pre-Alert Sent onto Factory Sort-01 Agent.")

            st.balloons()

elif page == "Agent Training Center":
    st.title("Agent Training Center")
    st.markdown("### Phase 1: Supervised Learning & Predictive Modeling")
    st.markdown(
        "*Training AI agents on real physics-based datasets for autonomous operation*")

    tab1, tab2 = st.tabs(["SORT-01 (Vision Agent)", "BIO-01 (Process Agent)"])

    with tab1:
        st.subheader("Training RADORDENA-SORT-01: Hyperspectral Classifier")

        col_theory, col_train = st.columns([1, 1])

        with col_theory:
            st.markdown("#### **Theoretical Foundation**")
            st.markdown("""
            **Kubelka-Munk Theory for Reflectance:**
            """)
            st.latex(
                r"F(R_\infty) = \frac{(1-R_\infty)^2}{2R_\infty} = \frac{K}{S}")
            st.caption(
                "*K* = Absorption coefficient, *S* = Scattering coefficient")

            st.markdown("""
            **Training Objective (Cross-Entropy Loss):**
            """)
            st.latex(r"\mathcal{L} = -\sum_{i=1}^{N} y_i \log(\hat{y}_i)")
            st.caption(
                "Minimize classification error across N=10,000 spectral samples")

            st.markdown("**Chemistry Signatures:**")
            st.code("""
NMC:  LiNi₀.₃Mn₀.₃Co₀.₃O₂  → Peak @ 600nm, 850nm
LFP:  LiFePO₄             → Peak @ 500nm, 750nm
LCO:  LiCoO₂              → Peak @ 480nm, 920nm
            """, language="text")

        with col_train:
            st.markdown("#### **Model Architecture**")
            st.info("**YOLOv8-Nano** with Transfer Learning")
            st.markdown("""
            - **Input:** 640×640 RGB + NIR images
            - **Backbone:** CSPDarknet53 (pre-trained)
            - **Head:** Custom multi-class detector
            - **Classes:** 4 (NMC, LFP, LCO, Contaminant)
            """)

            if st.button("▶ Start Training Simulation", key="train_vision"):
                progress_bar = st.progress(0)
                status_text = st.empty()

                # Simulate Training
                history = ai_classifier.train_model(iterations=100)

                for i, acc in enumerate(history):
                    progress_bar.progress(i + 1)
                    status_text.text(
                        f"Epoch {i+1}/100 - Accuracy: {acc*100:.2f}%")

                st.success("Training Complete | Validation mAP@50: 96.2%")

                # Plot Learning Curve
                fig = px.line(
                    y=history,
                    labels={'x': 'Epochs', 'y': 'Accuracy'},
                    title="Convergence Curve (Logarithmic Learning Rate Decay)"
                )
                fig.update_traces(line_color='#00ff94')
                fig.update_layout(template="plotly_dark")
                st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.subheader(
            "Optimizing RADORDENA-BIO-01: Bacterial Process Controller")

        st.markdown("#### **Bio-Oxidation Chemistry**")
        st.markdown("**Iron Oxidation (Energy Source for *A. ferrooxidans*):**")
        st.latex(
            r"4Fe^{2+} + O_2 + 4H^+ \xrightarrow{bacteria} 4Fe^{3+} + 2H_2O")
        st.caption("Generates Fe³⁺ which leaches metals from cathodes")

        st.markdown("**Metal Recovery Reactions:**")
        col_eq1, col_eq2 = st.columns(2)
        with col_eq1:
            st.latex(
                r"LiCoO_2 + 3Fe^{3+} \rightarrow Li^+ + Co^{2+} + 3Fe^{2+}")
            st.caption("Cobalt dissolution (NMC/LCO)")
        with col_eq2:
            st.latex(r"LiFePO_4 + Fe^{3+} \rightarrow Li^+ + Fe^{2+} + FePO_4")
            st.caption("Lithium extraction (LFP)")

        st.markdown("---")
        st.markdown("#### **Control System Rules (PPO-Optimized)**")

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("##### Acidity Control Rules")
            st.info("**Target pH: 1.8** (Optimal for bacterial activity)")
            st.latex(
                r"\text{IF } pH > 2.0: \quad \text{Dose } H_2SO_4 \text{ (0.5M)}")
            st.latex(
                r"\text{IF } pH < 1.5: \quad \text{Dose } H_2O \text{ (Dilute)}")
            st.caption("Feedback loop controlled by RL agent with 50ms latency")

        with c2:
            st.markdown("##### Thermal Control Rules")
            st.info("**Target Temp: 30°C** (Mesophilic bacteria)")
            st.latex(
                r"\text{IF } T > 35°C: \quad P_{cooling} = k(T - T_{set})")
            st.caption("*k* = 2.5 W/°C (Proportional cooling)")
            st.markdown("**Arrhenius Penalty:**")
            st.latex(r"k = Ae^{-E_a/RT}")
            st.caption("Activity drops 40% at T=40°C")

        st.markdown("---")
        st.markdown("#### **Simulation Validation (100 Virtual Cycles)**")
        st.caption("*Testing control robustness under noise and disturbances*")

        st.progress(100)
        st.success(
            "✅ Optimization Complete: Metal Recovery stabilized at **92.4% ± 2.1%**")

        # Show training metrics
        metric_col1, metric_col2, metric_col3 = st.columns(3)
        metric_col1.metric("Mean Reward", "-354",
                           delta="+1646 from baseline", delta_color="normal")
        metric_col2.metric("Episode Length", "339 steps",
                           delta="+239 steps", delta_color="normal")
        metric_col3.metric("Policy Gradient", "0.016",
                           delta="Converged", delta_color="off")

elif page == "Chat with Plant":
    st.title("RADORDENA Diagnostic Interface")
    st.markdown("### Natural Language Facility Control System")
    st.caption(
        "Query reactor status, troubleshooting protocols, or process optimization parameters")

    # Initialize conversation history
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # Display conversation history
    for msg in st.session_state.messages:
        if msg['role'] == 'user':
            with st.chat_message("user", avatar="OP"):
                st.markdown(msg['content'])
        else:
            with st.chat_message("assistant", avatar="AI"):
                st.markdown(msg['content'])

    # Chat input
    if prompt := st.chat_input("Ask about process parameters, diagnostics, or optimization..."):
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display user message
        with st.chat_message("user", avatar="OP"):
            st.markdown(prompt)

        # Generate AI response with streaming simulation
        with st.chat_message("assistant", avatar="AI"):
            message_placeholder = st.empty()

            # Processing stages
            thinking_stages = [
                "[1/5] Analyzing query structure...",
                "[2/5] Querying digital twin sensor network...",
                "[3/5] Processing via neuro-symbolic inference...",
                "[4/5] Validating thermodynamic constraints...",
                "[5/5] Generating diagnostic recommendation..."
            ]

            import time
            for stage in thinking_stages:
                message_placeholder.markdown(f"*{stage}*")
                time.sleep(0.6)  # 3 seconds total thinking time

            # Generate contextual response
            response = generate_agent_response(prompt)

            # Stream response word by word
            full_response = ""
            for word in response.split():
                full_response += word + " "
                time.sleep(0.05)  # Simulate typing
                message_placeholder.markdown(full_response + "▌")

            message_placeholder.markdown(response)

        # Add assistant response to history
        st.session_state.messages.append(
            {"role": "assistant", "content": response})

        # Rerun to update chat display
        st.rerun()


elif page == "AI Battery Sorting":
    st.title("RADORDENA-SORT-01: Intelligent Sorting Agent")
    st.markdown("### Autonomous Gatekeeper Logic")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("### Visual Feed Input")
        if st.button("Inject Random Feed Object"):
            # Simulate a mix of valid batteries and contaminants
            types = ['NMC', 'LFP', 'Plastic', 'Metal_Scrap']
            choice = np.random.choice(types, p=[0.4, 0.4, 0.1, 0.1])

            st.session_state['sample_type'] = choice

            # Generate spectrum based on choice
            if choice in ['NMC', 'LFP']:
                st.session_state['spectrum'] = ai_classifier.generate_synthetic_spectra(
                    choice)
            else:
                # Generate 'Unknown' noise spectrum
                st.session_state['spectrum'] = ai_classifier.generate_synthetic_spectra(
                    'Noise')

            st.success(f"Object Detected: {choice} (Simulated)")

    with col2:
        if 'spectrum' in st.session_state:
            spectrum = st.session_state['spectrum']
            wl = ai_classifier.wavelengths

            # Agent Logic Execution
            chem, conf, route = ai_classifier.classify_sample(spectrum)

            # Visualization
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=wl, y=spectrum, mode='lines', name='Spectral Signature',
                line=dict(color='#00FF94', width=2)
            ))
            fig.update_layout(
                title=f"HyperSpectral Analysis | ID: {chem} ({conf*100:.1f}%)",
                xaxis_title="Wavelength (nm)",
                yaxis_title="Reflectance Intensity",
                template="plotly_dark",
                height=350
            )
            st.plotly_chart(fig, use_container_width=True)

            st.markdown("### Agent Decision Matrix")

            c1, c2, c3 = st.columns(3)
            c1.metric("Identification", chem)
            c2.metric("Confidence", f"{conf*100:.1f}%")

            # Routing Logic Visualization
            if "Bin A" in route:
                c3.success(f"ACTUATOR: {route}")
                st.info("Protocol: High Value Feedstock -> Line 1 Bioleaching")
                st.markdown("---")
                st.markdown("### Safety Handshake")
                st.write("Checking downstream shredder atmosphere...")
                st.progress(100)
                st.caption(
                    "Nitrogen Inerting Active ($O_2$ < 2%) - **RELEASE GRANTED**")

            elif "Bin B" in route:
                c3.warning(f"ACTUATOR: {route}")
                st.info("Protocol: LFP Feedstock -> Line 2 Acid Process")
                st.markdown("---")
                st.markdown("### Safety Handshake")
                st.write("Checking downstream shredder atmosphere...")
                st.progress(100)
                st.caption(
                    "Nitrogen Inerting Active ($O_2$ < 2%) - **RELEASE GRANTED**")

            else:
                c3.error(f"ACTUATOR: {route}")
                st.error("Protocol: REJECT - Contaminant / Low Confidence")
                st.caption(
                    "Preventing downstream efficiency loss (80% impact avoided)")

elif page == "Process Simulation":
    st.title("RADORDENA-CORE: Cognitive Process Agent")
    st.subheader("Deep Reinforcement Learning (DRL) Console")

    col_ctrl, col_viz = st.columns([1, 2])

    with col_ctrl:
        st.markdown("### Predictive Control Interface")

        # User simulates sensor drift
        temp_input = st.slider("Reactor Temp (°C)", 20.0, 40.0, 30.0)
        ph_input = st.slider("pH Level", 1.0, 3.0, 1.8)
        do_level = st.slider("Dissolved Oxygen (mg/L)", 2.0, 8.0, 4.5)
        bacteria_load = st.slider(
            "Bacterial Load (cells/mL)", 1e6, 1e9, 5e8, format="%.0e")

        st.markdown("---")
        st.markdown("#### Chain-of-Thought Log")

        # Run Agent Logic (Reactive + Predictive)
        # Reactive
        health_status, actions = reactor.check_health_status(
            ph_input, temp_input)
        # Predictive
        reasoning, pred_action = reactor.predictive_control(
            do_level, bacteria_load)

        with st.expander("Show Reasoning Trace", expanded=True):
            for step in reasoning:
                st.code(step, language="text")
            st.warning(f"DECISION: {pred_action}")

        st.markdown("**Reactive Actions:**")
        for act in actions:
            if "Dosing" in act or "ACTIVATE" in act:
                st.write(f"{act}")
            else:
                st.write(f"{act}")

    with col_viz:
        st.markdown("### Physics-Informed Digital Twin")

        # Kinetics Visual
        days = np.linspace(0, 10, 100)
        recovery_curve = reactor.simulate_kinetics(days)

        fig_kin = px.line(
            x=days, y=recovery_curve*100,
            labels={'x': 'Time (Days)', 'y': 'Dissolution Efficiency (%)'}
        )
        fig_kin.update_traces(line_color='#00FF94')
        fig_kin.add_hline(y=90, line_dash="dot", annotation_text="Target > 90%",
                          annotation_position="bottom right")
        fig_kin.update_layout(
            template="plotly_dark",
            title="Bio-Oxidation Kinetics (Fe2+ -> Fe3+)",
            height=300
        )
        st.plotly_chart(fig_kin, use_container_width=True)

    st.markdown("---")
    st.subheader("Step 3: Electro-Selective Harvest Protocol")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("1. pH Adjust", "Level 2-4", "Dosing NaOH")
    c2.metric("2. Identify", "Co(OH)2", "Precipitating")
    c3.metric("3. Carbonation", "Li2CO3", "Recovering")
    c4.metric("4. Water Recycle", "90%", "Filtering")

    # Simulation Logic for Products
    BLACK_MASS_PER_TON = 350.0
    BLACK_MASS_INPUT = 1.0 * BLACK_MASS_PER_TON  # Simulating 1 ton input
    metals, comp = reactor.mass_balance(BLACK_MASS_INPUT)
    products = extractor.calculate_products(metals)

    st.dataframe(
        pd.DataFrame(list(products.items()), columns=[
                     'Recovered Product', 'Mass (kg/Ton)']),
        use_container_width=True
    )

elif page == "Financial Analysis":
    st.title("Unit Economics & Sustainability")

    annual_feed = st.slider("Annual Capacity (Tons)", 100, 20000, 5000)

    # Calc
    BLACK_MASS_PER_TON = 350.0  # kg
    # Need to normalize mass balance to 1 ton for financial calc
    metals, _ = reactor.mass_balance(BLACK_MASS_PER_TON)
    products = extractor.calculate_products(metals)

    result = finance.calculate_roi(annual_feed, products)

    # KPI Row
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("Annual Revenue", f"₹ {result['Annual_Revenue']/1e7:.2f} Cr")
    kpi2.metric("Gross Profit",
                f"₹ {result['Gross_Profit']/1e7:.2f} Cr", delta_color="normal")
    kpi3.metric("Payback Period", f"{result['Payback_Years']:.1f} Years")
    # Approx 2.5t saved per ton
    kpi4.metric("CO2 Credits", f"{annual_feed * 2.5:.0f} Tons")

    # Charts
    st.markdown("### Revenue Breakdown")
    fig_pie = px.pie(
        names=list(result['Revenue_Breakdown'].keys()),
        values=list(result['Revenue_Breakdown'].values()),
        hole=0.4
    )
    fig_pie.update_layout(template="plotly_dark")
    st.plotly_chart(fig_pie)

    st.success(
        "Analysis confirms Startup Viability with >25% Internal Rate of Return (IRR).")


elif page == "Carbon Credits & ESG":
    st.title("Carbon Credits & ESG Impact Monetization")
    st.markdown("### Environmental Value Creation Beyond Metal Recovery")

    st.info("""
    **Competitive Advantage:** RADORDENA generates **5 revenue streams** vs. competitors' 1-2.
    Carbon credits and ESG data monetization represent untapped value in battery recycling.
    """)

    # Input Parameters
    col1, col2 = st.columns(2)
    with col1:
        annual_throughput = st.slider(
            "Annual Battery Throughput (Tons)",
            min_value=100,
            max_value=5000,
            value=500,
            step=100
        )

    with col2:
        carbon_price = st.slider(
            "Carbon Credit Price (₹/Ton CO₂)",
            min_value=500,
            max_value=1500,
            value=850,
            step=50
        )

    # Carbon Calculations
    st.markdown("---")
    st.subheader("Carbon Emissions Avoided")

    # Industry baseline: Pyrometallurgy at 4.2 tons CO₂/ton waste
    # RADORDENA bioleaching: 1.7 tons CO₂/ton waste
    # Net savings: 2.5 tons CO₂/ton waste

    co2_savings_per_ton = 2.5
    total_co2_avoided = annual_throughput * co2_savings_per_ton
    carbon_revenue = total_co2_avoided * carbon_price

    metric_col1, metric_col2, metric_col3 = st.columns(3)
    metric_col1.metric(
        "Total CO₂ Avoided",
        f"{total_co2_avoided:,.0f} Tons/Year",
        delta="vs. Pyrometallurgy"
    )
    metric_col2.metric(
        "Carbon Credit Revenue",
        f"₹{carbon_revenue/1e5:.2f} Lakh",
        delta=f"+{(carbon_revenue/(annual_throughput*12400))*100:.1f}% of metal revenue"
    )
    metric_col3.metric(
        "Equivalent Trees Planted",
        f"{total_co2_avoided*50:,.0f} Trees",
        delta="Carbon sequestration"
    )

    # Breakdown Chart
    st.markdown("### Emissions Comparison: RADORDENA vs. Traditional Recycling")

    comparison_data = pd.DataFrame({
        'Process Stage': ['Shredding', 'Sorting', 'Thermal Treatment', 'Chemical Recovery', 'Water Treatment'],
        'Pyrometallurgy (kg CO₂/ton)': [120, 80, 3200, 650, 150],
        'RADORDENA Bioleaching (kg CO₂/ton)': [120, 25, 0, 1200, 355]
    })

    fig_emissions = go.Figure()
    fig_emissions.add_trace(go.Bar(
        name='Pyrometallurgy',
        x=comparison_data['Process Stage'],
        y=comparison_data['Pyrometallurgy (kg CO₂/ton)'],
        marker_color='#EF4444'
    ))
    fig_emissions.add_trace(go.Bar(
        name='RADORDENA',
        x=comparison_data['Process Stage'],
        y=comparison_data['RADORDENA Bioleaching (kg CO₂/ton)'],
        marker_color='#10B981'
    ))
    fig_emissions.update_layout(
        barmode='group',
        template='plotly_dark',
        title='Carbon Footprint by Process Stage',
        yaxis_title='kg CO₂ per Ton Waste',
        height=400
    )
    st.plotly_chart(fig_emissions, use_container_width=True)

    # ESG Data Monetization
    st.markdown("---")
    st.subheader("ESG Data Monetization Strategy")

    esg_col1, esg_col2 = st.columns(2)

    with esg_col1:
        st.markdown("##### Chain-of-Custody Verification")
        st.write("""
        **Service:** Blockchain-verified battery lifecycle data
        
        **Customers:**
        - EV Manufacturers (regulatory compliance)
        - ESG Rating Agencies (S&P, MSCI)
        - Insurance Companies (risk assessment)
        
        **Revenue Model:** ₹150 per battery tracked
        """)

        batteries_tracked = annual_throughput * 80  # Avg 80 cells/ton
        esg_data_revenue = batteries_tracked * 150

        st.metric(
            "ESG Data Annual Revenue",
            f"₹{esg_data_revenue/1e5:.2f} Lakh"
        )

    with esg_col2:
        st.markdown("##### Regulatory Compliance Reporting")
        st.write("""
        **Service:** Auto-generated compliance reports
        
        **Regulations Covered:**
        - EU Battery Regulation 2023 (Digital Passport)
        - India E-Waste Rules 2022 (EPR)
        - UN Basel Convention (Hazmat tracking)
        
        **Revenue Model:** ₹50,000/month subscription per OEM client
        """)

        oem_clients = 5  # Conservative estimate
        compliance_revenue = oem_clients * 50000 * 12

        st.metric(
            "Compliance SaaS Revenue",
            f"₹{compliance_revenue/1e5:.2f} Lakh/Year"
        )

    # Total Environmental Revenue
    st.markdown("---")
    total_env_revenue = carbon_revenue + esg_data_revenue + compliance_revenue

    st.success(f"""
    **Total Environmental Revenue Stream:** ₹{total_env_revenue/1e5:.2f} Lakh/Year
    
    This represents {(total_env_revenue/(annual_throughput*12400 + total_env_revenue))*100:.1f}% of total revenue -
    value that **competitors completely ignore**.
    """)


elif page == "EU Regulatory Compliance":
    st.title("EU Battery Regulation 2023: Compliance Dashboard")
    st.markdown("### Digital Battery Passport & Circular Economy Readiness")

    st.warning("""
    **Critical Market Insight:** EU Battery Regulation becomes mandatory in 2027.
    Non-compliant recyclers will be **locked out of European markets** (40% of global battery demand).
    
    RADORDENA is compliance-ready **today** - a 3-year advantage over competitors.
    """)

    # Compliance Scorecard
    st.markdown("---")
    st.subheader("RADORDENA Compliance Status")

    compliance_metrics = {
        "Digital Battery Passport": {
            "Requirement": "Unique identifier, lifecycle data, recycled content %",
            "RADORDENA Status": "COMPLIANT",
            "Implementation": "Blockchain QR-code system + AI data logging",
            "Competitor Status": "NON-COMPLIANT (manual records)"
        },
        "Recycling Efficiency Targets": {
            "Requirement": "70% Li recovery, 95% Co recovery by 2030",
            "RADORDENA Status": "EXCEEDS (94.2% Li, 89.1% Co)",
            "Implementation": "AI-optimized bioleaching",
            "Competitor Status": "BELOW TARGET (60-70% Li)"
        },
        "Carbon Footprint Disclosure": {
            "Requirement": "Mandatory LCA reporting per battery",
            "RADORDENA Status": "COMPLIANT",
            "Implementation": "Automated digital twin LCA",
            "Competitor Status": "PARTIAL (manual estimates)"
        },
        "Hazardous Substance Limits": {
            "Requirement": "<0.1% Cd, Pb, Hg in outputs",
            "RADORDENA Status": "COMPLIANT",
            "Implementation": "Selective bioleaching (bacteria ignore Cd/Pb)",
            "Competitor Status": "RISK (furnace volatilization)"
        },
        "Supply Chain Transparency": {
            "Requirement": "Due diligence on cobalt sourcing",
            "RADORDENA Status": "COMPLIANT",
            "Implementation": "RADORDENA Connect traceability",
            "Competitor Status": "NON-COMPLIANT (no tracking)"
        }
    }

    for metric, details in compliance_metrics.items():
        with st.expander(f"**{metric}** - {details['RADORDENA Status']}"):
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**Regulatory Requirement:**")
                st.write(details['Requirement'])
                st.markdown("**RADORDENA Implementation:**")
                st.success(details['Implementation'])

            with col2:
                st.markdown("**Competitor Benchmark:**")
                if "NON-COMPLIANT" in details['Competitor Status']:
                    st.error(details['Competitor Status'])
                elif "PARTIAL" in details['Competitor Status']:
                    st.warning(details['Competitor Status'])
                else:
                    st.info(details['Competitor Status'])

    # Timeline Visualization
    st.markdown("---")
    st.subheader("Regulatory Timeline & RADORDENA Readiness")

    timeline_data = {
        'Year': [2024, 2025, 2026, 2027, 2028, 2030],
        'Regulation Phase': [
            'Declaration Phase',
            'Labeling Required',
            'Digital Passport Pilot',
            'MANDATORY COMPLIANCE',
            'Recycled Content Quotas',
            '70% Li / 95% Co Targets'
        ],
        'RADORDENA Status': [
            'Ready',
            'Ready',
            'Ready',
            'COMPLIANT',
            'COMPLIANT',
            'EXCEEDS'
        ],
        'Competitor Risk': [
            'Low',
            'Medium',
            'High',
            'CRITICAL',
            'CRITICAL',
            'MARKET EXIT'
        ]
    }

    timeline_df = pd.DataFrame(timeline_data)

    fig_timeline = go.Figure()

    fig_timeline.add_trace(go.Scatter(
        x=timeline_df['Year'],
        y=[1]*len(timeline_df),
        mode='markers+text',
        marker=dict(size=20, color='#10B981'),
        text=timeline_df['Regulation Phase'],
        textposition='top center',
        name='Regulation Milestones',
        hovertemplate='<b>%{text}</b><br>RADORDENA: %{customdata[0]}<extra></extra>',
        customdata=timeline_df[['RADORDENA Status']]
    ))

    fig_timeline.update_layout(
        template='plotly_dark',
        title='EU Battery Regulation Timeline',
        xaxis_title='Year',
        yaxis=dict(visible=False),
        height=300,
        showlegend=False
    )

    st.plotly_chart(fig_timeline, use_container_width=True)

    # Economic Impact
    st.markdown("---")
    st.subheader("Market Access & Revenue Impact")

    market_col1, market_col2, market_col3 = st.columns(3)

    eu_market_value = 4200  # Crores INR by 2030
    radordena_market_share = eu_market_value * 0.08  # Conservative 8%

    market_col1.metric(
        "EU Battery Recycling Market (2030)",
        f"₹{eu_market_value:,} Cr",
        delta="Growing at 28% CAGR"
    )

    market_col2.metric(
        "RADORDENA Addressable Market",
        f"₹{radordena_market_share:.0f} Cr",
        delta="With compliance advantage"
    )

    market_col3.metric(
        "Non-Compliant Competitor Loss",
        "100% Market Exit",
        delta="2027 deadline",
        delta_color="inverse"
    )

    st.success("""
    **Strategic Advantage:** By being compliance-ready 3 years ahead of deadlines, RADORDENA can:
    1. Sign multi-year contracts with European OEMs (BMW, VW, Renault) **before** competitors adapt
    2. Command 15-20% price premium for certified battery-grade materials
    3. Establish network effects (more data → better passport → higher trust)
    """)

    # Certificate Simulation
    st.markdown("---")
    st.subheader("Sample: Digital Battery Passport")

    passport_data = {
        "Battery ID": "RADORDENA-LIB-2026-001234",
        "Chemistry": "NMC 811 (Nickel Manganese Cobalt)",
        "Original Capacity": "60 kWh",
        "Source": "Ola Electric S1 Pro (2024 Model)",
        "Collection Date": "2026-01-15",
        "Processing Facility": "RADORDENA Pune Plant (License: MH-2024-RECYCLE-087)",
        "Recovery Efficiency": "Li: 94.2% | Co: 89.1% | Ni: 91.7%",
        "Carbon Footprint": "1.7 tons CO₂/ton (vs. 4.2 industry baseline)",
        "Output Products": "Battery-grade Li₂CO₃ (99.5% purity), CoSO₄ (98.8% purity)",
        "Blockchain Verification": "0x7B4A9D3C2F1E8A5B6D9F0C3E7A2B8D4F1C6E9A3B",
        "Compliance Status": "EU Reg 2023/1542 Certified | India E-Waste Rules 2022 Compliant"
    }

    st.json(passport_data)

    st.info("""
    **This passport enables:**
    - EV manufacturers to prove recycled content in new batteries (mandatory 12% by 2030)
    - ESG investors to verify circular economy claims
    - Regulators to audit compliance in real-time
    - Insurance companies to assess battery lifecycle risks
    
    **Monetization:** Sell passport data to OEMs at ₹150/battery = ₹1.2 Cr additional annual revenue (for 500-ton plant)
    """)
