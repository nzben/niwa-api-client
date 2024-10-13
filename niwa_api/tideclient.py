from typing import Optional
import urllib.parse
import httpx

class TideAPIClient:
    """
    Client for the NIWA Tides API.
    """
    def __init__(self, api_key: str):
        self.base_url = "https://api.niwa.co.nz/tides"
        self.api_key = api_key
        self.headers = {
            'x-apikey': self.api_key
        }

    def _make_request(self, endpoint: str, params: dict):
        url = f"{self.base_url}{endpoint}"
        with httpx.Client() as client:
            response = client.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response
    
    async def _make_async_request(self, endpoint: str, params: dict):
        url = f"{self.base_url}{endpoint}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response

    def get_chart_png(self, lat: float, long: float, number_of_days: Optional[int] = None,
                      start_date: Optional[str] = None, datum: Optional[str] = None) -> bytes:
        """
        Get chart in PNG format, as an array of bytes.
        """
        params = self._prepare_params(lat, long, number_of_days, start_date, datum)
        response = self._make_request("/chart.png", params)
        return response.content
    
    async def get_chart_png_async(self, lat: float, long: float, number_of_days: Optional[int] = None,
                                  start_date: Optional[str] = None, datum: Optional[str] = None) -> bytes:
        """
        Get chart in PNG format asynchronously.
        """
        params = self._prepare_params(lat, long, number_of_days, start_date, datum)
        response = await self._make_async_request("/chart.png", params)
        return response.content

    def get_chart_png_url(self, lat: float, long: float, number_of_days: Optional[int] = None,
                    start_date: Optional[str] = None, datum: Optional[str] = None) -> str:
        """
        Get a direct URL to the chart in PNG format.
        """
        params = self._prepare_params(lat, long, number_of_days, start_date, datum)
        params['apikey'] = self.api_key
        return f"{self.base_url}/chart.png?{urllib.parse.urlencode(params)}"
    
    async def get_chart_png_url_async(self, lat: float, long: float, number_of_days: Optional[int] = None,
                    start_date: Optional[str] = None, datum: Optional[str] = None) -> str:
        """
        Get a direct URL to the chart in PNG format asynchronously.
        """
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
    
    async def get_chart_svg_async(self, lat: float, long: float, number_of_days: Optional[int] = 2,
                                  start_date: Optional[str] = None, datum: Optional[str] = None) -> str:
        """
        Get chart in SVG format asynchronously.
        """
        params = self._prepare_params(lat, long, number_of_days, start_date, datum)
        response = await self._make_async_request("/chart.svg", params)
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
    
    async def get_data_async(self, lat: float, long: float, number_of_days: Optional[int] = None,
                 start_date: Optional[str] = None, datum: Optional[str] = None,
                 interval: Optional[int] = None) -> dict:
        """
        Get tide data in JSON format asynchronously.
        """
        params = self._prepare_params(lat, long, number_of_days, start_date, datum, interval)
        response = await self._make_async_request("/data", params)
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
    
    async def get_data_csv_async(self, lat: float, long: float, number_of_days: Optional[int] = None,
                                 start_date: Optional[str] = None, datum: Optional[str] = None,
                                 interval: Optional[int] = None) -> str:
        """
        Get tide data in CSV format asynchronously.
        """
        params = self._prepare_params(lat, long, number_of_days, start_date, datum, interval)
        response = await self._make_async_request("/data.csv", params)
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