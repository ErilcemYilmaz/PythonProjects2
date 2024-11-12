# Artikel 5 Data Fetcher

## Overview

The Artikel 5 Data Fetcher is a collection of scripts designed to fetch, compare, and update company data from the Zefix API based on various criteria such as company name, UID, legal seat ID, and city. These scripts allow you to automate the process of updating your local CSV files with the latest data from the Zefix API.

## Features

- Fetch company data from the Zefix API based on different criteria.
- Compare and update local CSV files with the fetched data.
- Support for concurrent processing to speed up data fetching and updating.

## Scripts

### 1. `export_by_name.py`

Fetches and updates company data based on the company name.

### 2. `export_by_uid.py`

Fetches and updates company data based on the UID.

### 3. `export_by_name_and_legal_seat_id.py`

Fetches and updates company data based on the company name and legal seat ID.

### 4. `export_by_name_and_city.py`

Fetches and updates company data based on the company name and city.

## Configuration

The scripts use a configuration file (`config.py`) to specify the API endpoint and session details.
