import unittest
import os
from unittest.mock import MagicMock, patch
from busbull import BusLoader

class TestBusLoader(unittest.TestCase):
    def setUp(self):
        self.error_file = 'error.txt'
        self.data_file = 'data.txt'

    def tearDown(self):
        if os.path.exists(self.error_file):
            os.remove(self.error_file)
        if os.path.exists(self.data_file):
            os.remove(self.data_file)

    @patch('requests.get')
    def test_fetch_data_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": [{"bus_id": 1}, {"bus_id": 2}]}
        mock_get.return_value = mock_response

        fetch_config = {"key": "value"}
        data_file = "data.txt"
        error_file = "error.txt"
        url = "http://www.pieknafunkcja.pl"

        bus_loader = BusLoader(fetch_config, data_file, error_file, url)

        response = bus_loader._fetch_data()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"result": [{"bus_id": 1}, {"bus_id": 2}]})

    @patch('requests.get')
    def test_fetch_data_failure(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        fetch_config = {"key": "value"}
        data_file = "data.txt"
        error_file = "error.txt"
        url = "http://www.pieknafunkcja.pl"

        bus_loader = BusLoader(fetch_config, data_file, error_file, url)

        response = bus_loader._fetch_data()

        self.assertEqual(response.status_code, 404)

    @patch('requests.get')
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_start_gathering_data_succes(self, mock_open, mock_requests_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": [{"bus_id": 1}, {"bus_id": 2}]}
        mock_requests_get.return_value = mock_response

        loader = BusLoader(
                fetch_config={}, 
                data_file='data.txt', 
                error_file='error.txt', 
                url='http://example.com')

        loader.start_gathering_data(tics=2, sleep_time=0)

        self.assertEqual(mock_requests_get.call_count, 2)

        expected_calls = [unittest.mock.call('data.txt', 'a')]
        mock_open.assert_has_calls(expected_calls, any_order=True)

    @patch('requests.get')
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_start_gathering_data_error(self, mock_open, mock_requests_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"result": [{"bus_id": 1}, {"bus_id": 2}]}
        mock_requests_get.return_value = mock_response

        loader = BusLoader(
                fetch_config={}, 
                data_file='data.txt', 
                error_file='error.txt', 
                url='http://example.com')

        loader.start_gathering_data(tics=2, sleep_time=0)

        self.assertEqual(mock_requests_get.call_count, 2)

        expected_calls = [unittest.mock.call('error.txt', 'a')]
        mock_open.assert_has_calls(expected_calls, any_order=True)

if __name__ == '__main__':
    unittest.main()
