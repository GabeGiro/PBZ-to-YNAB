import dataclasses

@dataclasses.dataclass
class Transaction:
    date: str
    description: str
    amount: float