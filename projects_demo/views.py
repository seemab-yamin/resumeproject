import os
import re
import time

import pandas as pd
from django.conf import settings
from django.http import FileResponse
from django.shortcuts import render

from .google_maps_scraper import get_results as google_maps_scraper

# add global MEDIA ROOT path
MEDIA_ROOT = settings.MEDIA_ROOT


def construct_media_file_path(MEDIA_ROOT, file_name):
    """
    Construct Media File Path
    """
    return os.path.join(MEDIA_ROOT, file_name)


def sanitize_file_name(search_query):
    """Sanitizes a search query string to be used as a file name.

    Args:
      search_query: The search query string to sanitize.

    Returns:
      The sanitized search query string, suitable for use as a file name.
    """

    # Remove invalid characters that could cause issues with file names.
    valid_chars = r"[a-zA-Z0-9_\-\.]"
    search_query = re.sub(r"[^" + valid_chars + r"]", "_", search_query)

    # Limit the length of the file name to prevent excessive length.
    max_length = 100
    search_query = search_query[:max_length]

    return search_query


# Create your views here.
def projects_demo(request):
    return render(request, "projects_demo/index.html")


# Create your views here.
def google_maps_scraper_demo(request):
    """
    google_maps_scraper_demo executed google maps scraper and
    returns results with csv downloadable link.
    """
    if request.method == "POST":
        # fetch post data from request
        data = request.POST
        search_query = data.get("search_query")

        # execute google maps scraper
        results = google_maps_scraper(search_query)

        if results:
            # results fetched successfully
            message = "Records Fetched Successfully."
            results = [
                {
                    "name": item["name"],
                    "phone_number": item["phone_number"],
                    "website": item["website"],
                    "address": ", ".join(item["address"]),
                    "categories": ", ".join(item["category"]),
                    "country_region": item["country_county"],
                }
                for item in results
            ]
            file_name = f"{sanitize_file_name(search_query)}_{time.strftime('%Y-%m-%d_%H-%M-%S')}.csv"
            file_path = construct_media_file_path(MEDIA_ROOT, file_name)

            # construct data frame
            df = pd.DataFrame(results)

            # save df
            df.to_csv(file_path, index=0)
        else:
            # if failed to fetch results
            message = "Failed To Fetch Records."
            file_name = None

        output_data = {
            "search_query": search_query,
            "results": results,
            "message": message,
            "file_name": file_name,
        }
        return render(
            request,
            "projects_demo/google_maps_scraper-results.html",
            context=output_data,
        )
    return render(request, "projects_demo/google_maps_scraper.html")


def download_results(request, file_name):
    # construct file path
    file_path = construct_media_file_path(MEDIA_ROOT, file_name)
    # make file object
    response = FileResponse(open(file_path, "rb"))
    response["Content-Type"] = "application/octet-stream"
    response["Content-Disposition"] = f'attachment; filename="{file_name}"'
    return response
