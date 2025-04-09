from pinax.notifications.models import send


def send_notification(*args, **kwargs):
    """
    Interface for pinax send function.
    Ensures no exceptions are raised if the send function fails.
    """
    try:
        if 'request_user' in kwargs:
            kwargs['extra_context']['request_user'] = kwargs['request_user']
            del kwargs['request_user']
        return send(*args, **kwargs)
    except Exception as e:
        # Log the exception or handle it silently
        print(f"Notification send failed: {e}")
        return None
