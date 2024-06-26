import os
from concurrent.futures import ThreadPoolExecutor

import pandas as pd
import requests
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

load_dotenv()
api_endpoint = os.environ["API_ENDPOINT"]
username = os.environ["USERNAME"]
password = os.environ["PASSWORD"]


session = requests.Session()
session.auth = HTTPBasicAuth(username, password)


def fetch_data_from_api(uid):
    """
    Fetch data from the Zefix API for given UID.

    Args:
        uid (str): The UID of the company to search for.

    Returns:
        tuple: A tuple containing the data returned from the API and a boolean indicating the success of the request.
    """

    params = {
        "activeOnly": "true",
    }
    try:
        response = session.get(api_endpoint + uid, json=params)
        data = response.json()
        if response.status_code == 200 and data:
            return data, True
        else:
            return [], False
    except Exception as e:
        return [], False


def format_uid(uid):
    """
    Format a UID into the Swiss UID format.
    Args:
        uid (str): The UID to format.

    Returns:
        str: The formatted UID.
    """
    return "CHE-{}.{}.{}".format(uid[3:6], uid[6:9], uid[9:])


def process_row(row):
    """
    Process a row of data by fetching additional information from the Zefix API.

    Args:
        row (dict): A dictionary representing a row of data, with the company name under the "name" key.

    Returns:
        list: A list of dictionaries, each representing an updated row of data.
    """
    uid = row.get("uid", "")
    data, success = fetch_data_from_api(uid)
    if success:
        return [
            dict(
                row,
                zefixName=item.get("name", ""),
                zefixLegalSeat=item.get("legalSeat", ""),
                zefixLegalSeatId=item.get("legalSeatId", ""),
                zefixUid=format_uid(item.get("uid", "")),
                zefixStreet=(item.get("address", {}).get("street", "") or "")
                + (
                    " " + (item.get("address", {}).get("houseNumber", "") or "")
                    if item.get("address", {}).get("houseNumber", "")
                    else ""
                ),
                zefixSwissZipCode=item.get("address", {}).get("swissZipCode", ""),
                zefixCity=item.get("address", {}).get("city", ""),
            )
            for item in data
        ]
    else:
        return [
            dict(
                row,
                zefixName="#N/V",
                zefixLegalSeat="#N/V",
                zefixLegalSeatId="#N/V",
                zefixUid="#N/V",
                zefixStreet="#N/V",
                zefixSwissZipCode="#N/V",
                zefixCity="#N/V",
            )
        ]


def compare_and_update(input_csv, output_csv):
    """
    Compare and update a CSV file with data fetched from the Zefix API.

    Args:
        input_csv (str): The path to the input CSV file.
        output_csv (str): The path to the output CSV file.
    """
    df = pd.read_csv(input_csv, delimiter=";", encoding="ISO-8859-1")

    with ThreadPoolExecutor() as executor:
        results = executor.map(process_row, [row for _, row in df.iterrows()])

    updated_rows = [item for sublist in results for item in sublist]
    updated_df = pd.DataFrame(updated_rows)
    updated_df.reset_index(drop=True, inplace=True)
    updated_df.to_csv(output_csv, index=False)
    print(f"Updated data saved to {output_csv}.")


# Example usage:

# input_csv = r"C:\coding\test_Data\20240220_export_UID_NULL.csv"
# output_csv = r"C:\coding\test_Data\20240220_export_UID_NULL_update.csv"

# compare_and_update(input_csv, output_csv)
