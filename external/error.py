def error_wrapper(errors):
    return {", ".join(value).capitalize() for key, value in errors.items()}

