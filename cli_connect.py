# -*- coding: utf-8 -*-
"""
Created on Tue Jul 22 13:59:59 2025

@author: Kush Swarnkar
"""

import requests # Making HTTP requests.
import json
import argparse

def search_cli(query_term, api_host='http://localhost:5000'):
    url = f"{api_host}/search?q={query_term}"
    try:
        response = requests.get(url) # Sending GET request to the Flask API.
        response.raise_for_status() # Raise an exception for HTTP errors.
        results = response.json()
        if results:
            print(f"Files matching '{query_term}':")
            for file_info in results:
                print(f"FilePath: {file_info['file_name']}, URL: {file_info['file_url']}")
        else:
            print(f"No files found matching '{query_term}'.")
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to the search service: {e}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Command-line client for Document Search Application.")
    parser.add_argument("query", type=str, help="The search term to query for.")
    parser.add_argument("--host", type=str, default="http://localhost:5000",
                        help="Host and port of the search service API (default: http://localhost:5000).")
    args = parser.parse_args()
    search_cli(args.query, args.host)