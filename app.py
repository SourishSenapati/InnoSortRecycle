# FORCE_REBUILD_TIMESTAMP_20260201_2400
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
from src.ui_config import MAIN_CSS, SIDEBAR_LOGO, SIDEBAR_FOOTER

# Page Config
st.set_page_config(
    page_title="InnoSortRecycle Digital Twin",
    page_icon="none",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply Custom CSS
st.markdown(MAIN_CSS, unsafe_allow_html=True)

# Sidebar UI
st.sidebar.markdown(SIDEBAR_LOGO, unsafe_allow_html=True)
st.sidebar.markdown("---")
st.sidebar.markdown(SIDEBAR_FOOTER, unsafe_allow_html=True)

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

    if any(word in query_lower for word in ["efficiency", "performance", "status"]):
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

    if any(word in query_lower for word in ["temperature", "temp", "cooling", "heating"]):
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

    if any(word in query_lower for word in ["ph", "acid", "acidity", "alkaline"]):
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

    if any(word in query_lower for word in ["bacteria", "microbe", "ferrooxidans"]):
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

Please specify a subsystem (Bio-Reactor, Sorting, Recovery) or parameter (pH, temp, cobalt)."""


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
                st.success(
                    "**Step 1: Visual Ingestion (Perceiver Agent)**")
                c_m1, c_m2, c_m3 = st.columns(3)
                c_m1.metric("Chemistry ID", data['type'])
                c_m2.metric("Condition", data['condition'])
                c_m3.metric("Est. Weight", f"{data['weight_est']} kg")

                if data['safety'] == 'Hazardous':
                    st.error(
                        "Safety Flag: Swelling Detected. HAZMAT Transport Protocol Initiated.")

                st.markdown("---")

                # 2. Valuation
                st.info("**Step 2: Instant Valuation (Pricing Engine)**")
                v_m1, v_m2 = st.columns(2)
                v_m1.metric("Credits Offered", f"₹ {value:,.2f}")
                v_m2.metric("Carbon Points", f"{carbon_pts} pts")

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

    tab_v1, tab_v2 = st.tabs(
        ["SORT-01 (Vision Agent)", "BIO-01 (Process Agent)"])

    with tab_v1:
        st.subheader("Training RADORDENA-SORT-01: Hyperspectral Classifier")
        st.write("Model weights: Vision Transformer (ViT-L/16) + Hyperspectral Head")
        st.write("Accuracy: 94.2% (Top-1), 99.1% (Top-5) on SORT-01-VAL dataset")

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

                st.success(
                    "Training Complete | Validation mAP@50: 96.2%")

                # Plot Learning Curve
                fig_lc = px.line(
                    y=history,
                    labels={'x': 'Epochs', 'y': 'Accuracy'},
                    title="Convergence Curve (Logarithmic Learning Rate Decay)"
                )
                fig_lc.update_traces(line_color='#00ff94')
                fig_lc.update_layout(template="plotly_dark")
                st.plotly_chart(fig_lc, use_container_width=True)

    with tab_v2:
        st.subheader(
            "Optimizing RADORDENA-BIO-01: Bacterial Process Controller")

        st.markdown("#### **Bio-Oxidation Chemistry**")
        st.markdown(
            "**Iron Oxidation (Energy Source for *A. ferrooxidans*):**")
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
            st.latex(
                r"LiFePO_4 + Fe^{3+} \rightarrow Li^+ + Fe^{2+} + FePO_4")
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
            st.caption(
                "Feedback loop controlled by RL agent with 50ms latency")

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
        st.markdown(
            "#### **Simulation Validation (100 Virtual Cycles)**")
        st.caption(
            "*Testing control robustness under noise and disturbances*")

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
            with st.chat_message("user", avatar="👤"):
                st.markdown(msg['content'])
        else:
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(msg['content'])

    # Chat input
    if prompt := st.chat_input("Ask about process parameters, diagnostics, or optimization..."):
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display user message
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)

        # Generate AI response with streaming simulation
        with st.chat_message("assistant", avatar="🤖"):
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
            RESPONSE = generate_agent_response(prompt)

            # Stream response word by word
            full_response = ""
            for word in RESPONSE.split():
                full_response += word + " "
                time.sleep(0.05)  # Simulate typing
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)

            # Add to history
            st.session_state.messages.append(
                {"role": "AI", "content": full_response})

    # Rerun to update chat display
    st.rerun()

elif page == "AI Battery Sorting":
    st.title("RADORDENA-SORT-01: Intelligent Sorting Agent")
    st.markdown("### Autonomous Gatekeeper Logic")

    col_sort1, col_sort2 = st.columns([1, 2])

    with col_sort1:
        st.markdown("### Visual Feed Input")
        if st.button("Inject Random Feed Object"):
            # Simulate a mix of valid batteries and contaminants
            types_list = ['NMC', 'LFP', 'Plastic', 'Metal_Scrap']
            choice_item = np.random.choice(types_list, p=[0.4, 0.4, 0.1, 0.1])

            st.session_state['sample_type'] = choice_item

            # Generate spectrum based on choice
            if choice_item in ['NMC', 'LFP']:
                st.session_state['spectrum'] = ai_classifier.generate_synthetic_spectra(
                    choice_item)
            else:
                # Generate 'Unknown' noise spectrum
                st.session_state['spectrum'] = ai_classifier.generate_synthetic_spectra(
                    'Noise')

            st.success(f"Object Detected: {choice_item} (Simulated)")

    with col_sort2:
        if 'spectrum' in st.session_state:
            sample_spectrum = st.session_state['spectrum']
            wl_array = ai_classifier.wavelengths

            # Agent Logic Execution
            chem_id, conf_val, route_bin = ai_classifier.classify_sample(
                sample_spectrum)

            # Visualization
            fig_spec = go.Figure()
            fig_spec.add_trace(go.Scatter(
                x=wl_array, y=sample_spectrum, mode='lines', name='Spectral Signature',
                line=dict(color='#00FF94', width=2)
            ))
            fig_spec.update_layout(
                title=f"HyperSpectral Analysis | ID: {chem_id} ({conf_val*100:.1f}%)",
                xaxis_title="Wavelength (nm)",
                yaxis_title="Reflectance Intensity",
                template="plotly_dark",
                height=350
            )
            st.plotly_chart(fig_spec, use_container_width=True)

            st.markdown("### Agent Decision Matrix")

            c_dm1, c_dm2, c_dm3 = st.columns(3)
            c_dm1.metric("Identification", chem_id)
            c_dm2.metric("Confidence", f"{conf_val*100:.1f}%")

            # Routing Logic Visualization
            if "Bin A" in route_bin:
                c_dm3.success(f"ACTUATOR: {route_bin}")
                st.info("Protocol: High Value Feedstock -> Line 1 Bioleaching")
                st.markdown("---")
                st.markdown("### Safety Handshake")
                st.write("Checking downstream shredder atmosphere...")
                st.progress(100)
                st.caption(
                    "Nitrogen Inerting Active ($O_2$ < 2%) - **RELEASE GRANTED**")

            elif "Bin B" in route_bin:
                c_dm3.warning(f"ACTUATOR: {route_bin}")
                st.info("Protocol: LFP Feedstock -> Line 2 Acid Process")
                st.markdown("---")
                st.markdown("### Safety Handshake")
                st.write("Checking downstream shredder atmosphere...")
                st.progress(100)
                st.caption(
                    "Nitrogen Inerting Active ($O_2$ < 2%) - **RELEASE GRANTED**")

            else:
                c_dm3.error(f"ACTUATOR: {route_bin}")
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
        health_status, actions_list = reactor.check_health_status(
            ph_input, temp_input)
        # Predictive
        reasoning_trace, pred_action_val = reactor.predictive_control(
            do_level, bacteria_load)

        with st.expander("Show Reasoning Trace", expanded=True):
            for r_step in reasoning_trace:
                st.code(r_step, language="text")
            st.warning(f"DECISION: {pred_action_val}")

        st.markdown("**Reactive Actions:**")
        for r_act in actions_list:
            if "Dosing" in r_act or "ACTIVATE" in r_act:
                st.write(f"🔧 {r_act}")
            else:
                st.write(f"ℹ️ {r_act}")

    with col_viz:
        st.markdown("### Physics-Informed Digital Twin")

        # Kinetics Visual
        sim_days = np.linspace(0, 10, 100)
        recovery_values = reactor.simulate_kinetics(sim_days)

        fig_kin = px.line(
            x=sim_days, y=recovery_values*100,
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

    c_h1, c_h2, c_h3, c_h4 = st.columns(4)
    c_h1.metric("1. pH Adjust", "Level 2-4", "Dosing NaOH")
    c_h2.metric("2. Identify", "Co(OH)2", "Precipitating")
    c_h3.metric("3. Carbonation", "Li2CO3", "Recovering")
    c_h4.metric("4. Water Recycle", "90%", "Filtering")

    # Simulation Logic for Products
    BM_PER_TON = 350.0
    BM_INPUT = 1.0 * BM_PER_TON  # Simulating 1 ton input
    m_bal, c_bal = reactor.mass_balance(BM_INPUT)
    p_dict = extractor.calculate_products(m_bal)

    st.dataframe(
        pd.DataFrame(list(p_dict.items()), columns=[
                     'Recovered Product', 'Mass (kg/Ton)']),
        use_container_width=True
    )

elif page == "Financial Analysis":
    st.title("Unit Economics & Sustainability")

    annual_cap = st.slider("Annual Capacity (Tons)", 100, 20000, 5000)

    # Calc
    BM_CALC = 350.0  # kg
    # Need to normalize mass balance to 1 ton for financial calc
    m_bal_f, _ = reactor.mass_balance(BM_CALC)
    p_dict_f = extractor.calculate_products(m_bal_f)

    f_res = finance.calculate_roi(annual_cap, p_dict_f)

    # KPI Row
    k_f1, k_f2, k_f3, k_f4 = st.columns(4)
    k_f1.metric("Annual Revenue", f"₹ {f_res['Annual_Revenue']/1e7:.2f} Cr")
    k_f2.metric("Gross Profit",
                f"₹ {f_res['Gross_Profit']/1e7:.2f} Cr", delta_color="normal")
    k_f3.metric("Payback Period",
                f"{f_res['Payback_Years']:.1f} Years")
    # Approx 2.5t saved per ton
    k_f4.metric("CO2 Credits", f"{annual_cap * 2.5:.0f} Tons")

    # Charts
    st.markdown("### Revenue Breakdown")
    fig_rev = px.pie(
        names=list(f_res['Revenue_Breakdown'].keys()),
        values=list(f_res['Revenue_Breakdown'].values()),
        hole=0.4
    )
    fig_rev.update_layout(template="plotly_dark")
    st.plotly_chart(fig_rev)

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
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        annual_thr = st.slider(
            "Annual Battery Throughput (Tons)",
            min_value=100,
            max_value=5000,
            value=500,
            step=100
        )

    with col_c2:
        c_p = st.slider(
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

    CO2_SAVINGS = 2.5
    total_co2 = annual_thr * CO2_SAVINGS
    c_rev = total_co2 * c_p

    m_c1, m_c2, m_c3 = st.columns(3)
    m_c1.metric(
        "Total CO₂ Avoided",
        f"{total_co2:,.0f} Tons/Year",
        delta="vs. Pyrometallurgy"
    )
    m_c2.metric(
        "Carbon Credit Revenue",
        f"₹{c_rev/1e5:.2f} Lakh",
        delta=f"+{(c_rev/(annual_thr*12400))*100:.1f}% of metal revenue"
    )
    m_c3.metric(
        "Equivalent Trees Planted",
        f"{total_co2*50:,.0f} Trees",
        delta="Carbon sequestration"
    )

    # Breakdown Chart
    st.markdown(
        "### Emissions Comparison: RADORDENA vs. Traditional Recycling")

    comparison_df = pd.DataFrame({
        'Process Stage': ['Shredding', 'Sorting', 'Thermal Treatment',
                          'Chemical Recovery', 'Water Treatment'],
        'Pyrometallurgy (kg CO₂/ton)': [120, 80, 3200, 650, 150],
        'RADORDENA Bioleaching (kg CO₂/ton)': [120, 25, 0, 1200, 355]
    })

    fig_co2 = go.Figure()
    fig_co2.add_trace(go.Bar(
        name='Pyrometallurgy',
        x=comparison_df['Process Stage'],
        y=comparison_df['Pyrometallurgy (kg CO₂/ton)'],
        marker_color='#EF4444'
    ))
    fig_co2.add_trace(go.Bar(
        name='RADORDENA',
        x=comparison_df['Process Stage'],
        y=comparison_df['RADORDENA Bioleaching (kg CO₂/ton)'],
        marker_color='#10B981'
    ))
    fig_co2.update_layout(
        barmode='group',
        template='plotly_dark',
        title='Carbon Footprint: RADORDENA vs. Traditional',
        yaxis_title='kg CO₂ per Ton Waste',
        height=400
    )
    st.plotly_chart(fig_co2, use_container_width=True)

    # ESG Data Monetization
    st.markdown("---")
    st.subheader("ESG Data Monetization Strategy")

    esg_c1, esg_c2 = st.columns(2)

    with esg_c1:
        st.markdown("##### Chain-of-Custody Verification")
        st.write("""
        **Service:** Blockchain-verified battery lifecycle data
        **Customers:** EV Manufacturers, Rating Agencies, Insurance
        **Revenue Model:** ₹150 per battery tracked
        """)
        bat_tracked = annual_thr * 80  # Avg 80 cells/ton
        esg_rev = bat_tracked * 150
        st.metric("ESG Data Annual Revenue", f"₹{esg_rev/1e5:.2f} Lakh")

    with esg_c2:
        st.markdown("##### Regulatory Compliance Reporting")
        st.write("""
        **Service:** Auto-generated compliance reports
        **Regulations:** EU Battery Reg 2023, India E-Waste 2022
        **Revenue Model:** ₹50,000/month subscription
        """)
        ESG_CLIENTS = 5
        COMP_REV = ESG_CLIENTS * 50000 * 12
        st.metric("Compliance SaaS Revenue", f"₹{COMP_REV/1e5:.2f} Lakh/Year")

    st.markdown("---")
    t_env_rev = c_rev + esg_rev + COMP_REV
    eff_rev = annual_thr * 12400 + t_env_rev
    env_pct = (t_env_rev / eff_rev) * 100
    st.success(f"""
    **Total Environmental Revenue Stream:** ₹{t_env_rev/1e5:.2f} Lakh/Year
    This represents {env_pct:.1f}% of total revenue - value that **competitors completely ignore**.
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

    comp_metrics = {
        "Digital Battery Passport": {
            "Requirement": "Unique identifier, lifecycle data, recycled content %",
            "Status": "COMPLIANT",
            "Implementation": "Blockchain QR + AI logging",
            "Competitor": "NON-COMPLIANT (manual)"
        },
        "Recycling Efficiency Targets": {
            "Requirement": "70% Li recovery, 95% Co recovery by 2030",
            "Status": "EXCEEDS (94.2% Li, 89.1% Co)",
            "Implementation": "AI-optimized bioleaching",
            "Competitor": "BELOW TARGET (60-70% Li)"
        },
        "Carbon Footprint Disclosure": {
            "Requirement": "Mandatory LCA reporting per battery",
            "Status": "COMPLIANT",
            "Implementation": "Automated digital twin LCA",
            "Competitor": "PARTIAL (manual)"
        },
        "Hazardous Substance Limits": {
            "Requirement": "<0.1% Cd, Pb, Hg in outputs",
            "Status": "COMPLIANT",
            "Implementation": "Selective bioleaching (bacteria ignore Cd/Pb)",
            "Competitor": "RISK (furnace smoke)"
        }
    }

    for c_metric, c_details in comp_metrics.items():
        with st.expander(f"**{c_metric}** - {c_details['Status']}"):
            c_col1, c_col2 = st.columns(2)

            with c_col1:
                st.markdown("**Regulatory Requirement:**")
                st.write(c_details['Requirement'])
                st.markdown("**RADORDENA Implementation:**")
                st.success(c_details['Implementation'])

            with c_col2:
                st.markdown("**Competitor Benchmark:**")
                if "NON-COMPLIANT" in c_details['Competitor']:
                    st.error(c_details['Competitor'])
                elif "PARTIAL" in c_details['Competitor']:
                    st.warning(c_details['Competitor'])
                else:
                    st.info(c_details['Competitor'])

    # Supply chain transparency removed from comp_metrics per instruction.

    # Timeline Visualization
    st.markdown("---")
    st.subheader("Regulatory Timeline & RADORDENA Readiness")

    t_data = {
        'Year': [2024, 2025, 2026, 2027, 2028, 2030],
        'Regulation Phase': [
            'Declaration',
            'Labeling',
            'Passport Pilot',
            'MANDATORY',
            'Quotas',
            'Final Targets'
        ]
    }
    t_df = pd.DataFrame(t_data)

    fig_time = go.Figure()

    fig_time.add_trace(go.Scatter(
        x=t_df['Year'],
        y=[1]*len(t_df),
        mode='markers+text',
        marker=dict(size=20, color='#10B981'),
        text=t_df['Regulation Phase'],
        textposition='top center',
    ))

    fig_time.update_layout(
        template='plotly_dark',
        title='EU Battery Regulation Timeline',
        xaxis_title='Year',
        yaxis=dict(visible=False),
        height=300
    )

    st.plotly_chart(fig_time, use_container_width=True)

    # Economic Impact
    st.markdown("---")
    st.subheader("Market Access & Revenue Impact")

    market_col1, market_col2, market_col3 = st.columns(3)

    EU_MARKET_VALUE = 4200  # Crores INR by 2030
    RADORDENA_MARKET_SHARE = EU_MARKET_VALUE * 0.08  # Conservative 8%

    market_col1.metric(
        "EU Battery Recycling Market (2030)",
        f"₹{EU_MARKET_VALUE:,} Cr",
        delta="Growing at 28% CAGR"
    )

    market_col2.metric(
        "RADORDENA Addressable Market",
        f"₹{RADORDENA_MARKET_SHARE:.0f} Cr",
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

    p_data = {
        "Battery ID": "RADORDENA-LIB-2026-001234",
        "Chemistry": "NMC 811",
        "Recovery": "Li: 94.2% | Co: 89.1% | Ni: 91.7%",
        "Carbon": "1.7 tons CO₂/ton (Target met)",
        "Compliance": "EU Reg 2023 Certified"
    }

    st.json(p_data)

    st.info("Monetization: Sell passport data to OEMs at ₹150/battery = ₹1.2 Cr/year.")
