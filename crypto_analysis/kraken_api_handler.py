from typing import Any
import pandas as pd
import requests


class KrakenAPIHandler:
    """Handles API interaction with Kraken for cryptocurrency data."""

    OHLC_URL = "https://api.kraken.com/0/public/OHLC"
    ASSET_PAIRS_URL = 'https://api.kraken.com/0/public/AssetPairs'
    
    def __init__(self) -> None:
        pass
    
    def fetch_ohlc_data(self, pair: str, interval: int, since : int = None) -> pd.DataFrame:
        """
        Fetches OHLC data for a given cryptocurrency pair.
        Args:
            pair (str): Currency pair (e.g., "ETHUSD").
            interval (int): Time frame interval in minutes.
            since (int): Unix timestamp of the start date.
        Returns:
            pd.DataFrame: DataFrame of OHLC data.
        """
        try:
            params = {
                'pair': pair,
                'interval': interval,
                'since': since
            }
            response = requests.get(self.OHLC_URL, params=params)
            response.raise_for_status()
            response_data = response.json()
            
            if response_data['error']:
                raise Exception(f"Error fetching data: {response_data['error']}")
            
            data = response_data['result'][list(response_data['result'].keys())[0]]
            df = pd.DataFrame(
                data, 
                columns=['time', 'open', 'high', 'low', 'close', 'vwap', 'volume', 'count']
                )
            df = df.astype(
                {
                    'open': float, 
                    'high': float, 
                    'low': float, 
                    'close': float, 
                    'vwap': float, 
                    'volume': float, 
                    'count': int
                }
            )
            df['time'] = pd.to_datetime(df['time'], unit='s')
            return df
        
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {e}")
        
        except Exception as e:
            raise Exception(f"An error occurred: {e}")
        
    def fetch_asset_pairs(self) -> list:
        """
        Fetches all asset pairs available on Kraken.
        Returns:
            list: List of asset pairs.
        """
        try:
            response = requests.get(self.ASSET_PAIRS_URL)
            response.raise_for_status()
            response_data = response.json()
            
            if response_data['error']:
                raise Exception(f"Error fetching data: {response_data['error']}")
            
            return list(response_data['result'].keys())
        
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {e}")
        
        except Exception as e:
            raise Exception(f"An error occurred: {e}")


if __name__ == '__main__':
    # Example usage
    api = KrakenAPIHandler()
    pairs = api.fetch_asset_pairs()
    print(pairs)
    data = api.fetch_ohlc_data("ETHUSD", interval = 5)
    data = data.sort_values(by='time', ascending=False)
    print(data.head())
    print(data.info())
    
