import os
import json


class LoadData:
    """
    Serves to load json file from the dedicated folder json_file/*.json.
    Without specified json file it wil be loaded configClear_v2.json as default file.
    """
    DEFAULT_JSON_FILE = os.path.join(os.getcwd(), 'json_file', 'configClear_v2.json')

    def __init__(self, json_file_name: str = None):
        self.raw_data = dict
        if json_file_name is None:
            print(f'No json file had been entered. The system will take default file configClear_v2.json ')
            self.path_to_json_file = self.DEFAULT_JSON_FILE
        else:
            self.path_to_json_file = os.path.join(os.getcwd(), 'json_file', json_file_name)

    def load_json_file(self) -> dict:
        """
        Loads the specific json file from the folder json_file/.

        :return: loaded json file
        """
        with open(self.path_to_json_file) as json_file:
            self.raw_data = json.load(json_file)

        return self.raw_data
