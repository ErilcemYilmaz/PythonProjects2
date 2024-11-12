# SHAB Publication Data Fetcher

## Overview

The SHAB Publication Data Fetcher is a script designed to fetch, parse, and save publication data from the Swiss Official Gazette of Commerce (SHAB). This script allows you to search for specific keywords in SHAB publications, retrieve detailed information about the publications, and save the results to a CSV file.

## Features

- Fetch publication lists based on specified keywords and date ranges.
- Retrieve complete publication details for each publication in the list.
- Parse the publication XML to extract relevant information.
- Save the extracted data to a CSV file for further analysis.

## How It Works

1. **Configuration**: The script reads configuration settings from an INI file. This includes keywords to search for, date ranges, sub-rubrics, and publication states.
2. **Fetch Publication List**: The script sends a request to the SHAB API to fetch a list of publications based on the specified parameters.
3. **Fetch Complete Publication**: For each publication in the list, the script fetches the complete publication details using a reference URL.
4. **Parse Publication XML**: The script parses the XML content of each publication to extract relevant information such as company name, UID, address, and purpose.
5. **Save to CSV**: The extracted data is saved to a CSV file with a timestamped filename.

## Configuration

The script uses a configuration file (`BBF_filter_config.ini`) to specify the search parameters.
