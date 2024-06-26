from installation import Installation

# Class to store required information about each station
class Station:
    def __init__(self, id: int, name: str, installations: list[Installation] = None):
        self.id = id
        self.name = name
        if installations is None:
            installations = []
        self.installations = installations
    
    def __str__(self) -> str:
        header = f"Station #{self.id} ({self.name}):\n"
        installations_str = "\n".join([str(installation) for installation in self.installations])
        return header + installations_str + "\n---"
    
    def add_installation(self, installation: Installation):
        if not isinstance(self.installations, list):
            self.installations = []
        self.installations.append(installation)