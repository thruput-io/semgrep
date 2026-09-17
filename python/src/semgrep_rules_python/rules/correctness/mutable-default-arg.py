# ruleid: python-mutable-default-arg
def append_to(element, target=[]):
    target.append(element)
    return target

# ruleid: python-mutable-default-arg
def record_event(name, payload={}):
    payload[name] = True
    return payload

# ruleid: python-mutable-default-arg
def track_unique(item, seen=set()):
    seen.add(item)
    return seen

# ruleid: python-mutable-default-arg
def make_list(init=list()):
    return init

# ruleid: python-mutable-default-arg
def make_dict(init=dict()):
    return init

# ok: python-mutable-default-arg
def append_to_safe(element, target=None):
    if target is None:
        target = []
    target.append(element)
    return target

# ok: python-mutable-default-arg
def record_event_safe(name, payload=None):
    if payload is None:
        payload = {}
    payload[name] = True
    return payload

# ok: python-mutable-default-arg
def compute(x=1, y="default", flag=False, items=None):
    return (x, y, flag, items or [])
