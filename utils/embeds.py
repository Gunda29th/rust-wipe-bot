from datetime import datetime


def format_countdown(target_time):
    """
    Creates a readable countdown.
    """

    now = datetime.now(target_time.tzinfo)

    difference = target_time - now

    seconds = int(difference.total_seconds())


    if seconds <= 0:
        return "Expired"


    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60


    parts = []


    if days:
        parts.append(
            f"{days} day{'s' if days != 1 else ''}"
        )


    if hours:
        parts.append(
            f"{hours} hour{'s' if hours != 1 else ''}"
        )


    if minutes:
        parts.append(
            f"{minutes} minute{'s' if minutes != 1 else ''}"
        )


    return ", ".join(parts)