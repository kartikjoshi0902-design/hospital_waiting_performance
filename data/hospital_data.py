"""
Hospital Data Generator
========================
Generates realistic synthetic data for a multi-department hospital OPD.

All parameters are based on typical Indian hospital outpatient departments.
Data is documented with clear assumptions.

Assumptions:
- 5 departments representing common OPD specialties.
- Arrival rates (λ): patients per hour, following a Poisson process.
- Service rates (μ): patients served per hour per doctor (exponential service times).
- Current doctor allocation represents a typical (possibly suboptimal) staffing decision.
- The hospital operates 8 hours per day.
"""

import numpy as np
import pandas as pd


def get_default_departments():
    """
    Returns the default hospital department configuration.

    Each department is a dictionary with:
        - name (str): Department name
        - arrival_rate (float): λ — average patients arriving per hour
        - service_rate (float): μ — average patients one doctor can serve per hour
        - current_doctors (int): c — number of doctors currently assigned
        - priority_weight (float): Weight for optimization (higher = more critical)

    The data is designed so that:
        - General Medicine is a clear bottleneck (high utilization ~89%)
        - Cardiology is over-resourced (low utilization ~56%)
        - This imbalance allows optimization to demonstrate meaningful improvement.

    Returns:
        list[dict]: List of department configuration dictionaries.
    """
    departments = [
        {
            "name": "General Medicine",
            "arrival_rate": 10.0,       # λ = 10 patients/hour
            "service_rate": 3.0,        # μ = 3 patients/hour/doctor (20 min/patient)
            "current_doctors": 4,       # ρ = 10 / (4 × 3) ≈ 0.833 — HIGH (bottleneck)
            "priority_weight": 1.0,
        },
        {
            "name": "Pediatrics",
            "arrival_rate": 7.0,        # λ = 7 patients/hour
            "service_rate": 4.0,        # μ = 4 patients/hour/doctor (15 min/patient)
            "current_doctors": 2,       # ρ = 7 / (2 × 4) = 0.875 — HIGH
            "priority_weight": 1.0,
        },
        {
            "name": "Orthopedics",
            "arrival_rate": 5.0,        # λ = 5 patients/hour
            "service_rate": 2.5,        # μ = 2.5 patients/hour/doctor (24 min/patient)
            "current_doctors": 3,       # ρ = 5 / (3 × 2.5) ≈ 0.667 — MODERATE
            "priority_weight": 1.0,
        },
        {
            "name": "Cardiology",
            "arrival_rate": 5.0,        # λ = 5 patients/hour
            "service_rate": 2.0,        # μ = 2 patients/hour/doctor (30 min/patient)
            "current_doctors": 3,       # ρ = 5 / (3 × 2) ≈ 0.833 — HIGH
            "priority_weight": 1.2,     # Slightly higher priority (critical dept)
        },
        {
            "name": "Dermatology",
            "arrival_rate": 9.0,        # λ = 9 patients/hour
            "service_rate": 5.0,        # μ = 5 patients/hour/doctor (12 min/patient)
            "current_doctors": 2,       # ρ = 9 / (2 × 5) = 0.90 — VERY HIGH
            "priority_weight": 0.8,
        },
    ]
    return departments


def get_total_available_doctors():
    """
    Returns the total pool of doctors available for allocation.

    This number is intentionally larger than the sum of current allocations
    to allow the optimizer room to redistribute and improve the system.

    Returns:
        int: Total doctors available for allocation.
    """
    return 18


def generate_patient_arrivals(departments, hours=8, seed=42):
    """
    Generates a synthetic patient arrival log for display/demonstration purposes.

    Simulates one day of hospital operation using Poisson process arrivals
    and exponential service times.

    Args:
        departments (list[dict]): List of department configurations.
        hours (int): Number of operating hours to simulate. Default is 8.
        seed (int): Random seed for reproducibility.

    Returns:
        pd.DataFrame: DataFrame with columns:
            - patient_id (int)
            - department (str)
            - arrival_hour (float): Hour of day (0-8)
            - arrival_time (str): Formatted time string (HH:MM)
            - service_time_minutes (float): How long the consultation takes
    """
    np.random.seed(seed)
    records = []
    patient_id = 1

    for dept in departments:
        # Total expected patients in the day
        total_patients = np.random.poisson(dept["arrival_rate"] * hours)

        # Generate random arrival times (uniform over the operating period)
        arrival_hours = np.sort(np.random.uniform(0, hours, total_patients))

        for arr_hour in arrival_hours:
            # Service time from exponential distribution (in minutes)
            service_time = np.random.exponential(60.0 / dept["service_rate"])

            # Convert arrival hour to a clock time (starting at 9:00 AM)
            hour_of_day = 9 + int(arr_hour)
            minute_of_day = int((arr_hour % 1) * 60)
            time_str = f"{hour_of_day:02d}:{minute_of_day:02d}"

            records.append({
                "patient_id": patient_id,
                "department": dept["name"],
                "arrival_hour": round(arr_hour, 2),
                "arrival_time": time_str,
                "service_time_minutes": round(service_time, 1),
            })
            patient_id += 1

    df = pd.DataFrame(records)
    return df


def get_departments_dataframe(departments):
    """
    Converts the departments list to a formatted DataFrame for display.

    Args:
        departments (list[dict]): List of department configurations.

    Returns:
        pd.DataFrame: Formatted DataFrame with department information.
    """
    rows = []
    for dept in departments:
        utilization = dept["arrival_rate"] / (
            dept["current_doctors"] * dept["service_rate"]
        )
        rows.append({
            "Department": dept["name"],
            "Arrival Rate (λ, patients/hr)": dept["arrival_rate"],
            "Service Rate (μ, patients/hr/doctor)": dept["service_rate"],
            "Current Doctors": dept["current_doctors"],
            "Utilization (ρ)": round(utilization, 3),
            "Avg Service Time (min)": round(60 / dept["service_rate"], 1),
        })
    return pd.DataFrame(rows)
