class Sample:
    def __init__(self, name_description: str, total_area: float, collection_depth: float, phosphorus: float, potassium: float, organic_matter: float, pH: float, SMP: float, aluminum: float, H_Al: float, calcium: float, magnesium: float, copper: float, iron: float, manganese: float, zinc: float, base_saturation: float, CEC: float, v: float, aluminum_saturation: float, effective_CEC: float) -> None:
        self.name_description: str = name_description
        self.total_area: float = total_area
        self.collection_depth: float = collection_depth
        self.phosphorus: float = phosphorus
        self.potassium: float = potassium
        self.organic_matter: float = organic_matter
        self.pH: float = pH
        self.SMP: float = SMP
        self.aluminum: float = aluminum
        self.H_Al: float = H_Al
        self.calcium: float = calcium
        self.magnesium: float = magnesium
        self.copper: float = copper
        self.iron: float = iron
        self.manganese: float = manganese
        self.zinc: float = zinc
        self.base_saturation: float = base_saturation
        self.CEC: float = CEC
        self.v: float = v
        self.aluminum_saturation: float = aluminum_saturation
        self.effective_CEC: float = effective_CEC

