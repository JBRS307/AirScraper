from installation import Installation

class Station:
    def __init__(self, id: int, name: str, installations: list[Installation] = []):
        self.id = id
        self.name = name
        self.installations = installations
    
    def __str__(self) -> str:
        header = f"Station #{self.id} ({self.name}):\n"
        installations_str = "\n".join(self.installations)
        return header + installations_str