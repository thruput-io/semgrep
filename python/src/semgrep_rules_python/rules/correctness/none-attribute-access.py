def format_headers(headers):
    # ruleid: python-none-attribute-access
    auth = headers.get("Authorization").strip()

    # ruleid: python-none-attribute-access
    content_type = headers.get("Content-Type").lower()

    # ok: python-none-attribute-access
    safe_auth = headers.get("Authorization", "").strip()

    # ok: python-none-attribute-access
    val = headers.get("Content-Type")
    if val is not None:
        safe_ct = val.lower()

    return auth, content_type, safe_auth
