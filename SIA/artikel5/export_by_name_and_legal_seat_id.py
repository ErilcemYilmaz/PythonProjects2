from concurrent.futures import ThreadPoolExecutor

import pandas as pd

from .config import api_endpoint, session
from .utils import fetch_data_from_api, process_row


def fetch_data(name, legalSeatId):
    params = {"name": name, "legalSeatId": legalSeatId, "activeOnly": "true"}
    return fetch_data_from_api(session, api_endpoint, params)


def compare_and_update(input_csv, output_csv):
    df = pd.read_csv(input_csv, delimiter=";", encoding="ISO-8859-1")

    with ThreadPoolExecutor() as executor:
        results = executor.map(
            lambda row: process_row(
                row, fetch_data, row.get("name", ""), row.get("legalSeatId", "")
            ),
            [row for _, row in df.iterrows()],
        )

    updated_rows = [item for sublist in results for item in sublist]
    updated_df = pd.DataFrame(updated_rows)
    updated_df.reset_index(drop=True, inplace=True)
    updated_df.to_csv(output_csv, index=False)
    print(f"Updated data saved to {output_csv}.")