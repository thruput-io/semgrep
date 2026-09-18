def query_users(User, search_term):
    # ruleid: python-django-raw-sql
    User.objects.raw(f"SELECT * FROM myapp_user WHERE name = '{search_term}'")

    # ruleid: python-django-raw-sql
    User.objects.raw("SELECT * FROM myapp_user WHERE name = '%s'" % search_term)

    # ok: python-django-raw-sql
    User.objects.raw("SELECT * FROM myapp_user WHERE name = %s", [search_term])
