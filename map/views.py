from django.shortcuts import render
import json
import os
from django.conf import settings 

def update_combined_json():
    # Load the police data and duty data JSON files
    with open('policedata.json', 'r') as f1:
        file1 = json.load(f1)

    with open('policedutydata.json', 'r') as f2:
        file2 = json.load(f2)

    # Create a mapping from the duty data
    mapping = {item['off_name']: item for item in file2}

    # Combine the two JSON files
    combined = []
    for item in file1:
        if item['off_name'] in mapping:
            combined_item = {**item, **mapping[item['off_name']]}
            combined.append(combined_item)
        else:
            combined.append(item)

    for item in file2:
        if not any(i['off_name'] == item['off_name'] for i in file1):
            combined.append(item)

    # Define the path to save the combined JSON
    combined_file_path = os.path.join(settings.BASE_DIR, 'map', 'static', 'map', 'combinedpoldat.json')

    # Create the directory if it doesn't exist
    os.makedirs(os.path.dirname(combined_file_path), exist_ok=True)

    # Save the combined data to a JSON file
    with open(combined_file_path, 'w') as combined_file:
        json.dump(combined, combined_file, indent=2)

    return combined  # Return the combined data for the AJAX request


def show_map(request):
    # Trigger the JSON update
    update_combined_json()
    return render(request, 'map/map.html')


def update_json_view(request):
    """ Serve the combined JSON data for AJAX calls """
    combined = update_combined_json()
    return JsonResponse(combined, safe=False)