import numpy as np

class GlucosePredictor:
    """
    Placeholder for an LSTM or ML-based glucose predictor.
    Currently returns a noisy extrapolation.
    """

    def __init__(self):
        pass

    def predict_next(self, glucose_history):
        # Simple trend extrapolation for demo
        if len(glucose_history) < 3:
            return [glucose_history[-1]] * 12

        slope = np.mean(np.diff(glucose_history[-3:]))
        next_vals = [glucose_history[-1] + slope * i + np.random.normal(0, 2) for i in range(1, 13)]
        return np.clip(next_vals, 60, 250)
