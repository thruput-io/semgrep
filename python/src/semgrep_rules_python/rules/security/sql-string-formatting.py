def get_user(cursor, user_id, name):
    # ruleid: python-sql-string-formatting
    cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")

    # ruleid: python-sql-string-formatting
    cursor.execute("SELECT * FROM users WHERE name = '%s'" % name)

    # ruleid: python-sql-string-formatting
    cursor.execute("SELECT * FROM users WHERE id = {}".format(user_id))

    # ruleid: python-sql-string-formatting
    cursor.execute("SELECT * FROM users WHERE name = '" + name + "'")

    # ok: python-sql-string-formatting
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))

    # ok: python-sql-string-formatting
    cursor.execute("SELECT * FROM users WHERE id = :id AND name = :name", {"id": user_id, "name": name})
