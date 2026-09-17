def notify_user(user_id: str, message: str, attachment=None, channel="email"):
    pass

def execute():
    # ruleid: python-avoid-passing-none-literal
    notify_user("usr_123", "Hello", None)

    # ruleid: python-avoid-passing-none-literal
    notify_user("usr_123", "Hello", attachment=None)

    # ruleid: python-avoid-passing-none-literal
    notify_user("usr_123", "Hello", None, channel="slack")

    # ok: python-avoid-passing-none-literal
    notify_user("usr_123", "Hello")

    # ok: python-avoid-passing-none-literal
    notify_user("usr_123", "Hello", channel="slack")

    # ok: python-avoid-passing-none-literal
    val = getattr(dict(), "items", None)

    # ok: python-avoid-passing-none-literal
    header = {"Authorization": "Bearer token"}.get("Content-Type", None)
