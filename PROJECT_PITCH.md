# RADORDENA: Turning Urban Waste into Strategic Energy Assets

**Domain:** Clean Energy & Sustainable E-Waste Management
**Theme:** AI & Biotechnology Integrated Recycling

## 1. Executive Summary

RADORDENA is a hybrid, closed-loop Lithium-Ion Battery (LIB) recycling system designed specifically for the Indian market. It addresses the critical inefficiency of current pyrometallurgical methods by integrating **AI-driven hyperspectral sorting** with **low-energy bio-hydrometallurgy**. This solution recovers **>95% of critical minerals** (Lithium, Cobalt, Nickel) at **~30% lower operating costs** than traditional smelting, ensuring economic viability and environmental sustainability.

## 2. Problem Statement

As India targets significant EV penetration, battery waste is projected to rise from ~2 GWh in 2023 to **128 GWh by 2030**.

- **The Bottleneck:** Global recycling rates hover around 5%. Traditional methods (smelting) are energy-intensive, produce toxic emissions, and struggle to separate diverse battery chemistries (e.g., mixing LFP and NMC batteries).
- **The Risk:** In India, informal recycling causes severe toxic pollution and results in low material recovery.
- **The Need:** With projections of 1.6 million tons of EV battery waste globally by 2030, a cost-efficient solution is required to manage the surplus capacity.

## 3. The Solution: RADORDENA Process Overview

RADORDENA replaces the "burn it all" approach with a precision **"Sort-Bioleach-Recover"** pipeline.

### Phase 1: Intelligent Sorting (The "Eyes")

- **Technology:** Hyperspectral imaging (400-1000 nm) combined with Machine Learning (ML) models.
- **Function:** Scans incoming batteries to identify chemistry signatures (NMC vs. LFP) with **95% accuracy**.
- **Pre-processing:** Sorted batteries are discharged in a 5% NaCl solution and shredded under Nitrogen ($N_2$) gas to prevent thermal runaway.

### Phase 2: Bioleaching (The "Core")

- **Innovation:** Uses _Acidithiobacillus ferrooxidans_ bacteria to dissolve metals at ambient temperature ($30^\circ C$), replacing high-heat furnaces.
- **Efficiency:** Achieves **>90% recovery** of Li, Co, Ni, and Mn in 4-7 days.
- **Sustainability:** Reduces chemical use by 50% compared to traditional hydrometallurgy.

### Phase 3: Electro-Selective Recovery (The "Harvest")

- **Process:** The metal-rich liquid (leachate) undergoes solvent extraction and precipitation to recover high-purity salts.
- **Closing the Loop:** Lithium is recovered as Lithium Carbonate ($Li_2CO_3$) via carbonation, while Graphite and other residues are recovered for secondary applications.

## 4. Technical Methodology (Deep Dive)

### A. Chemical Mechanism (Bioleaching Equations)

The core innovation is the indirect bioleaching mechanism where bacteria regenerate the oxidizing agent.

**Bacterial Regeneration:**
Bacteria oxidize ferrous iron ($Fe^{2+}$) to ferric iron ($Fe^{3+}$) using oxygen:
$$4Fe^{2+} + O_{2} + 4H^+ \xrightarrow{\text{bacteria}} 4Fe^{3+} + 2H_{2}O$$

**Metal Dissolution:**
The ferric iron acts as an oxidant, attacking the cathode material (Li-Ni-Mn-Co oxide) to release metals:
$$LiNi_{1/3}Mn_{1/3}Co_{1/3}O_{2} + 6H^+ + 2Fe^{3+} \rightarrow 2Li^+ + Ni^{2+} + Mn^{2+} + Co^{2+} + 2Fe^{2+} + H_2O$$

**Precipitation:**
Metals are recovered sequentially by adjusting pH (e.g., Cobalt recovery):
$$Co^{2+} + 2NaOH \rightarrow Co(OH)_{2}\downarrow + 2Na^{+}$$
