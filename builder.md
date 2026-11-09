# Builder Guide: Hospital Patient Wait-Time Optimization

> **A step-by-step developer guide for implementing the project from scratch.**
> Designed for beginners — no step is left unexplained.

---

## Table of Contents

1. [Project Folder Structure](#1-project-folder-structure)
2. [Technology Stack and Dependencies](#2-technology-stack-and-dependencies)
3. [File Responsibilities](#3-file-responsibilities)
4. [Implementation Steps (In Order)](#4-implementation-steps-in-order)
5. [Algorithm Explanations and Pseudocode](#5-algorithm-explanations-and-pseudocode)
6. [Input/Output Specifications](#6-inputoutput-specifications)
7. [Integrating the Two OR Techniques](#7-integrating-the-two-or-techniques)
8. [Testing and Debugging Instructions](#8-testing-and-debugging-instructions)

---

## 1. Project Folder Structure

```
OperationResearch/
│
├── README.md                        # Project overview, install, usage
├── implementation_plan.md           # Problem statement, math, roadmap
├── builder.md                       # THIS FILE — developer guide
├── requirements.txt                 # Python package dependencies
│
├── data/
│   ├── __init__.py                  # Makes 'data' a Python package
│   └── hospital_data.py            # Generates synthetic hospital data
│
├── models/
│   ├── __init__.py                  # Makes 'models' a Python package
│   ├── queueing_model.py           # M/M/c queueing theory engine
│   └── optimization_model.py       # Linear programming optimizer
│
├── utils/
│   ├── __init__.py                  # Makes 'utils' a Python package
│   └── helpers.py                   # Formatting and shared utilities
│
├── app.py                           # Main Streamlit entry point
│
└── pages/
    ├── 1_📊_Current_Analysis.py     # Page: Baseline analysis dashboard
    ├── 2_🔧_Optimization.py         # Page: Run optimization & see results
    └── 3_📈_Comparison.py           # Page: Before vs. After comparison
```

### Why This Structure?

- **`data/`**: Separates data generation from business logic.
- **`models/`**: Each OR technique gets its own file — easy to test independently.
- **`utils/`**: Shared code that doesn't belong to any one model.
- **`pages/`**: Streamlit's multi-page app convention — each file becomes a navigation page.
- **`app.py`**: The entry point that Streamlit runs. It sets up the home page.

---

## 2. Technology Stack and Dependencies

### Core Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `streamlit` | ≥ 1.28 | Interactive web dashboard |
| `numpy` | ≥ 1.24 | Numerical calculations (factorial, arrays) |
| `pandas` | ≥ 2.0 | DataFrames for tabular data |
| `plotly` | ≥ 5.18 | Interactive charts and visualizations |
| `scipy` | ≥ 1.11 | Optimization solver (`scipy.optimize`) |

### requirements.txt

```
streamlit>=1.28.0
numpy>=1.24.0
pandas>=2.0.0
plotly>=5.18.0
scipy>=1.11.0
```

### Installation

```bash
# Navigate to project directory
cd OperationResearch

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Mac/Linux
# venv\Scripts\activate   # On Windows

# Install dependencies
pip install -r requirements.txt
```

---

## 3. File Responsibilities

### `data/hospital_data.py`
**Purpose:** Generate and provide synthetic hospital department data.

**Responsibilities:**
- Define a function that returns a list of department dictionaries.
- Each dictionary contains: department name, arrival rate (λ), service rate (μ), and current doctor count (c).
- Provide a function to generate individual patient arrival records for display.
- All data parameters should be realistic and documented.

**Does NOT:** Perform any calculations or optimization.

---

### `models/queueing_model.py`
**Purpose:** Implement M/M/c queueing theory calculations.

**Responsibilities:**
- Calculate the Erlang C probability (probability of waiting).
- Calculate average queue length (Lq).
- Calculate average waiting time in queue (Wq).
- Calculate average time in system (Ws).
- Calculate server utilization (ρ).
- Analyze all departments and return a summary DataFrame.

**Key function signatures:**
```python
def erlang_c(c: int, arrival_rate: float, service_rate: float) -> float
def calculate_mmc_metrics(arrival_rate: float, service_rate: float, num_servers: int) -> dict
def analyze_all_departments(departments: list) -> pd.DataFrame
```

**Does NOT:** Optimize anything — only calculates metrics for given inputs.

---

### `models/optimization_model.py`
**Purpose:** Find the optimal doctor allocation across departments.

**Responsibilities:**
- Take the list of departments and total available doctors as input.
- Enumerate feasible integer allocations (or use optimization).
- For each feasible allocation, calculate total weighted waiting time using queueing model.
- Return the allocation that minimizes total waiting time.
- Return comparison metrics (before vs. after).

**Key function signatures:**
```python
def optimize_doctor_allocation(departments: list, total_doctors: int) -> dict
def get_optimization_comparison(departments: list, optimal_allocation: dict) -> pd.DataFrame
```

**Does NOT:** Handle UI or visualization.

---

### `utils/helpers.py`
**Purpose:** Shared utility functions.

**Responsibilities:**
- Format time values (minutes/seconds) for display.
- Format numbers with appropriate precision.
- Color-coding helpers for metrics (green = good, red = bad).
- Constants used across the project.

---

### `app.py`
**Purpose:** Main Streamlit entry point — the Home page.

**Responsibilities:**
- Configure the Streamlit page (title, icon, layout).
- Display project introduction and overview.
- Explain the two OR techniques briefly.
- Provide navigation guidance to other pages.

**Does NOT:** Contain analysis or optimization logic.

---

### `pages/1_📊_Current_Analysis.py`
**Purpose:** Baseline queueing analysis dashboard.

**Responsibilities:**
- Load department data.
- Run M/M/c analysis on current (baseline) allocation.
- Display KPI cards: total patients/day, avg wait time, max wait time.
- Show department-wise metrics table.
- Visualize waiting times, utilization, and queue lengths with charts.
- Highlight bottleneck departments.
- Allow users to adjust parameters via sidebar sliders.

---

### `pages/2_🔧_Optimization.py`
**Purpose:** Run optimization and show results.

**Responsibilities:**
- Allow user to set total available doctors.
- Run the LP-based optimization.
- Display the optimal allocation.
- Show how doctors are redistributed.
- Display resulting metrics for the optimized scenario.
- Explain the optimization process step by step.

---

### `pages/3_📈_Comparison.py`
**Purpose:** Side-by-side before vs. after comparison.

**Responsibilities:**
- Run both baseline and optimized analyses.
- Display KPI comparison cards (with improvement percentages).
- Show grouped bar charts comparing metrics.
- Show doctor allocation changes (before → after).
- Provide a summary of improvements.

---

## 4. Implementation Steps (In Order)

### Step 1: Create Project Structure

```bash
mkdir -p OperationResearch/{data,models,utils,pages}
touch OperationResearch/data/__init__.py
touch OperationResearch/models/__init__.py
touch OperationResearch/utils/__init__.py
```

### Step 2: Create `requirements.txt`

Write the dependencies file as shown in Section 2.

### Step 3: Implement `data/hospital_data.py`

```python
# Pseudocode:
def get_default_departments():
    return [
        {
            "name": "General Medicine",
            "arrival_rate": 12,       # λ: patients per hour
            "service_rate": 3.0,      # μ: patients per hour per doctor
            "current_doctors": 3      # c: number of doctors
        },
        # ... more departments
    ]
```

**Synthetic data guidelines:**
- Arrival rates: 5-15 patients/hour (realistic for OPD).
- Service rates: 2-5 patients/hour (12-30 min per patient).
- Doctor counts: 2-4 per department.
- Create one department that is clearly a bottleneck (high ρ).
- Create one department that is over-resourced (low ρ).

### Step 4: Implement `models/queueing_model.py`

This is the mathematical core. Implement carefully.

```python
# Pseudocode for Erlang C:
def erlang_c(c, lam, mu):
    a = lam / mu                    # offered load
    rho = a / c                     # utilization per server

    if rho >= 1:
        return None  # unstable system

    # Calculate P0 (probability system is empty)
    sum_terms = sum(a^k / k! for k in range(c))
    last_term = (a^c / c!) * (1 / (1 - rho))
    P0 = 1 / (sum_terms + last_term)

    # Erlang C value
    C = (a^c / c!) * (1 / (1 - rho)) * P0
    return C
```

```python
# Pseudocode for metrics:
def calculate_mmc_metrics(lam, mu, c):
    rho = lam / (c * mu)
    C = erlang_c(c, lam, mu)

    Lq = C * rho / (1 - rho)        # avg queue length
    Wq = Lq / lam                    # avg wait time (hours)
    Ws = Wq + 1/mu                   # avg system time (hours)
    Ls = lam * Ws                    # avg number in system

    return {
        "utilization": rho,
        "prob_waiting": C,
        "avg_queue_length": Lq,
        "avg_wait_time_hours": Wq,
        "avg_wait_time_minutes": Wq * 60,
        "avg_system_time_hours": Ws,
        "avg_system_time_minutes": Ws * 60,
        "avg_in_system": Ls
    }
```

### Step 5: Implement `models/optimization_model.py`

```python
# Pseudocode for optimization:
def optimize_doctor_allocation(departments, total_doctors):
    n = len(departments)

    # Minimum doctors needed for stability in each dept
    min_doctors = [ceil(dept.arrival_rate / dept.service_rate) + 1
                   for dept in departments]

    # Remaining doctors to distribute
    remaining = total_doctors - sum(min_doctors)

    # Try all feasible allocations using recursive enumeration
    # For each allocation, compute total weighted waiting time
    best_allocation = None
    best_cost = infinity

    for each feasible allocation:
        cost = sum(
            dept.arrival_rate * Wq(dept.arrival_rate, dept.service_rate, alloc[i])
            for i, dept in enumerate(departments)
        )
        if cost < best_cost:
            best_cost = cost
            best_allocation = allocation

    return best_allocation
```

**Implementation note:** For 5 departments and ~18 doctors, the number of feasible allocations is manageable (a few thousand at most). A simple recursive generator or `itertools` approach works fine.

### Step 6: Implement `utils/helpers.py`

```python
def format_time(minutes):
    """Format minutes into a readable string."""
    if minutes < 1:
        return f"{minutes * 60:.0f} seconds"
    return f"{minutes:.1f} minutes"

def get_status_color(utilization):
    """Return color based on utilization level."""
    if utilization < 0.6:
        return "green"    # Under-utilized
    elif utilization < 0.85:
        return "orange"   # Normal
    else:
        return "red"      # Overloaded
```

### Step 7: Implement `app.py`

```python
import streamlit as st

st.set_page_config(
    page_title="Hospital Wait-Time Optimizer",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 Hospital Patient Wait-Time Optimizer")
st.markdown("### Using Operations Research to Reduce Patient Waiting Times")

# Project overview, technique explanations, navigation
```

### Step 8: Implement Page 1 — Current Analysis

- Use `st.columns()` for KPI cards at the top.
- Use `plotly.express` for bar charts and gauges.
- Use `st.dataframe()` for the metrics table.
- Add sidebar sliders to let users adjust arrival/service rates.

### Step 9: Implement Page 2 — Optimization

- Add a number input for total available doctors.
- Show a "Run Optimization" button.
- Display results in a clear table format.
- Show which departments gain/lose doctors.

### Step 10: Implement Page 3 — Comparison

- Compute both baseline and optimized metrics.
- Use grouped bar charts (`plotly.graph_objects`).
- Show improvement percentages with delta indicators.
- Add a summary paragraph.

### Step 11: Polish and Test

- Verify all mathematical formulas against textbook examples.
- Test edge cases (very high utilization, single doctor).
- Add tooltips and explanatory text.
- Ensure responsive layout.

---

## 5. Algorithm Explanations and Pseudocode

### 5.1 Erlang C Algorithm (Detailed)

```
FUNCTION erlang_c(c, lambda, mu):
    a ← lambda / mu          // offered load (Erlangs)
    rho ← a / c              // per-server utilization

    IF rho >= 1 THEN
        RETURN error("System is unstable")
    END IF

    // Step 1: Compute summation terms for P0
    sum ← 0
    FOR k FROM 0 TO c-1:
        sum ← sum + (a^k / k!)
    END FOR

    // Step 2: Compute the last term
    last ← (a^c / c!) × (1 / (1 - rho))

    // Step 3: P0 = probability system is empty
    P0 ← 1 / (sum + last)

    // Step 4: Erlang C value
    C ← last × P0

    RETURN C
END FUNCTION
```

### 5.2 Doctor Allocation Optimization (Detailed)

```
FUNCTION optimize_allocation(departments[], total_doctors):
    n ← length(departments)

    // Step 1: Find minimum viable allocation
    FOR EACH dept IN departments:
        min_c[dept] ← ceil(dept.lambda / dept.mu) + 1
    END FOR

    IF sum(min_c) > total_doctors THEN
        RETURN error("Not enough doctors for stability")
    END IF

    // Step 2: Start with minimum allocation
    remaining ← total_doctors - sum(min_c)

    // Step 3: Greedy improvement — assign remaining doctors
    //         one at a time to the department where adding
    //         a doctor reduces total waiting time the most
    current_alloc ← copy(min_c)

    FOR i FROM 1 TO remaining:
        best_reduction ← 0
        best_dept ← -1

        FOR EACH dept_index IN 0..n-1:
            current_Wq ← compute_Wq(dept, current_alloc[dept_index])
            new_Wq ← compute_Wq(dept, current_alloc[dept_index] + 1)
            reduction ← dept.lambda × (current_Wq - new_Wq)

            IF reduction > best_reduction THEN
                best_reduction ← reduction
                best_dept ← dept_index
            END IF
        END FOR

        current_alloc[best_dept] ← current_alloc[best_dept] + 1
    END FOR

    RETURN current_alloc
END FUNCTION
```

**Why greedy works here:** Adding a doctor always reduces waiting time in that department. The marginal benefit decreases as more doctors are added. This means the greedy approach (always add to the department with the greatest marginal benefit) produces an optimal or near-optimal solution. For small problem sizes, this is equivalent to the full enumeration approach.

---

## 6. Input/Output Specifications

### Inputs

| Input | Type | Source | Range |
|-------|------|--------|-------|
| Department names | List[str] | `hospital_data.py` | 4-6 departments |
| Arrival rate (λ) | float | User slider / default | 1-20 patients/hr |
| Service rate (μ) | float | User slider / default | 1-10 patients/hr |
| Current doctors (c) | int | Default data | 1-10 per dept |
| Total doctors available | int | User input | 10-30 |

### Outputs

| Output | Type | Unit |
|--------|------|------|
| Server utilization (ρ) | float | 0-1 (or percentage) |
| Probability of waiting | float | 0-1 (or percentage) |
| Average queue length (Lq) | float | patients |
| Average wait time (Wq) | float | minutes |
| Average system time (Ws) | float | minutes |
| Optimal doctor allocation | List[int] | doctors per dept |
| Waiting time improvement | float | percentage |

---

## 7. Integrating the Two OR Techniques

The two techniques are connected as follows:

```
┌─────────────────────────────────────────────────────────┐
│                    DATA LAYER                            │
│  hospital_data.py → departments with λ, μ, c           │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│              TECHNIQUE 1: QUEUEING THEORY               │
│                                                          │
│  queueing_model.py                                       │
│  Input:  λ, μ, c for each department                    │
│  Output: Wq, Lq, ρ, P(wait) for each department        │
│                                                          │
│  Used in: Page 1 (Current Analysis)                      │
│           Page 2 (to evaluate candidate allocations)     │
│           Page 3 (to compute both scenarios)             │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│           TECHNIQUE 2: LINEAR PROGRAMMING               │
│                                                          │
│  optimization_model.py                                   │
│  Input:  departments, total_doctors                      │
│  Process: For each candidate allocation, call            │
│           queueing_model to get Wq(c_i)                 │
│  Output:  Optimal c_i for each department               │
│                                                          │
│  Used in: Page 2 (Optimization)                          │
│           Page 3 (Comparison)                            │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│                 PRESENTATION LAYER                        │
│  Streamlit pages display results, charts, comparisons    │
└─────────────────────────────────────────────────────────┘
```

**Integration points in code:**

```python
# In optimization_model.py:
from models.queueing_model import calculate_mmc_metrics

def objective_function(allocation, departments):
    total_cost = 0
    for i, dept in enumerate(departments):
        metrics = calculate_mmc_metrics(
            dept["arrival_rate"],
            dept["service_rate"],
            allocation[i]
        )
        # Weight by arrival rate (more patients = more important)
        total_cost += dept["arrival_rate"] * metrics["avg_wait_time_minutes"]
    return total_cost
```

---

## 8. Testing and Debugging Instructions

### 8.1 Unit Testing the Queueing Model

**Test Case 1: Known M/M/1 result**
- λ = 4, μ = 5, c = 1
- Expected ρ = 0.8
- Expected Wq = ρ / (μ - λ) = 0.8 / 1 = 0.8 hours = 48 minutes
- Expected Lq = ρ² / (1 - ρ) = 0.64 / 0.2 = 3.2

**Test Case 2: M/M/2 verification**
- λ = 6, μ = 4, c = 2
- Expected ρ = 0.75
- Verify against published M/M/c tables.

**Test Case 3: Stability check**
- λ = 10, μ = 3, c = 3 → ρ = 1.11 → should return error/warning.

### 8.2 Testing the Optimizer

**Test Case 1: Already optimal**
- If current allocation is already optimal, optimizer should return same allocation.

**Test Case 2: Obvious bottleneck**
- One department with ρ = 0.95, another with ρ = 0.3.
- Optimizer should move doctors from low-ρ to high-ρ department.

**Test Case 3: Minimum viability**
- Total doctors = sum of minimum required → only one feasible allocation.

### 8.3 Debugging Tips

1. **Print intermediate values**: Add `st.write(metrics)` or `print()` statements to verify calculations.
2. **Compare with online calculators**: Use online M/M/c calculators to verify your results:
   - Search "M/M/c queue calculator" and compare Wq, Lq values.
3. **Check units**: Ensure λ and μ are in the same units (patients/hour). Wq will be in hours — convert to minutes for display.
4. **Watch for division by zero**: When ρ = 1 or c = 0, formulas break. Add guards.
5. **Factorial overflow**: For large c values, use `math.factorial()` which handles big integers in Python.

### 8.4 Running the Application

```bash
# From the project root directory:
streamlit run app.py

# The app opens at http://localhost:8501
# Navigate using the sidebar to visit each page
```

### 8.5 Common Issues

| Issue | Cause | Fix |
|-------|-------|-----|
| "Module not found" | Import paths wrong | Run from project root; use relative imports |
| Infinite Wq | ρ ≥ 1 (unstable) | Add more doctors or reduce arrival rate |
| Blank page | Error in page file | Check terminal for error traceback |
| Charts not showing | Plotly not installed | `pip install plotly` |
| Sidebar empty | Files not in `pages/` folder | Ensure correct folder structure |

