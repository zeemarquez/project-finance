import requests
import pandas as pd
from datetime import datetime

def fetch_nasa_power_data(lat, lon, start_date:datetime, end_date:datetime):
    """
    Fetches solar and cloud data from NASA POWER API.
    Dates must be in YYYYMMDD format.
    """
    url = "https://power.larc.nasa.gov/api/temporal/hourly/point"
    
    # Define parameters: 
    # GHI, DNI, and Cloud Amount
    parameters = [
        "ALLSKY_SFC_SW_DWN", 
        "ALLSKY_SFC_SW_DNI", 
        "CLOUD_AMT"
    ]

    
    #start = "20230101"
    #end = "20230110"
    
    params = {
        "parameters": ",".join(parameters),
        "community": "RE",      # Renewable Energy community
        "longitude": lon,
        "latitude": lat,
        "start": start_date.strftime("%Y%m%d"),
        "end": end_date.strftime("%Y%m%d"),
        "format": "JSON",
        "time_standard": "UTC"
    }

    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        
        # The data is nested inside 'properties' -> 'parameter'
        # We'll extract each parameter and create a DataFrame
        records = data['properties']['parameter']
        df = pd.DataFrame(records)
        
        # Convert the index (YYYYMMDD string) to actual datetime objects
        df.index = pd.to_datetime(df.index, format='%Y%m%d%H').tz_localize('UTC')
        df.index.name = "time"
        
        # Clean up column names for readability
        df.columns = ["ghi", "dni", "cloud_coverage"]
        return df
    else:
        print(f"Error: {response.status_code}")
        return None

if __name__ == '__main__':

    # --- Usage Example ---
    # Coordinates for Los Angeles, CA
    latitude = 34.0522
    longitude = -118.2437
    start = "20230101"
    end = "20230110"

    data_df = fetch_nasa_power_data(latitude, longitude, start, end)

    if data_df is not None:
        print(data_df)