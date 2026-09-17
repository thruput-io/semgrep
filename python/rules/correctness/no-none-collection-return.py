from typing import List, Dict, Set, Optional

# ruleid: python-no-none-collection-return
def get_tags(post_id: int) -> list[str]:
    if not post_id:
        return None
    return ["news", "tech"]

# ruleid: python-no-none-collection-return
def get_headers(raw: str) -> Dict[str, str]:
    if not raw:
        return None
    return {"Content-Type": "application/json"}

# ruleid: python-no-none-collection-return
def get_ids(flag: bool) -> set[int]:
    if not flag:
        return None
    return {1, 2, 3}

# ok: python-no-none-collection-return
def get_tags_safe(post_id: int) -> list[str]:
    if not post_id:
        return []
    return ["news", "tech"]

# ok: python-no-none-collection-return
def get_optional_tags(post_id: int) -> Optional[List[str]]:
    if not post_id:
        return None
    return ["news", "tech"]
