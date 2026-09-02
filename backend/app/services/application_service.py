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


def is_confirmation(user_message: str) -> bool:
    """Very simple yes/no detection for confirming an application."""
    msg = user_message.lower().strip()
    yes_words = ["yes", "haan", "han", "ha", "confirm", "submit", "ok", "theek hai"]
    return any(word in msg for word in yes_words)


def is_rejection(user_message: str) -> bool:
    """Detects if the user wants to cancel/decline the application."""
    msg = user_message.lower().strip()
    no_words = ["no", "nahi", "nahin", "cancel", "not now", "later"]
    return any(word in msg for word in no_words)