def clamp(value: float, min_v: float, max_v: float):
    """
    Returns a clamped value between min and max values
    :param: float value : transformed value
    :param: float min_v : minimum value
    :param: float max_v : maximum value
    """
    return max(min(value, max_v), min_v)


def remap(value: float, min_v: float, max_v: float):
    """
    Returns a remapped value between 0 and 1 using min and max values
    :param: float value : transformed value
    :param: float min_v : minimum value
    :param: float max_v : maximum value
    """
    return (clamp(value, min_v, max_v) - min_v) / (max_v - min_v)
