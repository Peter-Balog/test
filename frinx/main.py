from frinx.process_data.load_file.load_file import LoadData
from frinx.process_data.save_data.save_data import SaveDataPostgreSQL


class ProcessData(SaveDataPostgreSQL):
    """
    Reads specific data from json file and transfers them into PostgreSQL database.
    """

    def __init__(self, json_file_name: str = None):
        """
        :param json_file_name: the name of json file e.g. configClear_v2.json which is stored in a folder json_file
        """
        super().__init__()
        self.raw_data = LoadData(json_file_name=json_file_name).load_json_file()

    def get_raw_data(self, key: str = None) -> [[]]:
        """
        Gets values from nested dictionary based on keys.

        :param key: which has to be looked for in nested dictionary
        :return: 2D list array from nested dictionary
        """
        load_data = [self.raw_data]
        result = []
        while load_data:
            elem = load_data.pop()
            if isinstance(elem, dict):
                for k, v in elem.items():
                    if k == key:
                        result.append(v)
                    if isinstance(elem, (list, dict)):
                        load_data.append(v)
            elif isinstance(elem, list):
                for obj in elem:
                    load_data.append(obj)
        return result

    def main_build_table(self, device_interface: list) -> None:
        """
        The main method which will find data based on the key and calls other methods to write found data and also
        calls to close created table in PostgreSQL.

        :param device_interface: supported items are ['BDI', 'Loopback', 'Port-channel', TenGigabitEthernet', \
                                'GigabitEthernet']
        """
        for i in device_interface:
            if i == 'BDI':
                data = self.get_raw_data(key='BDI')[5]  # BDI data starts at the fifth position
            elif i == 'Loopback':
                data = self.get_raw_data(key='Loopback')[0]
            elif i == 'Port-channel':
                data = self.get_raw_data(key='Port-channel')[0]
            elif i == 'TenGigabitEthernet':
                data = self.get_raw_data(key='TenGigabitEthernet')[0]
            elif i == 'GigabitEthernet':
                data = self.get_raw_data(key='GigabitEthernet')[0]
            else:
                raise NameError(f'Could not find the device interface configuration for {i}. Only following '
                                f'interfaces are supported: BDI, Loopback, Port-channel, TenGigabitEthernet, '
                                f'GigabitEthernet ')
            self.data_for_lines(device_interface=i, data=data)
        self.close_postgre()

    def data_for_lines(self, device_interface: str, data: list) -> None:
        """
        Pickup data based on names and writes into columns.

        :param device_interface: supported names are 'BDI', 'Loopback', 'Port-channel', TenGigabitEthernet', \
                                'GigabitEthernet'
        :param data: nested dictionary in a list with all requested values
        """
        for i in range(len(data)):
            name = device_interface + str((data[i]).get('name'))
            description = (data[i]).get('description')
            config = data[i]
            port_channel_id = (data[i]).get('port_channel_id')
            max_frame_size = (data[i]).get('mtu')
            self.add_data_to_table(name=name, description=description, config=config, port_channel_id=port_channel_id,
                                   max_frame_size=max_frame_size)

    def close_postgre(self) -> None:
        """
        Closes the connection to PostgreSQL.
        """
        self.close()


if __name__ == '__main__':
    x = ProcessData()
    x.main_build_table(['Port-channel', 'TenGigabitEthernet', 'GigabitEthernet'])
    # x.main_build_table(['BDI', 'Loopback', 'Port-channel', 'TenGigabitEthernet', 'GigabitEthernet'])
