# Implementation Plan: Hospital Patient Wait-Time Optimization

## 1. Problem Statement

Hospitals frequently experience long patient waiting times due to inefficient resource allocation and unpredictable patient arrivals. Patients arriving at outpatient departments (OPDs) often face extended waits because:

- **Uneven doctor allocation**: Some departments are overstaffed while others are understaffed.
- **Unpredictable patient flow**: Arrival rates vary by time of day and department.
- **No analytical framework**: Decisions about staffing are based on intuition rather than mathematical models.

This project addresses the problem: **How can we use Operations Research techniques to analyze, predict, and reduce patient waiting times in a multi-department hospital outpatient setting?**

---

## 2. Project Objectives

1. **Model** the hospital outpatient system mathematically using Queueing Theory.
2. **Optimize** doctor allocation across departments using Linear Programming.
3. **Compare** baseline (current) vs. optimized scenarios quantitatively.
4. **Visualize** the improvements through an interactive Streamlit dashboard.
5. **Demonstrate** that traditional OR techniques can meaningfully improve hospital operations.

---

## 3. Selected Operations Research Techniques

### Technique 1: Queueing Theory — M/M/c Model

**What it is:**
The M/M/c model is a multi-server queueing model where:
- **M** (first): Patient arrivals follow a **Markov (Poisson)** process.
- **M** (second): Service times follow a **Markov (Exponential)** distribution.
- **c**: There are **c** parallel servers (doctors) serving the queue.

**Why chosen:**
- Directly models the hospital waiting-line problem.
- Produces exact formulas for average waiting time, queue length, and server utilization.
- Easy to understand: patients arrive → wait in queue → get served by a doctor.
- No simulation needed — closed-form analytical results.
- Industry standard for healthcare capacity planning.

**What it tells us:**
- Average time a patient waits in the queue (Wq).
- Average number of patients waiting (Lq).
- Probability that all doctors are busy (patient must wait).
- Doctor utilization rate (how busy each doctor is).

### Technique 2: Linear Programming — Doctor Allocation Optimization

**What it is:**
Linear Programming (LP) is a mathematical optimization technique that finds the best allocation of limited resources subject to constraints. Here, we allocate a fixed number of doctors across departments to minimize total patient waiting time.

**Why chosen:**
- Naturally complements Queueing Theory: QT tells us the waiting time for a given allocation; LP finds the best allocation.
- Classic OR technique with well-understood mathematics.
- Easy to implement using Python's `scipy.optimize` or `PuLP`.
- Produces clear, actionable recommendations (move X doctors from department A to department B).
- Beginner-friendly: the concept of "minimize an objective subject to constraints" is intuitive.

**What it tells us:**
- The optimal number of doctors to assign to each department.
- The resulting reduction in total weighted waiting time.
- Which departments are bottlenecks and which are over-resourced.

### Why This Combination Works

```
┌──────────────────────┐      ┌──────────────────────────┐
│   Queueing Theory    │      │   Linear Programming     │
│   (M/M/c Model)      │      │   (Doctor Allocation)    │
│                      │      │                          │
│  INPUT: λ, μ, c      │─────▶│  INPUT: Wq(c) from QT   │
│  OUTPUT: Wq, Lq, ρ   │      │  OUTPUT: Optimal c_i     │
│                      │      │  for each department     │
│  "How long do        │      │  "Where should we        │
│   patients wait?"    │      │   place doctors?"        │
└──────────────────────┘      └──────────────────────────┘
         │                              │
         ▼                              ▼
   ┌─────────────────────────────────────────┐
   │     COMPARISON: Before vs. After        │
   │     Dashboard with KPIs & Charts        │
   └─────────────────────────────────────────┘
```

Queueing Theory **diagnoses** the problem; Linear Programming **prescribes** the solution.

---

## 4. Mathematical Concepts and Formulas

### 4.1 M/M/c Queueing Model

**Parameters:**
| Symbol | Meaning |
|--------|---------|
| λ (lambda) | Patient arrival rate (patients/hour) |
| μ (mu) | Service rate per doctor (patients/hour) |
| c | Number of doctors (servers) |
| ρ = λ / (c × μ) | Traffic intensity (utilization per server) |

**Stability condition:** ρ < 1 (i.e., λ < c × μ)

**Erlang C Formula** — Probability that an arriving patient must wait:

```
                (c × ρ)^c
P(wait) = C(c, λ/μ) = ────────────────────────────────────────
                        c! × (1 - ρ)            c-1   (c×ρ)^k
                                      +  Σ     ────────
                                         k=0     k!
```

More precisely:

```
         (cρ)^c / (c! × (1 - ρ))
C(c,a) = ─────────────────────────────────
         Σ_{k=0}^{c-1} (a^k / k!) + (a^c / (c! × (1-ρ)))
```

where a = λ/μ (offered load).

**Performance Metrics:**

| Metric | Formula | Meaning |
|--------|---------|---------|
| Lq | C(c, a) × ρ / (1 - ρ) | Average queue length |
| Wq | Lq / λ | Average waiting time in queue |
| Ws | Wq + 1/μ | Average total time in system |
| Ls | λ × Ws | Average number in system |

### 4.2 Linear Programming for Doctor Allocation

**Decision Variables:**
- c_i = number of doctors assigned to department i (integer)

**Objective Function:**
Minimize total weighted waiting time across all departments:

```
Minimize  Z = Σ_i  (λ_i × Wq_i(c_i))
```

