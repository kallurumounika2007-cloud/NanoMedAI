import pandas as pd
import numpy as np

def generate_glucose_trace(hours=6, interval=5, scenarios=None):
    """
    Simulate glucose levels over time (simplified)
    - hours: total simulation time
    - interval: minutes between measurements
    - scenarios: dict with keys 'meal', 'exercise', 'stress', 'sleep'
    Returns DataFrame with columns: Time, Glucose
    """
    if scenarios is None:
        scenarios = {'meal': False, 'exercise': False, 'stress': False, 'sleep': False}

    total_points = int(hours*60 / interval)
    time_index = pd.date_range(start='08:00', periods=total_points, freq=f'{interval}min')

    # base glucose around 100 mg/dL with small noise
    glucose = 100 + np.random.normal(0, 5, size=total_points)

    # scenario effects
    if scenarios.get('meal', False):
        glucose += np.linspace(0, 40, total_points)
    if scenarios.get('exercise', False):
        glucose -= np.linspace(0, 20, total_points)
    if scenarios.get('stress', False):
        glucose += np.linspace(0, 15, total_points)
    if scenarios.get('sleep', False):
        glucose -= np.linspace(0, 10, total_points)

    df = pd.DataFrame({'Time': time_index, 'Glucose': glucose})
    return df
