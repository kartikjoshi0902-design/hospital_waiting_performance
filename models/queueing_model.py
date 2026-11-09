"""
Queueing Theory Model — M/M/c
===============================
Implements the M/M/c (multi-server) queueing model for hospital departments.

The M/M/c model assumes:
- Patient arrivals follow a Poisson process with rate λ (Markovian arrivals).
- Service times follow an Exponential distribution with rate μ (Markovian service).
- There are c identical servers (doctors) serving a single FIFO queue.

Key formulas implemented:
- Erlang C formula: probability an arriving patient must wait.
- Average queue length (Lq), waiting time (Wq), system time (Ws).
- Server utilization (ρ).

Reference:
    Gross, D. & Harris, C.M. (1998). Fundamentals of Queueing Theory. Wiley.
"""

import math
import pandas as pd


def erlang_c(num_servers, arrival_rate, service_rate):
    """
    Calculates the Erlang C probability — the probability that an arriving
    patient finds all servers busy and must wait in the queue.

    This is the core formula of the M/M/c model.

    Formula:
        C(c, a) = [(a^c / c!) × (1 / (1 - ρ))] / [Σ_{k=0}^{c-1} (a^k / k!) + (a^c / c!) × (1 / (1 - ρ))]

    where:
        a = λ / μ  (offered load in Erlangs)
        ρ = a / c  (utilization per server)

    Args:
        num_servers (int): c — number of doctors (servers).
        arrival_rate (float): λ — patient arrival rate (patients/hour).
        service_rate (float): μ — service rate per doctor (patients/hour).

    Returns:
        float: Erlang C probability (0 to 1), or None if system is unstable.
    """
    c = num_servers
    lam = arrival_rate
    mu = service_rate

    # Offered load (total work arriving per unit time, in Erlangs)
    a = lam / mu

    # Per-server utilization
    rho = a / c

    # --- Stability check ---
    # The system is stable only if ρ < 1 (servers can handle the load)
    if rho >= 1.0:
        return None  # Unstable: queue grows without bound

    # --- Calculate the summation terms ---
    # Σ_{k=0}^{c-1} (a^k / k!)
    summation = 0.0
    for k in range(c):
        summation += (a ** k) / math.factorial(k)

    # The last term: (a^c / c!) × (1 / (1 - ρ))
    last_term = ((a ** c) / math.factorial(c)) * (1.0 / (1.0 - rho))

    # P0: probability the system is empty (all servers idle)
    p0 = 1.0 / (summation + last_term)

    # Erlang C value
    erlang_c_value = last_term * p0

    return erlang_c_value


