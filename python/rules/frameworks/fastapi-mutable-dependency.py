from fastapi import FastAPI
from typing import List, Optional

app = FastAPI()

# ruleid: python-fastapi-mutable-dependency
@app.get("/items")
def get_items(filter_tags: list = []):
    return filter_tags

# ruleid: python-fastapi-mutable-dependency
@app.post("/items")
async def create_items(metadata: dict = {}):
    return metadata

# ok: python-fastapi-mutable-dependency
@app.get("/safe-items")
def get_safe_items(filter_tags: Optional[List[str]] = None):
    return filter_tags or []
