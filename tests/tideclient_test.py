from unittest.mock import patch
import pytest
from niwa_api_client.tideclient import TideAPIClient

@pytest.fixture
def client():
    api_key = 'TEST_API_KEY'
    return TideAPIClient(api_key)

def test_get_data_success(client):
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

    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        data = client.get_data(lat=lat, long=long)

        assert data == mock_response

def test_get_data_failure(client):
    lat = -36.8406
    long = 174.7400

    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 401
        mock_get.return_value.json.return_value = {"error": "Unauthorized"}

    with pytest.raises(Exception):
        client.get_data(lat=lat, long=long)

