def error_wrapper(errors):
    return {
        ", ".join([str(msg).capitalize() for msg in value])
        for key, value in errors.items()
    }
