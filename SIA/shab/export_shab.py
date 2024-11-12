import os
from datetime import datetime, timedelta
from xml.etree import ElementTree

from config import read_config
from utils import (
    fetch_complete_publication,
    fetch_publication_list,
    parse_publication_xml,
    save_to_csv,
)


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
