from typing import Tuple, Optional


def evaluate_temperature_bounds(temp_c: float) -> Tuple[bool, Optional[str]]:
    """
    Checks if temperature violates composting biological thresholds.
    Requires heat below 65.0°C to preserve beneficial microbes.
    """
    if temp_c > 65.0:
        return True, f"Critical High Temperature: {temp_c}°C exceeds composting safety limits."
    return False, None


def evaluate_humidity_bounds(humidity_pct: float) -> Tuple[bool, Optional[str]]:
    """
    Checks if moisture level exits operational biological bounds (20% - 75%).
    """
    if humidity_pct < 20.0:
        return True, f"Moisture Too Dry: {humidity_pct}% humidity restricts biological breakdown."
    if humidity_pct > 75.0:
        return True, f"Moisture Too Wet: {humidity_pct}% humidity risks anaerobic odors."
    return False, None


def evaluate_hardware_flags(quality_flag: str) -> Tuple[bool, Optional[str]]:
    """
    Checks if quality flags indicate firmware sensor failures or missing readings.
    """
    if quality_flag in ("sensor_error", "missing", "out_of_range"):
        return True, f"Hardware Error Alert: Sensor reports quality state '{quality_flag}'."
    return False, None


def evaluate_state_transitions(status: str) -> Tuple[bool, Optional[str]]:
    """
    Identifies high-priority state changes needing notification (e.g. ready_candidate).
    """
    if status == "ready_candidate":
        return True, "Compost Ready: State machine indicates batch is a ready candidate. Action needed."
    if status == "needs_attention":
        return True, "Attention Required: State machine reports active needs_attention status."
    return False, None
