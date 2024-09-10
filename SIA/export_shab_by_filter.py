import configparser
import csv
import os
from datetime import datetime, timedelta
from xml.etree import ElementTree

import requests

# Base URL for fetching multiple publications
BASE_URL = "https://amtsblattportal.ch/api/v1/publications/xml"


def read_config(config_file):
    """Read configuration from the .ini file."""
    config = configparser.ConfigParser()
    config.read(config_file)
    return config


def fetch_publication_list(params):
    """Fetch the publication list based on the provided parameters."""
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        return response.content
    else:
        print(f"Error fetching publication list: {response.status_code}")
        return None


def fetch_complete_publication(publication_ref):
    """Fetch the complete publication using the ref URL."""
    response = requests.get(publication_ref)
    if response.status_code == 200:
        return response.content
    else:
        print(f"Error fetching publication: {response.status_code}")
        return None


def parse_publication_xml(xml_content, keyword):
    """Parse the complete publication XML and extract required information."""
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
    """Save data to a CSV file."""
    with open(file_path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


def main():
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