where Wq_i(c_i) is the average waiting time in department i with c_i doctors (from M/M/c model).

**Constraints:**
1. Total doctors available: Σ_i c_i ≤ C_total
2. Minimum doctors per department: c_i ≥ 1 for all i
3. Stability: c_i × μ_i > λ_i for all i (system must be stable)
4. Integer: c_i ∈ {1, 2, 3, ...}

**Note:** Because Wq(c) is a nonlinear function of c, and c must be integer, we use an enumeration/search approach over feasible integer allocations rather than a pure LP solver. This is still within the LP/optimization framework and is practical because the search space is small (typically 4-6 departments, 15-25 total doctors).

---

## 5. Proposed System Architecture

```
OperationResearch/
│
├── README.md                    # Project overview and usage guide
├── implementation_plan.md       # This file
├── builder.md                   # Developer guide
├── requirements.txt             # Python dependencies
│
├── data/
│   └── hospital_data.py         # Synthetic data generation
│
├── models/
│   ├── __init__.py
│   ├── queueing_model.py        # M/M/c queueing theory calculations
│   └── optimization_model.py    # LP-based doctor allocation optimizer
│
├── utils/
│   ├── __init__.py
│   └── helpers.py               # Shared utility functions
│
├── app.py                       # Main Streamlit application
│
└── pages/
    ├── 1_📊_Current_Analysis.py  # Baseline queueing analysis
    ├── 2_🔧_Optimization.py      # LP optimization and results
    └── 3_📈_Comparison.py        # Before vs. After comparison
```

---

## 6. Data Requirements and Assumptions

### Synthetic Data Design

Since real hospital data is sensitive and hard to obtain, we generate realistic synthetic data:

**Department Configuration (5 departments):**

| Department | Arrival Rate (λ, patients/hr) | Service Rate (μ, patients/hr per doctor) | Current Doctors (c) |
|------------|------|------|------|
| General Medicine | 12 | 3.0 | 3 |
| Pediatrics | 8 | 4.0 | 2 |
| Orthopedics | 6 | 2.5 | 2 |
| Cardiology | 5 | 2.0 | 3 |
| Dermatology | 10 | 5.0 | 2 |

**Total doctors available:** 18 (current usage: 12, allowing reallocation)

### Key Assumptions

1. **Poisson arrivals**: Patient arrivals are random and independent (standard assumption).
2. **Exponential service times**: Consultation durations follow an exponential distribution.
3. **FIFO queue discipline**: Patients are served in order of arrival.
4. **Steady-state analysis**: We analyze the system in its long-run average behavior.
5. **Single queue per department**: Each department has one waiting line.
6. **No patient abandonment**: Patients wait until served (no balking or reneging).
7. **Homogeneous doctors**: All doctors in a department have the same service rate.
8. **8-hour operational day**: The hospital OPD operates for 8 hours per day.

---

## 7. Step-by-Step Implementation Roadmap

### Phase 1: Documentation (Steps 1-3)
1. ✅ Create `implementation_plan.md` (this file)
2. ✅ Create `builder.md` (developer guide)
3. ✅ Create `README.md` (project overview)

### Phase 2: Core Models (Steps 4-6)
4. Implement `data/hospital_data.py` — synthetic data generation
5. Implement `models/queueing_model.py` — M/M/c calculations
6. Implement `models/optimization_model.py` — doctor allocation optimizer

### Phase 3: Utilities (Step 7)
7. Implement `utils/helpers.py` — formatting, shared functions

### Phase 4: Dashboard (Steps 8-11)
8. Implement `app.py` — main Streamlit app with navigation
9. Implement `pages/1_📊_Current_Analysis.py` — baseline analysis page
10. Implement `pages/2_🔧_Optimization.py` — optimization page
11. Implement `pages/3_📈_Comparison.py` — comparison page

### Phase 5: Polish (Steps 12-13)
12. Add styling, tooltips, and explanatory text
13. Test end-to-end and verify calculations

---

## 8. Expected Outcomes

### Quantitative Results (Expected)
- **20-40% reduction** in average patient waiting time after optimization.
- **Identification of 1-2 bottleneck departments** that are severely understaffed.
- **Improved doctor utilization balance** — no department above 90% or below 40% utilization.

### Dashboard Deliverables
- Interactive KPI cards showing key metrics.
- Department-wise waiting time bar charts (before vs. after).
- Doctor utilization gauges.
- Queue length comparison charts.
- Clear textual explanation of what each OR technique does.

### Educational Value
- Clear demonstration that mathematical optimization outperforms intuition-based staffing.
- Reproducible results with adjustable parameters.
- Understandable by non-technical audiences through the dashboard.

---

## 9. Possible Limitations

1. **Steady-state assumption**: Real hospitals have time-varying arrival rates (rush hours). Our model assumes constant rates.
2. **Exponential service times**: Real consultation times may not be perfectly exponential (some are longer for complex cases).
3. **No priority queues**: Emergency patients are not modeled separately.
4. **Integer optimization simplification**: We use enumeration rather than true integer programming for small problem sizes.
5. **Single-stage model**: We don't model multi-stage patient flows (e.g., registration → consultation → lab → pharmacy).
6. **No appointment scheduling**: We model walk-in (random arrival) scenarios only.
7. **Homogeneous doctors**: In reality, senior doctors may serve faster than junior ones.

These limitations are acceptable for a demonstration project and can be noted as future improvements.

