"""
UI Configuration and Static Assets for InnoSortRecycle.
"""

# Custom CSS for Premium Look
MAIN_CSS = """
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

    /* Alert Boxes */
    .stAlert {
        background: rgba(26, 35, 50, 0.6);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        border-left: 4px solid #00ff94;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }

    /* Mobile Optimization */
    @media (max-width: 768px) {
        h1 { font-size: 2rem !important; }
        .main .block-container { padding: 1rem; }
        .metric-card { padding: 20px; margin-bottom: 1rem; }
        [data-testid="stMetricValue"] { font-size: 1.75rem !important; }
        .stButton>button { width: 100%; padding: 1rem; }
    }
</style>
"""

SIDEBAR_LOGO = """
<div style="text-align: center; padding: 1.5rem 0 1rem 0;">
    <svg width="80" height="80" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="logoGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#00ff94;stop-opacity:1" />
                <stop offset="100%" style="stop-color:#00d4ff;stop-opacity:1" />
            </linearGradient>
        </defs>
        <circle cx="50" cy="50" r="45" fill="none" stroke="url(#logoGrad)" stroke-width="2" stroke-dasharray="20,10" />
        <path d="M30 50 Q50 20 70 50 T30 50" fill="none" stroke="url(#logoGrad)" stroke-width="4" stroke-linecap="round">
            <animateTransform attributeName="transform" type="rotate" from="0 50 50" to="360 50 50" dur="10s" repeatCount="indefinite" />
        </path>
        <circle cx="50" cy="50" r="8" fill="#00ff94">
            <animate attributeName="r" values="8;12;8" dur="3s" repeatCount="indefinite" />
            <animate attributeName="opacity" values="1;0.5;1" dur="3s" repeatCount="indefinite" />
        </circle>
    </svg>
    <h2 style="color: #ffffff; font-size: 1.5rem; margin-top: 1rem; letter-spacing: 0.05em;">
        RADORDENA <span style="color: #00ff94; font-weight: 400;">Connect</span>
    </h2>
</div>
"""

SIDEBAR_FOOTER = """
<div style="position: fixed; bottom: 20px; left: 20px; color: rgba(255,255,255,0.4); font-size: 0.8rem;">
    RADORDENA v2.0.1<br>
    Titanium Reliability Kernel
</div>
"""
