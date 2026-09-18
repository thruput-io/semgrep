def notify_user(user_id: str, message: str, attachment=None, channel="email"):
    pass

def execute():
    # ruleid: python-avoid-passing-none-literal
    notify_user("usr_123", "Hello", None)

    # ruleid: python-avoid-passing-none-literal
    notify_user("usr_123", "Hello", attachment=None)

    # ruleid: python-avoid-passing-none-literal
    notify_user("usr_123", "Hello", None, channel="slack")

    # ruleid: python-avoid-passing-none-literal
    val = getattr(dict(), "items", None)

    # ruleid: python-avoid-passing-none-literal
    header = {"Authorization": "Bearer token"}.get("Content-Type", None)

    # ok: python-avoid-passing-none-literal
    notify_user("usr_123", "Hello")

    # ok: python-avoid-passing-none-literal
    notify_user("usr_123", "Hello", channel="slack")

    # ok: python-avoid-passing-none-literal
    safe_header = {"Authorization": "Bearer token"}.get("Content-Type")

    # ok: python-avoid-passing-none-literal
    safe_val = getattr(dict(), "items", "default")
