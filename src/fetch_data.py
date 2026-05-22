import os
import requests
import pandas as pd
import argparse
from datetime import datetime, timedelta

API_KEY = os.getenv("NASA_API_KEY")
URL = "https://api.nasa.gov/neo/rest/v1/feed"

if not API_KEY:
    raise ValueError("NASA_API_KEY environment variable is not set.")

def fetch(start_date=None, days=7):
    if start_date:
        start = datetime.strptime(start_date, "%Y-%m-%d").date()
    else:
        start = datetime.utcnow().date()

    end = start + timedelta(days=days - 1)
    

    params = {
        "start_date": start.isoformat(),
        "end_date": end.isoformat(),
        "api_key": API_KEY
    }

    r = requests.get(URL, params=params)
    r.raise_for_status()
    data = r.json()

    rows = []

    for date, neos in data["near_earth_objects"].items():
        for neo in neos:
            rows.append({
                "id": neo["id"],
                "name": neo["name"],
                "date": date,
                "diameter_min_km": neo["estimated_diameter"]["kilometers"]["estimated_diameter_min"],
                "diameter_max_km": neo["estimated_diameter"]["kilometers"]["estimated_diameter_max"],
                "hazardous": neo["is_potentially_hazardous_asteroid"],
                "velocity_km_s": float(neo["close_approach_data"][0]["relative_velocity"]["kilometers_per_second"]),
                "miss_distance_km": float(neo["close_approach_data"][0]["miss_distance"]["kilometers"])
            })
    
    df_new = pd.DataFrame(rows)
    file_path = "data/neos.csv"

    if os.path.exists(file_path):
        df_existing = pd.read_csv(file_path)

        # Combine old and new
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)

        # Remove duplicates based on name + date
        df_combined = df_combined.drop_duplicates(subset=["id", "date"])

        df_combined.to_csv(file_path, index=False)
        print("Appended new data and removed duplicates.")
    else:
        df_new.to_csv(file_path, index=False)
        print("Created new neos.csv file.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=str, help="Start date (YYYY-MM-DD)")
    parser.add_argument("--days", type=int, default=7, help="Number of days to fetch")

    args = parser.parse_args()

    fetch(start_date=args.start, days=args.days)