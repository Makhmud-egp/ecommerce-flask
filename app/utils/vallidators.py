def validate_quantity(quantity):
    """Validate cart quantity"""
    if not isinstance(quantity, int):
        return False

    if quantity <= 0:
        return False

    if quantity > 100:
        return False

    return True, None