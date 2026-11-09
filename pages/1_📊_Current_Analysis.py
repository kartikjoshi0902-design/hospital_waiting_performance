"""
📊 Current Analysis — Baseline Queueing Theory Dashboard
==========================================================
Diagnostic analysis of current hospital outpatient operations using
the M/M/c stochastic queueing model.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from data.hospital_data import get_default_departments, generate_patient_arrivals
from models.queueing_model import analyze_all_departments, calculate_mmc_metrics
from utils.helpers import format_time
from utils.ui_theme import inject_custom_css, render_header, render_sidebar_branding, apply_plotly_theme, COLORS

# ─── Page Configuration ──────────────────────────────────────────
st.set_page_config(
    page_title="Baseline Operations Analysis | M/M/c Model",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Inject UI Theme ─────────────────────────────────────────────
inject_custom_css()
render_sidebar_branding()

# ─── Header ──────────────────────────────────────────────────────
render_header(
    title="Baseline Operations Analysis",
    subtitle="M/M/c Multi-Server Stochastic Queueing Diagnostics & Congestion Analysis",
    tag="STAGE 1 • SYSTEM DIAGNOSIS",
    icon="📊"
)

# ─── Sidebar: Controls & Presets ─────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Operating Scenario")
    scenario = st.selectbox(
        "Select Operating Condition Preset",
        [
            "Standard Shift (Baseline)",
            "Monday Morning Rush (+30% Demand)",
            "Staff Shortage (-1 Doctor in Med/Derma)",
            "Custom Configuration"
        ],
        help="Quickly load typical operational scenarios to assess system resilience."
    )

    departments = get_default_departments()

    if scenario == "Monday Morning Rush (+30% Demand)":
        for d in departments:
            d["arrival_rate"] = round(d["arrival_rate"] * 1.3, 1)
        st.info("⚡ Influx increased by 30% across all outpatient departments.")
    elif scenario == "Staff Shortage (-1 Doctor in Med/Derma)":
        for d in departments:
            if d["name"] in ["General Medicine", "Dermatology"]:
                d["current_doctors"] = max(1, d["current_doctors"] - 1)
        st.warning("⚠️ 1 doctor absent in General Medicine and Dermatology.")

    is_custom = (scenario == "Custom Configuration")

    if is_custom:
        st.markdown("---")
        st.markdown("#### ✏️ Custom Parameter Tuner")
        for i, dept in enumerate(departments):
            with st.expander(f"🩺 {dept['name']}", expanded=(i == 0)):
                departments[i]["arrival_rate"] = st.slider(
                    "Arrival Rate λ (pts/hr)",
                    min_value=1.0, max_value=25.0,
                    value=float(dept["arrival_rate"]), step=0.5,
                    key=f"arr_{i}"
                )
                departments[i]["service_rate"] = st.slider(
                    "Service Rate μ (pts/hr/doc)",
                    min_value=1.0, max_value=10.0,
                    value=float(dept["service_rate"]), step=0.5,
                    key=f"srv_{i}"
                )
                departments[i]["current_doctors"] = st.slider(
                    "Assigned Doctors (c)",
                    min_value=1, max_value=10,
                    value=int(dept["current_doctors"]), step=1,
                    key=f"doc_{i}"
                )

# ─── Run Queueing Analysis ───────────────────────────────────────
results_df = analyze_all_departments(departments)

# Calculate system-wide KPIs
total_patients_day = results_df["Patients/Day"].sum()
total_arrival = sum(d["arrival_rate"] for d in departments)

# Filter out unstable infinities for mean calculations
finite_waits = [
    r["Avg Wait (min)"] for _, r in results_df.iterrows()
    if r["Avg Wait (min)"] != float("inf")
]
unstable_count = (results_df["Utilization (ρ)"] >= 1.0).sum()
bottleneck_count = ((results_df["Utilization (ρ)"] >= 0.85) & (results_df["Utilization (ρ)"] < 1.0)).sum()
max_util = results_df["Utilization (ρ)"].max()

# Weighted average wait time across all patients
weighted_wait = sum(
    r["Avg Wait (min)"] * d["arrival_rate"]
    for (_, r), d in zip(results_df.iterrows(), departments)
    if r["Avg Wait (min)"] != float("inf")
) / total_arrival

# ─── Executive KPI Cards ─────────────────────────────────────────
st.markdown("### Executive Diagnostic Summary")

k1, k2, k3, k4, k5 = st.columns(5)

with k1:
    st.metric(
        "Expected Daily Volume",
        f"{int(total_patients_day)} Patients",
        delta="8-Hour Total Volume",
        delta_color="off",
        help="Total patient volume arriving across an 8-hour shift"
    )
with k2:
    st.metric(
        "Weighted Mean Delay",
        format_time(weighted_wait) if weighted_wait else "N/A",
        delta="Arrival-Weighted",
        delta_color="off",
        help="System-wide average waiting time weighted by department arrival volume"
    )
with k3:
    max_wait = max(finite_waits) if finite_waits else float("inf")
    st.metric(
        "Peak Clinic Delay",
        format_time(max_wait) if max_wait != float("inf") else "∞ Unstable",
        delta="Longest Queue" if max_wait > 20 else "Normal",
        delta_color="inverse"
    )
with k4:
    st.metric(
        "Peak Staff Utilization",
        f"{max_util:.1%}",
        delta="Over Capacity" if max_util >= 0.85 else "Stable",
        delta_color="inverse" if max_util >= 0.85 else "normal"
    )
with k5:
    critical_total = unstable_count + bottleneck_count
    st.metric(
        "Bottleneck Clinics",
        f"{critical_total} / {len(departments)}",
        delta=f"{unstable_count} Unstable" if unstable_count > 0 else f"{bottleneck_count} Overloaded",
        delta_color="inverse" if critical_total > 0 else "normal"
    )

st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

# ─── Alert Callout ───────────────────────────────────────────────
unstable_depts = results_df[results_df["Utilization (ρ)"] >= 1.0]["Department"].tolist()
bottleneck_depts = results_df[(results_df["Utilization (ρ)"] >= 0.85) & (results_df["Utilization (ρ)"] < 1.0)]["Department"].tolist()

if unstable_depts:
    st.markdown(f"""
    <div class="pro-callout pro-callout-danger">
        <div>
            <strong>CRITICAL INSTABILITY:</strong> Department(s) <strong>{', '.join(unstable_depts)}</strong> operate at or above 100% capacity (&rho; &ge; 1.0).
            Patient inflow exceeds service capacity, causing queues to grow indefinitely without immediate staff reallocation.
        </div>
    </div>
    """, unsafe_allow_html=True)
elif bottleneck_depts:
    st.markdown(f"""
    <div class="pro-callout pro-callout-warning">
        <div>
            <strong>CAPACITY BOTTLENECK:</strong> Clinic(s) <strong>{', '.join(bottleneck_depts)}</strong> operate above the 85% safety threshold.
            Patients experience excessive waiting delays. Algorithmic reallocation is recommended.
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="pro-callout pro-callout-success">
        <div>
            <strong>STABLE OPERATIONS:</strong> All outpatient departments operate within standard capacity thresholds (&rho; &lt; 85%).
        </div>
    </div>
    """, unsafe_allow_html=True)

# ─── Performance Data Table ──────────────────────────────────────
st.markdown("### Department Queueing Performance Matrix")

# Prepare styled dataframe
table_df = results_df.copy()

st.dataframe(
    table_df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Department": st.column_config.TextColumn("Department", width="medium"),
        "Arrival Rate (λ)": st.column_config.NumberColumn("Arrival Rate (λ)", format="%.1f / hr"),
        "Service Rate (μ)": st.column_config.NumberColumn("Service Rate (μ)", format="%.1f / hr"),
        "Doctors (c)": st.column_config.NumberColumn("Doctors (c)", format="%d"),
        "Utilization (ρ)": st.column_config.ProgressColumn(
            "Physician Utilization (ρ)",
            min_value=0.0,
            max_value=1.1,
            format="%.1f%%",
            help="Optimal: 50-70%, Near Capacity: 70-85%, Critical: >85%"
        ),
        "P(Wait)": st.column_config.NumberColumn("P(Wait)", format="%.1f%%", help="Probability an arriving patient must wait"),
        "Avg Wait (min)": st.column_config.NumberColumn("Mean Delay (min)", format="%.1f min", help="Expected delay in queue"),
        "Avg Queue Length": st.column_config.NumberColumn("Mean Queue (pts)", format="%.1f", help="Expected patients in queue"),
        "Patients/Day": st.column_config.NumberColumn("Daily Volume", format="%d"),
    }
)

st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

# ─── Visual Analytics Tabs ───────────────────────────────────────
st.markdown("### Visual Diagnostic Analytics")

tab1, tab2, tab3, tab4 = st.tabs([
    "Wait Time Breakdown",
    "Utilization & Capacity Benchmarks",
    "Non-Linear Queue Congestion Curve",
    "Daily Arrival Timeline"
])

# --- Tab 1: Wait Time Breakdown ---
with tab1:
    plot_df = results_df.copy()
    max_finite = plot_df["Avg Wait (min)"].replace(float("inf"), 0).max()
    cap_val = max(max_finite * 1.3, 30)
    plot_df["Display Wait"] = plot_df["Avg Wait (min)"].apply(lambda x: min(x, cap_val))

    fig_wait = px.bar(
        plot_df,
        x="Department",
        y="Display Wait",
        color="Display Wait",
        color_continuous_scale=["#10b981", "#f59e0b", "#ef4444"],
        text="Display Wait",
        labels={"Display Wait": "Wait Time (min)"}
    )
    fig_wait.update_traces(
        texttemplate="%{text:.1f} min",
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>Average Wait: %{y:.1f} min<extra></extra>"
    )
    fig_wait.add_hline(
        y=15.0,
        line_dash="dot",
        line_color="#64748b",
        annotation_text="Hospital Target SLA (15 min)",
        annotation_position="top left",
        annotation_font=dict(size=11, color="#64748b")
    )
    fig_wait.update_layout(
        title="Average Patient Wait Time by Specialty",
        yaxis_title="Average Waiting Time (minutes)",
        xaxis_title="",
        coloraxis_showscale=False
    )
    apply_plotly_theme(fig_wait, height=430)
    st.plotly_chart(fig_wait, use_container_width=True)

    st.markdown("""
    <div style="font-size: 0.88rem; color: #64748b;">
        💡 <strong>Key Operational Takeaway:</strong> Clinics with bars exceeding the 15-minute SLA target are primary targets for physician reallocation in Stage 2.
    </div>
    """, unsafe_allow_html=True)

# --- Tab 2: Utilization ---
with tab2:
    colors = []
    for u in results_df["Utilization (ρ)"].values:
        if u >= 0.85:
            colors.append("#ef4444")
        elif u >= 0.70:
            colors.append("#f59e0b")
        elif u >= 0.50:
            colors.append("#10b981")
        else:
            colors.append("#0ea5e9")

    fig_util = go.Figure()
    fig_util.add_trace(go.Bar(
        x=results_df["Department"],
        y=results_df["Utilization (ρ)"],
        marker_color=colors,
        text=[f"{v:.1%}" for v in results_df["Utilization (ρ)"]],
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>Utilization: %{y:.1%}<extra></extra>"
    ))

    fig_util.add_hline(
        y=0.85, line_dash="dash", line_color="#ef4444",
        annotation_text="Overloaded Zone (≥85%)", annotation_position="top right"
    )
    fig_util.add_hline(
        y=0.70, line_dash="dash", line_color="#f59e0b",
        annotation_text="Busy Zone (70%)", annotation_position="top right"
    )
    fig_util.add_hline(
        y=0.50, line_dash="dot", line_color="#10b981",
        annotation_text="Optimal Utilization (50%)", annotation_position="bottom right"
    )

    fig_util.update_layout(
        title="Doctor Utilization (ρ) vs Capacity Benchmarks",
        yaxis_title="Utilization Ratio",
        yaxis=dict(tickformat=".0%", range=[0, max(1.15, max(results_df["Utilization (ρ)"]) + 0.15)]),
        xaxis_title="",
        showlegend=False
    )
    apply_plotly_theme(fig_util, height=430)
    st.plotly_chart(fig_util, use_container_width=True)

    st.markdown("""
    <div style="display: flex; gap: 15px; font-size: 0.82rem; margin-top: 5px;">
        <span style="color: #ef4444; font-weight: 700;">● Red: Overloaded (≥85%)</span>
        <span style="color: #f59e0b; font-weight: 700;">● Amber: Busy (70-85%)</span>
        <span style="color: #10b981; font-weight: 700;">● Green: Optimal (50-70%)</span>
        <span style="color: #0ea5e9; font-weight: 700;">● Blue: Under-utilized (&lt;50%)</span>
    </div>
    """, unsafe_allow_html=True)

# --- Tab 3: Non-Linear Queue Explosion Curve ---
with tab3:
    st.markdown("#### The Mathematical Law of Congestion: Non-Linear Queue Growth")
    st.markdown("""
    A fundamental law of Queueing Theory is that **waiting time does NOT scale linearly with utilization**.
    As utilization exceeds **80%**, the queue explodes asymptotically towards infinity.
    """)

    # Let user pick a clinic to view its theoretical curve
    selected_dept_name = st.selectbox(
        "Select Department to Inspect Operating Point on Theoretical Curve",
        [d["name"] for d in departments],
        index=0
    )
    sel_dept = next(d for d in departments if d["name"] == selected_dept_name)

    c_val = sel_dept["current_doctors"]
    mu_val = sel_dept["service_rate"]
    curr_lam = sel_dept["arrival_rate"]
    curr_rho = curr_lam / (c_val * mu_val)

    # Compute theoretical curve
    rho_range = np.linspace(0.15, 0.96, 45)
    curve_waits = []
    for r in rho_range:
        sim_lam = r * c_val * mu_val
        m = calculate_mmc_metrics(sim_lam, mu_val, c_val)
        curve_waits.append(m["avg_wait_time_minutes"])

    curr_metrics = calculate_mmc_metrics(curr_lam, mu_val, c_val)
    curr_wait_val = curr_metrics["avg_wait_time_minutes"]

    fig_curve = go.Figure()

    # The theoretical curve
    fig_curve.add_trace(go.Scatter(
        x=rho_range,
        y=curve_waits,
        mode="lines",
        name=f"Theoretical M/M/{c_val} Curve",
        line=dict(color="#2563eb", width=3),
        hovertemplate="Utilization: %{x:.1%}<br>Predicted Wait: %{y:.1f} min<extra></extra>"
    ))

    # The current operating point
    fig_curve.add_trace(go.Scatter(
        x=[curr_rho],
        y=[curr_wait_val],
        mode="markers+text",
        name="Current Operating Point",
        marker=dict(size=14, color="#ef4444" if curr_rho >= 0.85 else "#10b981", symbol="circle", line=dict(color="white", width=2)),
        text=[f"Current: {curr_rho:.1%} ({curr_wait_val:.1f}m)"],
        textposition="top center",
        textfont=dict(size=12, weight=700, color="#0f172a")
    ))

    # Danger zone shaded area
    fig_curve.add_vrect(
        x0=0.85, x1=1.0,
        fillcolor="rgba(239, 68, 68, 0.12)",
        layer="below",
        line_width=0,
        annotation_text="Critical Congestion Zone (≥85%)",
        annotation_position="top left",
        annotation_font=dict(size=11, color="#ef4444")
    )

    fig_curve.update_layout(
        title=f"Theoretical Wait Curve for {selected_dept_name} (c = {c_val} Doctors, μ = {mu_val:.1f} pts/hr)",
        xaxis_title="Traffic Intensity / Doctor Utilization (ρ)",
        yaxis_title="Expected Wait Time Wq (minutes)",
        xaxis=dict(tickformat=".0%", range=[0.1, 1.0]),
        yaxis=dict(range=[0, max(curve_waits) * 1.1])
    )
    apply_plotly_theme(fig_curve, height=440)
    st.plotly_chart(fig_curve, use_container_width=True)

    st.info(
        f"💡 **Insight for {selected_dept_name}:** Notice the steep 'elbow' of the curve after 80%. "
        f"Even a tiny 5% increase in arrival load causes waiting times to surge exponentially. "
        f"This is why adding just 1 doctor can collapse wait times from 30+ minutes down to 3 minutes!"
    )

# --- Tab 4: Patient Arrivals ---
with tab4:
    arrivals_df = generate_patient_arrivals(departments)

    dept_counts = arrivals_df["department"].value_counts().reset_index()
    dept_counts.columns = ["Department", "Patients"]

    col_sim_1, col_sim_2 = st.columns([1, 1.3])

    with col_sim_1:
        fig_sim_bar = px.bar(
            dept_counts,
            x="Department",
            y="Patients",
            color="Department",
            title="Simulated Patient Registrations (8-Hour Shift)",
            text="Patients"
        )
        fig_sim_bar.update_traces(textposition="outside")
        fig_sim_bar.update_layout(showlegend=False, yaxis_title="Patient Count", xaxis_title="")
        apply_plotly_theme(fig_sim_bar, height=380)
        st.plotly_chart(fig_sim_bar, use_container_width=True)

    with col_sim_2:
        fig_timeline = px.histogram(
            arrivals_df,
            x="arrival_hour",
            color="department",
            nbins=16,
            title="Hourly Influx Timeline (Starting at 09:00 AM)",
            labels={"arrival_hour": "Shift Hour (0 to 8)", "department": "Specialty"}
        )
        fig_timeline.update_layout(yaxis_title="Arrivals per Interval", barmode="stack")
        apply_plotly_theme(fig_timeline, height=380)
        st.plotly_chart(fig_timeline, use_container_width=True)

    with st.expander("🔍 Inspect Simulated Outpatient Event Records (First 15 Patients)"):
        st.dataframe(arrivals_df.head(15), use_container_width=True, hide_index=True)

# ─── Mathematical Background Expander ────────────────────────────
st.markdown("---")
with st.expander("📐 Mathematical Reference: M/M/c Multi-Server Queueing Theory"):
    st.markdown(r"""
    ### Theoretical Foundation: The Erlang C Model

    The outpatient department is modeled as an **M/M/c queueing system**, where:
    - $\lambda$: Mean patient arrival rate per hour (Poisson process)
    - $\mu$: Mean service rate per doctor per hour (Exponential distribution)
    - $c$: Number of parallel doctors (servers)
    - $a = \frac{\lambda}{\mu}$: Offered load in Erlangs
    - $\rho = \frac{a}{c} = \frac{\lambda}{c \cdot \mu}$: Server utilization (traffic intensity)

    **Stability Criterion:**
    The system reaches steady-state equilibrium if and only if $\rho < 1$ ($\lambda < c \cdot \mu$).
    If $\rho \geq 1$, the queue grows infinitely without bound.

    **Erlang C Delay Probability Formula:**
    The probability that an arriving patient must wait in queue before being called into consultation:

    $$P(\text{Wait}) = C(c, a) = \frac{\frac{a^c}{c!} \left(\frac{1}{1-\rho}\right)}{\sum_{k=0}^{c-1} \frac{a^k}{k!} + \frac{a^c}{c!} \left(\frac{1}{1-\rho}\right)}$$

    **Performance Metrics (Little's Law Relations):**
    - **Mean Queue Length:** $L_q = C(c, a) \cdot \frac{\rho}{1 - \rho}$
    - **Mean Waiting Time in Queue:** $W_q = \frac{L_q}{\lambda}$
    - **Mean Time in Department:** $W_s = W_q + \frac{1}{\mu}$
    - **Total Patients in Department:** $L_s = \lambda \cdot W_s = L_q + \frac{\lambda}{\mu}$
    """)

# ─── Navigation Footer ───────────────────────────────────────────
st.markdown("---")
c_foot_1, c_foot_2 = st.columns([2, 1])
with c_foot_1:
    st.markdown("Next: Proceed to **Stage 2: Resource Optimizer** to find the optimal doctor allocation.")
with c_foot_2:
    st.page_link("pages/2_🔧_Optimization.py", label="Proceed to Stage 2: Optimization ➔", icon="🔧", use_container_width=True)
