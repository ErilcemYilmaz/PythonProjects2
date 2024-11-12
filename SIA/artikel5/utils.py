# utils.py
import requests
from requests.auth import HTTPBasicAuth


def fetch_data_from_api(session, api_endpoint, params):
    """
    Fetch data from the Zefix API.

    Args:
        session (requests.Session): The session object with authentication.
        api_endpoint (str): The API endpoint URL.
        params (dict): The parameters for the API request.

    Returns:
        tuple: A tuple containing the data returned from the API and a boolean indicating the success of the request.
    """
    try:
        response = session.post(api_endpoint, json=params)
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


def process_row(row, fetch_data_func, *fetch_args):
    """
    Process a row of data by fetching additional information from the Zefix API.

    Args:
        row (dict): A dictionary representing a row of data.
        fetch_data_func (function): The function to fetch data from the API.
        fetch_args (tuple): Additional arguments for the fetch_data_func.

    Returns:
        list: A list of dictionaries, each representing an updated row of data.
    """
    data, success = fetch_data_func(*fetch_args)
    if success:
        return [
            dict(
                row,
                zefixName=item.get("name", ""),
                zefixLegalSeat=item.get("legalSeat", ""),
                zefixLegalSeatId=item.get("legalSeatId", ""),
                zefixUid=item.get("uid", ""),
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
            )
        ]


def process_row_uid(row, fetch_data_func, *fetch_args):
    """
    Process a row of data by fetching additional information from the Zefix API.
    Specifically for fetching data by UID.

    """
    data, success = fetch_data_func(*fetch_args)
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


def process_row_with_city_check(row, fetch_data_func, *fetch_args):
    """
    Process a row of data by fetching additional information from the Zefix API and checking the city.
    Specifically for fetching data by name and checking the city.

    """
    data, success = fetch_data_func(*fetch_args)
    if success:
        city = row.get("city", "").lower()
        matching_item = next(
            (item for item in data if item.get("legalSeat", "").lower() == city),
            None,
        )
        if matching_item:
            return [
                dict(
                    row,
                    zefixName=matching_item.get("name", ""),
                    zefixLegalSeat=matching_item.get("legalSeat", ""),
                    zefixLegalSeatId=matching_item.get("legalSeatId", ""),
                    zefixUid=matching_item.get("uid", ""),
                    zefixChid=matching_item.get("chid", ""),
                )
            ]
    return [
        dict(
            row,
            zefixName="#N/V",
            zefixLegalSeat="#N/V",
            zefixLegalSeatId="#N/V",
            zefixUid="#N/V",
            zefixChid="#N/V",
        )
    ]
