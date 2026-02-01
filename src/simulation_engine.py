"""
Simulation Engine module for InnoSortRecycle Digital Twin.
This module handles the mass balance stoichiometry and reaction kinetics for the process.
"""
import numpy as np


class BioleachingReactor:
    """
    RADORDENA-BIO-01: Simulates the biological reactor, handling kinetics, mass balance,
    and autonomous life-support logic (pH, Temp, Dosing).
    """

    def __init__(self, volume_l=10000.0, efficiency=0.92, residence_time_days=7.0):
        self.volume_l = float(volume_l)
        self.efficiency = float(efficiency)
        self.residence_time = float(residence_time_days)

        # Stoichiometry constants (simplified for molecular weights)
        self.molecular_weights = {
            'Li': 6.94, 'Ni': 58.69, 'Mn': 54.94, 'Co': 58.93, 'O': 16.00,
            'Fe': 55.85, 'S': 32.06, 'H': 1.01
        }

    def predictive_control(self, current_do, bacteria_count_cells_ml):
        """
        RADORDENA-CORE Capability: Predictive Model-Based Control (PINN Simulation).
        Predicts Oxygen crash based on bacteria growth.
        """
        prediction_horizon_mins = 20
        # Simple biological constraint model:
        # High bacteria (>10^8) consumes O2 exponentially.

        if bacteria_count_cells_ml > 1e8 and current_do < 5.0:
            # Prediction: DO will crash to zero in < 20 mins
            reasoning = [
                f"State: High Bacterial Load ({bacteria_count_cells_ml:.0e} cells/mL).",
                f"Trend: DO at {current_do} mg/L is marginally stable.",
                f"Prediction (T+{prediction_horizon_mins}m): Oxygen Crash imminent due to "
                "exponential consumption.",
                "Strategy: Pre-emptive Aeration Boost required to maintain homeostasis."
            ]
            action = "INCREASE AERATION (Pre-emptive)"
        else:
            reasoning = [
                "State: Bacterial consumption stable.",
                f"Prediction (T+{prediction_horizon_mins}m): DO levels remain within safe bounds.",
                "Strategy: Maintain current energy efficiency."
            ]
            action = "Maintain Flow"

        return reasoning, action

    def check_health_status(self, current_ph, current_temp):
        """
        Agent Logic: Life Support Loop
        returns: (Status Message, Action Taken)
        """
        status = "Stable"
        actions = []

        # Rule 1: Acidity
        if current_ph > 2.0:
            status = "Warning: pH High"
            actions.append("Dosing H2SO4 (Acid)")
        elif current_ph < 1.5:
            status = "Warning: pH Low"
            actions.append("Dosing Water Buffer")

        # Rule 2: Temperature
        if current_temp > 35.0:
            status = "CRITICAL: Bacterial Heat Stress"
            actions.append("ACTIVATE COOLING SYSTEM")
        elif current_temp < 25.0:
            status = "Warning: Low Temp"
            actions.append("Activate Heating")

        if not actions:
            actions.append("Maintaining Aeration")

        return status, actions

    def simulate_kinetics(self, time_points):
        """
        Simulate the leaching concentration over time using Michaelis-Menten-like kinetics
        approximated for bioleaching (S-curve).
        """
        # Logistic growth model for bacteria-driven leaching
        # C(t) = C_max / (1 + exp(-k*(t - t_mid)))
        rate_constant = 1.2  # Rate constant
        time_midpoint = self.residence_time / 2.0

        recovery = self.efficiency / \
            (1 + np.exp(-rate_constant * (time_points - time_midpoint)))
        return recovery

    def mass_balance(self, black_mass_input_kg):
        """
        Calculate output metals based on input Black Mass (NMC)
        Input Assumption: NMC 811 (Li Ni0.8 Mn0.1 Co0.1 O2) or similar mix
        PDF Data: 1 ton battery -> 350kg Black Mass
        Black Mass Composition: Li: 7.1%, Ni: 14.3%, Mn: 10%, Co: 11.4%
        (Approx from PDF '25kg Li from 350kg BM' -> ~7%)
        """
        # Based on PDF "Case Study": 350kg BM -> 25kg Li, 50kg Ni, 35kg Mn, 40kg Co.
        # Let's derive fractions from this reliable data.
        bm_mass = 350.0
        composition = {
            'Li': 25.0 / bm_mass,
            'Ni': 50.0 / bm_mass,
            'Mn': 35.0 / bm_mass,
            'Co': 40.0 / bm_mass
        }

        outputs = {}
        for metal, fraction in composition.items():
            theoretical_mass = black_mass_input_kg * fraction
            recovered_mass = theoretical_mass * self.efficiency
            outputs[metal] = recovered_mass

        # Reagent Consumption (PDF: "Bacteria/nutrients cheap", 5% H2SO4)
        # 4Fe2+ + O2 + 4H+ -> ...
        # Simplified: Acid consumption proportionality
        # Assume 0.5 kg H2SO4 per kg Black Mass (Industrial heuristic)
        outputs['H2SO4_Consumed'] = black_mass_input_kg * 0.5
        outputs['Water_Usage'] = black_mass_input_kg * \
            4.0  # 4:1 L/S ratio often used

        return outputs, composition


class ElectroRecovery:
    """
    Simulates the electrochemical recovery and precipitation layer.
    """

    def __init__(self):
        self.purity = 0.999  # 99.9%

    def calculate_products(self, metal_masses):
        """
        Convert metal mass to salt mass.
        Li -> Li2CO3
        Co -> Co(OH)2
        Ni -> Ni(OH)2
        Mn -> MnCO3
        """
        # Molecular weights
        mw_li = 6.94
        mw_li2co3 = 73.89
        factor_li = mw_li2co3 / (2 * mw_li)

        mw_co = 58.93
        mw_cooh2 = 92.95
        factor_co = mw_cooh2 / mw_co

        mw_ni = 58.69
        mw_nioh2 = 92.71
        factor_ni = mw_nioh2 / mw_ni

        mw_mn = 54.94
        mw_mnco3 = 114.95
        factor_mn = mw_mnco3 / mw_mn

        products = {
            'Li2CO3': metal_masses.get('Li', 0) * factor_li,
            'Co(OH)2': metal_masses.get('Co', 0) * factor_co,
            'Ni(OH)2': metal_masses.get('Ni', 0) * factor_ni,
            'MnCO3': metal_masses.get('Mn', 0) * factor_mn
        }
        return products
