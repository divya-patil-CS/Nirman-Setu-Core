def match_scheme_from_message(user_message: str, eligible_schemes: list) -> dict | None:
    """
    Checks if the user's message mentions one of their eligible schemes by name.
    Simple substring match — good enough for a hackathon demo.
    """
    msg_lower = user_message.lower()
    for scheme in eligible_schemes:
        if scheme["name"].lower() in msg_lower:
            return scheme
    return None