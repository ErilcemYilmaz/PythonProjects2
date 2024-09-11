import configparser
import csv
import os
from datetime import datetime, timedelta
from xml.etree import ElementTree

import requests

# Base URL for fetching multiple publications
BASE_URL = "https://amtsblattportal.ch/api/v1/publications/xml"


def read_config(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    return config


def fetch_publication_list(params):
    """
    Fetch the publication list based on the provided parameters.

    Args:
        params (dict): Dictionary of parameters to be sent in the API request.

    Returns:
        bytes: XML content of the publication list if the request is successful, None otherwise.
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
        publication_ref (str): Reference URL to fetch the complete publication.

    Returns:
        bytes: XML content of the complete publication if the request is successful, None otherwise.
    """
    response = requests.get(publication_ref)
    if response.status_code == 200:
        return response.content
    else:
        print(f"Error fetching publication: {response.status_code}")
        return None


def parse_publication_xml(xml_content, keyword):
    """
    Parse the complete publication XML and extract required information.

    Args:
        xml_content (bytes): XML content of the complete publication.
        keyword (str): Keyword used for the search.

    Returns:
        dict: Dictionary containing the extracted information.
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
        data (list): List of dictionaries containing the data to be saved.
        file_path (str): Path to the CSV file.
        fieldnames (list): List of field names for the CSV file.

    Returns:
        None
    """
    with open(file_path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


def main():
    """
    Main function to fetch, parse, and save publication data to a CSV file.
    """
    config = read_config(r"C:\coding\test_Data\results\BBF_filter_config.ini")

    keywords = config.get("FilterParams", "keywords").split(",")
    publication_date_daily = config.get(
        "FilterParams", "publicationDate_daily", fallback="NO"
    )

    if publication_date_daily.upper() == "YES":
        start_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        end_date = start_date
    else:
        start_date = config.get("FilterParams", "publicationDate.start")
        end_date = config.get("FilterParams", "publicationDate.end")

    sub_rubrics = config.get("FilterParams", "subRubrics")
    publication_states = config.get("FilterParams", "publicationStates")

    complete_publications = []

    for keyword in keywords:
        params = {
            "keyword": keyword.strip(),
            "publicationDate.start": start_date,
            "publicationDate.end": end_date,
            "subRubrics": sub_rubrics,
            "publicationStates": publication_states,
        }

        publication_list_xml = fetch_publication_list(params)
        if publication_list_xml:
            root = ElementTree.fromstring(publication_list_xml)
            publication_refs = [
                pub.get("ref")
                for pub in root.findall(".//publication")
                if pub.get("ref")
            ]

            for ref in publication_refs:
                complete_publication_xml = fetch_complete_publication(ref)
                if complete_publication_xml:
                    publication_data = parse_publication_xml(
                        complete_publication_xml, keyword.strip()
                    )
                    complete_publications.append(publication_data)

    start_date_formatted = datetime.strptime(start_date, "%Y-%m-%d").strftime("%Y%m%d")
    end_date_formatted = datetime.strptime(end_date, "%Y-%m-%d").strftime("%Y%m%d")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = config.get("Paths", "output_path")
    filename = f"{timestamp}_BBF_{start_date_formatted}_{end_date_formatted}.csv"
    csv_file_path = os.path.join(output_path, filename)

    fieldnames = [
        "keyword",
        "company",
        "uid",
        "seat",
        "street",
        "houseNumber",
        "swissZipCode",
        "town",
        "purpose",
    ]
    save_to_csv(complete_publications, csv_file_path, fieldnames)


if __name__ == "__main__":
    main()
