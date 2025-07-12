import json
import os

class Saver:
    def __init__(self, basedir: str):
        self.basedir: str = basedir

        if not os.path.exists(basedir):
            os.makedirs(basedir)

    def save(self, obj: dict[str, str]):
        strToSave = json.dumps(obj)

        filename: str = f'{obj["name"]}.json'
        filepath = os.path.join(self.basedir, filename)
        open(filepath, 'wb').write( strToSave.encode() )