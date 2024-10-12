import requests
from typing import Optional
import urllib.parse
class TideAPIClient:
    def __init__(self, api_key: str):
        self.base_url = "https://api.niwa.co.nz/tides"
        self.api_key = api_key
        self.headers = {
            'x-apikey': self.api_key
        }

    def _make_request(self, endpoint: str, params: dict, stream: bool = False):
        url = f"{self.base_url}{endpoint}"
        params['apikey'] = self.api_key  # Include API key in query params
        response = requests.get(url, headers=self.headers, params=params, stream=stream)
        response.raise_for_status()
        return response

    def get_chart_png(self, lat: float, long: float, number_of_days: Optional[int] = None,
                      start_date: Optional[str] = None, datum: Optional[str] = None) -> bytes:
        """
        Get chart in PNG format.
        """
        params = self._prepare_params(lat, long, number_of_days, start_date, datum)
        response = self._make_request("/chart.png", params)
        return response.content

    def get_chart_png_url(self, lat: float, long: float, number_of_days: Optional[int] = None,
                    start_date: Optional[str] = None, datum: Optional[str] = None) -> str:
        params = self._prepare_params(lat, long, number_of_days, start_date, datum)
        params['apikey'] = self.api_key
        return f"{self.base_url}/chart.png?{urllib.parse.urlencode(params)}"

    def get_chart_svg(self, lat: float, long: float, number_of_days: Optional[int] = 2,
                      start_date: Optional[str] = None, datum: Optional[str] = None) -> str:
        """
        Get chart in SVG format.
        """
        params = self._prepare_params(lat, long, number_of_days, start_date, datum)
        response = self._make_request("/chart.svg", params)
        return response.text

    def get_data(self, lat: float, long: float, number_of_days: Optional[int] = None,
                 start_date: Optional[str] = None, datum: Optional[str] = None,
                 interval: Optional[int] = None) -> dict:
        """
        Get tide data in JSON format.
        """
        params = self._prepare_params(lat, long, number_of_days, start_date, datum, interval)
        response = self._make_request("/data", params)
        return response.json()

    def get_data_csv(self, lat: float, long: float, number_of_days: Optional[int] = None,
                     start_date: Optional[str] = None, datum: Optional[str] = None,
                     interval: Optional[int] = None) -> str:
        """
        Get tide data in CSV format.
        """
        params = self._prepare_params(lat, long, number_of_days, start_date, datum, interval)
        response = self._make_request("/data.csv", params)
        return response.text

    def _prepare_params(self, lat, long, number_of_days, start_date, datum, interval=None):
        params = {
            'lat': str(lat),
            'long': str(long)
        }
        if number_of_days is not None:
            params['numberOfDays'] = number_of_days
        if start_date is not None:
            params['startDate'] = start_date
        if datum is not None:
            params['datum'] = datum
        if interval is not None:
            params['interval'] = interval
        return params