"""
Optimization Model — Doctor Allocation using Linear Programming
=================================================================
Finds the optimal allocation of a fixed pool of doctors across
hospital departments to minimize total weighted patient waiting time.

Approach:
    This is an integer optimization problem. Since the search space is small
    (5 departments, ~18 doctors), we use a greedy marginal-gain algorithm:

    1. Start with the minimum viable allocation (enough doctors for stability).
    2. Iteratively assign one remaining doctor at a time to the department
       where adding a doctor produces the greatest reduction in total
       weighted waiting time.

    This greedy approach works because the waiting-time function Wq(c) is
    convex and decreasing in c — adding a doctor always helps, but with
    diminishing returns. Under these conditions, the greedy assignment
    is provably optimal.

    This is equivalent to solving:
        Minimize  Z = Σ_i  w_i × λ_i × Wq_i(c_i)
        Subject to: Σ_i c_i ≤ C_total
                    c_i ≥ c_min_i  for all i
                    c_i ∈ integers

Reference:
    Hillier, F.S. & Lieberman, G.J. (2021). Introduction to Operations Research.
"""

import math
import pandas as pd
from models.queueing_model import calculate_mmc_metrics


def find_minimum_doctors(departments):
    """
    Finds the minimum number of doctors each department needs for stability.

    For stability, we need ρ < 1, i.e., c × μ > λ, i.e., c > λ/μ.
    Since c must be an integer, c_min = floor(λ/μ) + 1.

    Args:
        departments (list[dict]): List of department configurations.

    Returns:
        list[int]: Minimum doctors required for each department.
    """
    min_doctors = []
    for dept in departments:
        # Minimum c such that c > λ/μ
        min_c = math.floor(dept["arrival_rate"] / dept["service_rate"]) + 1
        min_doctors.append(min_c)
    return min_doctors


def calculate_total_weighted_wait(departments, allocation):
    """
    Calculates the total weighted waiting time for a given allocation.

    The objective function is:
        Z = Σ_i  w_i × λ_i × Wq_i(c_i)

    This represents the total "patient-hours wasted waiting" per hour,
    weighted by department priority.

    Args:
        departments (list[dict]): List of department configurations.
        allocation (list[int]): Number of doctors assigned to each department.

    Returns:
        float: Total weighted waiting time (patient-minutes/hour).
                Returns infinity if any department is unstable.
    """
    total = 0.0
    for i, dept in enumerate(departments):
        metrics = calculate_mmc_metrics(
            arrival_rate=dept["arrival_rate"],
            service_rate=dept["service_rate"],
            num_servers=allocation[i],
        )

        if not metrics["is_stable"]:
            return float("inf")

        # Weighted waiting: (priority) × (patients/hr) × (wait in minutes)
        weight = dept.get("priority_weight", 1.0)
        total += weight * dept["arrival_rate"] * metrics["avg_wait_time_minutes"]

    return total


