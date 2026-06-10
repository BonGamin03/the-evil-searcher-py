from dataclasses import dataclass, field
from typing import List

@dataclass
class User:
    email: str
    password: str
    read_docs: List[int] = field(default_factory=list)
