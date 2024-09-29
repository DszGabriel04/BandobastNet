from django.shortcuts import render
import json
import os
from django.conf import settings 

def show_map(request):
    # Load JSON files
    with open('policedata.json', 'r') as f1:
        file1 = json.load(f1)

    with open('policedutydata.json', 'r') as f2:
        file2 = json.load(f2)

    # Create a mapping from file2
    mapping = {item['off_name']: item for item in file2}

    # Combine the two files
    combined = []

    for item in file1:
        if item['off_name'] in mapping:
            # Merge the objects
            combined_item = {**item, **mapping[item['off_name']]}
            combined.append(combined_item)
        else:
            combined.append(item)  # Add the original item if no match

    # Optionally, add any items from file2 that aren't in file1
    for item in file2:
        if not any(i['off_name'] == item['off_name'] for i in file1):
            combined.append(item)

    # Define the path to the combined JSON file in the static directory
    combined_file_path = os.path.join(settings.BASE_DIR, 'map', 'static', 'map', 'combinedpoldat.json')

    # Create the directory if it doesn't exist
    os.makedirs(os.path.dirname(combined_file_path), exist_ok=True)

    # Save the combined JSON to the new file in the static directory
    with open(combined_file_path, 'w') as combined_file:
        json.dump(combined, combined_file, indent=2)


    return render(request, 'map/map.html')
