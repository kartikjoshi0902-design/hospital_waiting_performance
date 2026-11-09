"""
Hospital Patient Wait-Time & Capacity Optimizer
=================================================
Executive Overview & System Architecture.

Demonstrating the application of Operations Research (Queueing Theory &
Integer Linear Programming) to optimize physician allocation and reduce
patient waiting times in hospital outpatient departments (OPDs).
"""

import streamlit as st
import pandas as pd
from utils.ui_theme import inject_custom_css, render_header, render_sidebar_branding, COLORS
from data.hospital_data import get_default_departments, get_departments_dataframe, get_total_available_doctors

# ─── Page Configuration ──────────────────────────────────────────
st.set_page_config(
    page_title="Hospital Flow Optimizer | Operations Research",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Inject UI Theme ─────────────────────────────────────────────
inject_custom_css()
render_sidebar_branding()

with st.sidebar:
    st.markdown("### Operational Scope")
    st.markdown(
        """
        This decision support system applies **M/M/c Queueing Theory** and
        **Integer Linear Programming (LP)** to optimize physician staffing
        across multi-specialty outpatient clinics.
        """
    )
    st.markdown("---")
    st.markdown(
        """
        <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 10px 12px; font-size: 0.82rem;">
            <div style="color: #64748b; font-weight: 600; margin-bottom: 2px;">OPERATING SHIFT</div>
            <div style="color: #0f172a; font-weight: 700;">8 Hours / Day (09:00 – 17:00)</div>
            <div style="color: #64748b; font-weight: 600; margin-top: 8px; margin-bottom: 2px;">ACTIVE DEPARTMENTS</div>
            <div style="color: #1d4ed8; font-weight: 700;">5 Specialized OPD Clinics</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("---")
    st.caption("Operations Research Decision Support System")

# ─── Executive Header ────────────────────────────────────────────
render_header(
    title="Hospital Outpatient Flow & Resource Allocation Optimizer",
    subtitle="A mathematical operations research framework integrating M/M/c queueing models and integer programming to eliminate outpatient bottlenecks.",
    tag="OPERATIONS RESEARCH • HEALTHCARE CAPACITY PLANNING",
)

# ─── Operational Challenges ──────────────────────────────────────
st.markdown("### Outpatient Capacity & Bottleneck Dynamics")
st.markdown(
    "Long outpatient waiting times are rarely caused by an absolute shortage of personnel. "
    "Rather, they emerge from **structural mismatch** between stochastic patient arrival patterns "
    "and inflexible physician shift allocations."
)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown("""
    <div class="challenge-card">
        <div class="challenge-title">Excessive Patient Delay</div>
        <p class="challenge-desc">Bottleneck clinics experience average queueing delays over 40 minutes for a standard 15-minute consultation.</p>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="challenge-card">
        <div class="challenge-title">Capacity-Demand Asymmetry</div>
        <p class="challenge-desc">High-demand specialties are chronically overwhelmed while adjacent clinics operate below 55% utilization.</p>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="challenge-card">
        <div class="challenge-title">Clinical Burnout Risk</div>
        <p class="challenge-desc">Physicians in overloaded departments operate at sustained utilization rates exceeding 85%, degrading care quality.</p>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown("""
    <div class="challenge-card">
        <div class="challenge-title">Throughput Attrition</div>
        <p class="challenge-desc">Prolonged wait times lead to patient walkouts (reneging), diminished satisfaction scores, and lost clinical revenue.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

# ─── Operations Research Methodologies ────────────────────────────
st.markdown("### Operations Research Methodologies")
st.markdown("The platform leverages two complementary mathematical techniques:")

m1, m2 = st.columns(2)

with m1:
    st.markdown("""
    <div class="method-card blue-border">
        <div class="method-badge-container">
            <span class="status-badge status-badge-info">Diagnostic Model</span>
        </div>
        <h4 class="method-title">1. M/M/c Multi-Server Queueing Theory</h4>
        <p class="method-desc">
            Evaluates steady-state performance under stochastic Poisson arrival rates (λ) and exponential consultation times (μ) across parallel physician servers (c).
        </p>
        <div class="formula-container">
            <strong>Erlang-C Delay Probability:</strong><br>
            P(Wait &gt; 0) = C(c, a) = [ (a^c / c!) · (1 / (1 - ρ)) ] / [ Σ (a^k / k!) + (a^c / c!) · (1 / (1 - ρ)) ]
        </div>
        <ul class="method-list">
            <li><strong>Waiting Time in Queue (Wq):</strong> Quantifies expected delay prior to consultation</li>
            <li><strong>Physician Utilization (ρ = λ / cμ):</strong> Measures true clinical workload percentage</li>
            <li><strong>Queue Length (Lq):</strong> Forecasts physical waiting lounge capacity needs</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown("""
    <div class="method-card green-border">
        <div class="method-badge-container">
            <span class="status-badge status-badge-success">Prescriptive Model</span>
        </div>
        <h4 class="method-title">2. Integer Linear Programming & Marginal Optimization</h4>
        <p class="method-desc">
            Computes the optimal integer distribution of physicians across departments to minimize total patient waiting time subject to staffing constraints.
        </p>
        <div class="formula-container">
            <strong>Optimization Objective:</strong><br>
            min Σ [ w_i · λ_i · Wq_i(c_i) ] subject to Σ c_i ≤ C_total, ρ_i &lt; 1
        </div>
        <ul class="method-list">
            <li><strong>Convex Marginal Allocation:</strong> Progressively allocates staff where delay reduction is highest</li>
            <li><strong>Stability Constraints:</strong> Strictly enforces ρ &lt; 1.0 across all departments</li>
            <li><strong>Priority Weighting:</strong> Incorporates clinical acuity weights (e.g., Cardiology vs. Dermatology)</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

# ─── 3-Phase Analytics Architecture ──────────────────────────────
st.markdown("### Analytics Workflow")
st.markdown("The end-to-end optimization pipeline is structured into three progressive stages:")

w1, w2, w3 = st.columns(3)

with w1:
    st.markdown("""
    <div class="workflow-card">
        <div class="workflow-step-tag" style="color: #1d4ed8;">Stage 1</div>
        <div class="workflow-title">Baseline Diagnostics</div>
        <p class="workflow-desc">Assess current arrival rates, calculate department wait times, and detect critical bottlenecks.</p>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/1_📊_Current_Analysis.py", label="Run Baseline Diagnostics", icon="📊", use_container_width=True)

with w2:
    st.markdown("""
    <div class="workflow-card">
        <div class="workflow-step-tag" style="color: #059669;">Stage 2</div>
        <div class="workflow-title">Staffing Optimization</div>
        <p class="workflow-desc">Execute the marginal allocation algorithm to rebalance doctors and eliminate queue congestion.</p>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/2_🔧_Optimization.py", label="Execute Optimization Model", icon="🔧", use_container_width=True)

with w3:
    st.markdown("""
    <div class="workflow-card">
        <div class="workflow-step-tag" style="color: #4f46e5;">Stage 3</div>
        <div class="workflow-title">Performance Audit</div>
        <p class="workflow-desc">Quantify percentage delay reduction, daily patient hours saved, and resource efficiency gains.</p>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/3_📈_Comparison.py", label="View Comparative Audit", icon="📈", use_container_width=True)

st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)

# ─── Baseline Hospital OPD Parameters ────────────────────────────
st.markdown("### Baseline Outpatient Department Profile")
st.markdown("Current operating parameters based on standard multi-specialty hospital outpatient departments:")

depts = get_default_departments()
df = get_departments_dataframe(depts)
total_pool = get_total_available_doctors()
current_assigned = sum(d["current_doctors"] for d in depts)
daily_patients = sum(d["arrival_rate"] * 8 for d in depts)

k1, k2, k3, k4 = st.columns(4)
k1.metric("Outpatient Clinics", f"{len(depts)} Active", delta="Specialized OPDs", delta_color="off", help="Number of evaluated clinical specialties")
k2.metric("Assigned Physicians", f"{int(current_assigned)} Doctors", delta="Current Allocation", delta_color="off", help="Total doctors currently assigned")
k3.metric("Expected Patient Inflow", f"{int(daily_patients)} / Day", delta="8-Hour Operating Shift", delta_color="off", help="Expected patient volume across 8 operating hours")
k4.metric("Physician Pool Budget", f"{total_pool} Doctors", delta=f"{total_pool - current_assigned} Reserve for Optimization", delta_color="normal", help="Maximum pool available for optimization")

st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

# Formatted Table
display_df = df.copy()
st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Department": st.column_config.TextColumn("Department", width="medium"),
        "Arrival Rate (λ, patients/hr)": st.column_config.NumberColumn("Arrival Rate (λ / hr)", format="%.1f"),
        "Service Rate (μ, patients/hr/doctor)": st.column_config.NumberColumn("Service Rate (μ / doc / hr)", format="%.1f"),
        "Current Doctors": st.column_config.NumberColumn("Assigned Doctors", format="%d"),
        "Utilization (ρ)": st.column_config.ProgressColumn(
            "Physician Utilization (ρ)",
            min_value=0.0,
            max_value=1.0,
            format="%.1f%%",
        ),
        "Avg Service Time (min)": st.column_config.NumberColumn("Consultation Duration", format="%.1f min"),
    },
)

st.markdown(
    """
    <div class="pro-callout pro-callout-warning">
        <strong>Initial Diagnostic Observation:</strong>
        <em>Dermatology</em> and <em>General Medicine</em> are operating in high-congestion territory (83.3% – 90.0% utilization),
        creating substantial waiting queues. Meanwhile, <em>Orthopedics</em> operates comfortably at 66.7%.
        Proceed to <strong>Baseline Diagnostics</strong> to inspect the queue metrics in detail.
    </div>
    """,
    unsafe_allow_html=True,
)
