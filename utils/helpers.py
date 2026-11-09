"""
Utility Functions
==================
Shared helper functions for formatting, display, and constants.
"""


# ─── Constants ───────────────────────────────────────────────────

OPERATING_HOURS = 8  # Hospital OPD operates 8 hours per day
START_HOUR = 9       # OPD starts at 9:00 AM


# ─── Time Formatting ─────────────────────────────────────────────

def format_time(minutes):
    """
    Formats a time value in minutes into a human-readable string.

    Examples:
        format_time(0.5)  → "30 sec"
        format_time(5.3)  → "5.3 min"
        format_time(75)   → "1h 15min"
        format_time(inf)  → "∞ (unstable)"

    Args:
        minutes (float): Time in minutes.

    Returns:
        str: Formatted time string.
    """
    if minutes == float("inf"):
        return "∞ (unstable)"
    if minutes < 1:
        return f"{minutes * 60:.0f} sec"
    if minutes < 60:
        return f"{minutes:.1f} min"
    hours = int(minutes // 60)
    mins = int(minutes % 60)
    return f"{hours}h {mins}min"


def format_number(value, decimals=1):
    """
    Formats a number with the specified decimal places.
    Handles infinity gracefully.

    Args:
        value (float): Number to format.
        decimals (int): Number of decimal places.

    Returns:
        str: Formatted number string.
    """
    if value == float("inf"):
        return "∞"
    return f"{value:.{decimals}f}"


# ─── Status and Color Helpers ────────────────────────────────────

def get_utilization_status(utilization):
    """
    Returns a status label and color based on server utilization.

    Guidelines (common in healthcare OR literature):
        - < 50%: Under-utilized (resources being wasted)
        - 50-70%: Normal (healthy operating range)
        - 70-85%: Busy (approaching capacity)
        - 85-100%: Overloaded (long wait times expected)
        - ≥ 100%: Unstable (queue grows infinitely)

    Args:
        utilization (float): Server utilization (ρ), 0 to 1+.

    Returns:
        tuple: (status_label: str, color: str)
    """
    if utilization >= 1.0:
        return "🔴 UNSTABLE", "red"
    elif utilization >= 0.85:
        return "🔴 Overloaded", "red"
    elif utilization >= 0.70:
        return "🟡 Busy", "orange"
    elif utilization >= 0.50:
        return "🟢 Normal", "green"
    else:
        return "🔵 Under-used", "blue"


def get_improvement_color(improvement_pct):
    """
    Returns a color based on the improvement percentage.

    Args:
        improvement_pct (float): Percentage improvement (positive = better).

    Returns:
        str: Color string for display.
    """
    if improvement_pct >= 30:
        return "green"
    elif improvement_pct >= 10:
        return "orange"
    elif improvement_pct > 0:
        return "yellow"
    else:
        return "red"


# ─── Metric Calculation Helpers ──────────────────────────────────

def calculate_daily_patients(arrival_rate, hours=OPERATING_HOURS):
    """
    Calculates the expected number of patients per day.

    Args:
        arrival_rate (float): λ — patients per hour.
        hours (int): Operating hours per day.

    Returns:
        int: Expected patients per day.
    """
    return int(arrival_rate * hours)


def calculate_daily_wait_hours(arrival_rate, avg_wait_minutes, hours=OPERATING_HOURS):
    """
    Calculates total patient-hours wasted waiting per day in a department.

    This metric represents the cumulative waiting burden:
        total_wait_hours = (patients/day) × (avg_wait_minutes / 60)

    Args:
        arrival_rate (float): λ — patients per hour.
        avg_wait_minutes (float): Average waiting time in minutes.
        hours (int): Operating hours per day.

    Returns:
        float: Total patient-hours of waiting per day.
    """
    patients_per_day = arrival_rate * hours
    return patients_per_day * (avg_wait_minutes / 60.0)

