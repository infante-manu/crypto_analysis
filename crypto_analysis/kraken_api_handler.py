import requests
import pandas as pd

class KrakenAPIHandler:
    """Handles API interaction with Kraken for cryptocurrency data."""

    OHLC_URL = "https://api.kraken.com/0/public/OHLC"
    ASSET_PAIRS_URL = "https://api.kraken.com/0/public/AssetPairs"

    def fetch_ohlc_data(self, pair: str, interval: int, since: int = None) -> pd.DataFrame:
        """
        Fetches OHLC data for a given cryptocurrency pair.

        Args:
            pair (str): Currency pair (e.g., "ETHUSD").
            interval (int): Time frame interval in minutes.
            since (int, optional): Unix timestamp of the start date.

        Returns:
            pd.DataFrame: DataFrame of OHLC data.
        """
        try:
            # Request parameters and API call
            params = {'pair': pair, 'interval': interval, 'since': since}
            response = requests.get(self.OHLC_URL, params=params)
            response.raise_for_status()  # Raise an HTTPError for bad responses

            # Parse response data
            response_data = response.json()
            if response_data['error']:
                raise ValueError(f"API Error: {response_data['error']}")

            # Validate data structure
            result_data = response_data.get('result', {})
            if not result_data:
                raise ValueError("API response is missing 'result' data.")

            # Extract OHLC data
            pair_data = list(result_data.values())[0]
            if not pair_data:
                raise ValueError("No OHLC data found for the given pair.")

            df = pd.DataFrame(pair_data, columns=['time', 'open', 'high', 'low', 'close', 'vwap', 'volume', 'count'])
            df = df.astype({
                'open': float, 'high': float, 'low': float, 'close': float, 
                'vwap': float, 'volume': float, 'count': int
            })
            df['time'] = pd.to_datetime(df['time'], unit='s')
            return df

        except requests.RequestException as e:
            raise ConnectionError(f"Failed to fetch data from Kraken API: {e}")
        except (KeyError, ValueError, TypeError) as e:
            raise ValueError(f"Error parsing API response data: {e}")

    def fetch_asset_pairs(self) -> list:
        """Fetches all asset pairs available on Kraken."""
        try:
            response = requests.get(self.ASSET_PAIRS_URL)
            response.raise_for_status()
            response_data = response.json()

            if response_data['error']:
                raise ValueError(f"API Error: {response_data['error']}")

            return list(response_data['result'].keys())

        except requests.RequestException as e:
            raise ConnectionError(f"Failed to fetch asset pairs from Kraken API: {e}")
        except (KeyError, ValueError, TypeError) as e:
            raise ValueError(f"Error parsing API response data: {e}")
        
    def get_asset_pairs(self):
        """Returns asset pairs available on Kraken."""
        return self.fetch_asset_pairs()

# Usage example:
if __name__ == '__main__':
    # Example usage
    api = KrakenAPIHandler()
    pairs = api.fetch_asset_pairs()
    print(pairs)
    data = api.fetch_ohlc_data("ETHUSD", interval = 5)
    data = data.sort_values(by='time', ascending=False)
    print(data.head())
    print(data.info())