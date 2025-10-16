def autonomous_controller(pred_glucose, current_glucose):
    """
    Dummy controller: simple proportional logic
    """
    error = pred_glucose[-1] - current_glucose
    dose = max(min(error * 0.05, 5), 0)  # scale error to [0,5] U
    return dose


