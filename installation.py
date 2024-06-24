# Class to store required information about installations
class Installation:
    def __init__(self, id: int, station_id: int, param_code: str):
        self.id = id
        self.station_id = station_id
        self.param_code = param_code
    
    def __str__(self):
        return f"installation #{self.id}: '{self.param_code}'"