def calculate_mmc_metrics(arrival_rate, service_rate, num_servers):
    """
    Calculates all key performance metrics for an M/M/c queue.

    Args:
        arrival_rate (float): λ — patient arrival rate (patients/hour).
        service_rate (float): μ — service rate per doctor (patients/hour).
        num_servers (int): c — number of doctors.

    Returns:
        dict: Dictionary containing:
            - utilization (float): ρ — server utilization (0 to 1)
            - prob_waiting (float): Erlang C probability
            - avg_queue_length (float): Lq — average patients in queue
            - avg_wait_time_hours (float): Wq — average wait time (hours)
            - avg_wait_time_minutes (float): Wq — average wait time (minutes)
            - avg_system_time_hours (float): Ws — average total time in system (hours)
            - avg_system_time_minutes (float): Ws — average total time (minutes)
            - avg_in_system (float): Ls — average patients in system (queue + service)
            - is_stable (bool): Whether the system is stable (ρ < 1)
            - patients_per_day (float): Expected patients in an 8-hour day

        Returns metrics with infinity/error values if the system is unstable.
    """
    c = num_servers
    lam = arrival_rate
    mu = service_rate

    # Per-server utilization
    rho = lam / (c * mu)

    # Check stability
    if rho >= 1.0:
        return {
            "utilization": rho,
            "prob_waiting": 1.0,
            "avg_queue_length": float("inf"),
            "avg_wait_time_hours": float("inf"),
            "avg_wait_time_minutes": float("inf"),
            "avg_system_time_hours": float("inf"),
            "avg_system_time_minutes": float("inf"),
            "avg_in_system": float("inf"),
            "is_stable": False,
            "patients_per_day": lam * 8,
        }

    # Get Erlang C probability
    ec = erlang_c(c, lam, mu)

    # --- Performance Metrics ---

    # Lq: Average number of patients waiting in the queue
    # Lq = C(c, a) × ρ / (1 - ρ)
    lq = ec * rho / (1.0 - rho)

    # Wq: Average time a patient spends waiting in the queue (hours)
    # Wq = Lq / λ  (Little's Law)
    wq = lq / lam

    # Ws: Average total time in the system (waiting + service)
    # Ws = Wq + 1/μ
    ws = wq + (1.0 / mu)

    # Ls: Average number of patients in the system (queue + being served)
    # Ls = λ × Ws  (Little's Law)
    ls = lam * ws

    return {
        "utilization": round(rho, 4),
        "prob_waiting": round(ec, 4),
        "avg_queue_length": round(lq, 4),
        "avg_wait_time_hours": round(wq, 6),
        "avg_wait_time_minutes": round(wq * 60, 2),
        "avg_system_time_hours": round(ws, 6),
        "avg_system_time_minutes": round(ws * 60, 2),
        "avg_in_system": round(ls, 4),
        "is_stable": True,
        "patients_per_day": round(lam * 8, 0),
    }


def analyze_all_departments(departments):
    """
    Runs M/M/c analysis on all departments and returns a summary DataFrame.

    Args:
        departments (list[dict]): List of department configurations. Each dict
            must have keys: 'name', 'arrival_rate', 'service_rate', 'current_doctors'.

    Returns:
        pd.DataFrame: DataFrame with one row per department and columns:
            Department, Doctors, Arrival Rate, Service Rate, Utilization,
            P(Wait), Avg Queue Length, Avg Wait (min), Avg System Time (min),
            Avg In System, Status, Patients/Day
    """
    rows = []
    for dept in departments:
        metrics = calculate_mmc_metrics(
            arrival_rate=dept["arrival_rate"],
            service_rate=dept["service_rate"],
            num_servers=dept["current_doctors"],
        )

        # Determine status label based on utilization
        rho = metrics["utilization"]
        if not metrics["is_stable"]:
            status = "🔴 UNSTABLE"
        elif rho >= 0.85:
            status = "🔴 Overloaded"
        elif rho >= 0.70:
            status = "🟡 Busy"
        elif rho >= 0.50:
            status = "🟢 Normal"
        else:
            status = "🔵 Under-used"

        rows.append({
            "Department": dept["name"],
            "Doctors": dept["current_doctors"],
            "Arrival Rate (λ)": dept["arrival_rate"],
            "Service Rate (μ)": dept["service_rate"],
            "Utilization (ρ)": metrics["utilization"],
            "P(Wait)": metrics["prob_waiting"],
            "Avg Queue Length": metrics["avg_queue_length"],
            "Avg Wait (min)": metrics["avg_wait_time_minutes"],
            "Avg System Time (min)": metrics["avg_system_time_minutes"],
            "Avg In System": metrics["avg_in_system"],
            "Status": status,
            "Patients/Day": metrics["patients_per_day"],
        })

    return pd.DataFrame(rows)


def analyze_with_allocation(departments, allocation):
    """
    Runs M/M/c analysis using a custom doctor allocation (instead of current).

    This is used to evaluate optimized allocations.

    Args:
        departments (list[dict]): List of department configurations.
        allocation (list[int]): Number of doctors assigned to each department.

    Returns:
        pd.DataFrame: Same format as analyze_all_departments().
    """
    # Create modified departments with the new allocation
    modified = []
    for i, dept in enumerate(departments):
        mod_dept = dept.copy()
        mod_dept["current_doctors"] = allocation[i]
        modified.append(mod_dept)

    return analyze_all_departments(modified)