def optimize_doctor_allocation(departments, total_doctors):
    """
    Finds the optimal doctor allocation using a greedy marginal-gain algorithm.

    Algorithm:
        1. Assign minimum doctors to each department (for stability).
        2. Calculate remaining doctors to distribute.
        3. For each remaining doctor, assign to the department where adding
           one doctor produces the largest reduction in total weighted wait time.

    This greedy approach is optimal because Wq(c) is convex-decreasing:
    the marginal benefit of adding a doctor decreases as c increases.

    Args:
        departments (list[dict]): List of department configurations.
        total_doctors (int): Total number of doctors available.

    Returns:
        dict: Optimization results containing:
            - optimal_allocation (list[int]): Best doctor assignment per department.
            - current_allocation (list[int]): Original doctor assignment.
            - min_allocation (list[int]): Minimum viable assignment.
            - total_doctors (int): Total doctors used.
            - baseline_cost (float): Total weighted wait before optimization.
            - optimized_cost (float): Total weighted wait after optimization.
            - improvement_pct (float): Percentage improvement.
            - is_feasible (bool): Whether a feasible solution was found.
            - allocation_changes (list[dict]): Per-department change details.
    """
    n = len(departments)

    # --- Step 1: Find minimum viable allocation ---
    min_alloc = find_minimum_doctors(departments)
    min_total = sum(min_alloc)

    # Check feasibility
    if total_doctors < min_total:
        return {
            "optimal_allocation": None,
            "current_allocation": [d["current_doctors"] for d in departments],
            "min_allocation": min_alloc,
            "total_doctors": total_doctors,
            "baseline_cost": None,
            "optimized_cost": None,
            "improvement_pct": 0,
            "is_feasible": False,
            "allocation_changes": [],
            "message": (
                f"Need at least {min_total} doctors for system stability, "
                f"but only {total_doctors} are available."
            ),
        }

    # --- Step 2: Start with minimum allocation ---
    current_alloc = list(min_alloc)
    remaining = total_doctors - min_total

    # --- Step 3: Greedy assignment of remaining doctors ---
    for _ in range(remaining):
        best_reduction = -1
        best_dept = 0

        for i in range(n):
            # Current cost with this allocation
            current_cost = calculate_total_weighted_wait(departments, current_alloc)

            # Try adding one doctor to department i
            trial_alloc = list(current_alloc)
            trial_alloc[i] += 1
            trial_cost = calculate_total_weighted_wait(departments, trial_alloc)

            # Marginal reduction in total weighted waiting time
            reduction = current_cost - trial_cost

            if reduction > best_reduction:
                best_reduction = reduction
                best_dept = i

        # Assign the doctor to the best department
        current_alloc[best_dept] += 1

    # --- Step 4: Compute results ---
    original_alloc = [d["current_doctors"] for d in departments]
    baseline_cost = calculate_total_weighted_wait(departments, original_alloc)
    optimized_cost = calculate_total_weighted_wait(departments, current_alloc)

    if baseline_cost > 0:
        improvement_pct = ((baseline_cost - optimized_cost) / baseline_cost) * 100
    else:
        improvement_pct = 0.0

    # Per-department changes
    changes = []
    for i, dept in enumerate(departments):
        orig_metrics = calculate_mmc_metrics(
            dept["arrival_rate"], dept["service_rate"], original_alloc[i]
        )
        opt_metrics = calculate_mmc_metrics(
            dept["arrival_rate"], dept["service_rate"], current_alloc[i]
        )
        changes.append({
            "department": dept["name"],
            "original_doctors": original_alloc[i],
            "optimized_doctors": current_alloc[i],
            "doctor_change": current_alloc[i] - original_alloc[i],
            "original_wait_min": orig_metrics["avg_wait_time_minutes"],
            "optimized_wait_min": opt_metrics["avg_wait_time_minutes"],
            "original_utilization": orig_metrics["utilization"],
            "optimized_utilization": opt_metrics["utilization"],
            "original_queue_length": orig_metrics["avg_queue_length"],
            "optimized_queue_length": opt_metrics["avg_queue_length"],
        })

    return {
        "optimal_allocation": current_alloc,
        "current_allocation": original_alloc,
        "min_allocation": min_alloc,
        "total_doctors": total_doctors,
        "baseline_cost": round(baseline_cost, 2),
        "optimized_cost": round(optimized_cost, 2),
        "improvement_pct": round(improvement_pct, 2),
        "is_feasible": True,
        "allocation_changes": changes,
        "message": "Optimization completed successfully.",
    }


def get_optimization_comparison(departments, optimization_result):
    """
    Creates a comparison DataFrame from optimization results.

    Args:
        departments (list[dict]): List of department configurations.
        optimization_result (dict): Output from optimize_doctor_allocation().

    Returns:
        pd.DataFrame: Comparison table with before/after metrics for each department.
    """
    if not optimization_result["is_feasible"]:
        return pd.DataFrame()

    rows = []
    for change in optimization_result["allocation_changes"]:
        # Calculate wait time improvement percentage
        if change["original_wait_min"] > 0:
            wait_improvement = (
                (change["original_wait_min"] - change["optimized_wait_min"])
                / change["original_wait_min"]
            ) * 100
        else:
            wait_improvement = 0.0

        rows.append({
            "Department": change["department"],
            "Doctors (Before)": change["original_doctors"],
            "Doctors (After)": change["optimized_doctors"],
            "Change": f"{change['doctor_change']:+d}",
            "Wait Time Before (min)": round(change["original_wait_min"], 2),
            "Wait Time After (min)": round(change["optimized_wait_min"], 2),
            "Wait Improvement (%)": round(wait_improvement, 1),
            "Utilization Before": f"{change['original_utilization']:.1%}",
            "Utilization After": f"{change['optimized_utilization']:.1%}",
        })

    return pd.DataFrame(rows)

