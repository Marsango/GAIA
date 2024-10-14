import os
import json
from typing import Any


class GraphParameters:
    def __init__(self) -> None:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.file_location = os.path.join(base_dir, 'graphs_parameters.json')


    def get_graph_parameters(self, graph_type: str):
        try:
            with open(self.file_location, "r") as file:
                saved_parameters: dict[Any, Any] = json.load(file)
                return saved_parameters[graph_type]
        except:
            return {"very low": 0, "low": 0, "medium": 0, "high": 0, "very high": 0}

    def set_graph_parameters(self, graph_type: str, new_values: dict[str, float]):
        with open(self.file_location, "r") as file:
            saved_parameters: dict[Any, Any] = json.load(file)
        saved_parameters[graph_type] = new_values
        with open(self.file_location, "w") as file:
            json.dump(saved_parameters, file)