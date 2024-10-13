import pytest
from pytest_httpx import HTTPXMock
from niwa_api.tideclient import TideAPIClient

@pytest.fixture
def client():
    api_key = 'TEST_API_KEY'
    return TideAPIClient(api_key)

lat = -36.8406
long = 174.7400
mock_response = {
    "heights": [
            {"time": "2023-10-12T00:00:00Z", "value": 2.5},
            {"time": "2023-10-12T01:00:00Z", "value": 2.7},
        ],
        "metadata": {
            "latitude": lat,
        "longitude": long,
        "datum": "LAT",
    }
}

def test_get_data_success(client, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        json=mock_response
    )

    data = client.get_data(lat=lat, long=long)
    assert data == mock_response

@pytest.mark.asyncio
async def test_get_data_async(client, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        json=mock_response
    )
    data = await client.get_data_async(lat=lat, long=long)
    assert data == mock_response

def test_get_chart_png_url(client):
    lat = -36.8406
    long = 174.7400
    url = client.get_chart_png_url(lat=lat, long=long)
    assert url == "https://api.niwa.co.nz/tides/chart.png?lat=-36.8406&long=174.74&apikey=TEST_API_KEY"

def test_get_data_failure(client):
    lat = -36.8406
    long = 174.7400

    with pytest.raises(Exception):
        client.get_data(lat=lat, long=long)

