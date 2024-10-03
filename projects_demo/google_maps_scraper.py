import json
import sys
import urllib.parse

import pandas as pd
import requests


def make_request(query_string):
    """
    make_request performs query search and returns the response.

    Args:
        query_string: The query string to search.

    Returns:
        response of the get request or None if any error comes up.
    """
    encoded_query = urllib.parse.quote_plus(query_string)

    url = f"https://www.google.com/search?tbm=map&hl=en&gl=in&pb=!4m12!1m3!1d14159546.506860917!2d76.7698374!3d18.81817715!2m3!1f0!2f0!3f0!3m2!1i1536!2i703!4f13.1!7i20!10b1!12m21!1m2!18b1!30b1!2m3!5m1!6e2!20e3!10b1!12b1!13b1!16b1!17m1!3e1!20m4!5e2!6b1!8b1!14b1!46m1!1b0!94b1!19m4!2m3!1i360!2i120!4i8!20m57!2m2!1i203!2i100!3m2!2i4!5b1!6m6!1m2!1i86!2i86!1m2!1i408!2i240!7m42!1m3!1e1!2b0!3e3!1m3!1e2!2b1!3e2!1m3!1e2!2b0!3e3!1m3!1e8!2b0!3e3!1m3!1e10!2b0!3e3!1m3!1e10!2b1!3e2!1m3!1e9!2b1!3e2!1m3!1e10!2b0!3e3!1m3!1e10!2b1!3e2!1m3!1e10!2b0!3e4!2b1!4b1!9b0!22m6!1sLbb4ZtKPG_6e4-EPycyakAs%3A3!2s1i%3A0%2Ct%3A11887%2Cp%3ALbb4ZtKPG_6e4-EPycyakAs%3A3!7e81!12e3!17sLbb4ZtKPG_6e4-EPycyakAs%3A111!18e15!24m100!1m31!13m9!2b1!3b1!4b1!6i1!8b1!9b1!14b1!20b1!25b1!18m20!3b1!4b1!5b1!6b1!9b1!12b1!13b1!14b1!17b1!20b1!21b1!22b1!25b1!27m1!1b0!28b0!31b0!32b0!33m1!1b0!10m1!8e3!11m1!3e1!14m1!3b1!17b1!20m2!1e3!1e6!24b1!25b1!26b1!29b1!30m1!2b1!36b1!39m3!2m2!2i1!3i1!43b1!52b1!54m1!1b1!55b1!56m1!1b1!65m5!3m4!1m3!1m2!1i224!2i298!71b1!72m19!1m5!1b1!2b1!3b1!5b1!7b1!4b1!8m10!1m6!4m1!1e1!4m1!1e3!4m1!1e4!3sother_user_reviews!6m1!1e1!9b1!89b1!98m3!1b1!2b1!3b1!103b1!113b1!117b1!122m1!1b1!125b0!126b1!127b1!26m4!2m3!1i80!2i92!4i8!30m28!1m6!1m2!1i0!2i0!2m2!1i530!2i703!1m6!1m2!1i1486!2i0!2m2!1i1536!2i703!1m6!1m2!1i0!2i0!2m2!1i1536!2i20!1m6!1m2!1i0!2i683!2m2!1i1536!2i703!34m18!2b1!3b1!4b1!6b1!8m6!1b1!3b1!4b1!5b1!6b1!7b1!9b1!12b1!14b1!20b1!23b1!25b1!26b1!37m1!1e81!42b1!47m0!49m9!3b1!6m2!1b1!2b1!7m2!1e3!2b1!8b1!9b1!50m4!2e2!3m2!1b1!3b1!67m2!7b1!10b1!69i708&q={encoded_query}&oq={encoded_query}&tch=1"

    payload = {}
    headers = {"accept": "*/*", "accept-language": "en-GB,en;q=0.9"}

    try:
        response = requests.request("GET", url, headers=headers, data=payload)

        response.raise_for_status()
        return response
    except Exception as err:
        print(f"Exception occurred:make_request:{err}:{query_string}")
        return None


def parse_response(response, query_string):
    """
    parse_response does parsing of the data and returns list of dictionaries data.

    Args:
        response: The response object to parse data from.
        query_string: To match the response data

    Returns:
        master_records will be a list of dictionaries with all the parsed data records.
    """

    data = json.loads(response.text.rstrip('/*""*/'))
    data = data["d"].split("\n", 1)[1]

    data = json.loads(data)

    new_data = [item for item in data if item]
    new_data = [item for item in new_data if item[0] == query_string]
    new_data = new_data[0] if new_data else []

    results_data = new_data[1][1:] if new_data else []

    master_records = []
    for result in results_data:
        result = result[-1]
        address = result[2]
        location = result[9]
        name = result[11]
        category = result[13]
        address_2 = result[14]
        complete_name = result[18]
        country_county = result[30]

        try:
            phone_number = result[178][0][0]
        except:  # noqa: E722
            phone_number = ""

        try:
            website = result[7][1]
        except:  # noqa: E722
            website = ""

        record = {
            "name": name,
            "complete_name": complete_name,
            "phone_number": phone_number,
            "website": website,
            "address": address,
            "address_2": address_2,
            "category": category,
            "country_county": country_county,
            "location": location,
        }
        master_records.append(record)
    return master_records


def get_results(query_string: str) -> list[dict]:
    """
    get_results calls make request and on success parse_response.

    Args:
        query_string: The query string to search.

    Returns:
        results of the get request or None if any error comes up.
    """

    # make request only responsible for making request
    response = make_request(query_string)

    # parse data only for parsing data
    if response:
        print("Parsing Response")
        results = parse_response(response, query_string)
    else:
        print(f"No Response Found:\t{query_string}")
        results = []
    return results


def save_output(results, output_file_path):
    """
    save_output saves list of dictionaries into csv.

    Args:
        results: List of dictionaries to save.
        output_file_path: Path to output file.

    Returns:
    Boolean: If saving was a success.
    """
    try:
        df = pd.DataFrame(results)
        df.to_csv(output_file_path, index=0)
        print(f"Output File Saved:\t{output_file_path}")
        return True
    except Exception as err:
        print(f"Exception Occurred:save_output:\t{err}")
        return False


if __name__ == "__main__":
    # query to search
    query_string = sys.argv[1]

    # get list of dictionaries
    results = get_results(query_string)

    if results:
        # save output in csv
        output_file_path = f"{query_string}_dataset.csv"
        save_output(results, output_file_path)
    else:
        print("No Results Found.")
