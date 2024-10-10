## Python API Client for NIWA's APIs

This Python package provides a convenient way to interact with NIWA's APIs. It includes functionality to fetch tide data, generate tide charts, and handle various data formats.

*Disclaimer: This is not an official NIWA package. I have nothing to do with NIWA other than enjoying using their open APIs.*

### Installation

You can install the package using pip:

```bash
pip install niwa-api-client
```

### Usage

#### Tide Data

To fetch tide data, you can use the `TideAPIClient` class. Here's an example of how to use it:

```python
from niwa_api_client import TideAPIClient

client = TideAPIClient(api_key='YOUR_API_KEY')
data = client.get_data(lat=lat, long=long)
print(data)
```

### CLI

The package also includes a command-line interface (CLI) for interacting with the APIs. You can use the `niwa-api-client` command to fetch tide data or generate tide charts.

#### Fetch Tide Data

To fetch tide data, use the `fetch-tide-data` command:

```bash
niwa-api-client fetch-tide-data --lat -36 --long 174 
```
You can either pass the api key as an argument:

```bash
niwa-api-client fetch-tide-data --lat -36 --long 174 --api-key YOUR_API_KEY
```

Or set the API_KEY environment variable:

```bash
export API_KEY=YOUR_API_KEY
niwa-api-client fetch-tide-data --lat -36 --long 174 
```





