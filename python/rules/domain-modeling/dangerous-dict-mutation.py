def clean_dict(data):
    # ruleid: python-dangerous-iteration-mutation
    for k in data:
        if k.startswith("_"):
            del data[k]

    # ruleid: python-dangerous-iteration-mutation
    for k in data.keys():
        if k == "secret":
            del data[k]

    # ruleid: python-dangerous-iteration-mutation
    for item in data:
        if item == "remove_me":
            data.remove(item)

    # ok: python-dangerous-iteration-mutation
    for k in list(data.keys()):
        if k.startswith("_"):
            del data[k]

    # ok: python-dangerous-iteration-mutation
    for item in list(data):
        if item == "remove_me":
            data.remove(item)
