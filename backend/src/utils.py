import dataclasses
import json


class DataclassJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o) # pyright: ignore
        return super().default(o)
