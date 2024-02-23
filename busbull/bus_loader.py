import time
import json
import requests
from tqdm import tqdm

class BusLoader():
    def __init__(
            self,
            fetch_config: dict,
            data_file,
            error_file,
            url):
        self.fetch_config = fetch_config
        self.data_file    = data_file
        self.error_file   = error_file
        self.url          = url


    def _fetch_data(self):
        final_url = self.url

        for key, val in self.fetch_config.items():
            final_url += key + "=" + val + "&"

        response = requests.get(final_url)

        return response

    def _log_response(self, response):
        if response.status_code == 200:
            data = response.json()
            if data["result"] == "B\u0142\u0119dna metoda lub parametry wywo\u0142ania":
                return
            with open(self.data_file, 'a') as f:
                for bus_info in data["result"]:
                    f.write(json.dumps(bus_info))
                    f.write("\n")
        else:
            with open(self.error_file, 'a') as f:
                f.write('Request failed with status code:', response.status_code)
            print('Request failed with status code:', response.status_code)

    def start_gathering_data(self, tics, sleep_time):
        for i in tqdm(range(0, tics)):
            response=self._fetch_data()
            self._log_response(response)
            time.sleep(sleep_time)

