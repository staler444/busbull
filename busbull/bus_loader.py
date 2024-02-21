import time
import json
import requests
from tqdm import tqdm

def _fetch_data(config: dict, url):
    final_url = url

    for key, val in config.items():
        final_url += key + "=" + val + "&"

    response = requests.get(final_url)

    return response

def _log_response(response, data_file, error_file):
    if response.status_code == 200:
        data = response.json()
        with open(data_file, 'a') as f:
            f.write(json.dumps(data))
            f.write("\n")
    else:
        with open(error_file, 'a'):
            f.write('Request failed with status code:', response.status_code)
        print('Request failed with status code:', response.status_code)

def _start_gathering_data(
        fetch_config: dict,
        data_file,
        error_file,
        tics,
        url,
        sleep_time,
    ):
    for i in tqdm(range(0, tics)):
        response=_fetch_data(fetch_config, url)
        _log_response(
            response=response,
            data_file=data_file,
            error_file=error_file)
        time.sleep(sleep_time)

