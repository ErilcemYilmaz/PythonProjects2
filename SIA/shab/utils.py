# utils.py
import csv
from datetime import datetime, timedelta
from xml.etree import ElementTree

import requests

BASE_URL = "https://amtsblattportal.ch/api/v1/publications/xml"


def fetch_publication_list(params):
    """
    Fetch the publication list based on the provided parameters.

    Args:
        params (dict): The parameters for the API request.

    Returns:
        str: The XML content of the publication list.
    """
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        return response.content
    else:
        print(f"Error fetching publication list: {response.status_code}")
        return None


def fetch_complete_publication(publication_ref):
    """
    Fetch the complete publication using the ref URL.

    Args:
        publication_ref (str): The reference URL for the publication.

    Returns:
        str: The XML content of the complete publication.
    """
    response = requests.get(publication_ref)
    if response.status_code == 200:
        return response.content
    else:
        print(f"Error fetching publication: {response.status_code}")
        return None


def get_text(element, path):
    """
    Helper function to get text from an XML element or return a default value.

    Args:
        element (Element): The XML element.
        path (str): The XPath to the desired text.

    Returns:
        str: The text content of the element or a default value.
    """
    return element.findtext(path) if element is not None else "#"


def parse_publication_xml(xml_content, keyword):
    """
    Parse the complete publication XML and extract required information.

    Args:
        xml_content (str): The XML content of the publication.
        keyword (str): The keyword used for the search.

    Returns:
        dict: A dictionary containing the extracted information.
    """
    root = ElementTree.fromstring(xml_content)
    company = root.find(".//company")
    address = root.find(".//address")
    purpose = root.find(".//purpose")

    data = {
        "keyword": keyword,
        "company": company.findtext(".//name", ""),
        "uid": company.findtext(".//uid", ""),
        "seat": company.findtext(".//seat", ""),
        "street": address.findtext(".//street", ""),
        "houseNumber": address.findtext(".//houseNumber", ""),
        "swissZipCode": address.findtext(".//swissZipCode", ""),
        "town": address.findtext(".//town", ""),
        "purpose": purpose.findtext(".", "#") if purpose is not None else "#",
    }

    return data


def save_to_csv(data, file_path, fieldnames):
    """
    Save data to a CSV file.

    Args:
        data (list): The data to save.
        file_path (str): The path to the CSV file.
        fieldnames (list): The field names for the CSV file.

    Returns:
        None
    """
    with open(file_path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
