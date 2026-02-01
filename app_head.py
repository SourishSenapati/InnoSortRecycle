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
