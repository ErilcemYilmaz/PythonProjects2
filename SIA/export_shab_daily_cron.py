import csv
import os
import sys
from datetime import datetime, timedelta
from xml.etree import ElementTree

import requests

# Base URL for fetching multiple publications
BASE_URL = "https://amtsblattportal.ch/api/v1/publications/xml"


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
        "company": company.findtext(".//name", "#") if company is not None else "#",
        "uid": company.findtext(".//uid", "#") if company is not None else "#",
        "seat": company.findtext(".//seat", "#") if company is not None else "#",
        "street": address.findtext(".//street", "#") if address is not None else "#",
        "houseNumber": (
            address.findtext(".//houseNumber", "#") if address is not None else "#"
        ),
        "swissZipCode": (
            address.findtext(".//swissZipCode", "#") if address is not None else "#"
        ),
        "town": address.findtext(".//town", "#") if address is not None else "#",
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
    if len(sys.argv) != 3:
        start_date = input(
            "Enter start date (YYYY-MM-DD) or press Enter to use current date: "
        )
        if not start_date:
            start_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        output_path = input("Enter output path: ")
        if not output_path:
            print("Output path is required.")
            sys.exit(1)
    else:
        start_date = sys.argv[1]
        output_path = sys.argv[2]

    try:
        datetime.strptime(start_date, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        sys.exit(1)

    end_date = datetime.now().strftime("%Y-%m-%d")
    keywords = [
        "Architekt, Architektur, Ingenieur, Ingenieurwesen, Generalunternehmung, Raumplanung, Bauleitung"
    ]

    complete_publications = []

    for keyword in keywords:
        params = {
            "keyword": keyword.strip(),
            "publicationDate.start": start_date,
            "publicationDate.end": end_date,
            "subRubrics": "HR01",  # HR01 for new entries
            "publicationStates": "PUBLISHED",  # mandatory for API
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
    start_date_formatted = datetime.strptime(end_date, "%Y-%m-%d").strftime("%Y%m%d")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_BBF_{start_date_formatted}_{start_date_formatted}.csv"
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
