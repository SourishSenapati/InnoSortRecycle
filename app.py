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
                         "Financial Analysis"])

# Initialize Engines
reactor = BioleachingReactor()
extractor = ElectroRecovery()
ai_classifier = HyperspectralClassifier()
finance = FinancialModel()
connector = ConnectAgent()

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
    st.markdown("Phase 1: Supervised Learning & Rule Optimization")

    tab1, tab2 = st.tabs(["SORT-01 (Vision)", "BIO-01 (Process)"])

    with tab1:
        st.subheader("Training RADORDENA-SORT-01")
        st.write(
            "**Goal:** Teach AI to distinguish NMC, LFP, and Contaminants using "
            "10,000 spectral signatures."
        )

        if st.button("Start Training Sequence"):
            progress_bar = st.progress(0)
            status_text = st.empty()

            # Simulate Training
            history = ai_classifier.train_model(iterations=100)

            for i, acc in enumerate(history):
                progress_bar.progress(i + 1)
                status_text.text(f"Epoch {i+1}/100 - Accuracy: {acc*100:.2f}%")

            st.success("Training Complete! Model Validation Accuracy: >95%")

            # Plot Learning Curve
            fig = px.line(
                y=history,
                labels={'x': 'Epochs', 'y': 'Accuracy'},
                title="Model Learning Curve (Logarithmic)"
            )
            fig.update_layout(template="plotly_dark")
            st.plotly_chart(fig)

    with tab2:
        st.subheader("Optimizing RADORDENA-BIO-01")
        st.write("**Goal:** Define optimal rules for bacterial life support.")

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### Acidity Rules")
            st.info("Target pH: 1.8")
            st.write("- IF pH > 2.0: Dose H2SO4")
            st.write("- IF pH < 1.5: Dose Water")

        with c2:
            st.markdown("#### Thermal Rules")
            st.info("Target Temp: 30°C")
            st.write("- IF Temp > 35°C: Emergency Cooling")

        st.markdown("#### Simulation Validation")
        st.caption("Testing parameters against 100 virtual cycles...")
        st.progress(100)
        st.success("Optimization Complete: Metal Recovery stabilized at >90%")

elif page == "Chat with Plant":
    st.title("Chat with RADORDENA")
    st.markdown("### Natural Language Facility Interface (LLM-Powered)")

    # Chat Interface
    user_query = st.text_input("Ask the Cognitive Engine a question...",
                               placeholder="e.g., Why is the Cobalt recovery rate low in Tank 4?")

    if user_query:
        st.markdown("---")
        col_user, col_agent = st.columns([1, 4])

        with col_user:
            st.info(f"**Operator:**\n{user_query}")

        with col_agent:
            # Simulate Context-Aware Reasoning
            if "Cobalt" in user_query or "Tank 4" in user_query:
                RESPONSE_TEXT = """
                **Analysis:** Tank 4 pH drifted to **4.2**.
                
                **Reasoning:**
                1.  *Observation:* High pH caused premature precipitation of Manganese ($Mn(OH)_2$).
                2.  *Impact:* Contaminant carry-over to the Cobalt filter circuit.
                
                **Corrective Action:**
                *   I have autonomously lowered pH to **3.8**.
                *   Increased solvent flow by **15%**.
                
                *Expect purity to restore in 45 minutes.*
                """
                st.success(f"**RADORDENA Agent:**\n{RESPONSE_TEXT}")

            elif "efficiency" in user_query.lower():
                st.success("""
                **RADORDENA Agent:**
                Current Bio-Reactor Efficiency is **92%**.
                *   Bacterial Count: $5.2 \\times 10^8$ cells/mL.
                *   Fe2+ Oxidation Rate: Optimal.
                """)
            else:
                st.warning("""
                **RADORDENA Agent:**
                I am processing your query. Please specify a subsystem (Bio-Reactor, Sorting Line, or Recovery Tank).
                """)

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
        "Analysis confirms **Startup Viability** with >25% Internal Rate of Return (IRR).")
